import os
import openai
import tiktoken
from openai import OpenAI

openai.api_key = os.environ.get("OPENAI_KEY") or os.environ.get(
    "OPENAI_API_KEY", "")
ADVANCED_SYSTEM_MESSAGE = """
Ты работаешь с лекционным текстом. Твоя задача:
- Аккуратно исправить орфографические и пунктуационные ошибки.
- Сохранить эмоциональные отступления, авторский стиль, метафоры.
- НЕ сокращать текст и не менять порядок мыслей.
- Там, где возможно, добавить структуру в формате Markdown:
    - Заголовки (## ) для новых смысловых блоков.
    - Выделять ключевые мысли жирным шрифтом (**важное**).
    - Преобразовывать перечисления в аккуратные списки (- пункт).
- Сохранять плавность и естественность текста.
- Не делать резких переписок или изменений смысла.

Главная цель: повысить читаемость, оформить текст структурно красиво, но оставить авторскую подачу живой.
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
                                              temperature=0.5,
                                              max_tokens=2000)
    return response.choices[0].message.content


def process_text_with_chatgpt(text: str) -> str:
    chunks = split_text_by_tokens(text)
    results = [process_chunk(chunk) for chunk in chunks]
    return "\n\n".join(results)
