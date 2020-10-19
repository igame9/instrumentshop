import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import DBManage


def auth(login, password, window, extrawindow):
    if DBManage.checkUser(login, password) == 1:
        tkinter.messagebox.showinfo(title="Успех", message="Вы успешно активировались")
        window.deiconify()
        extrawindow.destroy()
        return True
    else:
        tkinter.messagebox.showerror(title="Ошибка", message="Неверные логин или пароль")
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
        sys.exit()


def notebook(window):
    notebk = ttk.Notebook(window)
    style = ttk.Style()
    style.configure("1.TFrame", background="gray22")
    style.configure("2.TFrame", background="gray22")
    style.configure("3.TFrame", background="gray22")
    notebk.pack(fill='both', expand='yes')
    frame1 = ttk.Frame(window, style="1.TFrame")
    frame2 = ttk.Frame(window, style="2.TFrame")
    frame3 = ttk.Frame(window, style="3.TFrame")
    frame4 = ttk.Frame(window)
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()
    notebk.add(frame1, text='Клиенты')
    notebk.add(frame2, text='Сотрудники')
    notebk.add(frame3, text="Склад")
    notebk.add(frame4, text="Поставка")
    widgets(frame1)


def takeid(id, out):
    name = DBManage.selectClientName(id)
    if name == 0:
        name = ""
    if name == "" or name == []:
        name = "Отсутствует данная запись в БД"
    out.configure(text=name)


def addClient(name, family, outchange1, outchange2):
    if name == '' or family == '':
        tkinter.messagebox.showwarning(title="Внимание", message="Нельзя добавить пустого сотрудника")
        return False
    DBManage.clientAdd(name, family)
    outchange1.delete(0, END)
    outchange2.delete(0, END)
    return True


def widgets(frame1):
    button1 = Button(frame1, text='Получить клиента по id', width=18, height=1, fg='black',
                     command=lambda: takeid(entry1.get(), label1))
    label1 = Label(frame1, width=50, height=10)
    entry1 = Entry(frame1, width=5)
    label2 = Label(frame1, width=30, height=1, text="Введите id клиента для поиска")
    sep1 = ttk.Separator(frame1, orient="vertical")
    entry2 = Entry(frame1, width=60)
    entry3 = Entry(frame1, width=60)
    button2 = Button(frame1, text='Добавить нового клиента', width=23, height=1,
                     command=lambda: addClient(entry2.get(), entry3.get(), entry2, entry3))
    label3 = Label(frame1, width=5, height=1, text="Имя", bg="gray22")
    label4 = Label(frame1, width=7, height=1, text="Фамилия", bg="gray22")
    # Упаковка виджетов
    entry1.place(x=35, y=630)
    button1.place(x=100, y=630)
    label1.place(x=35, y=470)
    label2.place(x=110, y=470)
    sep1.place(x=0, y=460, relwidth=1)
    entry2.place(x=500, y=470)
    entry3.place(x=500, y=500)
    button2.place(x=500, y=630)
    label3.place(x=450, y=470)
    label4.place(x=440, y=500)


def showWindow():
    window = Tk()
    geometryWindow(window)
    notebook(window)
    window.mainloop()


if __name__ == '__main__':
    showWindow()
