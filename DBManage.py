import psycopg2
import tkinter.messagebox

import connectionParams

loginUser = ''  # тут хранится логин пользователя, получаемый из функции main.auth()


def selectClientName(Email):  # функция достать клиента по id из БД - вызывает функцию getClient
    client = []
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='9810', host=connectionParams.host, port=connectionParams.host)
        cursor = conn.cursor()
        cursor.callproc('getclientbyemail', [Email])  # пример вызова функции из БД , имя и параметр на вход
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


def testConn():
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user='andrey',
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
    except psycopg2.OperationalError:
        return False
    return True


def clientAdd(name, family, telephone, email):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='9810', host=connectionParams.host, port=connectionParams.port)
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
        conn = psycopg2.connect(dbname=connectionParams.dbName, user='andrey',
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
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
        conn = psycopg2.connect(dbname=connectionParams.dbName, user='andrey',
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
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
    inform = []
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='9810', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('checkdelete', [id])  # пример вызова функции из БД , имя и параметр на вход
        info = cursor.fetchall()
        for inf in info:
            message = inf[0]
        cursor.close()
        conn.commit()
        conn.close()
        return message
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.RaiseException):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка удаления клиента, "
                                                             "возможно имеется незакрытый чек "
                                                             "или клиент не существует ")
        return False


def topCheque():
    rating = []
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='9810', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('topcheque', [])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        for data in data:
            rating.append(data)
        cursor.close()
        conn.commit()
        conn.close()
        return rating
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getListIdClient(timeanddate):
    ListId = []
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='9810', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('idfromclient', [timeanddate])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        for data in data:
            ListId.append(data)
        cursor.close()
        conn.commit()
        conn.close()
        return ListId
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getInstrumentFromWarehouse():
    userRole = getRole(loginUser)
    listInstrument = []
    if userRole == 'sellerpiano':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getpianofromwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            for data in data:
                listInstrument.append(data)
            cursor.close()
            conn.commit()
            conn.close()
            return listInstrument
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False

    elif userRole == 'sellerflute':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user='seller_flute',
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getflutefromwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            for data in data:
                listInstrument.append(data)
            cursor.close()
            conn.commit()
            conn.close()
            return listInstrument
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False

    elif userRole == 'sellerguitar':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getguitarfromwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            for data in data:
                listInstrument.append(data)
            cursor.close()
            conn.commit()
            conn.close()
            return listInstrument
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False

    elif userRole == 'andrey':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getpianofromwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            for data in data:
                listInstrument.append(data)
            cursor.close()
            conn.commit()
            conn.close()
            return listInstrument
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False

    else:
        tkinter.messagebox.showinfo(title="Внимание", message="Действия для вашего отдела еще не назначены")
        return False


def getDescriptionPiano(id):
    userRole = getRole(loginUser)
    if userRole == 'sellerpiano':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getdescriptionpiano', [id])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
            return data
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False

    elif userRole == 'sellerflute':
        userRole = 'seller_flute'
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getdescriptionflute', [id])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
            return data
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False

    elif userRole == 'andrey':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getdescriptionpiano', [id])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
            return data
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False

    elif userRole == 'sellerguitar':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('getdescriptionguitar', [id])  # пример вызова функции из БД , имя и параметр на вход
            data = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
            return data
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
            tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False

    else:
        tkinter.messagebox.showinfo(title="Внимание", message="Дефствия для вашего отдела еще не назначены")
        return False


def addDescription(idd, text):
    userRole = getRole(loginUser)
    if userRole == 'sellerflute':
        userRole = 'seller_flute'
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('descriptionaddflute',
                            [idd, text])  # пример вызова функции из БД , имя и параметр на вход
            cursor.close()
            conn.commit()
            conn.close()
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
            tkinter.messagebox.showerror(title="Ошибка",
                                         message="Ошибка подключения к БД, возможно описание с таким ключом уже есть")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False
        tkinter.messagebox.showinfo(title="Успех", message="Описание успешно добавлено в базу")
        return True

    elif userRole == 'sellerguitar':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('descriptionaddguitar',
                            [idd, text])  # пример вызова функции из БД , имя и параметр на вход
            cursor.close()
            conn.commit()
            conn.close()
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
            tkinter.messagebox.showerror(title="Ошибка",
                                         message="Ошибка подключения к БД, возможно описание с таким ключом уже есть")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False
        tkinter.messagebox.showinfo(title="Успех", message="Описание успешно добавлено в базу")
        return True

    elif userRole == 'sellerpiano':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('descriptionaddpiano',
                            [idd, text])  # пример вызова функции из БД , имя и параметр на вход
            cursor.close()
            conn.commit()
            conn.close()
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
            tkinter.messagebox.showerror(title="Ошибка",
                                         message="Ошибка подключения к БД, возможно описание с таким ключом уже есть")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False
        tkinter.messagebox.showinfo(title="Успех", message="Описание успешно добавлено в базу")
        return True

    else:
        tkinter.messagebox.showinfo(title="Внимание", message="Действия для вашего отдела еще не назначены")
        return False


