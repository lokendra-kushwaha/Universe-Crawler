import streamlit as st
from streamlit_mic_recorder import speech_to_text

st.title("🎤 Voice Search")
st.write("For search click on the mic and speek:")


text = speech_to_text(
    language='en-US',
    use_container_width=True,
    just_once=True,
    key='STT'
)


if text:
    st.success(f"search: {text}")