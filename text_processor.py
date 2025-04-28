import os
from openai import OpenAI


def split_text_into_chunks(text, chunk_size=None, line_count=None):
    """
    Split a long text into smaller chunks for processing.
    Either by character count or by number of sentences.
    """
    # Split text into sentences (approximately)
    sentences = []
    # Split by common sentence endings while preserving line breaks
    for paragraph in text.split('\n'):
        paragraph_sentences = []
        # Common Russian sentence endings
        for sent_end in ['. ', '! ', '? ', '... ']:
            paragraph = paragraph.replace(sent_end, sent_end + '|||||')
        # Split by our marker
        for sent in paragraph.split('|||||'):
            if sent.strip():
                paragraph_sentences.append(sent)
        sentences.extend(paragraph_sentences)

    # If no chunk specifications are provided, return as single chunk
    if not chunk_size and not line_count:
        return [text]

    # If line count is specified, split by number of sentences
    if line_count:
        chunks = []
        total_sentences = len(sentences)

        for i in range(0, total_sentences, line_count):
            chunk_sentences = sentences[i:i + line_count]
            chunks.append(' '.join(chunk_sentences))

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
    Сохрани весь текст полностью, исправляя только пунктуацию и структуру без удаления предложений, примеров, пояснений или терминов.
    Требования к оформлению:
    Разбей текст на логические блоки с подзаголовками. Не нужно их мельчить.  
    Важно не упустить детали  
    Перечисления и примеры оформляй в аккуратные списки.
    Все роли, термины и ключевые идеи должны остаться без изменений.
    Подача текста должна быть в формате учебной книги: чисто, тезисно, логично, легко читаемо.
    Сохраняй авторский стиль и интонацию — не перефразируй.
    Оставляй все примеры и пояснения.
    Не упрощай и не обобщай текст — все детали и нюансы важны.
    Цель: текст должен читаться как глава учебной книги — ясно структурированный, но с сохранением живого авторского тона
    Ответь в формате Markdown. Но никаких тегов вроде тройной обратной кавычки не используй. Просто маркдаун
    Вот текст для обработки:
    
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role":
                "system",
                "content":
                "You are a Russian language expert who improves transcribed text while preserving its content."
            }, {
                "role": "user",
                "content": prompt + text
            }],
            temperature=0.3,  # Lower temperature for more consistent results
            max_tokens=4096,  # Adjust as needed
        )

        # Extract the improved text from the response
        improved_text = response.choices[0].message.content
        return improved_text

    except Exception as e:
        raise Exception(f"Error processing text with ChatGPT: {str(e)}")
