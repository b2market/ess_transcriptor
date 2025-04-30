
# Запуск Russian Text Enhancer в Docker

## Локальный запуск с Docker Compose

1. Скопируйте файл `.env-example` в `.env` и укажите ваш API ключ OpenAI:
   ```
   cp .env-example .env
   ```

2. Отредактируйте файл `.env` и добавьте ваш API ключ OpenAI:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Запустите приложение с Docker Compose:
   ```
   docker-compose up -d
   ```

4. Приложение будет доступно по адресу: http://localhost:5001

## Запуск в Portainer

1. В интерфейсе Portainer перейдите к вашему стеку (Stack) или создайте новый.

2. Загрузите файл docker-compose.yml или вставьте его содержимое в поле редактора.

3. Добавьте переменную окружения OPENAI_API_KEY в настройках стека (во вкладке Environment variables).

4. Нажмите Deploy the stack для запуска приложения.

5. Приложение будет доступно на указанном хосте по порту 5001.

## Примечания

- Файл docker-compose.yml настроен для сохранения конфигурации Streamlit через volume
- Убедитесь, что порт 5001 не занят другими приложениями
- Для изменения порта, измените его как в docker-compose.yml, так и в Dockerfile
