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
    inform = []
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='9810', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='9810', host='192.168.56.101', port='5432')
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


def getListIdClient():
    ListId = []
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='9810', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('idfromclient', [])  # пример вызова функции из БД , имя и параметр на вход
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


def getPianinoFromWarehouse():
    listPianino = []
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('getpianofromwarehouse', [])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        for data in data:
            listPianino.append(data)
        cursor.close()
        conn.commit()
        conn.close()
        return listPianino
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getDescriptionPiano(id):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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


def addDescription(idd, text):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,

                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('descriptionadd',
                        [idd, text])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showerror(title="Ошибка",
                                     message="Ошибка подключения к БД, возможно описание с таким ключом уже есть")
        return False
    tkinter.messagebox.showinfo(title="Успех", message="Описание успешно добавлено в базу")
    return True


def updateDescription(text, id):
    userRole = getRole(loginUser)
    try:
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,

                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('updatedescription',
                        [text, id])  # пример вызова функции из БД , имя и параметр на вход
        cursor.close()
        conn.commit()
        conn.close()
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showerror(title="Ошибка",
                                     message="Ошибка подключения к БД")
        return False
    tkinter.messagebox.showinfo(title="Успех", message="Описание успешно обновлено")
    return True


def getPianoParams(id):
    try:
        userRole = getRole(loginUser)
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
        cursor = conn.cursor()
        cursor.callproc('getparampiano', [id])  # пример вызова функции из БД , имя и параметр на вход
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return data
    except (psycopg2.OperationalError, psycopg2.errors.InvalidTextRepresentation):
        tkinter.messagebox.showerror(title="Ошибка", message="Ошибка подключения к БД")
        return False


def getInfoAboutYou(login):
    try:
        userInfo = []
        conn = psycopg2.connect(dbname='InstrumentalMusic', user='andrey',
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
        conn = psycopg2.connect(dbname='InstrumentalMusic', user=userRole,
                                password='98106547', host='192.168.56.101', port='5432')
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
