import datetime
import base64
import os
import secrets
import string
import subprocess
from tkinter import *
from cryptography.fernet import Fernet

import psycopg2
from psycopg2 import sql

import module_2
import module_3


def open_module_2():
    root.withdraw()  # скрыть текущее окно
    module_2.show_another_window(root)  # открыть окно из working_with_customer_orders


def open_module_3():
    root.withdraw()  # скрыть текущее окно
    module_3.show_another_window(root)  # открыть окно из working_with_customer_orders


root = Tk()
root.title("Модуль 1")

width = 1000
height = 800


# Центрирование окна
def center_window(window, width, height):
    # Получаем ширину и высоту экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Вычисляем координаты для размещения окна по центру
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Устанавливаем размеры окна и его положение
    window.geometry(f'{width}x{height}+{x}+{y}')


center_window(root, width, height)

# Окно для перехода на другую страницу
frame_buttons = Frame(root, bg='#5F9EA0', bd=5)
frame_buttons.place(relx=0, y=0, relwidth=1, height=50)


# Кнопка для перехода на второй модуль
button_switching_to_the_module_2 = Button(frame_buttons,
                                          text="Перейти на второй модуль",
                                          font=("Arial", 10, "bold"),
                                          command=open_module_2)
button_switching_to_the_module_2.place(relx=0.3, rely=0.5, anchor='center')


# Кнопка для перехода на третий модуль
button_switching_to_the_module_3 = Button(frame_buttons,
                                          text="Перейти на третий модуль",
                                          font=("Arial", 10, "bold"),
                                          command=open_module_3)
button_switching_to_the_module_3.place(relx=0.7, rely=0.5, anchor='center')


class EmptyFieldError(Exception):
    """Пользовательское исключение для пустого поля"""
    pass


# Подключение к базе данных
def connect_db(db_name):
    return psycopg2.connect(
        dbname=db_name,
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )


# Генерация рандомного пароля
def generate_random_password(length):
    letters = string.ascii_letters
    digits = string.digits
    characters = letters + digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    if not any(char.isdigit() for char in random_string):
        random_string = random_string[:-1] + secrets.choice(digits)
    return random_string


# Создание 11-ти пользователей
def create_user():
    conn = connect_db('demo')
    conn.autocommit = True
    cursor = conn.cursor()

    for i in range(1, 12):
        try:
            connect_db(f"DB{i}")

            try:
                # Создание базы данных DB и подключение к ней
                cursor.execute(f'CREATE DATABASE "DB"')
                conn_db = connect_db(f"DB")
                conn_db.autocommit = True
                cursor_db = conn_db.cursor()

                # Создание таблицы пользователей
                cursor_db.execute(f"""CREATE TABLE "Users"(
                                    id bigserial,
                                    login text,
                                    password text,
                                    PRIMARY KEY (id))""")
                cursor_db.close()
                conn_db.close()
            except:
                info['text'] = f'Пользователи с базой данных DB уже созданы'

            # Генерация рандомного пароля
            random_password = generate_random_password(6)
            # Создание пользователя с рандомным паролем
            cursor.execute(f"CREATE USER u{i} WITH PASSWORD '{random_password}'")
            # Выдача прав только на одну таблицу
            cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE "DB{i}" TO u{i}')

            conn_db = connect_db(f"DB")
            conn_db.autocommit = True
            cursor_db = conn_db.cursor()

            # Заполнение таблицы Users
            cursor_db.execute(f"""INSERT INTO "Users"(
                                login, password)
                                VALUES ('u{i}', '{random_password}')""")

            info['text'] = f'Пользователи с заполненной базой данных DB успешно созданы'

            cursor_db.close()
            conn_db.close()
        except psycopg2.errors.DuplicateObject:
            info['text'] = f'Пользователи с базой данных DB уже созданы'

        except psycopg2.OperationalError:
            info['text'] = f'Сначала создайте 11 баз данных'

    cursor.close()
    conn.close()


# Создание 11-ти баз данных
def create_database():
    # Подключение к базе данных с передачей имени
    conn = connect_db('demo')
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        for i in range(1, 12):
            # Создание баз данных
            cursor.execute(f'CREATE DATABASE "DB{i}"')
            info['text'] = f'Базы данных успешно созданы'
    except:
        info['text'] = f'Базы данных уже созданы'

    # Закрытие подключения к базе данных
    cursor.close()
    conn.close()


# Создание полотна, какой у него фон и какая обводка
frame = Frame(root, bg='#ffb700', bd=5)
frame.place(relx=0.15, y=60, relwidth=0.7, height=260)

# Кнопка для создания баз данных
button_create_data_base = Button(frame, text='Создать 11 баз данных',
                                 font=("Arial", 10, "bold"), command=create_database)
button_create_data_base.place(relx=0.5, y=25, anchor='center')

# Кнопка для создания пользователей
button_create_user = Button(frame, text='Создать 11 пользователей с базой данных DB и заполнить таблицу Users',
                            font=("Arial", 10, "bold"), command=create_user)
button_create_user.place(relx=0.5, y=65, anchor='center')

# Ключ и инициализация Fernet
key = b'Rqqy2VVSKv6_yu3EGOYs2BWHCVyJbSyjyNXXpQ_p8X0='
cipher_suite = Fernet(key)


