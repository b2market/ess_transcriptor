
# Запуск проекта Russian Text Enhancer в Portainer

## Вариант 1: Клонирование Git репозитория и сборка контейнера

1. В Portainer перейдите в раздел "Stacks" и нажмите "Add stack".

2. Создайте файл `docker-compose.yml` с следующим содержимым:
```yaml
version: '3.8'

services:
  russian-text-enhancer:
    image: russian-text-enhancer
    container_name: russian-text-enhancer
    restart: unless-stopped
    ports:
      - "5001:5001"
    environment:
      - OPENAI_API_KEY=ваш_openai_api_ключ
    volumes:
      - ./.streamlit:/app/.streamlit
```

3. В разделе "Build Method" выберите "Repository".

4. Вставьте URL вашего Git репозитория в поле "Repository URL".

5. Нажмите "Deploy the stack".

## Вариант 2: Запуск с готовым docker-compose.yml из репозитория

1. Клонируйте ваш репозиторий на сервер, где установлен Portainer:
```bash
git clone URL_ВАШЕГО_РЕПОЗИТОРИЯ
```

2. Перейдите в директорию с проектом:
```bash
cd имя_вашего_проекта
```

3. Создайте файл `.env` с вашим API ключом OpenAI:
```
OPENAI_API_KEY=ваш_openai_api_ключ
```

4. В Portainer перейдите в "Stacks" -> "Add stack".

5. В разделе "Build Method" выберите "Upload" или "Web editor" и загрузите/вставьте содержимое docker-compose.yml из вашего репозитория.

6. В секции "Environment variables" добавьте переменную `OPENAI_API_KEY` с вашим ключом OpenAI API.

7. Нажмите "Deploy the stack".

## Проверка работы

После успешного запуска ваше приложение должно быть доступно по адресу:
```
http://IP_СЕРВЕРА:5001
```

Где `IP_СЕРВЕРА` - это IP-адрес вашего сервера, на котором запущен Portainer.
