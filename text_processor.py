import os
import openai
import tiktoken
from openai import OpenAI

openai.api_key = os.environ.get("OPENAI_KEY") or os.environ.get(
    "OPENAI_API_KEY", "")
ADVANCED_SYSTEM_MESSAGE = """
Ты работаешь с лекционным текстом, который подаётся частями. Твоя задача:

1. Сохрани каждое предложение и каждую мысль из исходного текста. Ни один смысловой фрагмент не должен быть потерян — даже если он кажется повтором, отступлением или уточнением. Если в тексте есть перечисление (например: первое, второе, третье), обязательно убедись, что все пункты отражены в результате. Если мысль началась в предыдущей части, сделай плавный переход и восстанови полный смысл.

2. Аккуратно исправь орфографические и пунктуационные ошибки. Сохрани эмоциональные отступления, авторский стиль, метафоры. Не сокращай текст и не меняй порядок мыслей. Не переписывай смысл — твоя задача не перефразировать, а очистить и структурировать.

3. Оформи результат в формате Markdown:
- Используй заголовки (#, ##) для смысловых блоков, а не для каждого абзаца.
- Выделяй жирным ключевые понятия, важные мысли, названия этапов, инструментов, техник.
- Выделяй курсивом коучинговые вопросы и вопросы к размышлению.
- Сложные предложения с несколькими идеями разбивай на пункты в виде списка.
- Все перечисления (даже если они не оформлены явно) оформи как списки.
- Убедись, что ни один пункт не потерян.

4. Результат должен быть читаемым, структурированным и вдохновляющим — как обучающий материал. Сохрани плавность текста, не делай резких логических скачков. Переходы между частями должны быть плавными и логичными.

5. Перед выводом результата обязательно проверь:
- Все ли перечисления из оригинала отражены?
- Все ли предложения, особенно начинающиеся с «и», «также», «дополню», «вспомним еще» и т.п., сохранены?
- Присутствуют ли все предложения оригинала в результате?
- Все ли коучинговые вопросы выделены курсивом?

Выполни обработку строго по этим правилам.

"""

# Используем модель с поддержкой большого контекста
MODEL = "chatgpt-4o-latest"
MAX_TOKENS_PER_CHUNK = 3000  # с запасом до лимита модели


def count_tokens(text: str, model: str = MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def split_text_by_tokens(text: str, max_tokens: int = MAX_TOKENS_PER_CHUNK):
    encoding = tiktoken.encoding_for_model(MODEL)
    tokens = encoding.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = encoding.decode(tokens[i:i + max_tokens])
        chunks.append(chunk)
    return chunks


client = OpenAI(api_key=os.environ.get("OPENAI_KEY")
                or os.environ.get("OPENAI_API_KEY", ""))


def process_chunk(chunk: str, system_message: str = ADVANCED_SYSTEM_MESSAGE):
    # Count tokens in both system message and user message
    system_token_count = count_tokens(system_message)
    user_token_count = count_tokens(chunk)
    total_tokens = system_token_count + user_token_count
    
    # Print token information to Streamlit
    import streamlit as st
    st.info(f"Token counts - System: {system_token_count}, User chunk: {user_token_count}, Total: {total_tokens}")
    
    response = client.chat.completions.create(model=MODEL,
                                              messages=[{
                                                  "role":
                                                  "system",
                                                  "content":
                                                  system_message
                                              }, {
                                                  "role": "user",
                                                  "content": chunk
                                              }],
                                              temperature=0.1,
                                              max_tokens=3500)
    return response.choices[0].message.content


def extract_summary(text: str, max_tokens=1500) -> str:
    """Создает краткий обзор текста для сохранения контекста"""
    # Если текст короткий, нет необходимости в создании резюме
    if count_tokens(text) <= max_tokens:
        return ""

    summary_prompt = "Создай очень краткое содержание этого текста (200-300 слов), перечисляя только основные темы и ключевые моменты:"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Ты эксперт по созданию кратких резюме текстов."
            },
            {
                "role": "user",
                "content": f"{summary_prompt}\n\n{text[:50000]}"
            }  # Ограничиваем для создания общего обзора
        ],
        temperature=0.1,
        max_tokens=800)

    return response.choices[0].message.content


def process_text_with_chatgpt(text: str) -> str:
    """Обрабатывает текст с сохранением контекста между чанками"""
    # Создаем общий контекст всего текста
    # context_summary = extract_summary(text)

    chunks = split_text_by_tokens(text)
    total_chunks = len(chunks)
    results = []

    # Сообщение с контекстом для каждого чанка
    context_message = f"""
Это часть большого текста, разделенного на {total_chunks} частей. 

"""

    # Добавляем информацию о положении чанка в общем тексте
    for i, chunk in enumerate(chunks):
        position_info = f"[Часть {i+1} из {total_chunks}]\n\n"
        chunk_with_context = f"{position_info}{context_message}\n\n{chunk}"
        result = process_chunk(chunk_with_context)

        # Удаляем технические обозначения из результата
        result = result.replace(position_info, "")
        results.append(result)

    return "\n\n".join(results)
