import os
import openai
import tiktoken
from openai import OpenAI

openai.api_key = os.environ.get("OPENAI_KEY") or os.environ.get(
    "OPENAI_API_KEY", "")
ADVANCED_SYSTEM_MESSAGE = """
Ты работаешь с лекционным текстом, который разделен на части для обработки. Твоя задача:

- Аккуратно исправить орфографические и пунктуационные ошибки.
- Каждое предложение должно сохранить исходный смысл.
- Сохранить эмоциональные отступления, авторский стиль, метафоры.
- НЕ сокращать текст и не менять порядок мыслей.
- Там, где возможно, добавить структуру в формате Markdown:
    - Заголовки markdown для новых смысловых блоков.
    - Выделять ключевые мысли жирным шрифтом (**важное**).
    - Выделять сильные коучинговые вопросы курсивом (*вопрос*).
    - Если предложение сложное то разбить его на отдельные предложения или тезисы в виде списка (- пункт).
    - Преобразовывать перечисления в аккуратные списки (- пункт).
- Сохранять плавность и естественность текста.
- Не делать резких переписок или изменений смысла.
- Обрабатывай только свой фрагмент текста, однако учитывай общий контекст если он предоставлен.
- Если это не первая часть текста, убедись что переход между частями плавный.
- Если видишь, что мысль продолжается с предыдущей части, сделай плавный переход.

Главная цель: повысить читаемость, оформить текст структурно красиво, но оставить авторскую подачу живой и сохранить целостность всего материала.
"""

# Используем модель с поддержкой большого контекста
MODEL = "gpt-4-turbo"
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
                                              max_tokens=2000)
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
            {"role": "system", "content": "Ты эксперт по созданию кратких резюме текстов."},
            {"role": "user", "content": f"{summary_prompt}\n\n{text[:50000]}"}  # Ограничиваем для создания общего обзора
        ],
        temperature=0.3,
        max_tokens=800
    )
    
    return response.choices[0].message.content

def process_text_with_chatgpt(text: str) -> str:
    """Обрабатывает текст с сохранением контекста между чанками"""
    # Создаем общий контекст всего текста
    context_summary = extract_summary(text)
    
    chunks = split_text_by_tokens(text)
    total_chunks = len(chunks)
    results = []
    
    # Сообщение с контекстом для каждого чанка
    context_message = f"""
Это часть большого текста, разделенного на {total_chunks} частей. 
При обработке учитывай следующий общий контекст всего текста:

{context_summary}

Сосредоточься только на текущем фрагменте, но имей в виду общий контекст.
"""
    
    # Добавляем информацию о положении чанка в общем тексте 
    for i, chunk in enumerate(chunks):
        position_info = f"[Часть {i+1} из {total_chunks}]\n\n"
        chunk_with_context = f"{position_info}{context_message if context_summary else ''}\n\n{chunk}"
        result = process_chunk(chunk_with_context)
        
        # Удаляем технические обозначения из результата
        result = result.replace(position_info, "")
        results.append(result)
    
    return "\n\n".join(results)