def updateDescription(text, id):
    userRole = getRole(loginUser)
    if userRole == 'sellerflute':
        userRole = 'seller_flute'
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('updatedescriptionflute',
                            [text, id])  # пример вызова функции из БД , имя и параметр на вход
            cursor.close()
            conn.commit()
            conn.close()
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
            tkinter.messagebox.showerror(title="Ошибка",
                                         message="Ошибка подключения к БД")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False
        tkinter.messagebox.showinfo(title="Успех", message="Описание успешно обновлено")
        return True

    elif userRole == 'sellerguitar':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('updatedescriptionguitar',
                            [text, id])  # пример вызова функции из БД , имя и параметр на вход
            cursor.close()
            conn.commit()
            conn.close()
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
            tkinter.messagebox.showerror(title="Ошибка",
                                         message="Ошибка подключения к БД")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False
        tkinter.messagebox.showinfo(title="Успех", message="Описание успешно обновлено")
        return True
    elif userRole == 'sellerpiano':
        try:
            conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                    password='98106547', host=connectionParams.host, port=connectionParams.port)
            cursor = conn.cursor()
            cursor.callproc('updatedescriptionpiano',
                            [text, id])  # пример вызова функции из БД , имя и параметр на вход
            cursor.close()
            conn.commit()
            conn.close()
        except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
            tkinter.messagebox.showerror(title="Ошибка",
                                         message="Ошибка подключения к БД")
            return False
        except psycopg2.errors.RaiseException:
            tkinter.messagebox.showerror(title="Ошибка", message="Неправомерный доступ")
            return False
        tkinter.messagebox.showinfo(title="Успех", message="Описание успешно обновлено")
        return True
    else:
        tkinter.messagebox.showinfo(title="Внимание", message="Действия для вашего отдела еще не назначены")
        return False


def getInstrumentParams(id):
    userRole = getRole(loginUser)
    if userRole == 'sellerflute':
        userRole = 'seller_flute'

    conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                            password='98106547', host=connectionParams.host, port=connectionParams.port)
    cursor = conn.cursor()
    cursor.callproc('getparaminstrument', [id])  # пример вызова функции из БД , имя и параметр на вход
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data


