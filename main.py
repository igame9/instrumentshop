import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import DBManage
import psycopg2


def auth(login, password, window, extrawindow):
    if DBManage.checkUser(login, password) == 1 and DBManage.getRole(login) != "None":
        tkinter.messagebox.showinfo(title="Успех", message="Вы успешно активировались")
        DBManage.loginUser = login  # передача логина в DBManage
        window.deiconify()
        extrawindow.destroy()
        return True
    else:
        tkinter.messagebox.showerror(title="Ошибка", message="Неверные логин или пароль или ошибка роли")
        return False


def login(window):
    extraWindow = Toplevel(window, bg="gray22")  # создание доп окна
    extraWindow.title("Авторизация")
    extraWindow.geometry('250x70+40+80')
    extraWindow.resizable(False, False)
    inputLogin = Entry(extraWindow, width=20)
    inputPassword = Entry(extraWindow, width=20)
    buttonLogin = Button(extraWindow, text='Войти', width=18, height=1, fg='black',
                         command=lambda: auth(inputLogin.get(), inputPassword.get(), window, extraWindow))
    extraWindow.protocol("WM_DELETE_WINDOW", window.destroy)  # Закрываю основное окно,
    # по закрытии регистрации, чтобы основное не висело
    inputLogin.pack()
    inputPassword.pack()
    buttonLogin.pack()


def geometryWindow(window):
    window.withdraw()
    login(window)
    window.resizable(True, True)
    window.title("Магазин музыкальных инструментов")
    window["bg"] = "gray22"
    window.geometry('1000x700+40+80')
    if DBManage.testConn() != True:
        tkinter.messagebox.showwarning(title="Внимание", message="Отсутствует соединение с БД")
        tkinter.messagebox.showwarning(title="Внимание", message="Приложение будет закрыто")
        sys.exit("Приложение не смогло установить соединение с сервером БД")


def notebook(window):
    notebk = ttk.Notebook(window)
    style = ttk.Style()
    style.configure("0.TFrame", background="gray22")
    style.configure("1.TFrame", background="gray22")
    style.configure("2.TFrame", background="gray22")
    style.configure("3.TFrame", background="gray22")
    style.configure("4.TFrame", background="gray22")
    style.configure("5.TFrame", background="gray22")
    style.configure("6.TFrame", background="gray22")
    style.configure("7.TFrame", background="gray22")
    notebk.pack(fill='both', expand='yes')
    frame0 = ttk.Frame(window, style="0.TFrame")
    frame1 = ttk.Frame(window, style="1.TFrame")
    frame2 = ttk.Frame(window, style="2.TFrame")
    frame3 = ttk.Frame(window, style="3.TFrame")
    frame4 = ttk.Frame(window, style="4.TFrame")
    frame5 = ttk.Frame(window, style="5.TFrame")
    frame6 = ttk.Frame(window, style="6.TFrame")
    frame7 = ttk.Frame(window, style="7.TFrame")
    frame0.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()
    frame5.pack()
    frame6.pack()
    frame7.pack()
    notebk.add(frame0, text="О тебе")
    notebk.add(frame1, text='Клиенты')
    notebk.add(frame2, text='Сотрудники')
    notebk.add(frame3, text="Отдел пианино")
    notebk.add(frame4, text="Отдел флейт")
    notebk.add(frame5, text="Отдел поставки")
    notebk.add(frame6, text="Склад")
    notebk.add(frame7, text="Справочник")
    widgets(frame0, frame1, frame2, frame3, frame4, frame5, frame6, frame7)  # тут осторожнее


def takeid(id, out1, out2, out3, out4):
    name = DBManage.selectClientName(id)
    if name == 0:
        name = ""
    if name == "" or name == []:
        out1.configure(text="Данные не найдены")
        out2.configure(text="")
        out3.configure(text="")
        out4.configure(text="")
        return False
    out1.configure(text=name[0])
    out2.configure(text=name[1])
    out3.configure(text=name[2])
    out4.configure(text=name[3])


