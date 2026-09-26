import base64
import os
import time
from io import BytesIO

import streamlit as st
from sarvamai import SarvamAI


LANGUAGES = {
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Odia": "od-IN",
    "English (India)": "en-IN",
    "Assamese": "as-IN",
    "Urdu": "ur-IN",
    "Nepali": "ne-IN",
    "Maithili": "mai-IN",
    "Bodo": "brx-IN",
    "Dogri": "doi-IN",
    "Sanskrit": "sa-IN",
    "Konkani": "kok-IN",
    "Kashmiri": "ks-IN",
    "Sindhi": "sd-IN",
    "Santali": "sat-IN",
    "Manipuri": "mni-IN",
}

TTS_LANGUAGES = {
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Odia": "od-IN",
    "English (India)": "en-IN",
}

STT_LANGUAGES = {"Auto-detect": "unknown", **LANGUAGES}

VOICES = {
    "Male": [
        "shubh", "aditya", "rahul", "rohan", "amit", "dev", "ratan",
        "varun", "manan", "sumit", "kabir", "aayan", "ashutosh",
        "advait", "anand", "tarun", "sunny", "mani", "gokul", "vijay",
        "mohit", "rehan", "soham",
    ],
    "Female": [
        "ritu", "priya", "neha", "pooja", "simran", "kavya", "ishita",
        "shreya", "roopa", "tanya", "shruti", "suhani", "kavitha", "rupali",
    ],
}
VOICE_OPTIONS = [
    (voice, gender)
    for gender, voices in VOICES.items()
    for voice in voices
]
TERMINAL_DOCUMENT_STATES = {
    "completed", "partially_completed", "failed", "rejected"
}
SUPPORTED_AUDIO = [
    "wav", "mp3", "m4a", "aac", "ogg", "opus", "flac", "webm",
    "mp4", "aiff", "amr",
]


def translate_text(client, text, source_language_code, target_language_code):
    if source_language_code == target_language_code:
        return text
    response = client.text.translate(
        input=text,
        source_language_code=source_language_code,
        target_language_code=target_language_code,
        model="mayura:v1",
    )
    return response.translated_text


def extract_document_text(client, uploaded_file, language_code):
    file_data = (
        uploaded_file.name,
        BytesIO(uploaded_file.getvalue()),
        uploaded_file.type,
    )
    job = client.doc_ai.digitise(
        file=[file_data],
        language=language_code,
        output_format="md",
    )

    with st.status("Sarvam Vision is reading the document", expanded=False) as status:
        job_status = job.status.lower()
        deadline = time.monotonic() + 180
        while job_status not in TERMINAL_DOCUMENT_STATES:
            if time.monotonic() >= deadline:
                raise TimeoutError("Document processing took too long. Please try again.")
            time.sleep(3)
            progress = client.doc_ai.get_status(job_id=job.job_id)
            job_status = progress.status.lower()
            status.update(label=f"Reading document: {job_status}", state="running")

        if job_status not in {"completed", "partially_completed"}:
            raise RuntimeError(f"Sarvam Vision could not process this document ({job_status}).")

        results = client.doc_ai.get_results(job_id=job.job_id)
        pages = [
            page.content.strip()
            for document in results.documents
            for page in (document.pages or [])
            if page.content and page.content.strip()
        ]
        status.update(label="Document text extracted", state="complete")

    if not pages:
        raise ValueError("No readable text was found in the uploaded document.")
    return "\n\n".join(pages)


def create_audio(client, text, language_code, speaker, pace, audio_format):
    if len(text) > 2500:
        raise ValueError(
            "Bulbul v3 supports up to 2,500 characters per request. "
            "Use Summarize & speak for longer text."
        )
    response = client.text_to_speech.convert(
        text=text,
        language_code=language_code,
        speaker=speaker,
        pace=pace,
        model="bulbul:v3",
        output_audio_codec=audio_format.lower(),
    )
    return base64.b64decode("".join(response.audios))


def summarize_text(client, text):
    response = client.chat.completions(
        model="sarvam-105b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize the source in clear, natural English for listening. "
                    "Keep the summary under 1,200 characters, preserve the key facts "
                    "and conclusions, and do not add information."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=700,
        reasoning_effort=None,
    )
    summary = response.choices[0].message.content
    if not summary:
        raise RuntimeError("Sarvam-105B returned an empty summary.")
    return summary.strip()


def get_api_key():
    api_key = os.getenv("SARVAM_API_KEY")
    if api_key:
        return api_key
    try:
        return st.secrets["SARVAM_API_KEY"]
    except Exception:
        return None


st.set_page_config(page_title="Sarvam Voice Studio", page_icon=":material/graphic_eq:")
st.title("Sarvam Voice Studio")
st.write("Create, summarize, and translate speech across Indian languages.")

workflow = st.radio(
    "Workflow",
    ["Text to speech", "Summarize & speak", "Translate speech"],
    horizontal=True,
)

