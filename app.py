import streamlit as st
from utils.rag import load_documents, retrieve_context
from utils.web_search import search_web
from models.llm import generate_response

st.set_page_config(page_title="AI Fashion Assistant", layout="wide")

# Background image + styling
st.markdown(
    """
    <style>

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1490481651871-ab68de25d43d");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: black;
        font-weight: 500;
    }

    /* All text black */
    p, span, label, div {
        color: black !important;
        font-weight: 500;
    }

    /* Bold headings */
    h1, h2, h3 {
        color: black !important;
        font-weight: 800 !important;
    }

    /* Chat bubbles */
    .stChatMessage {
        background-color: rgba(255,255,255,0.85);
        border-radius: 12px;
        padding: 10px;
        color: black;
        font-weight: 500;
    }

    /* Radio button text */
    .stRadio label {
        color: black !important;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Centered title
st.markdown(
    "<h1 style='text-align:center;'>Your Everyday Fashion Design Assistant</h1>",
    unsafe_allow_html=True
)

# Upload documents
uploaded_files = st.file_uploader(
    "Upload Fashion Documents (PDF)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:
    st.success("Documents uploaded successfully!")

# Response mode
mode = st.radio(
    "How do you want your response?",
    ["Short", "Detailed"]
)

# Load documents
try:
    texts, index = load_documents()
except Exception as e:
    st.error(f"Error loading documents: {e}")
    texts, index = [], None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Ask anything about fashion design...")

if user_input:

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    context = ""

    if index is not None:
        context = retrieve_context(user_input, texts, index)

    if context.strip() == "":
        context = search_web(user_input)

    prompt = f"""
You are a fashion design expert chatbot.

Context:
{context}

Question:
{user_input}

Give a {mode} answer.
"""

    response = generate_response(prompt)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)

st.divider()

# Fashion palette generator
st.subheader("Fashion Color Palette Generator")

occasion = st.selectbox(
    "Select Occasion",
    ["Casual Wear", "Wedding", "Party", "Summer Outfit", "Winter Outfit"]
)

if st.button("Generate Color Palette"):

    prompt = f"Suggest 5 color palettes for {occasion} fashion outfits."

    palette = generate_response(prompt)

    st.write(palette)