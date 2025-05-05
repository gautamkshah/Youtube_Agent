import streamlit as st
import requests
import os

BACKEND_URL = "http://localhost:8000"  

st.set_page_config(page_title="YouTube RAG Chat", layout="wide")

st.title("🎥 Chat with Youtube")

with st.sidebar:
    st.header("Video Processing")
    video_id = st.text_input(
        "Enter YouTube Video ID", 
        help="Just the ID part (e.g., 'dQw4w9WgXcQ')"
    )
    
    if st.button("Process Video"):
        if video_id:
            with st.spinner("Processing video transcript..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/process_video",
                        json={"video_id": video_id}
                    )
                    if response.status_code == 200:
                        st.success("Video processed successfully!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please enter a video ID")

st.header("Ask Questions About the Video")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know about the video?"):
    if "video_id" not in locals() or not video_id:
        st.warning("Please process a video first")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask_question",
                    json={
                        "video_id": video_id,
                        "question": prompt
                    }
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found")
                    st.markdown(answer)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    st.error(f"API Error: {error_msg}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")