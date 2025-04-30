import streamlit as st
import os
from dotenv import load_dotenv
import text_processor
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
Текст разбивается на части и обрабатывается нейросетью с учётом стилистики, структуры и общего контекста.
""")

with st.expander("Дополнительные настройки"):
    max_tokens = st.slider(
        "Максимальное количество токенов на фрагмент",
        min_value=1000,
        max_value=5000,
        value=3000,
        step=500,
        help="Больше токенов - меньше фрагментов, но дольше обработка каждого фрагмента"
    )
    
    create_summary = st.checkbox(
        "Создать общее резюме текста для сохранения контекста",
        value=True,
        help="Создаёт краткое резюме всего текста для лучшей связности между фрагментами"
    )

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

            # Prepare the progress display components
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Обновляем max_tokens из пользовательских настроек
            text_processor.MAX_TOKENS_PER_CHUNK = max_tokens
            
            # Process the text with visual progress tracking
            if create_summary and len(user_text) > 5000:
                with st.spinner("Создание контекстного резюме текста..."):
                    context_summary = text_processor.extract_summary(user_text)
                    st.info(f"Создано резюме текста для сохранения контекста ({len(context_summary.split())} слов)")
            
            chunks = text_processor.split_text_by_tokens(user_text, max_tokens)
            total_chunks = len(chunks)
            
            if total_chunks > 10:
                st.warning(f"Текст разбит на {total_chunks} частей. Обработка может занять некоторое время.")
            
            results = []
            
            for i, chunk in enumerate(chunks):
                # Update progress indicators
                progress_percent = i / total_chunks
                progress_bar.progress(progress_percent)
                status_text.text(f"Обработано {i+1} из {total_chunks} частей текста ({int(progress_percent*100)}%)")

                # Process the current chunk with context
                with st.spinner(f"Обработка части {i+1}/{total_chunks}..."):
                    # Добавляем номер части для лучшего понимания места в тексте
                    position_prefix = f"[Часть {i+1} из {total_chunks}]\n\n"
                    
                    if create_summary and 'context_summary' in locals() and len(chunks) > 1:
                        context_msg = f"""
Это часть большого текста из {total_chunks} частей. 

Обрабатываемый фрагмент:
"""
                        chunk_with_context = position_prefix + context_msg + chunk
                        result = text_processor.process_chunk(chunk_with_context)
                    else:
                        # Если не создаем резюме, обрабатываем как обычно
                        chunk_with_position = position_prefix + chunk
                        result = text_processor.process_chunk(chunk_with_position)
                    
                    # Удаляем технические метки из результата
                    result = result.replace(position_prefix, "")
                    results.append(result)

            # Complete the progress bar
            progress_bar.progress(1.0)
            status_text.text("Обработка завершена!")
            
            # Display token information summary
            total_input_tokens = text_processor.count_tokens(user_text)
            st.info(f"Размер исходного текста: {total_input_tokens} токенов, разбит на {total_chunks} частей.")

            # Join all processed chunks
            output = "\n\n".join(results)

            st.success("Обработка завершена!")
            st.download_button("📥 Скачать результат", output, file_name="processed_text.txt", mime="text/plain")
            st.text_area("Результат:", output, height=500)
        except Exception as e:
            st.error(f"Ошибка при обработке текста: {str(e)}")
    else:
        st.warning("Пожалуйста, введите текст для обработки.")