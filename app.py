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
    text = uploaded_file.read().decode("utf-8")
    st.info("Обработка текста... Пожалуйста, подождите.")
    output = process_text_with_chatgpt(text)
    st.success("Обработка завершена!")
    st.download_button("📥 Скачать результат", output, file_name="processed_text.txt", mime="text/plain")
    st.text_area("Результат:", output, height=500)
