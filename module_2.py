from tkinter import *
from tkinter import ttk

import psycopg2


def show_another_window(previous_window):
    def go_back_to_main():
        root.destroy()
        previous_window.deiconify()  # показать предыдущее окно

    root = Tk()
    root.title("Модуль 2")

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

    width = 900
    height = 700

    center_window(root, width, height)

    # Подключение к базе данных
    def connect_db(db_name):
        return psycopg2.connect(
            dbname=db_name,
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )

    # Обновление данных в таблице
    def update_table(data):
        for row in tree.get_children():
            tree.delete(row)
        for row in data:
            tree.insert('', END, values=row)

    # Полотно
    frame_main = Frame(root, bg='#00bfff', bd=2)
    frame_main.place(relx=0, y=0, relwidth=1, height=400)

    # Кнопка для возврата на main.py
    button_go_back_to_main = Button(frame_main, text="Вернуться в первый модуль", font=("Arial", 11, "bold"),
                                    command=go_back_to_main)
    button_go_back_to_main.place(relx=0.5, y=15, relwidth=0.3, height=30, anchor='center')

    # Рассчет суммы к оплате
    def calculate_the_amount_payable():
        conn = connect_db('demo')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("""SELECT
                                Clients.Client,
                                Clients.Phone,
                                Clients.Email,
                                Orders.orderid,
                                Orders.OrderDate,
                                (products.price * Orders.quantity_product + services.price * Orders.quantity_service) AS total_payable
                            FROM Orders
                            LEFT JOIN products ON Orders.productID = products.productID
                            LEFT JOIN services ON Orders.serviceID = services.serviceID
                            LEFT JOIN Clients ON Orders."clientID" = Clients."clientID"
                            ORDER BY Orders.OrderDate ASC""")
        clients = cursor.fetchall()
        # Вывод данных в таблицу
        update_table(clients)

        cursor.close()
        conn.close()

    # Кнопка для рассчета оплаты
    button = Button(frame_main, text="Рассчитать сумму к оплате", font=("Arial", 11, "bold"),
                    command=calculate_the_amount_payable)
    button.place(relx=0.5, y=55, relwidth=0.3, height=30, anchor='center')

    def delete_products_japan():
        conn = connect_db('demo')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Products WHERE CountryOfOrigin = 'Япония'")

        deleted_rows = cursor.rowcount  # Количество удалённых строк

        if deleted_rows > 0:
            info['text'] = 'Все товары из Японии успешно удалены'
        else:
            info['text'] = 'Все товары из Японии уже удалены'

        cursor.close()
        conn.close()

    # Кнопка для удаления товаров из Японии
    button_delete_products_japan = Button(frame_main, text="Удалить товары из Японии", font=("Arial", 11, "bold"),
                                          command=delete_products_japan)
    button_delete_products_japan.place(relx=0.5, y=308, relwidth=0.3, height=30, anchor='center')

    def update_the_price_of_Russian():
        conn = connect_db('demo')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("UPDATE Products SET Price = GREATEST(Price * 0.9, 0) WHERE CountryOfOrigin = 'Россия'")
        info['text'] = f'Цены на товары из России успешно уменьшены на 10%'

        cursor.close()
        conn.close()

    # Кнопка для удаления товаров из Японии
    button_update_the_price_of_Russian = Button(frame_main,
                                                text="Уменьшить цену на товары из России на 10%",
                                                font=("Arial", 11, "bold"), command=update_the_price_of_Russian)
    button_update_the_price_of_Russian.place(relx=0.5, y=350, relwidth=0.4, height=30, anchor='center')

    # Окно для вывода информации
    frame_bottom_info = Frame(root, bg='#5F9EA0', bd=5)
    frame_bottom_info.place(relx=0.15, y=450, relwidth=0.7, height=100)

    # Текстовая надпись, в которую будет выводиться информация
    info = Label(frame_bottom_info, text='Поле для вывода информации', bg='#ffb700', font=("Arial", 12, "bold"))
    info.place(relx=0.5, y=45, anchor='center')

    # Таблица для отображения результатов поиска
    columns = ("name", "phone", "email", "orderid", "orderdate", "payable")
    tree = ttk.Treeview(frame_main, columns=columns, show="headings")
    tree.heading("name", text="Клиент")
    tree.heading("phone", text="Телефон")
    tree.heading("email", text="Электронная почта")
    tree.heading("orderid", text="Номер заказа")
    tree.heading("orderdate", text="Дата заказа")
    tree.heading("payable", text="К оплате")

    tree.column("name", width=120)
    tree.column("phone", width=130)
    tree.column("email", width=160)
    tree.column("orderid", width=80)
    tree.column("orderdate", width=100)
    tree.column("payable", width=100)

    tree.place(relx=0.5, y=180, relwidth=0.9, height=200, anchor='center')

    root.mainloop()
