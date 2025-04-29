        import os
        import openai
        import tiktoken

        openai.api_key = os.environ.get("OPENAI_KEY") or os.environ.get("OPENAI_API_KEY", "")
        OPTIMIZED_SYSTEM_MESSAGE = """
        Ты работаешь с учебным, лекционным текстом, который должен сохранить авторский стиль, плавность и структуру повествования.
        Прочти текст и аккуратно:
        - Исправь орфографические и пунктуационные ошибки.
        - Сохрани эмоциональные выражения, повторения, авторские отступления и метафоры.
        - Не меняй порядок предложений и абзацев.
        - Не сокращай текст, не убирай смысловые блоки.
        - Не переписывай текст от себя.

        Цель: сделать текст чище и легче для чтения, сохраняя стиль, эмоции и авторский поток мысли.
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

        client = OpenAI(api_key=os.environ.get("OPENAI_KEY") or os.environ.get("OPENAI_API_KEY", ""))

        def process_chunk(chunk: str, system_message: str = OPTIMIZED_SYSTEM_MESSAGE):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": chunk}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            return response.choices[0].message.content

        def process_text_with_chatgpt(text: str) -> str:
            chunks = split_text_by_tokens(text)
            results = [process_chunk(chunk) for chunk in chunks]
            return "\n\n".join(results)
