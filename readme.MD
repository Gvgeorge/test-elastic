Решение тестового задания:

"Необходимо написать очень простой поисковик по текстам документов. Данные хранятся в БД по желанию, поисковый индекс в эластике."

Сделал на фастапи, документацию фреймворк генерирует сам.
Использовал SQLite для простоты. Вебсервер, я так понимаю, тоже поднимать не требуется.

Поднимать либо через запуск файла main.py, раскомментировав, в настройках "settings.py" соответствующую строку, и установив переменные окружения ELASTIC_USERNAME и ELASTIC_PASSWORD (elastic, elastic).

Либо через докер docker-compose up.

Непосредственно поиск по адресу elastic/search/{text}. Удаление elastic/delete_doc/{doc_id}


По структуре, в папке api - вьюхи, в сервисах - логика, в моделях - модели pydantic.

Структура БД в tables.py, настройки в settings.py