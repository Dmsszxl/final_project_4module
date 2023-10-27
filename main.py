import tkinter as tk
from tkinter import ttk
import sqlite3




#создаем приложение(окно)
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    #Метод для хранения и инициализации объектов графического интерфейса
    def init_main(self):
        #панель инструментов
        tb = tk.Frame(bg='#d7d8e0', bd=2)
        tb.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        #добавление
        button_open_dialog = tk.Button(tb, bg='#d7d8e0', bd=0,
                                    image=self.add_img, command=self.open_dialog)
        button_open_dialog.pack(side=tk.LEFT)

        #изменение данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        button_edit_dialog = tk.Button(tb, bg='#d7d8e0', bd=0, 
                                    image=self.update_img, command=self.open_update_dialog)
        button_edit_dialog.pack(side=tk.LEFT)

        #удаление записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        button_delete = tk.Button(tb, bg='#d7d8e0', bd=0, 
                               image=self.delete_img, command=self.delete_records)
        button_delete.pack(side=tk.LEFT)

        #поиск
        self.search_img = tk.PhotoImage(file='./img/search.png')
        button_search = tk.Button(tb, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search_dialog)
        button_search.pack(side=tk.LEFT)

        #обновление
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        button_refresh = tk.Button(tb, bg='#d7d8e0', bd=0, 
                                image=self.refresh_img, command=self.view_records)
        button_refresh.pack(side=tk.LEFT)

        #Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'),
                                 height=45, show='headings')
        
        #параметры колонкам
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        # подписи
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("salary", text='Зарплата')

        #упаковка
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # добавление данных
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # обновление данных
    def update_record(self, name, tel, email, salary):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?''',
                          (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # вывод в виджет
    def view_records(self):
        self.db.c.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]
        
    # удаление записей
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    # метод дочернего окна
    def open_dialog(self):
        Child()

    # метод окна для изменения данных
    def open_update_dialog(self):
        Update()

    # метод окна для поиска
    def open_search_dialog(self):
        Search()

# класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        #подписи
        l_name = tk.Label(self, text='ФИО:')
        l_name.place(x=50, y=50)
        l_select = tk.Label(self, text='Телефон')
        l_select.place(x=50, y=80)
        l_sum = tk.Label(self, text='E-mail')
        l_sum.place(x=50, y=110)
        l_pay = tk.Label(self, text='Зарплата')
        l_pay.place(x=50, y=140)

        #строка ввода для наименования
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        #строка ввода для email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        #строка ввода для телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        #строка ввода для зарплаты
        self.entry_wage = ttk.Entry(self)
        self.entry_wage.place(x=200, y=140)

        #закрытие дочернего окна
        self.btn_cancel = ttk.Button(
            self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_wage.get()))
    

#класс окна для обновления
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_tel.get(),
                                                                          self.entry_wage.get()))

        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_wage.insert(0, row[4])


# класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        l_search = tk.Label(self, text='Поиск')
        l_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        button_cancel.place(x=185, y=50)

        button_search = ttk.Button(self, text='Поиск')
        button_search.place(x=105, y=50)
        button_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        button_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')


# класс БД
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS db (id integer primary key, name text, tel text, email text, salary text)''')
        self.conn.commit()

    # метод добавления в БД
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO db (name, tel, email, salary) VALUES (?, ?, ?, ?)''',
                       (name, tel, email,salary))
        self.conn.commit()




if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Сотрудники компании')
    root.geometry('800x600')
    root.resizable(False, False)
    root.mainloop()

    