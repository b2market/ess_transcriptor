
#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Russian Text Enhancer - Installation ===${NC}"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Ошибка: Python 3 не найден. Установите Python 3.11 или новее.${NC}"
    exit 1
fi

# Проверка версии Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${YELLOW}Найден Python ${PYTHON_VERSION}${NC}"

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Создание виртуального окружения...${NC}"
    python3 -m venv venv
fi

# Активация виртуального окружения
echo -e "${YELLOW}Активация виртуального окружения...${NC}"
source venv/bin/activate

# Обновление pip
echo -e "${YELLOW}Обновление pip...${NC}"
pip install --upgrade pip

# Установка зависимостей
echo -e "${YELLOW}Установка зависимостей...${NC}"
pip install -r requirements.txt

# Создание .env файла если его нет
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Создание .env файла...${NC}"
    cp .env-example .env
    echo -e "${RED}ВАЖНО: Отредактируйте файл .env и добавьте ваш OpenAI API ключ!${NC}"
fi

# Создание скрипта автоактивации
echo -e "${YELLOW}Создание скрипта автоактивации...${NC}"
cat > .envrc << 'EOF'
#!/bin/bash
source venv/bin/activate
export PATH="$VIRTUAL_ENV/bin:$PATH"
echo "Виртуальное окружение активировано"
EOF

chmod +x .envrc

echo -e "${GREEN}=== Установка завершена! ===${NC}"
echo -e "${YELLOW}Для автоматической активации окружения при входе в директорию:${NC}"
echo -e "1. Установите direnv: brew install direnv (macOS) или apt install direnv (Ubuntu)"
echo -e "2. Добавьте в ~/.bashrc или ~/.zshrc: eval \"\$(direnv hook bash)\" или eval \"\$(direnv hook zsh)\""
echo -e "3. Выполните: direnv allow"
echo ""
echo -e "${GREEN}Запуск: ./start.sh${NC}"
