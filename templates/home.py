import os

from AutoTechDecktop.views.view import open_service_order
from tkinter import *
from PIL import Image


class HomeTemplate:
    def __init__(self, ct):
        self.window = ct.CTk()
        self.ct = ct
        self.base_dir = os.path.dirname(__file__)

    def home_template(self):
        self.window.geometry('800x600')
        self.window.title('Painel de navegação')
        icon_path = os.path.join(self.base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_left = self.ct.CTkFrame(self.window, width=200, height=720)
        frame_left.pack(side=LEFT)

        frame_right = self.ct.CTkFrame(self.window, width=998, height=720)
        frame_right.pack(side=RIGHT)

        image_path = os.path.join(self.base_dir, 'img', 'painel2.png')

        image_bg = self.ct.CTkImage(dark_image=Image.open(image_path), size=(998, 720))
        lbl_image = self.ct.CTkLabel(frame_right, image=image_bg, text="")
        lbl_image.place(relx=0.01, rely=0.01, relwidth=1.0, relheight=1.0)

        image_path = os.path.join(self.base_dir, 'img', 'logo.png')

        logo_bg = self.ct.CTkImage(dark_image=Image.open(image_path), size=(195, 195))
        lbl_image = self.ct.CTkLabel(frame_left, image=logo_bg, text="")
        lbl_image.place(x=10, y=20)

        btn_windonw_service_order = self.ct.CTkButton(
            frame_left, text='Odem de serviço', width=50, font=('helvetica', 20), fg_color='DARKRED', command=open_service_order)
        btn_windonw_service_order.place(x=20, y=200)

        btn_windonw_report = self.ct.CTkButton(
            frame_left, text='Relatorio', width=165, font=('helvetica', 20), fg_color='DARKRED')
        btn_windonw_report.place(x=20, y=250)










        return self.window.mainloop()
