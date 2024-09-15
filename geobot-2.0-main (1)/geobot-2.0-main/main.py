import json
import requests
from streamlit_lottie import st_lottie
from openai import OpenAI
import streamlit as st

# Function to load Lottie animation from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_icon = load_lottieurl("https://lottie.host/1783f84a-32c3-427c-bebb-8fac48d8e40f/9TeO74mzCu.json")
lottie_icon2 = load_lottieurl("https://lottie.host/c376c048-bff6-48aa-8316-c395d97c0d36/Wt70ECGLSm.json")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize Streamlit session state variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []

# Define sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["GeoBot Chat", "Voice Search"]
)

# Display different pages based on user selection
if page == "GeoBot Chat":
    # Display GeoBot chat interface
    with st.sidebar:
        st.title('🤖💬 GeoBot ')
        st.sidebar.markdown(
            f"""
            <div style="padding: 20px;">
                {st_lottie(lottie_icon2, speed=1, width=200, height=200)}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.title("Recent Prompt ")
        for user_message in st.session_state.user_messages:
            st.caption(f":robot_face: {user_message}")

    # Display Lottie animation on the right side with custom CSS
    if lottie_icon is not None:
        st.write(
            f"""
            <div style="position: absolute; right: 100px; top: -10%; padding: 20px;">
                {st_lottie(lottie_icon, speed=1, width=600, height=600)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Chat input and interaction
    if prompt := st.chat_input("Message...."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_messages.append(prompt)  # Store user messages separately for sidebar

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif page == "Voice Search":
    # Display voice search page
    st.title("Voice Search")
    # Add voice search functionality here

