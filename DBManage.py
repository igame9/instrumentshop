import sys
import psycopg2
import tkinter.messagebox


def selectClientName(id):  # функция достать клиента по id из БД - вызывает функцию selers
    client = []
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('selers', [id])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()  # возвращает список всех строк, полученных из запроса
        for data in data:
            name = data[0]
            family = data[1]
            client.append(name)
            client.append(family)
        cursor.close()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message="Успешное подключение к БД, ожидайте результат")
    return client


def selectDB():
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.execute("select * from client")
        data = cursor.fetchall()  # возвращает список всех строк, полученных из запроса
        cursor.close()
        conn.close()
    except psycopg2.OperationalError:
        print("Ошибка подключения к БД")
    print("Подключение прошло")
    return data


def testConn():
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
    except psycopg2.OperationalError:
        return False
    return True


def clientAdd(name, family):
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('clientadd', [name, family])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message=" Клиент успешно добавлен в базу")
    return True


def addQuery():
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO client (name,family) VALUES ('Niko','Two')")
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message="Успешное добавление нового пользователя")


def deleteQuery(id):
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.execute("DELETE from client where idclient = " + str(id))
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message="Успешное удаление данных")


def checkUser(name, family):
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('checkuser', [name, family])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()  # возвращает список всех строк, полученных из запроса
        for data in data:
            flag = data[0]
        cursor.close()
        conn.commit()
        conn.close()
        return flag
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
