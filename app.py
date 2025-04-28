import streamlit as st
import os
from dotenv import load_dotenv
from text_processor import process_text_with_chatgpt, split_text_into_chunks

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Russian Text Enhancer",
    page_icon="📝",
    layout="wide"
)

st.title("Russian Text Enhancer")
st.markdown("""
This application processes transcribed Russian text through GPT-4o to improve readability while preserving content.
It fixes punctuation, improves structure, and renders text in an easy-to-read manner.
""")

# Check for API key
api_key = os.environ.get("OPENAI_KEY") 
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
if not api_key:
    # Display debugging information
    st.warning("OpenAI API key not found in environment variables. Please add OPENAI_KEY to your Secrets tab.")
    st.info("Available environment variables: " + ", ".join([key for key in os.environ.keys() if "OPENAI" in key or "API" in key or "KEY" in key]))
    st.info("Please enter your OpenAI API key.")
    
    # Add input field for API key
    manual_api_key = st.text_input("OpenAI API Key", type="password")
    if manual_api_key:
        api_key = manual_api_key
        os.environ["OPENAI_KEY"] = manual_api_key
        st.success("API key set for this session!")
else:
    st.success("OpenAI API key found in environment variables.")

# Input methods
input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"])

text_input = ""
if input_method == "Paste Text":
    text_input = st.text_area("Paste your Russian text here:", height=300)
else:
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    if uploaded_file is not None:
        text_input = uploaded_file.read().decode("utf-8")
        st.text_area("File content:", text_input, height=300)

# Process options
if text_input:
    st.subheader("Processing Options")
    
    # Chunking method selector
    chunking_method = st.radio(
        "Chunking method:",
        ["By Sentence Count", "By Character Count"],
        help="Choose how to split your text for processing"
    )
    
    chunk_size = None
    line_count = None
    
    if chunking_method == "By Character Count":
        chunk_size = st.slider(
            "Chunk size (characters)",
            min_value=1000,
            max_value=10000,
            value=4000,
            step=500,
            help="Size of text chunks to process separately. Larger chunks provide better context but may hit API limits."
        )
    else:  # By Sentence Count
        line_count = st.slider(
            "Number of sentences per chunk",
            min_value=20,
            max_value=150,
            value=50,
            step=5,
            help="Number of sentences to include in each chunk. 50 sentences is recommended for optimal processing."
        )
    
    model = st.selectbox(
        "Select OpenAI model",
        ["gpt-4o"],
        help="GPT-4o is the latest and recommended model"
    )

    if st.button("Process Text"):
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            with st.spinner("Processing text through GPT-4o..."):
                try:
                    # Split text into chunks based on selected method
                    chunks = split_text_into_chunks(text_input, chunk_size, line_count)
                    
                    # Process each chunk
                    processed_chunks = []
                    progress_bar = st.progress(0)
                    
                    for i, chunk in enumerate(chunks):
                        processed_chunk = process_text_with_chatgpt(chunk, model=model)
                        processed_chunks.append(processed_chunk)
                        progress_bar.progress((i + 1) / len(chunks))
                    
                    # Combine processed chunks
                    processed_text = "\n\n".join(processed_chunks)
                    
                    # Display processed text
                    st.subheader("Processed Text")
                    st.markdown(processed_text)
                    
                    # Download option
                    st.download_button(
                        label="Download processed text as Markdown",
                        data=processed_text,
                        file_name="enhanced_text.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Note:** This application uses OpenAI's GPT-4o to enhance Russian transcribed text.")
