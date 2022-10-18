from tkinter import messagebox
import mysql.connector as mc
from tkinter import *
from tkinter import ttk


class GUI:
    def __init__(self, root):
        self.root = root
        self.f1 = ("Arial", 14)

        # Config
        self.root.geometry("800x500")
        # Connect to database
        self.conn = mc.connect(
            host="localhost",
            user="test",
            password="test"
        )

        self.cur = self.conn.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS school")

        self.conn = mc.connect(
            host="localhost",
            user="test",
            password="test",
            database="student"
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS school(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), department VARCHAR(255), grade FLOAT)")

    def start(self):
        self.main = Frame(self.root)
        self.main.pack(fill="both", expand=1)
        self.menu()
        self.root.mainloop()

    def menu(self):
        id_entry = Entry(self.main, font=self.f1)
        id_entry.place(relx=0.02, rely=0.03, anchor="nw", relwidth=0.05)
        Button(self.main, text="Search ID", font=self.f1, command=lambda: self.get_id(id_entry.get())).place(relx=0.08,
                                                                                                             rely=0.02,
                                                                                                             anchor="nw")

        name_entry = Entry(self.main, font=self.f1)
        name_entry.place(relx=0.24, rely=0.03, anchor="nw", relwidth=0.15)
        Button(self.main, text="Search Name", font=self.f1, command=lambda: self.get_name(name_entry.get())).place(
            relx=0.4, rely=0.02, anchor="nw")

        column = ["ID", "Name", "Department", "Grade"]
        self.tree = ttk.Treeview(self.main, columns=column, selectmode="extended", show="headings")
        self.tree.place(relx=0.02, rely=0.125, relwidth=0.8, relheight=0.7, anchor="nw")
        for i in column:
            self.tree.heading(i, text=i)
            self.tree.column(i, width=100)
        self.refreshtv()

        Button(self.main, text="ADD", font=self.f1, command=self.add).place(relx=0.85, rely=0.125, anchor="nw")
        Button(self.main, text="UPDATE", font=self.f1, command=self.update).place(relx=0.85, rely=0.25, anchor="nw")
        Button(self.main, text="DELETE", font=self.f1, command=self.delete).place(relx=0.85, rely=0.375, anchor="nw")

        Button(self.main, text="SORT by grade", font=self.f1, command=lambda: self.sort("grade")).place(relx=0.02,
                                                                                                        rely=0.85,
                                                                                                        anchor="nw")
        Button(self.main, text="SORT by department", font=self.f1, command=lambda: self.sort("department")).place(
            relx=0.22, rely=0.85, anchor="nw")

    def sort(self, order):
        if order == "grade":
            self.refreshtv("SELECT * FROM school ORDER by grade")
        elif order == "department":
            self.refreshtv("SELECT * FROM school ORDER by department")
            x = Toplevel()
            x.geometry("400x400")
            self.cur.execute("SELECT department, grade FROM school ORDER by department")
            info = self.cur.fetchall()
            s_imfo = []
            for i in info:
                s_imfo.append(i[0])
            s_imfo = set(s_imfo)
            result = []
            for i in sorted(s_imfo):
                sum = 0
                count = 0
                for n in info:
                    if i[0] in n:
                        count += 1
                        sum += n[1]
                result.append("{}: {}".format(i, sum / count))
            var = 0
            for i in result:
                Label(x, text=i, font=self.f1).place(relx=0.1, rely=0.01 + var, anchor="nw")
                var += 0.1

    def refreshtv(self, query="SELECT * FROM school"):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute(query)
        for i in self.cur.fetchall():
            self.tree.insert("", END, values=i)

    def add(self):
        x = Toplevel()
        x.geometry("400x400")
        Label(x, text="Name", font=self.f1).place(relx=0.1, rely=0.2, anchor="nw")
        e1 = Entry(x, font=self.f1)
        e1.place(relx=0.42, rely=0.2, anchor="nw")

        Label(x, text="department", font=self.f1).place(relx=0.1, rely=0.4, anchor="nw")
        e2 = Entry(x, font=self.f1)
        e2.place(relx=0.42, rely=0.4, anchor="nw")

        Label(x, text="grade", font=self.f1).place(relx=0.1, rely=0.6, anchor="nw")
        e3 = Entry(x, font=self.f1)
        e3.place(relx=0.42, rely=0.6, anchor="nw")

        def submit():
            self.cur.execute("INSERT INTO school (name,department,grade) VALUES (%s,%s,%s)",
                             (e1.get(), e2.get(), e3.get()))
            self.conn.commit()
            self.refreshtv()
            x.destroy()

        Button(x, text="Submit", font=self.f1, command=submit).place(relx=0.5, rely=0.8, anchor="center")

    def update(self):
        try:
            select = self.tree.item(self.tree.selection())["values"][0]
        except:
            messagebox.showerror(message="SELECT ITEM")
            return
        x = Toplevel()
        x.geometry("400x400")
        Label(x, text="Name", font=self.f1).place(relx=0.1, rely=0.2, anchor="nw")
        e1 = Entry(x, font=self.f1)
        e1.place(relx=0.42, rely=0.2, anchor="nw")

        Label(x, text="department", font=self.f1).place(relx=0.1, rely=0.4, anchor="nw")
        e2 = Entry(x, font=self.f1)
        e2.place(relx=0.42, rely=0.4, anchor="nw")

        Label(x, text="grade", font=self.f1).place(relx=0.1, rely=0.6, anchor="nw")
        e3 = Entry(x, font=self.f1)
        e3.place(relx=0.42, rely=0.6, anchor="nw")

        def submit():
            self.cur.execute(
                "UPDATE school SET name='{}', department='{}', grade='{}' WHERE id='{}'".format(e1.get(), e2.get(),
                                                                                                e3.get(), select))
            self.conn.commit()
            self.refreshtv()
            x.destroy()

        Button(x, text="Submit", font=self.f1, command=submit).place(relx=0.5, rely=0.8, anchor="center")

    def delete(self):
        try:
            select = self.tree.item(self.tree.selection())["values"][0]
        except:
            messagebox.showerror(message="SELECT ITEM")
            return
        self.cur.execute("DELETE FROM school WHERE id='{}'".format(select))
        self.conn.commit()
        self.refreshtv()

    def get_id(self, id):
        if len(id) == 0:
            self.refreshtv()
        else:
            self.refreshtv("SELECT * FROM school WHERE id='{}'".format(id))

    def get_name(self, name):
        if len(name) == 0:
            self.refreshtv()
        else:
            self.refreshtv("SELECT * FROM school WHERE name='{}'".format(name))


root = Tk()
app = GUI(root)
app.start()