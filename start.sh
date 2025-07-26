
#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Russian Text Enhancer - Запуск ===${NC}"

# Проверка существования виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${RED}Виртуальное окружение не найдено. Сначала запустите ./install.sh${NC}"
    exit 1
fi

# Активация виртуального окружения
echo -e "${YELLOW}Активация виртуального окружения...${NC}"
source venv/bin/activate

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}Файл .env не найден. Создайте его из .env-example и добавьте ваш OpenAI API ключ.${NC}"
    exit 1
fi

# Проверка наличия API ключа
if ! grep -q "OPENAI.*=.*[a-zA-Z0-9]" .env; then
    echo -e "${RED}OpenAI API ключ не найден в .env файле. Добавьте ваш ключ.${NC}"
    exit 1
fi

# Проверка установленных пакетов
echo -e "${YELLOW}Проверка зависимостей...${NC}"
python -c "import streamlit, openai, tiktoken" 2>/dev/null || {
    echo -e "${RED}Не все зависимости установлены. Запустите ./install.sh${NC}"
    exit 1
}

echo -e "${GREEN}Запуск приложения на http://localhost:9000${NC}"
echo -e "${YELLOW}Для остановки нажмите Ctrl+C${NC}"
echo ""

# Запуск Streamlit на порту 9000
streamlit run app.py --server.port 9000 --server.address 0.0.0.0
