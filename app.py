import streamlit as st
import os
from dotenv import load_dotenv
from text_processor import process_text_with_chatgpt

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

uploaded_file = st.file_uploader("Загрузите .txt файл с текстом", type=["txt"])

if uploaded_file:
    try:
        text = uploaded_file.read().decode("utf-8")
        st.info("Обработка текста... Пожалуйста, подождите.")
        output = process_text_with_chatgpt(text)
        st.success("Обработка завершена!")
        st.download_button("📥 Скачать результат", output, file_name="processed_text.txt", mime="text/plain")
        st.text_area("Результат:", output, height=500)
    except Exception as e:
        st.error(f"Ошибка при обработке файла: {str(e)}")
        st.info("Попробуйте напрямую вставить текст в поле ниже:")
        user_text = st.text_area("Вставьте текст для обработки:", height=300)
        if st.button("Обработать текст"):
            if user_text:
                try:
                    output = process_text_with_chatgpt(user_text)
                    st.success("Обработка завершена!")
                    st.download_button("📥 Скачать результат", output, file_name="processed_text.txt", mime="text/plain")
                    st.text_area("Результат:", output, height=500)
                except Exception as e:
                    st.error(f"Ошибка при обработке текста: {str(e)}")