# Функция шифрования паролей
def encrypt_passwords():
    try:
        conn = connect_db('DB')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute('SELECT login, password FROM "Users"')
        users = cursor.fetchall()

        try:
            for user in users:
                if len(user[1]) > 6:
                    info['text'] = f'Пароли уже зашифрованы'
                else:
                    # Шифрация пароля
                    encrypted_password = cipher_suite.encrypt(user[1].encode())
                    # Кодировка зашифрованных паролей в base64
                    encoded_password = base64.urlsafe_b64encode(encrypted_password).decode()
                    # Подставка зашифрованного пароля с проверкой к какому пользователю
                    cursor.execute('UPDATE "Users" SET password = %s WHERE login = %s', (encoded_password, user[0]))
                    info['text'] = f'Пароли успешно зашифрованы'
        except:
            info['text'] = f'Не удалось зашифровать пароли'
        cursor.close()
        conn.close()
    except:
        info['text'] = f'Сначала создайте 11 пользователей с базой данных DB'


# Кнопка при нажатии которой будет срабатывать метод шифрования паролей "encrypt_passwords"
button_for_password_encryption = Button(frame, text='Зашифровать пароли в базе данных', font=("Arial", 10, "bold"),
                                        command=encrypt_passwords)
button_for_password_encryption.place(relx=0.5, y=105, anchor='center')


# Функция дешифрования паролей
def decrypt_passwords():
    try:
        conn = connect_db('DB')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute('SELECT login, password FROM "Users"')
        users = cursor.fetchall()

        decrypted_users = []
        try:
            for user in users:
                # Декодировка паролей из base64
                decoded_password = base64.urlsafe_b64decode(user[1])
                # Дешифровка закодированных паролей
                decrypted_password = cipher_suite.decrypt(decoded_password).decode()
                decrypted_users.append((user[0], decrypted_password))
                info_text = "\n".join([f"логин: {user[0]}, пароль: {user[1]}" for user in decrypted_users])
                info.config(text=info_text)
        except:
            info['text'] = f'Сначала зашифруйте пароли'

        cursor.close()
        conn.close()
    except:
        info['text'] = f'Сначала создайте 11 пользователей с базой данных DB'


# Кнопка при нажатии которой будет срабатывать метод шифрования паролей "encrypt_passwords"
button_for_decrypt_passwords = Button(frame, text='Просмотр расшифрованных паролей', font=("Arial", 10, "bold"),
                                      command=decrypt_passwords)
button_for_decrypt_passwords.place(relx=0.5, y=145, anchor='center')


# Бэкап базы данных
def backup_database(data):
    try:
        # Проверка на существование базы данных
        conn = connect_db('DB')
        conn.close()
        # подключение к базе данных для создания бэкапа
        user = "postgres"
        password = "123"
        host = "localhost"
        db_name = data
        backup_folder = r"C:\main\tK\backup"
        backup_file = os.path.join(backup_folder, f"{db_name}.sql")

        dump_command = [
            'pg_dump',
            '-U', user,
            '-h', host,
            '-F', 'c',  # формат .sql
            '-f', backup_file,  # имя файла резервной копии
            db_name
        ]

        try:
            # Устанавливаем переменную окружения PGPASSWORD для передачи пароля
            env = {
                'PGPASSWORD': password,
                **os.environ  # Наследуем текущие переменные окружения
            }

            # Выполнение бэкапа
            subprocess.run(dump_command, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            info['text'] = f'Успешное создание бэкапа базы данных DB'

        except subprocess.CalledProcessError as e:
            info['text'] = f'Не удается найти дерикторию'
    except psycopg2.OperationalError:
        info['text'] = f'Сначала создайте 11 пользователей с базой данных DB'


# Кнопка при нажатии которой будет срабатывать метод "backup_database"
button_for_creating_a_database_backup = Button(frame, text='Создать бэкап базы данных DB', font=("Arial", 10, "bold"),
                                               command=lambda: backup_database('DB'))
button_for_creating_a_database_backup.place(relx=0.5, y=185, anchor='center')


# Восстановление базы данных
def restore_database():
    # подключение к базе данных
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_USER = "postgres"
    DB_PASSWORD = "123"
    NEW_DB_NAME = "DB_restore"  # Имя новой базы данных для восстановления

    # Путь к файлу резервной копии
    BACKUP_FILE = r"C:\main\tK\backup\DB.sql"

    # Проверка наличия файла резервной копии
    if not os.path.exists(BACKUP_FILE):
        info['text'] = f'Сначала создайте бэкап базы данных'
        raise FileNotFoundError(f'Файл бэкапа {BACKUP_FILE} не найден')

    # Создание новой базы данных
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database="postgres")
        conn.autocommit = True
        cursor = conn.cursor()
        # Создание новой базы данных
        cursor.execute(f'CREATE DATABASE "{NEW_DB_NAME}"')

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        pass

    # Восстановление данных в новую базу данных
    restore_command = [
        "pg_restore",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", NEW_DB_NAME,
        "-v", BACKUP_FILE
    ]

    # Установка переменной окружения для пароля
    env = os.environ.copy()
    env['PGPASSWORD'] = DB_PASSWORD

    # Восстановление базы данных
    result = subprocess.run(restore_command, env=env)

    # Вывод информации пользователю
    if result.returncode == 0:
        info['text'] = f'Восстановление базы данных успешно завершено'
    else:
        info['text'] = f'База данных уже восстановлена'


# Кнопка при нажатии которой будет срабатывать метод "restore_database"
button_for_creating_a_database_backup = Button(frame, text='Восстановить базу данных DB в базу данных DB_restore',
                                               font=("Arial", 10, "bold"),
                                               command=restore_database)
button_for_creating_a_database_backup.place(relx=0.5, y=225, anchor='center')

# Окно для вывода информации
frame_bottom_info = Frame(root, bg='#ffb700', bd=5)
frame_bottom_info.place(relx=0.15, y=400, relwidth=0.7, height=210)

# Текстовая надпись, в которую будет выводиться информация
info = Label(frame_bottom_info, text='Поле для вывода информации', bg='#ffb700', font=("Arial", 12, "bold"))
info.place(relx=0.5, y=98, anchor='center')

root.mainloop()