def addClient(name, family, telephone, email, outchange1, outchange2, outchange3, outchange4):
    if name == '' or family == '' or telephone == '' or email == '':
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя добавить пустого сотрудника")
        return False
    DBManage.clientAdd(name, family, telephone, email)
    outchange1.delete(0, END)
    outchange2.delete(0, END)
    outchange3.delete(0, END)
    outchange4.delete(0, END)
    return True


def deleteClient(id, out):
    if id == '':
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя удалить пустого клиента")
        return False
    import psycopg2
    try:
        if DBManage.deleteClient(id) == 'Успешное удаление':
            out.delete(0, END)
            tkinter.messagebox.showinfo(title="Успех", message="Клиент успешно удален")
        else:
            tkinter.messagebox.showwarning(title="Ошибка", message="Ошибка доступа")
    except psycopg2.errors.ForeignKeyViolation:
        tkinter.messagebox.showwarning(title="Внимание", message="Не стоит удалять клиента из базы, "
                                                                 "если в базе сохранились записи о его покупках")


def saveRatingInFile(text):
    Rating = text.get(1.0, END)
    fileWriter = open('rating.txt', 'w', encoding='utf-8')
    fileWriter.write(Rating)
    fileWriter.close()


def ratingcheque(text):
    text.configure(state=NORMAL)
    text.delete(1.0, END)
    try:
        rating = DBManage.topCheque()
        for rate in rating:
            text.insert(END, str(rate).replace('\\xa0', '').replace("(", "").replace(")", "").replace("'", "") + '\n')
        text.configure(state=DISABLED)
    except TypeError:
        tkinter.messagebox.showerror(title="Ошибка доступа", message="Невозможно выполнить действие")


def getIdClient(text):
    text.configure(state=NORMAL)
    text.delete(1.0, END)
    try:
        listId = DBManage.getListIdClient()
        for id in listId:
            text.insert(END, str(id).replace(")", "").replace("(", "").replace(",", "") + '\n')
        text.configure(state=DISABLED)
    except TypeError:
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getPianino(text):
    text.configure(state=NORMAL)
    text.delete(1.0, END)
    try:
        listPianino = DBManage.getPianinoFromWarehouse()
        for pianino in listPianino:
            text.insert(END, str(pianino).replace(")", "").replace("(", "").replace(",", "").
                        replace("                ", " ").replace("              ", "") + '\n')
        text.configure(state=DISABLED)
    except TypeError:
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getDescriptionPiano(id, text):
    """
    :param id:
    :param text:
    :return False or insert in text4:
    """
    text.configure(state=NORMAL)
    text.delete(1.0, END)
    try:
        description = DBManage.getDescriptionPiano(id)
        params = DBManage.getPianoParams(id)
        if description == False:
            tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")
            return False
        if description == []:
            text.insert(END, "Описания не найдено".replace("\n", "") + '\n')
        else:
            text.insert(END,
                        str(description).replace(")", "").replace("(", "").
                        replace("]", "").replace("[", "").replace(",", "").replace("'", "").replace("\\n", "") +
                        '\n' + "**********************" + "\n" + "Параметры инструмента:" + "\n" +
                        str(params).replace("[", "").replace("]", "").replace(")", "").replace("(", "").replace(",",
                                                                                                                ""))
            text.configure(state=NORMAL)
    except TypeError:
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def addDescription(id, text):
    DBManage.addDescription(id, text)


def updateDescription(text, id):
    DBManage.updateDescription(text, id)


