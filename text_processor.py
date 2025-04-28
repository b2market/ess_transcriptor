import os
from openai import OpenAI


def split_text_into_chunks(text, chunk_size=None, line_count=None):
    """
    Split a long text into smaller chunks for processing.
    Either by character count or by number of lines.
    """
    # If no chunk specifications are provided, return as single chunk
    if not chunk_size and not line_count:
        return [text]

    # If line count is specified, split by number of raw lines
    if line_count:
        # Split the text into individual lines
        lines = text.split('\n')
        chunks = []

        # Create chunks of the specified number of lines
        for i in range(0, len(lines), line_count):
            chunk_lines = lines[i:i + line_count]
            # Join the lines back together to form a chunk
            chunk = '\n'.join(chunk_lines)
            # Only add non-empty chunks
            if chunk.strip():
                chunks.append(chunk)

        # Ensure we have at least one chunk, even if it's smaller than line_count
        if not chunks and text.strip():
            chunks.append(text)

        return chunks

    # Otherwise split by character count
    if chunk_size:
        # If text is shorter than chunk_size, return it as a single chunk
        if len(text) <= chunk_size:
            return [text]

        chunks = []

        # Try to split on paragraph breaks
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for paragraph in paragraphs:
            # If adding this paragraph exceeds chunk size and we already have content
            if len(current_chunk) + len(
                    paragraph) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = paragraph
            # Otherwise, add to current chunk
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(current_chunk)

        # If we have extremely long paragraphs, we might need to split them further
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= chunk_size:
                final_chunks.append(chunk)
            else:
                # Split by sentences (roughly)
                sentences = chunk.replace('. ', '.\n').split('\n')
                sub_chunk = ""

                for sentence in sentences:
                    if len(sub_chunk) + len(
                            sentence) > chunk_size and sub_chunk:
                        final_chunks.append(sub_chunk)
                        sub_chunk = sentence
                    else:
                        if sub_chunk:
                            sub_chunk += " " + sentence
                        else:
                            sub_chunk = sentence

                if sub_chunk:
                    final_chunks.append(sub_chunk)

        return final_chunks

    return [text]


def process_text_with_chatgpt(text, api_key=None, model="gpt-4o"):
    """
    Process Russian text through ChatGPT to enhance readability
    while preserving content.
    """
    # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    # do not change this unless explicitly requested by the user

    # Use environment variable if api_key is not provided
    if not api_key:
        # Try to get API key from different environment variables
        api_key = os.environ.get("OPENAI_KEY")

        # If not found, print debugging information
        if not api_key:
            print("DEBUG - Environment variables:", [
                key
                for key in os.environ.keys() if "OPENAI" in key or "API" in key
            ])
            # Try alternate key name as fallback
            api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise Exception(
            "No OpenAI API key found. Please add OPENAI_KEY to your Secrets tab. Available env vars: "
            + str([key for key in os.environ.keys()]))

    client = OpenAI(api_key=api_key)

    # The prompt provided by the user
    prompt = """
   Тебе нужно обработать текст по следующим требованиям:

   В прошлый раз было слишком много сокращего и упущено. Многое осталось в монолитном виде. Попробуй еще раз.

1. Исправь только орфографию, пунктуацию и структурные ошибки. Содержание текста изменять запрещено.
2. Сохрани все авторские примеры, пояснения, термины и перечисления. Ничего не убирай и не добавляй.
3. Оформи текст в формате структурированной книги:
   - Логические части разделяй пустой строкой.
   - Для крупных смысловых блоков добавляй заголовки в формате Markdown:
     - `#` — для основного заголовка темы.
     - `##` — для крупных разделов внутри темы.
     - `###` — для подпунктов или вложенных блоков.
   - Перечисления оформляй списками через дефис `-`.
   - Основные идеи или важные термины выделяй **жирным** (`**`).
   - Акценты внутри текста оформляй *курсивом* (`*`).
4. Абзацы делай короткими (3–5 строк), без длинных полотен текста.
5. Стилистику текста сохраняй авторскую: учебно-повествовательную, серьёзную.
6. Все блоки должны быть легко читаемыми, понятными как для книги или учебника.
7. Не нужно делать выводы, заключения или рекомендации.

Запрещается:
- Сокращать примеры, описания, термины.
- Перефразировать текст.
- Добавлять что-то от себя.
- Менять последовательность подачи мыслей.

Формат ответа: чистый текст с применением Markdown-разметки для структуры и акцентов.

Задача — оформить текст так, чтобы он выглядел как готовая глава учебной книги, только исправленный и структурированный.



    Вот текст для обработки:

    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role":
                "system",
                "content":
                "Ты - редактор, который профессионально корректирует текст, сохраняя его содержание. Ты имеешь экспертизу в коучинге"
            }, {
                "role": "user",
                "content": prompt + text
            }],
            temperature=0,  # Lower temperature for more consistent results
            # Check the length of the input text to set max_tokens
            max_tokens=len(text.split()) +
            100  # Allow some buffer for output tokens
        )

        # Extract the improved text from the response
        improved_text = response.choices[0].message.content
        return improved_text

    except Exception as e:
        raise Exception(f"Error processing text with ChatGPT: {str(e)}")