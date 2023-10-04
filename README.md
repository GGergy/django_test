![pipline](https://gitlab.example.com/git@gitlab.crja72.ru/157809-gergyalt-47231.git/badges/main/pipeline.svg)
# создание виртуальной среды
python -m venv venv

# Активация виртуальной среды
source venv/bin/activate

# Установка зависимостей
pip install -r requirements/prod.txt

- для запуска проекта в режиме разработки или тестировки используйте файлы test.txt и dev.txt соответственно 

# Настройка ключа
Откройте файл lyceum/lyceum/test.env, и в поле "SECRET" впишите свой секретный ключ

# Запуск хоста
- cd lyceum
- python manage.py runserver
