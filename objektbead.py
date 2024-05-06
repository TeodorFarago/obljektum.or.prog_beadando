import tkinter as tk
from tkinter import messagebox
import datetime


class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 10000)


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 15000)


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglal(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(foglalas)
                return foglalas
        return None

    def foglalas_ar(self, foglalas):
        return foglalas.szoba.ar

    def foglalas_lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return True
        return False

    def listaz_foglalasok(self):
        return self.foglalasok


def fill_data(szalloda):
    egyagyas1 = EgyagyasSzoba("101")
    egyagyas2 = EgyagyasSzoba("102")
    ketagyas = KetagyasSzoba("201")
    szalloda.uj_szoba(egyagyas1)
    szalloda.uj_szoba(egyagyas2)
    szalloda.uj_szoba(ketagyas)

    szalloda.foglal("101", "2024-05-07")
    szalloda.foglal("101", "2024-05-08")
    szalloda.foglal("102", "2024-05-07")
    szalloda.foglal("201", "2024-05-09")
    szalloda.foglal("201", "2024-05-10")


def foglalas_felulet(szalloda):
    def foglalas():
        szobaszam = szobaszam_entry.get()
        datum = datum_entry.get()
        try:
            datum = datetime.datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            messagebox.showinfo("Hiba", "Hibás dátumformátum! Helyes formátum: YYYY-MM-DD")
            return
        if datum < datetime.datetime.now():
            messagebox.showinfo("Hiba", "A foglalás csak jövőbeli dátumra lehetséges!")
            return
        foglalas = szalloda.foglal(szobaszam, datum.strftime("%Y-%m-%d"))
        if foglalas:
            messagebox.showinfo("Siker", f"Foglalás sikeres! Ár: {szalloda.foglalas_ar(foglalas)} Ft")

    foglalas_felulet = tk.Toplevel()
    foglalas_felulet.title("Foglalás")

    szobaszam_label = tk.Label(foglalas_felulet, text="Szoba száma:")
    szobaszam_label.grid(row=0, column=0)
    szobaszam_entry = tk.Entry(foglalas_felulet)
    szobaszam_entry.grid(row=0, column=1)

    datum_label = tk.Label(foglalas_felulet, text="Dátum (YYYY-MM-DD):")
    datum_label.grid(row=1, column=0)
    datum_entry = tk.Entry(foglalas_felulet)
    datum_entry.grid(row=1, column=1)

    foglalas_button = tk.Button(foglalas_felulet, text="Foglalás", command=foglalas)
    foglalas_button.grid(row=2, columnspan=2)


def lemondas_felulet(szalloda):
    def lemondas():
        szobaszam = szobaszam_entry.get()
        datum = datum_entry.get()
        foglalas = None
        for foglalas in szalloda.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                break
        if foglalas:
            if szalloda.foglalas_lemondas(foglalas):
                messagebox.showinfo("Siker", "Foglalás lemondva.")
            else:
                messagebox.showinfo("Hiba", "Nem létező foglalás!")

    lemondas_felulet = tk.Toplevel()
    lemondas_felulet.title("Lemondás")

    szobaszam_label = tk.Label(lemondas_felulet, text="Szoba száma:")
    szobaszam_label.grid(row=0, column=0)
    szobaszam_entry = tk.Entry(lemondas_felulet)
    szobaszam_entry.grid(row=0, column=1)

    datum_label = tk.Label(lemondas_felulet, text="Dátum (YYYY-MM-DD):")
    datum_label.grid(row=1, column=0)
    datum_entry = tk.Entry(lemondas_felulet)
    datum_entry.grid(row=1, column=1)

    lemondas_button = tk.Button(lemondas_felulet, text="Lemondás", command=lemondas)
    lemondas_button.grid(row=2, columnspan=2)


def listazas_felulet(szalloda):
    foglalasok = szalloda.listaz_foglalasok()
    foglalasok_text = ""
    for foglalas in foglalasok:
        foglalasok_text += f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}\n"
    messagebox.showinfo("Foglalások listája", foglalasok_text)


szalloda = Szalloda("Kiváló Szálloda")
fill_data(szalloda)

app = tk.Tk()
app.title("Szállodai foglaláskezelő")

foglalas_button = tk.Button(app, text="Foglalás", command=lambda: foglalas_felulet(szalloda))
foglalas_button.pack(pady=5)

lemondas_button = tk.Button(app, text="Lemondás", command=lambda: lemondas_felulet(szalloda))
lemondas_button.pack(pady=5)

listazas_button = tk.Button(app, text="Foglalások listázása", command=lambda: listazas_felulet(szalloda))
listazas_button.pack(pady=5)

kilepes_button = tk.Button(app, text="Kilépés", command=app.quit)
kilepes_button.pack(pady=5)

app.mainloop()
