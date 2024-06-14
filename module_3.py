from tkinter import *
from tkinter import ttk
import psycopg2


def show_another_window(previous_window):
    root = Tk()
    root.title("Модуль 3")

    # Возврат на main.py
    def go_back_to_main():
        root.destroy()
        previous_window.deiconify()  # показать предыдущее окно

    button = Button(root, text="Вернуться в первый модуль", font=("Arial", 10, "bold"), bg="lightblue",
                    command=go_back_to_main)
    button.pack(padx=10, pady=10)

    # Центрирование окна
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f'{width}x{height}+{x}+{y}')

    # Настройка ширины и высоты
    width = 800
    height = 500

    center_window(root, width, height)

    # Подключение к базе данных
    def connect_db():
        return psycopg2.connect(
            dbname="demo",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )

    # Поиск в базе данных по вводу пользователя
    def search_database(query):
        conn = connect_db()
        cursor = conn.cursor()

        query_str = """        
                    SELECT
                        Clients.Client AS Client,
                        Clients.Phone AS Phone,
                        Clients.Email AS Email,
                        Orders.OrderDate,
                        Employees.Employee AS Employee
                    FROM Orders
                    LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                    LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
                    WHERE Client LIKE %s
                    OR Clients.phone LIKE %s
                    OR Clients.email LIKE %s
                    OR Employee LIKE %s"""
        cursor.execute(query_str, (f'{query}%', f'{query}%', f'{query}%', f'{query}%',))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    # Фильтр по выбору пользователя
    def filter_database(client_name):
        conn = connect_db()
        cursor = conn.cursor()

        query_str = """SELECT
                            Clients.Client AS Client,
                            Clients.Phone AS Phone,
                            Clients.Email AS Email,
                            Orders.OrderDate,
                            Employees.Employee AS Employee
                        FROM Orders
                        LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                        LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
                        WHERE Client LIKE %s"""
        cursor.execute(query_str, (f'{client_name}%',))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    # Поиск по вводу пользователя и обновление таблицы
    def search_action():
        query = search_entry.get()
        results = search_database(query)
        update_table(results)

    # Фильтр клиента и обновление таблицы
    def filter_action():
        client_name = client_combobox.get()
        results = filter_database(client_name)
        update_table(results)

    # Обновление данных в таблице
    def update_table(data):
        for row in tree.get_children():
            tree.delete(row)
        for row in data:
            tree.insert('', END, values=row)

    # Вывод всех клиентов
    def get_client_list():
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""SELECT DISTINCT
                                Clients.Client AS Client,
                                Clients.Phone AS Phone,
                                Clients.Email AS Email,
                                Orders.OrderDate,
                                Employees.Employee AS Employee
                            FROM Orders
                            LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                            LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID""")
        clients = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return clients

    # Поле ввода и кнопка "Найти"
    search_frame = Frame(root)
    search_frame.pack(pady=10)

    sort_label = Label(search_frame, text="Введите строку поиска:", font=("Arial", 10, "bold"))
    sort_label.pack(side=LEFT)

    # Строка поиска
    search_entry = Entry(search_frame, width=40, font=("Arial", 12))
    search_entry.pack(side=LEFT, padx=10)

    search_button = Button(search_frame, text="Найти", font=("Arial", 10, "bold"), bg="lightblue",
                           command=search_action)
    search_button.pack(side=LEFT)

    # Выпадающий список клиентов и кнопка "Фильтровать"
    filter_frame = Frame(root)
    filter_frame.pack(pady=10)

    sort_label = Label(filter_frame, text="Выберите клиента:", font=("Arial", 10, "bold"))
    sort_label.pack(side=LEFT)

    clients = get_client_list()
    client_combobox = ttk.Combobox(filter_frame, values=clients, font=("Arial", 10))
    client_combobox.pack(side=LEFT, padx=10)

    filter_button = Button(filter_frame, text="Фильтровать", font=("Arial", 10, "bold"), bg="lightblue",
                           command=filter_action)
    filter_button.pack(side=LEFT)

    # Сортировка и радио кнопки

    # Словарь для перевода
    translation_dict = {
        "Клиент": "Client",
        "Дата заказа": "OrderDate",
        "Сотрудник": "Employee"
    }

    def filter_sort():
        conn = connect_db()
        cursor = conn.cursor()

        order_by = sort_combobox.get()
        translated_value = translation_dict.get(order_by, "")

        if var_radio.get() == 0:
            cursor.execute(f"""SELECT
                                    Clients.Client AS Client,
                                    Clients.Phone AS Phone,
                                    Clients.Email AS Email,
                                    Orders.OrderDate,
                                    Employees.Employee AS Employee
                                FROM Orders
                                LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                                LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID ORDER BY {translated_value} DESC""")
        elif var_radio.get() == 1:
            cursor.execute(f"""SELECT
                                    Clients.Client AS Client,
                                    Clients.Phone AS Phone,
                                    Clients.Email AS Email,
                                    Orders.OrderDate,
                                    Employees.Employee AS Employee
                                FROM Orders
                                LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                                LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID ORDER BY {translated_value} ASC""")

        results_all_clients = cursor.fetchall()
        cursor.close()
        conn.close()
        update_table(results_all_clients)

    sort_frame = Frame(root)
    sort_frame.pack(pady=10)

    sort_label = Label(sort_frame, text="Сортировать по:", font=("Arial", 10, "bold"))
    sort_label.pack(side=LEFT)

    sort_combobox = ttk.Combobox(sort_frame, values=["Клиент", "Дата заказа", "Сотрудник"], font=("Arial", 10))
    sort_combobox.set("Клиент")
    sort_combobox.pack(side=LEFT, padx=10)

    var_radio = IntVar(root)

    asc_button = Radiobutton(sort_frame, text="По возрастанию", variable=var_radio, value=1, font=("Arial", 10))
    asc_button.pack(side=LEFT, padx=10)

    desc_button = Radiobutton(sort_frame, text="По убыванию", variable=var_radio, value=0, font=("Arial", 10))
    desc_button.pack(side=LEFT, padx=10)

    sort_button = Button(sort_frame, text="Сортировать", font=("Arial", 10, "bold"), bg="lightblue",
                         command=filter_sort)
    sort_button.pack(side=LEFT, padx=20)

    # Вывод всех клиентов из базы данных
    filter_all_frame = Frame(root)
    filter_all_frame.pack(pady=10)

    def filter_all_clients():
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(f"""SELECT
                                Clients.Client AS Client,
                                Clients.Phone AS Phone,
                                Clients.Email AS Email,
                                Orders.OrderDate,
                                Employees.Employee AS Employee
                            FROM Orders
                            LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                            LEFT JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID""")
        results_all_clients = cursor.fetchall()

        cursor.close()
        conn.close()

        update_table(results_all_clients)

    filter_all_clients_button = Button(filter_all_frame, text="Показать все", font=("Arial", 10, "bold"),
                                       bg="lightblue", command=filter_all_clients)
    filter_all_clients_button.pack()

    # Таблица для отображения результатов поиска
    columns = ("name", "phone", "email", "orderdate", "Employee")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("name", text="Клиент")
    tree.heading("phone", text="Телефон")
    tree.heading("email", text="Электронная почта")
    tree.heading("orderdate", text="Дата заказа")
    tree.heading("Employee", text="Сотрудник")

    tree.column("name", width=120)
    tree.column("phone", width=130)
    tree.column("email", width=160)
    tree.column("orderdate", width=100)
    tree.column("Employee", width=120)

    tree.pack(pady=10, padx=10)

    root.mainloop()
