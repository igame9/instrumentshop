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
    style.configure("5.TFrame", background="gray22")
    notebk.pack(fill='both', expand='yes')
    frame0 = ttk.Frame(window, style="0.TFrame")
    frame1 = ttk.Frame(window, style="1.TFrame")
    frame2 = ttk.Frame(window, style="2.TFrame")
    frame3 = ttk.Frame(window, style="3.TFrame")
    frame4 = ttk.Frame(window)
    frame5 = ttk.Frame(window, style="5.TFrame")
    frame0.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()
    frame5.pack()
    notebk.add(frame0, text="О тебе")
    notebk.add(frame1, text='Клиенты')
    notebk.add(frame2, text='Сотрудники')
    notebk.add(frame3, text="Отдел пианино")
    notebk.add(frame4, text="Отдел флейт")
    notebk.add(frame5, text="Отдел поставки")
    widgets(frame0, frame1, frame3, frame5)  # тут осторожнее


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
    except psycopg2.errors.InvalidDatetimeFormat:
        tkinter.messagebox.showwarning(title="Внимание", message="Неверный формат времени")


def addInformSupply(in1, in2, in1name, in2name):
    if in1 == "" or in2 == "":
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя добавить пустые данные")
        return False
    try:
        if DBManage.addInformSupply(in1, in2):
            tkinter.messagebox.showinfo(title="Успех", message="Информация о поставке успешно обновлена")
            in1name.delete(0, END)
            in2name.delete(0, END)
    except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.UniqueViolation):
        tkinter.messagebox.showwarning(title="Внимание",
                                       message="Указан неверный номер поставки или инструмента, проверьте, "
                                               "что указан существующий код поставки "
                                               "или, что номер инструмента уникальный")


def widgets(frame0, frame1, frame3, frame5):
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
    text3.tag_configure('bold', font='Helvetica 12 bold')
    button9 = Button(frame3, text="Получить все пианино со склада", width=25, height=1,
                     command=lambda: getPianino(text3))
    text4 = Text(frame3, width=60, height=10)
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
    button13 = Button(frame5, text="Получить информацию о поставках", width=29, height=1,
                      command=lambda: getSupplyInfo(text5))
    button14 = Button(frame5, text="Зарегистрировать новую поставку в системе", width=35, height=1,
                      command=lambda: addSupply(entry8.get(), entry9.get(), entry8, entry9))
    entry8 = Entry(frame5, width=60)
    entry9 = Entry(frame5, width=60)
    label11 = Label(frame5, width=14, height=1, text="ID поставки", bg="gray22")
    label12 = Label(frame5, width=14, height=1, text="Дата поставки", bg="gray22")
    entry10 = Entry(frame5, width=60)
    entry11 = Entry(frame5, width=60)
    label13 = Label(frame5, width=15, height=1, text="ID поставки", bg="gray22")
    label14 = Label(frame5, width=15, height=1, text="ID инструмента", bg="gray22")
    button15 = Button(frame5, text="Добавить информацию о поставке", width=35, height=1, command=lambda:
    addInformSupply(entry10.get(), entry11.get(), entry10, entry11))
    # .........................................................................................Frame5 end
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


def showWindow():
    window = Tk()
    geometryWindow(window)
    notebook(window)
    window.mainloop()


if __name__ == '__main__':
    showWindow()
