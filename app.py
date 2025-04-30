
import streamlit as st
import os
from dotenv import load_dotenv
from text_processor import process_text_with_chatgpt, split_text_by_tokens, process_chunk

load_dotenv()

st.set_page_config(
    page_title="Russian Text Enhancer",
    page_icon="📝",
    layout="wide"
)

st.title("Russian Text Enhancer")
st.markdown("""
Это приложение улучшает читаемость длинных русскоязычных текстов с помощью GPT-4.
Текст разбивается на части и обрабатывается нейросетью с учётом стилистики и структуры.
""")

api_key = os.environ.get("OPENAI_KEY") or os.environ.get("OPENAI_API_KEY", "")
if not api_key:
    st.warning("OpenAI API key не найден. Добавьте OPENAI_KEY в .env или Secrets.")
    st.stop()

# Replace file upload with text area
user_text = st.text_area("Вставьте текст для обработки:", height=300, placeholder="Вставьте сюда русский текст для обработки...")

if st.button("Обработать текст"):
    if user_text:
        try:
            st.info("Обработка текста... Пожалуйста, подождите.")
            
            # Create a progress bar
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            # Modify text_processor.py to work with this function
            def process_with_progress(text):
                chunks = split_text_by_tokens(text)
                total_chunks = len(chunks)
                results = []
                
                for i, chunk in enumerate(chunks):
                    # Update progress
                    progress_percent = (i / total_chunks)
                    progress_bar.progress(progress_percent)
                    progress_text.text(f"Обработано {i+1} из {total_chunks} частей текста ({int(progress_percent*100)}%)")
                    
                    # Process chunk
                    with st.spinner(f"Обработка части {i+1}/{total_chunks}..."):
                        result = process_chunk(chunk)
                        results.append(result)
                
                # Complete the progress bar
                progress_bar.progress(1.0)
                progress_text.text("Обработка завершена!")
                
                return "\n\n".join(results)
            
            # Process text with progress tracking
            output = process_with_progress(user_text)
            
            st.success("Обработка завершена!")
            st.download_button("📥 Скачать результат", output, file_name="processed_text.txt", mime="text/plain")
            st.text_area("Результат:", output, height=500)
        except Exception as e:
            st.error(f"Ошибка при обработке текста: {str(e)}")
    else:
        st.warning("Пожалуйста, введите текст для обработки.")