def aboutYou(text):
    actionAndrey = "Тебе доступны все возможности из всех вкладок!"
    actionClientDep = "Тебе доступны все возможности из вкладки <Клиенты>"
    actionSellerPiano = "Тебе доступны все возможности из вкладки <Отдел пианино>"
    actionGuest = "Тебе ничего не доступно, у тебя гостевая роль"
    actionSellerFlute = "Тебе доступны все возможности из вкладки <Отдел флейт>"
    actionsupplydep = "Тебе доступны все возможности из вкладки <Отдел поставки>"
    actionWarehouseDep = "Тебе доступны все возможности из вкладки <Склад>"
    infoUser = DBManage.getInfoAboutYou(DBManage.loginUser)
    if infoUser[3] == "andrey":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionAndrey)
    elif infoUser[3] == "clientdep":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionClientDep)
    elif infoUser[3] == "sellerpiano":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionSellerPiano)
    elif infoUser[3] == "guest":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionGuest)
    elif infoUser[3] == "sellerflute":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionSellerFlute)
    elif infoUser[3] == "supplydep":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionsupplydep)
    elif infoUser[3] == "warehousedep":
        text.insert(END, "Приветствую!" + "\n" + "Имя: " + str(infoUser[0]) + "\n" +
                    "Фамилия: " + str(infoUser[1]) + "\n" + "Login: " + str(infoUser[2]) + "\n" +
                    "Роль аккаунта: " + infoUser[3] + "\n" + "Твои возможности: " + actionWarehouseDep)
    else:
        text.insert(END, "Внимание информация для твоей роли не назначена!")
    text.configure(state=DISABLED)


def getSupplyInfo(text):
    try:
        text.configure(state=NORMAL)
        text.delete(1.0, END)
        supplyInfo = DBManage.getSupplyinfo()
        for info in supplyInfo:
            text.insert(END,
                        "id поставки,дата,id инструмента" + "\n" + "************" + "\n" + str(info[0]) + "\n" + str(
                            info[1]) +
                        "\n" + str(info[2]) + "\n" + "************")
        text.configure(state=DISABLED)
    except psycopg2.errors.InsufficientPrivilege:
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def addSupply(in1, in2, in1name, in2name):
    if in1 == "" or in2 == "":
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя добавить пустую поставку")
        return False
    try:
        if DBManage.addSupply(in1, in2):
            tkinter.messagebox.showinfo(title="Успех", message="Поставка успешно добавлена")
            in1name.delete(0, END)
            in2name.delete(0, END)
    except (psycopg2.errors.InvalidDatetimeFormat, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Возможна ошибка доступа или ошибка формата ввода."
                                                                 "Проверьте есть ли у вас доступ к данной странице или"
                                                                 "правильность ввода даты GG-MM-DD")


def addInformSupply(in1, in2, in3, in1name, in2name, in3name):
    if in1 == "" or in2 == "":
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя добавить пустые данные")
        return False
    try:
        if DBManage.addInformSupply(in1, in2, in3):
            tkinter.messagebox.showinfo(title="Успех", message="Информация о поставке успешно обновлена")
            in1name.delete(0, END)
            in2name.delete(0, END)
            in3name.delete(0, END)
    except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showwarning(title="Внимание",
                                       message="Указан неверный номер поставки или инструмента, проверьте, "
                                               "что указан существующий код поставки "
                                               "или, что номер инструмента уникальный, "
                                               "а так же, что такой тип id существует")