target_language = st.selectbox("Output language", options=list(TTS_LANGUAGES))
target_language_code = TTS_LANGUAGES[target_language]

if workflow == "Translate speech":
    source_language = st.selectbox("Spoken language", options=list(STT_LANGUAGES))
    audio_file = st.file_uploader("Upload audio", type=SUPPORTED_AUDIO)
    source_file = None
    text = ""
else:
    source_language = st.selectbox(
        "Input language",
        options=list(LANGUAGES),
        index=list(LANGUAGES).index("English (India)"),
    )
    source_file = st.file_uploader(
        "Upload a PDF or image (optional)",
        type=["pdf", "png", "jpg", "jpeg"],
    )
    audio_file = None
    if source_file:
        text = ""
        st.caption("The uploaded document will be read with Sarvam Vision. PDFs can contain up to 10 pages.")
    else:
        text = st.text_area(
            "Text",
            placeholder="Paste or type your text...",
            max_chars=100000 if workflow == "Summarize & speak" else 2500,
        )

voice = st.selectbox(
    "Voice",
    options=VOICE_OPTIONS,
    index=0,
    format_func=lambda choice: f"{choice[0].title()} · {choice[1]}",
)
voice_name = voice[0]
pace = st.slider("Speech speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
audio_format = st.radio("Audio format", ["MP3", "WAV"], horizontal=True)

button_label = {
    "Text to speech": "Generate speech",
    "Summarize & speak": "Summarize and speak",
    "Translate speech": "Translate and speak",
}[workflow]

for state_key in (
    "audio_bytes", "spoken_text", "display_text", "generated_language",
    "generated_format", "result_label",
):
    if state_key not in st.session_state:
        st.session_state[state_key] = None

if st.button(button_label, type="primary"):
    for state_key in (
        "audio_bytes", "spoken_text", "display_text", "generated_language",
        "generated_format", "result_label",
    ):
        st.session_state[state_key] = None

    api_key = get_api_key()
    if not api_key:
        st.error("Set SARVAM_API_KEY in the terminal or in Streamlit Cloud Secrets.")
    elif workflow == "Translate speech" and audio_file is None:
        st.warning("Upload an audio file first.")
    elif workflow != "Translate speech" and source_file is None and not text.strip():
        st.warning("Enter text or upload a PDF/image first.")
    else:
        try:
            client = SarvamAI(api_subscription_key=api_key)
            if workflow == "Translate speech":
                transcript = client.speech_to_text.transcribe(
                    file=(audio_file.name, BytesIO(audio_file.getvalue()), audio_file.type),
                    model="saaras:v3",
                    mode="transcribe",
                    language_code=STT_LANGUAGES[source_language],
                )
                source_text = transcript.transcript.strip()
                detected_language = transcript.language_code or STT_LANGUAGES[source_language]
                if not source_text:
                    raise ValueError("No speech was recognized in the uploaded audio.")
                if detected_language == "unknown":
                    raise ValueError("Could not detect the spoken language. Select it manually and try again.")
                spoken_text = translate_text(
                    client, source_text, detected_language, target_language_code
                )
                display_text = f"Recognized speech:\n\n{source_text}"
                result_label = "Translated speech"
            else:
                source_text = (
                    extract_document_text(
                        client, source_file, LANGUAGES[source_language]
                    )
                    if source_file
                    else text.strip()
                )
                if workflow == "Summarize & speak":
                    display_text = summarize_text(client, source_text)
                    spoken_text = translate_text(
                        client, display_text, "en-IN", target_language_code
                    )
                    result_label = "Summary"
                else:
                    spoken_text = translate_text(
                        client,
                        source_text,
                        LANGUAGES[source_language],
                        target_language_code,
                    )
                    display_text = source_text if source_file else None
                    result_label = "Generated speech"

            audio_bytes = create_audio(
                client,
                spoken_text,
                target_language_code,
                voice_name,
                pace,
                audio_format,
            )
            st.session_state.audio_bytes = audio_bytes
            st.session_state.spoken_text = spoken_text
            st.session_state.display_text = display_text
            st.session_state.generated_language = target_language
            st.session_state.generated_format = audio_format.lower()
            st.session_state.result_label = result_label
        except Exception as error:
            st.error(f"Generation failed: {error}")

if st.session_state.audio_bytes:
    st.subheader(st.session_state.result_label)
    if st.session_state.display_text:
        st.write(st.session_state.display_text)
    elif st.session_state.generated_language != "English (India)":
        st.write(st.session_state.spoken_text)

    file_extension = st.session_state.generated_format
    mime_type = "audio/mpeg" if file_extension == "mp3" else "audio/wav"
    st.audio(st.session_state.audio_bytes, format=mime_type)
    st.download_button(
        f"Download {file_extension.upper()}",
        data=st.session_state.audio_bytes,
        file_name=f"speech_{TTS_LANGUAGES[st.session_state.generated_language]}.{file_extension}",
        mime=mime_type,
    )