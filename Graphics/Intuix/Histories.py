import tkinter as tk
import Assets.Functions.Parser as p
from Assets.Functions.Data import shorten_string
from Graphics.Colors import get_main_theme_color, get_sub_theme_color
from PIL import ImageTk, Image
from Assets.Functions.Data import check_type



class TellyHistories(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.prepare()

    def populate(self, identifier, row):
        """Put in some fake data"""
        tab = tk.Frame(self.frame, height=150, bg="#FF6680", width=1000, borderwidth="1")


        img_box = tk.Frame(tab, width=100, height=100, bg=get_sub_theme_color(essence="string"))
        pic = ImageTk.PhotoImage(Image.open(check_type(p.StorageAPI().get_unknown(identifier=identifier, key="media"))))
        tk.Label(img_box, image=pic).pack()
        img_box.grid(column=0, rowspan=3, row=0)
        tk.Label(tab, text=shorten_string(p.StorageAPI().get_unknown(identifier=identifier, key="name"), 90)).grid(
            column=1, row=0)
        tk.Label(tab, text=shorten_string(p.StorageAPI().get_unknown(identifier=identifier, key="url"), 90)).grid(
            column=1, row=1)
        tk.Label(tab, text=shorten_string(p.StorageAPI().get_unknown(identifier=identifier, key="media"), 90)).grid(
            column=1, row=2)
        tab.pack(padx=5, pady=5)



    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def prepare(self):


        for i in range(len(p.StorageAPI().get_all_ids())):
            self.populate(row=i, identifier=p.StorageAPI().get_all_ids()[i])


class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Telly histories")
        self.window.iconbitmap("Assets/Media/downloader.ico")
        self.window.geometry("1000x700")

        topbar = tk.Frame(self.window, height=40)

        del_all = tk.Button(topbar, text="Delete All", padx=100, pady=10, bg="#FF5356")
        del_all.grid(column=0)

        topbar.pack()
        example = TellyHistories(self.window)
        example.pack(side="top", fill="both", expand=True)

    def run(self):
        self.window.mainloop()


    def quit(self):
        self.window.quit()