def numberOfSupply(in1):
    try:
        in1.configure(state=NORMAL)
        in1.delete(0, END)
        number = DBManage.getEmptyNumberOfSupply()
        in1.insert(END, number)
        in1.configure(state=DISABLED)
    except psycopg2.errors.InsufficientPrivilege:
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def numberOfInstrument(in1):
    try:
        in1.configure(state=NORMAL)
        in1.delete(0, END)
        number = DBManage.getEmptyNumberOfInstrument()
        in1.insert(END, number)
    except psycopg2.errors.InsufficientPrivilege:
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getSupplyFromId(in1, out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        supplyInfo = DBManage.getSupplyFromId(in1)
        for info in supplyInfo:
            out1.insert(END, "ID поставки, дата, ID инструмента" + "\n" + str(info[0]) + "\n" + str(info[1])
                        + "\n" + str(info[2]) + "\n")
    except (TypeError, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def saveAllSupply(text):
    Rating = text.get(1.0, END)
    fileWriter = open('allSupply.txt', 'w', encoding='utf-8')
    fileWriter.write(Rating)
    fileWriter.close()
    tkinter.messagebox.showinfo(title="Успех", message="Файл сохранен.")


def saveSuppliFromId(text):
    Rating = text.get(1.0, END)
    if Rating == "":
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя сохранить пустые данные")
        return False
    fileWriter = open('idSupply.txt', 'w', encoding='utf-8')
    fileWriter.write(Rating)
    fileWriter.close()
    tkinter.messagebox.showinfo(title="Успех", message="Файл сохранен.")


def getUnregisteredPianoInWarehouse(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        unregisteredPiano = DBManage.getUnregisteredPianoOnWarehouse()
        for pianoid in unregisteredPiano:
            out1.insert(END, str(pianoid[0]) + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getUnregisteredFluteInWarehouse(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        unregisteredPiano = DBManage.getUnregisteredFluteOnWarehouse()
        for fluteid in unregisteredPiano:
            out1.insert(END, str(fluteid[0]) + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getUnregisteredGuitarInWarehouse(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        unregisteredPiano = DBManage.getUnregisteredGuitarOnWarehouse()
        for guitarid in unregisteredPiano:
            out1.insert(END, str(guitarid[0]) + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getUnregisteredMicrophoneInWarehouse(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        unregisteredPiano = DBManage.getUnregisteredMicrophoneOnWarehouse()
        for microphoneid in unregisteredPiano:
            out1.insert(END, str(microphoneid[0]) + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def registerInstrumentOnWarehouse(in1, in2, in3, in4, out1, out2, out3, out4):  # + проверка
    # на занятость ячейки инструментов
    try:
        listIntPiano = []
        listIntFlute = []
        listIntGuitar = []
        listIntMicrophone = []
        emptycellInPiano = DBManage.getEmptyCellOnPianoWarehouse()
        if not emptycellInPiano:
            return False
        emptycellFlute = DBManage.getEmptyCellOnFluteWarehouse()
        emptycellGuitar = DBManage.getEmptyCellOnGuitarWarehouse()
        emptycellMicrophone = DBManage.getEmptyCellOnMicrophoneWarehouse()
        for cell in emptycellInPiano:
            listIntPiano.append(int(cell[0]))
        for cell in emptycellFlute:
            listIntFlute.append(int(cell[0]))
        for cell in emptycellGuitar:
            listIntGuitar.append(int(cell[0]))
        for cell in emptycellMicrophone:
            listIntMicrophone.append(int(cell[0]))

        if int(in1) == 1 and listIntGuitar[0] > int(in3):
            tkinter.messagebox.showwarning(title="Внимание", message="Такая ячейка на складе уже занята")
            return False
        elif int(in1) == 2 and listIntPiano[0] > int(in3):
            tkinter.messagebox.showwarning(title="Внимание", message="Такая ячейка на складе уже занята")
            return False
        elif int(in1) == 3 and listIntFlute[0] > int(in3):
            tkinter.messagebox.showwarning(title="Внимание", message="Такая ячейка на складе уже занята")
            return False
        elif int(in1) == 4 and listIntMicrophone[0] > int(in3):
            tkinter.messagebox.showwarning(title="Внимание", message="Такая ячейка на складе уже занята")
            return False

        out1.delete(0, END)
        out2.delete(0, END)
        out3.delete(0, END)
        out4.delete(0, END)
        if DBManage.registerInstrumentInWarehouse(in1, in2, in3, in4):
            tkinter.messagebox.showinfo(title="Успех", message="Инструмент зарегистрирован")
    except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.InsufficientPrivilege, TypeError, ValueError,):
        tkinter.messagebox.showwarning(title="Внимание", message="Проверьте правильность данных или ошибка доступа")


def setEmptyCellInPianoWareHouse(in1):
    try:
        in1.delete(0, END)
        Emptycell = DBManage.getEmptyCellOnPianoWarehouse()
        in1.insert(END, Emptycell)
    except (TypeError, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def setEmptyCellInFluteWareHouse(in1):
    try:
        in1.delete(0, END)
        Emptycell = DBManage.getEmptyCellOnFluteWarehouse()
        in1.insert(END, Emptycell)
    except (TypeError, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def setEmptyCellInGuitarWareHouse(in1):
    try:
        in1.delete(0, END)
        Emptycell = DBManage.getEmptyCellOnGuitarWarehouse()
        in1.insert(END, Emptycell)
    except (TypeError, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def setEmptyCellInMicrophoneWareHouse(in1):
    try:
        in1.delete(0, END)
        Emptycell = DBManage.getEmptyCellOnMicrophoneWarehouse()
        in1.insert(END, Emptycell)
    except (TypeError, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getDictwithInstrument(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        dictWitchInstrument = DBManage.getTypeInstrument()
        out1.insert(END, "ID type и наименование инструмента" + "\n")
        for instrument in dictWitchInstrument:
            out1.insert(END, str(instrument).replace(")", "").replace("(", "").replace("'", "") + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getDictwithArticulInstrument(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        dictWitchArticul = DBManage.getArticulInstrument()
        out1.insert(END, "ID type и наименование артикула" + "\n")
        for instrument in dictWitchArticul:
            out1.insert(END, str(instrument)
                        .replace("                  ", "")
                        .replace("              ", "")
                        .replace(")", "")
                        .replace("(", "")
                        .replace("           ", "")
                        .replace("            ", "")
                        .replace("'", "")
                        + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def getParamsInstrument(out1):
    try:
        out1.configure(state=NORMAL)
        out1.delete(1.0, END)
        dictWithParams = DBManage.getParamInstrument()
        out1.insert(END, "ID param и наименование параметра" + "\n")
        for instrument in dictWithParams:
            out1.insert(END, str(instrument).replace(")", "").replace("(", "").replace("'", "") + "\n")
        out1.configure(state=DISABLED)
    except (psycopg2.errors.InsufficientPrivilege, TypeError):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def addarticul(in1, in2, in3, in1name, in2name, in3name):
    if in1 == "" or in2 == "" or in3 == "":
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя создать пустой артикул")
        return False
    try:
        if DBManage.addArticul(in1, in2, in3):
            tkinter.messagebox.showinfo(title="Успех", message="Артикул успешно добавлен")
            in1name.delete(0, END)
            in2name.delete(0, END)
            in3name.delete(0, END)
    except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showwarning(title="Внимание",
                                       message="Проверьте корректность данных "
                                               "или же ошибка доступа")

def getEmptyArticulId(in1):
    try:
        in1.delete(0, END)
        freeId = DBManage.getEmptyIdArticulInsturment()
        in1.insert(END, freeId)
    except (TypeError, psycopg2.errors.InsufficientPrivilege):
        tkinter.messagebox.showwarning(title="Внимание", message="Ошибка доступа")


def widgets(frame0, frame1, frame2, frame3, frame4, frame5, frame6, frame7):
    # ..................................................................................Frame0
    text6 = Text(frame0, width=60, height=10)
    text6.tag_configure('bold', font='CenturyGothic 16 bold')
    buttoInfo = Button(frame0, text="Информация", width=10, height=1, command=lambda: aboutYou(text6))
    # ..................................................................................Frame0 end
    # ..................................................................................Frame1
    button1 = Button(frame1, text='Получить клиента по id', width=18, height=1, fg='black',
                     command=lambda: takeid(entry1.get(), label1, label7, label8, label9))
    label1 = Label(frame1, width=30, height=1)
    entry1 = Entry(frame1, width=5)
    label2 = Label(frame1, width=30, height=1, text="Введите id клиента для поиска")
    sep1 = ttk.Separator(frame1, orient="vertical")
    sep2 = ttk.Separator(frame1, orient="vertical")
    entry2 = Entry(frame1, width=60)
    entry3 = Entry(frame1, width=60)
    entry4 = Entry(frame1, width=60)
    entry5 = Entry(frame1, width=60)
    entry6 = Entry(frame1, width=5)
    # .....
    button2 = Button(frame1, text='Добавить нового клиента', width=23, height=1,
                     command=lambda: addClient(entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry2, entry3,
                                               entry4, entry5))
    button3 = Button(frame1, text='Удалить клиента', width=18, height=1,
                     command=lambda: deleteClient(entry6.get(), entry6))
    button4 = Button(frame1, text="Рейтинг чеков клиентов", width=18, height=1, command=lambda: ratingcheque(text))
    button6 = Button(frame1, text="Сохранить данные в файл", width=23, height=1, command=lambda: saveRatingInFile(text))
    button7 = Button(frame1, text="Получить всех клиентов", width=23, height=1, command=lambda: getIdClient(text2))
    label3 = Label(frame1, width=5, height=1, text="Имя", bg="gray22")
    label4 = Label(frame1, width=7, height=1, text="Фамилия", bg="gray22")
    label5 = Label(frame1, width=7, height=1, text="Телефон", bg="gray22")
    label6 = Label(frame1, width=7, height=1, text="E-Mail", bg="gray22")
    label7 = Label(frame1, width=30, height=1)
    label8 = Label(frame1, width=30, height=1)
    label9 = Label(frame1, width=30, height=1)
    label10 = Label(frame1, width=35, height=1, text="Введите id клиента для его удаления из базы", bg="gray22")
    text = Text(frame1, width=40, height=10)
    text.tag_configure('bold', font='Helvetica 12 bold')
    text2 = Text(frame1, width=40, height=10)
    text2.tag_configure('bold', font='Helvetica 12 bold')
    # .......................................................................................Frame1 end
    # ........................................................................................Frame3
    text3 = Text(frame3, width=60, height=10)
    text3.configure(state=DISABLED)
    text3.tag_configure('bold', font='Helvetica 12 bold')
    button9 = Button(frame3, text="Получить все пианино со склада", width=25, height=1,
                     command=lambda: getPianino(text3))
    text4 = Text(frame3, width=60, height=10)
    text4.configure(state=DISABLED)
    text4.tag_configure('bold', font='Helvetica 12 bold')
    entry7 = Entry(frame3, width=5)
    button10 = Button(frame3, text="Получить описание пианино", width=25, height=1,
                      command=lambda: getDescriptionPiano(entry7.get(), text4))
    button11 = Button(frame3, text="Добавить описание пианино", width=25, height=1,
                      command=lambda: addDescription(entry7.get(), text4.get(1.0, END)))
    button12 = Button(frame3, text="Обновить описание", width=25, height=1,
                      command=lambda: updateDescription(text4.get(1.0, END), entry7.get()))
    # .........................................................................................Frame3 end
    # .........................................................................................Frame5
    text5 = Text(frame5, width=35, height=10)
    text5.tag_configure('bold', font='Helvetica 12 bold')
    text5.configure(state=DISABLED)
    button13 = Button(frame5, text="Получить информацию о поставках", width=29, height=1,
                      command=lambda: getSupplyInfo(text5))
    button14 = Button(frame5, text="Зарегистрировать новую поставку в системе", width=35, height=1,
                      command=lambda: addSupply(entry8.get(), entry9.get(), entry8, entry9))
    button16 = Button(frame5, text="Допустимый номер поставки", width=25, height=1,
                      command=lambda: numberOfSupply(entry8))
    entry8 = Entry(frame5, width=60)
    entry8.configure(state=DISABLED)
    entry9 = Entry(frame5, width=60)
    label11 = Label(frame5, width=14, height=1, text="ID поставки", bg="gray22")
    label12 = Label(frame5, width=14, height=1, text="Дата поставки", bg="gray22")
    entry10 = Entry(frame5, width=60)
    button17 = Button(frame5, width=26, height=1, text="Допустимый номер инструмента",
                      command=lambda: numberOfInstrument(entry11))
    entry11 = Entry(frame5, width=60)
    entry11.configure(state=NORMAL)
    label13 = Label(frame5, width=15, height=1, text="ID поставки", bg="gray22")
    label14 = Label(frame5, width=15, height=1, text="ID инструмента", bg="gray22")
    button15 = Button(frame5, text="Добавить информацию о поставке", width=35, height=1, command=lambda:
    addInformSupply(entry10.get(), entry11.get(), entry13.get(), entry10, entry11, entry13))
    text7 = Text(frame5, width=35, height=10)
    text7.tag_configure('bold', font='Helvetica 12 bold')
    text7.configure(state=DISABLED)
    entry12 = Entry(frame5, width=5)
    button18 = Button(frame5, text="Получить информация о поставке по ID", width=31, height=1,
                      command=lambda: getSupplyFromId(entry12.get(), text7))
    button19 = Button(frame5, text="Сохранить информацию", width=20, height=1, command=lambda: saveAllSupply(text5))
    button20 = Button(frame5, text="Сохранить информацию", width=20, height=1, command=lambda: saveSuppliFromId(text7))
    entry13 = Entry(frame5, width=60)
    label15 = Label(frame5, width=15, height=1, text="Тип инструмента", bg="gray22")

    # .........................................................................................Frame5 end

    # .........................................................................................Frame6
    text8 = Text(frame6, width=35, height=10)
    text8.tag_configure('bold', font='Helvetica 12 bold')
    text8.configure(state=DISABLED)
    button21 = Button(frame6, text="Незарегистрированные пианино на складе", width=36,
                      command=lambda: getUnregisteredPianoInWarehouse(text8))
    entry14 = Entry(frame6, width=60)
    entry15 = Entry(frame6, width=60)
    entry16 = Entry(frame6, width=60)
    entry17 = Entry(frame6, width=60)
    label16 = Label(frame6, width=15, height=1, text="Тип инструмента", bg="gray22")
    label17 = Label(frame6, width=15, height=1, text="ID инструмента", bg="gray22")
    label18 = Label(frame6, width=15, height=1, text="Ячейка на складе", bg="gray22")
    label19 = Label(frame6, width=15, height=1, text="Артикул", bg="gray22")
    button22 = Button(frame6, text="Зарегистрировать инструмент на складе", width=35,
                      command=lambda: registerInstrumentOnWarehouse(entry14.get(), entry15.get()
                                                                    , entry16.get(), entry17.get(), entry14, entry15,
                                                                    entry16, entry17))
    button23 = Button(frame6, text="Свободная ячейка на складе пианино", width=35,
                      command=lambda: setEmptyCellInPianoWareHouse(entry16))
    button24 = Button(frame6, text="Незарегистрированные флейты на складе", width=36,
                      command=lambda: getUnregisteredFluteInWarehouse(text8))
    button25 = Button(frame6, text="Свободная ячейка на складе флейт", width=35,
                      command=lambda: setEmptyCellInFluteWareHouse(entry16))
    button26 = Button(frame6, text="Незарегистрированные гитары на складе", width=36,
                      command=lambda: getUnregisteredGuitarInWarehouse(text8))
    button27 = Button(frame6, text="Свободная ячейка на складе гитар", width=35,
                      command=lambda: setEmptyCellInGuitarWareHouse(entry16))
    button28 = Button(frame6, text="Незарегистрированные микрофоны на складе", width=36,
                      command=lambda: getUnregisteredMicrophoneInWarehouse(text8))
    button29 = Button(frame6, text="Свободная ячейка на складе микрофонов", width=35,
                      command=lambda: setEmptyCellInMicrophoneWareHouse(entry16))
    # .........................................................................................Frame6 end
    # .........................................................................................Frame7
    text9 = Text(frame7, width=35, height=10)
    text9.tag_configure('bold', font='Helvetica 12 bold')
    text9.configure(state=DISABLED)
    button30 = Button(frame7, text="Получить ID инструментов", width=39, command=lambda: getDictwithInstrument(text9))
    button31 = Button(frame7, text="Получить ID артикулов", width=39,
                      command=lambda: getDictwithArticulInstrument(text9))
    button32 = Button(frame7, text="Получить ID параметров", width=39, command=lambda: getParamsInstrument(text9))
    entry18 = Entry(frame7, width=60)
    entry19 = Entry(frame7, width=60)
    entry20 = Entry(frame7, width=60)
    label20 = Label(frame7, width=15, height=1, text="ID артикула", bg="gray22")
    label21 = Label(frame7, width=15, height=1, text="ID типа инструмента", bg="gray22")
    label22 = Label(frame7, width=15, height=1, text="Наименование", bg="gray22")
    button33 = Button(frame7, width=39, text="Зарегистрировать новый артикул",
                      command=lambda: addarticul(entry18.get(), entry19.get(), entry20.get(),
                                                 entry18, entry19, entry20))
    button34 = Button(frame7, width=39, text="Свободный ID артикула", command= lambda: getEmptyArticulId(entry18))
    # .........................................................................................Frame7 end
    # Упаковка виджетов
    entry1.place(x=35, y=630)
    button1.place(x=100, y=630)
    label1.place(x=35, y=500)
    label7.place(x=35, y=530)
    label8.place(x=35, y=560)
    label9.place(x=35, y=590)
    label2.place(x=35, y=470)
    sep1.place(x=0, y=460, relwidth=1)
    sep2.place(x=0, y=200, relwidth=1)
    entry2.place(x=500, y=470)
    entry3.place(x=500, y=500)
    entry4.place(x=500, y=530)
    entry5.place(x=500, y=560)
    entry6.place(x=1000, y=500)
    button2.place(x=500, y=630)
    button3.place(x=1000, y=530)
    label3.place(x=450, y=470)
    label4.place(x=440, y=500)
    label5.place(x=440, y=530)
    label6.place(x=440, y=560)
    label10.place(x=1000, y=470)
    text.place(x=25, y=210)
    text2.place(x=500, y=210)
    text3.place(x=10, y=10)
    button4.place(x=25, y=380)
    button6.place(x=177, y=380)
    button7.place(x=500, y=380)
    button9.place(x=10, y=180)
    text4.place(x=10, y=300)
    entry7.place(x=10, y=470)
    button10.place(x=50, y=470)
    button11.place(x=50, y=505)
    button12.place(x=50, y=540)
    text5.place(x=50, y=50)
    text6.place(x=1, y=1)
    buttoInfo.place(x=1, y=170)
    button13.place(x=50, y=220)
    entry8.place(x=500, y=50)
    entry9.place(x=500, y=100)
    button14.place(x=500, y=220)
    label11.place(x=390, y=50)
    label12.place(x=390, y=100)
    entry10.place(x=980, y=50)
    entry11.place(x=980, y=100)
    label13.place(x=870, y=50)
    label14.place(x=870, y=100)
    button15.place(x=980, y=220)
    button16.place(x=500, y=260)
    button17.place(x=980, y=260)
    text7.place(x=50, y=350)
    entry12.place(x=50, y=520)
    button18.place(x=50, y=550)
    button19.place(x=50, y=250)
    button20.place(x=50, y=580)
    text8.place(x=50, y=50)
    entry13.place(x=980, y=150)
    label15.place(x=870, y=150)
    button21.place(x=50, y=230)
    entry14.place(x=500, y=50)
    entry15.place(x=500, y=100)
    entry16.place(x=500, y=150)
    entry17.place(x=500, y=200)
    label16.place(x=370, y=50)
    label17.place(x=370, y=100)
    label18.place(x=370, y=150)
    label19.place(x=370, y=200)
    button22.place(x=500, y=250)
    button23.place(x=500, y=300)
    button24.place(x=50, y=260)
    button25.place(x=500, y=330)
    button26.place(x=50, y=290)
    button27.place(x=500, y=360)
    button28.place(x=50, y=320)
    button29.place(x=500, y=390)
    text9.place(x=50, y=50)
    button30.place(x=50, y=230)
    button31.place(x=50, y=260)
    button32.place(x=50, y=290)
    entry18.place(x=500, y=50)
    entry19.place(x=500, y=100)
    entry20.place(x=500, y=150)
    label20.place(x=370, y=50)
    label21.place(x=370, y=100)
    label22.place(x=370, y=150)
    button33.place(x=500, y=200)
    button34.place(x=500,y=230)

def showWindow():
    window = Tk()
    geometryWindow(window)
    notebook(window)
    window.mainloop()


if __name__ == '__main__':
    showWindow()
