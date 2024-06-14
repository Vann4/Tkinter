import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2 import sql

# Параметры подключения к базе данных
db_params = {
    'dbname': 'demo',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Подключение к базе данных
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Функция для получения данных из базы данных
def get_data():
    cur.execute("SELECT name, phone, email, order_date, order_status FROM ddd")
    return cur.fetchall()

# Функция для фильтрации данных
def filter_data(client_name):
    query = sql.SQL("SELECT name, phone, email, order_date, order_status FROM ddd WHERE client = %s")
    cur.execute(query, (client_name,))
    return cur.fetchall()

# Функция для отображения данных в таблице
def show_data(data):
    for row in tree.get_children():
        tree.delete(row)
    for row in data:
        tree.insert("", "end", values=row)

# Функция для обработки кнопки "Фильтровать"
def filter_button():
    client_name = client_combo.get()
    data = filter_data(client_name)
    show_data(data)

# Функция для обработки кнопки "Показать все"
def show_all_button():
    data = get_data()
    show_data(data)

# Создание основного окна
root = tk.Tk()
root.title("Работа с заказами клиентов")

# Виджеты для фильтрации и поиска
client_combo = ttk.Combobox(root)
client_combo.grid(row=0, column=1, padx=10, pady=10)

filter_button = tk.Button(root, text="Фильтровать", command=filter_button)
filter_button.grid(row=0, column=2, padx=10, pady=10)

show_all_button = tk.Button(root, text="Показать все", command=show_all_button)
show_all_button.grid(row=0, column=3, padx=10, pady=10)

# Таблица для отображения данных
columns = ("Клиент", "Телефон", "Электронная почта", "Дата заказа", "Сотрудник")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Заполнение combobox данными клиентов
cur.execute("SELECT DISTINCT name FROM ddd")
clients = [row[0] for row in cur.fetchall()]
client_combo['values'] = clients

# Показ всех данных при запуске программы
show_all_button

root.mainloop()

# Закрытие подключения к базе данных
cur.close()
conn.close()