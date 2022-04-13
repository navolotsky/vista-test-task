# Тестовое задание от Виста: телефонная книжка на PyQt + MariaDB
Приложение находится в процессе разработки.

В dev-окружении запускалось на Windows 10 + PyQt 5.12.1 + Python 3.7.9 x64 + MariaDB 10.6.4
В переменной окружения `PATH` [должен](https://doc.qt.io/qt-5/sql-driver.html#how-to-build-the-qmysql-plugin-on-windows) находиться путь к `libmysql.dll` или `libmariadb.dll`.

Запуск (при нахождении в директории проекта)
`python -m phone_book`

## Развертывание для разработки
### Сервер
1. Установить MariaDB обычным образом
2. Запустить `create_database.sql`
3. По желанию запустить `add_test_data.sql`
### Клиент
1. Создать виртуальное окружение Python 3.7+, например, через **virtualenv**
2. Активировать его
3. `python -m pip -r requirements.txt`. Важно установить PyQt5 версии не выше 5.12.1, поскольку в более поздних версиях в поставку не входит драйвер для MariaDB `qsqlmysql.dll`
4. В файле `phone_book/phone_book_defaults.ini` прописать настройки для соединия с БД.
5. С активированным виртуальным окружением, находясь в директории проекта, запустить программу: `python -m phone_book`