def getInfoAboutYou(login):
    try:
        userInfo = []
        conn = psycopg2.connect(dbname=connectionParams.dbName, user='andrey',
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getinfoaboutyou', [login])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        for data in data:
            name = data[0]
            family = data[1]
            login = data[2]
            role = data[3]
            userInfo.append(name)
            userInfo.append(family)
            userInfo.append(login)
            userInfo.append(role)
        cursor.close()
        conn.commit()
        conn.close()
        return userInfo
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getSupplyinfo():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getsupplyinfo', [])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return data
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def addSupply(idsupply, date):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('addsupply',
                        [idsupply, date])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def addInformSupply(supplycode, instrumentid, idtype):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('addinformsupply',
                        [supplycode, instrumentid, idtype])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyNumberOfSupply():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getemptynumberofsupply', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyNumberOfInstrument():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getemptynumberofinstrument', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getSupplyFromId(id):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getsupplyfromid', [id])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return data
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyCellOnPianoWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('emptycellonpianowarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getUnregisteredPianoOnWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('unregisteredpianoinwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def registerInstrumentInWarehouse(idtype, instrumentid, storagecell, idarticul):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('registerinstrument', [idtype, instrumentid, storagecell,
                                               idarticul])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getUnregisteredFluteOnWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('unregisteredfluteinwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyCellOnFluteWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('emptycellonflutewarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getUnregisteredGuitarOnWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('unregisteredguitarinwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyCellOnGuitarWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('emptycellonguitarwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getUnregisteredMicrophoneOnWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('unregisteredmicrophoneinwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyCellOnMicrophoneWarehouse():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('emptycellonmicrophonewarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getTypeInstrument():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('gettypeinstrument', [])  # пример вызова функции из БД , имя и параметр на вход
        types = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return types
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getArticulInstrument():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getarticulinstrument', [])  # пример вызова функции из БД , имя и параметр на вход
        articul = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return articul
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getParamInstrument():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getparamsinstrument', [])  # пример вызова функции из БД , имя и параметр на вход
        params = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return params
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def addArticul(idarticul, idtype, namearticul):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('addarticul',
                        [idarticul, idtype, namearticul])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getEmptyIdArticulInsturment():
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getemptyarticulinstrument', [])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getAllArticulsName():  # системная
    articulsName = []
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user="andrey",
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getallarticuls', [])  # пример вызова функции из БД , имя и параметр на вход
        allarticuls = cursor.fetchall()
        for articul in allarticuls:
            articulsName.append(str(articul).replace("                ", "").replace("'", "").replace(",", "").
                                replace("           ", "").replace(")", "").replace("(", ""))
        cursor.close()
        conn.commit()
        conn.close()
        return articulsName
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def findArticulFromName(nameArticul):  # системная
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user="andrey",
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('findarticulfromname', [nameArticul])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getAllTypes():  # системная
    typesName = []
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user="andrey",
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getlalltypes', [])  # пример вызова функции из БД , имя и параметр на вход
        alltypes = cursor.fetchall()
        for type in alltypes:
            typesName.append(str(type).replace("                ", "").replace("'", "").replace(",", "").
                             replace("           ", "").replace(")", "").replace("(", ""))
        cursor.close()
        conn.commit()
        conn.close()
        return typesName
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def findTypeFromName(typeName):
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user="andrey",
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('findidtypefromname', [typeName])  # пример вызова функции из БД , имя и параметр на вход
        number = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return number
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getAllRoles():
    allRoles = []
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user="andrey",
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getallroles', [])  # пример вызова функции из БД , имя и параметр на вход
        roles = cursor.fetchall()
        for role in roles:
            allRoles.append(role)
        cursor.close()
        conn.commit()
        conn.close()
        return allRoles
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def sellerAdd(name, family, telephone, email, login, password, role):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('selleradd',
                        [name, family, telephone, email, login, password,
                         role])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except psycopg2.OperationalError:
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    except psycopg2.errors.InsufficientPrivilege:
        tkinter.messagebox.showerror(title="Внимание", message="Ошибка доступа")
        return False
    except psycopg2.errors.InvalidTextRepresentation:
        tkinter.messagebox.showerror(title="Внимание", message="Ошибка доступа")
        return False
    tkinter.messagebox.showinfo(title="Успех", message=" Продавец успешно добавлен в базу")
    return True


def selectSellerByEmail(email):
    userRole = getRole(loginUser)
    sellerList = []
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('getsellerbyemail',
                        [email])  # пример вызова функции из БД , имя и параметр на вход
        seller = cursor.fetchall()
        for param in seller:
            name = param[0]
            family = param[1]
            telephone = param[2]
            email = param[3]
            login = param[4]
            password = param[5]
            role = param[6]
            sellerList.append(name)
            sellerList.append(family)
            sellerList.append(telephone)
            sellerList.append(email)
            sellerList.append(login)
            sellerList.append(password)
            sellerList.append(role)
        cursor.close()
        conn.commit()
        conn.close()
        return sellerList
    except psycopg2.OperationalError:
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False
    except psycopg2.errors.InsufficientPrivilege:
        tkinter.messagebox.showerror(title="Внимание", message="Ошибка доступа")
        return False
    except psycopg2.errors.InvalidTextRepresentation:
        tkinter.messagebox.showerror(title="Внимание", message="Ошибка доступа")
        return False


def updateSeller(name, family, telephonenumber, email, login, password, role):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname=connectionParams.dbName, user=userRole,
                                password='98106547', host=connectionParams.host, port=connectionParams.port)
        cursor = conn.cursor()
        cursor.callproc('updateseller',
                        [name, family, telephonenumber, email, login, password,
                         role])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showerror(title="Ошибка",
                                     message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message="Изменение сохранены")
    return True
