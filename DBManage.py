import psycopg2
import tkinter.messagebox

loginUser = ''  # тут хранится логин пользователя, получаемый из функции main.auth()


def selectClientName(id):  # функция достать клиента по id из БД - вызывает функцию getClient
    client = []
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='9810', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('getclient', [id])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()  # возвращает список всех строк, полученных из запроса
        for data in data:
            name = data[0]
            family = data[1]
            telephone = data[2]
            email = data[3]
            client.append(name)
            client.append(family)
            client.append(telephone)
            client.append(email)
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


def clientAdd(name, family, telephone, email):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='9810', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('clientadd',
                        [name, family, telephone, email])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message=" Клиент успешно добавлен в базу")
    return True


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


def getRole(login):
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('getrole', [login])  # пример вызова функции из БД , имя и параметр на вход
        role = cursor.fetchall()
        for data in role:
            namerole = data[0]
        conn.commit()
        conn.close()
        return str(namerole)
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def deleteClient(id):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='9810', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('deleteclient', [id])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
