import datetime
import os
from tkinter import ttk

import customtkinter

from tkinter import *
from PIL import Image

from AutoTechDecktop.database import Database, PartControl, ServiceControl, ServiceOrderControl
from AutoTechDecktop.make_excel import MakeOrder

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme('blue')


class AppHome:
    def __init__(self, window):
        self.window = window
        self.base_dir = os.path.dirname(__file__)
        self.home()
        self.service_order()

    def home(self):
        self.window.geometry('800x600')
        self.window.title('Painel de navegação')
        icon_path = os.path.join(self.base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_left = customtkinter.CTkFrame(self.window, width=200, height=720)
        frame_left.pack(side=LEFT)

        frame_right = customtkinter.CTkFrame(self.window, width=1200, height=720)
        frame_right.pack(side=RIGHT)

        image_path = os.path.join(self.base_dir, 'img', 'painel2.png')

        image_bg = customtkinter.CTkImage(dark_image=Image.open(image_path), size=(998, 720))
        lbl_image = customtkinter.CTkLabel(frame_right, image=image_bg, text="")
        lbl_image.place(relx=0.01, rely=0.01, relwidth=1.0, relheight=1.0)

        image_path = os.path.join(self.base_dir, 'img', 'logo.png')

        logo_bg = customtkinter.CTkImage(dark_image=Image.open(image_path), size=(195, 195))
        lbl_image = customtkinter.CTkLabel(frame_left, image=logo_bg, text="")
        lbl_image.place(x=5, y=20)

        btn_windonw_service_order = customtkinter.CTkButton(
            frame_left, text='Odem de serviço', width=50, font=('helvetica', 20), fg_color='DARKRED', command=self.service_order)
        btn_windonw_service_order.place(x=20, y=250)

        btn_windonw_report = customtkinter.CTkButton(
            frame_left, text='Relatorio', width=165, font=('helvetica', 20), fg_color='DARKRED')
        btn_windonw_report.place(x=20, y=300)

        self.window.mainloop()

    def service_order(self):
        self.window.destroy()
        new_window = customtkinter.CTk()
        AppServiceOrder(new_window)


class AppServiceOrder:
    def __init__(self, window):
        self.window = window
        self.base_dir = os.path.dirname(__file__)
        self.service_order()
        self.back_to_home()

    def service_order(self):
        self.window.geometry('800x600')
        self.window.title('Ordem de Serviço')
        icon_path = os.path.join(self.base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_title = customtkinter.CTkFrame(self.window, width=1200, height=80, bg_color='DARKRED', fg_color='DARKRED')
        frame_title.pack(side=TOP)

        logo_path = os.path.join(self.base_dir, 'img', 'logo1.png')
        logo = customtkinter.CTkImage(dark_image=Image.open(logo_path), size=(80, 80))

        label_img = customtkinter.CTkLabel(frame_title, image=logo, text="")
        label_img.place(x=10, y=2)

        lbl_title = customtkinter.CTkLabel(
            frame_title, text='AutoMecânica Valdir', text_color='white', font=('MIDNIGHTBLUE', 30))
        lbl_title.place(x=100, y=20)

        date = datetime.datetime.now()
        format_date = date.strftime('%d/%m/%y')
        lbl_title_right = customtkinter.CTkLabel(
            frame_title, text=f'fortaleza {format_date}', text_color='white', font=('MIDNIGHTBLUE', 20))
        lbl_title_right.place(x=630, y=40)

        # Carro
        frame_car = customtkinter.CTkFrame(self.window, width=800, height=40)
        frame_car.pack(side=TOP)

        # Nome do carro
        entry_car_name = customtkinter.CTkEntry(
            frame_car, placeholder_text='Veiculo', width=300, font=('helvetica', 18))
        entry_car_name.place(x=20, y=10)

        # Placa
        entry_car_plate = customtkinter.CTkEntry(frame_car, placeholder_text='Placa', width=200, font=('helvetica', 18))
        entry_car_plate.place(x=330, y=10)

        # Kilometragem
        entry_car_kms = customtkinter.CTkEntry(frame_car, placeholder_text='kms', width=250, font=('helvetica', 18))
        entry_car_kms.place(x=540, y=10)

        # Peças
        frame_part = customtkinter.CTkFrame(self.window, width=800, height=200)
        frame_part.pack(side=TOP)

        lbl_part = customtkinter.CTkLabel(frame_part, text='Peças', text_color='white', font=('MIDNIGHTBLUE', 18))
        lbl_part.place(x=350, y=5)

        # Quantidade
        entry_part_qtd = customtkinter.CTkEntry(frame_part, placeholder_text='Qtd', width=100, font=('helvetica', 18))
        entry_part_qtd.place(x=20, y=35)

        # item
        entry_part_item = customtkinter.CTkEntry(frame_part, placeholder_text='Item', width=350, font=('helvetica', 18))
        entry_part_item.place(x=130, y=35)
        # valor
        entry_part_value = customtkinter.CTkEntry(frame_part, placeholder_text='R$:00,00', width=150,
                                                  font=('helvetica', 18))
        entry_part_value.place(x=490, y=35)

        def delete_part_data():
            database = PartControl('basededados.db')
            database.truncate_part()

            for i in treeview_part.get_children():
                treeview_part.delete(i)

        def load_part_to_treeview():
            # Limpa os valores antigos no treeview
            for i in treeview_part.get_children():
                treeview_part.delete(i)

            # Recupera os dados do banco de dados
            database = PartControl('basededados.db')
            list_values = database.read_all_part()

            # Adiciona os dados ao treeview
            for row in list_values:
                treeview_part.insert("", END, values=[row[1], row[2], row[3]])

        def add_to_part():
            quantity = entry_part_qtd.get()
            item = entry_part_item.get()
            value = entry_part_value.get()

            database = PartControl('basededados.db')
            database.create_part(quantity, item, value)

            load_part_to_treeview()
            entry_part_qtd.delete(0, END)
            entry_part_item.delete(0, END)
            entry_part_value.delete(0, END)

        btn_add_part = customtkinter.CTkButton(
            frame_part, text='Adicionar', width=100, font=('helvetica', 18), fg_color='DARKRED', command=add_to_part)
        btn_add_part.place(x=650, y=35)

        cols = ('quantity', 'part', 'value')
        treeview_part = ttk.Treeview(frame_part, show='headings', columns=cols, height=10)

        treeview_part.column('quantity', width=100, minwidth=10, stretch=NO)
        treeview_part.heading('#1', text='Quantidade')
        treeview_part.column('part', width=660, minwidth=200, stretch=NO)
        treeview_part.heading('#2', text='Peças')
        treeview_part.column('value', width=200, minwidth=200, stretch=NO)
        treeview_part.heading('#3', text='Valor')

        treeview_part.place(x=20, y=100)

        part_scrollbar = Scrollbar(frame_part, orient='vertical')
        treeview_part.configure(yscrollcommand=part_scrollbar.set)
        part_scrollbar.place(x=960, y=100, relheight=0.60)

        # Service
        frame_service = customtkinter.CTkFrame(self.window, width=800, height=200)
        frame_service.pack(side=TOP)

        lbl_service = customtkinter.CTkLabel(frame_service, text='Serviços ', text_color='white',
                                             font=('MIDNIGHTBLUE', 18))
        lbl_service.place(x=350, y=5)

        entry_service_item = customtkinter.CTkEntry(frame_service, placeholder_text='item', width=510,
                                                    font=('helvetica', 18))
        entry_service_item.place(x=20, y=30)

        entry_service_value = customtkinter.CTkEntry(frame_service, placeholder_text='R$:00,00', width=150,
                                                     font=('helvetica', 18))
        entry_service_value.place(x=535, y=30)

        def delete_service_data():
            database = ServiceControl('basededados.db')
            database.truncate_service()

            for i in treeview_service.get_children():
                treeview_service.delete(i)

        def load_service_to_treeview():
            # Limpa os valores antigos no treeview
            for i in treeview_service.get_children():
                treeview_service.delete(i)

            # Recupera os dados do banco de dados
            database = ServiceControl('basededados.db')
            list_values = database.read_all_service()

            # Adiciona os dados ao treeview
            for row in list_values:
                treeview_service.insert("", END, values=[row[1], row[2]])

        def add_to_service():
            item = entry_service_item.get()
            value = entry_service_value.get()

            database = ServiceControl('basededados.db')

            database.create_service(item, value)

            load_service_to_treeview()
            entry_service_item.delete(0, END)
            entry_service_value.delete(0, END)

        btn_add_service = customtkinter.CTkButton(
            frame_service, text='Adicionar', width=100, font=('helvetica', 18), fg_color='DARKRED', command=add_to_service)
        btn_add_service.place(x=690, y=30)

        cols = ('service', 'value')
        treeview_service = ttk.Treeview(frame_service, show='headings', columns=cols, height=15)

        treeview_service.column('service', width=760, minwidth=200, stretch=NO)
        treeview_service.heading('#1', text='Serviço')
        treeview_service.column('value', width=200, minwidth=200, stretch=NO)
        treeview_service.heading('#2', text='Valor')

        treeview_service.place(x=20, y=100)

        service_scrollbar = Scrollbar(frame_service, orient='vertical')
        treeview_service.configure(yscrollcommand=service_scrollbar.set)
        service_scrollbar.place(x=960, y=100, relheight=0.60)

        def delete_service_order_data():
            database = ServiceOrderControl('basededados.db')
            database.truncate_service_order()

            entry_car_name.delete(0, END)
            entry_car_plate.delete(0, END)
            entry_car_kms.delete(0, END)

        def save_data():
            car_name = entry_car_name.get()
            car_plate = entry_car_plate.get()
            car_kms = entry_car_kms.get()

            service_oreder_control = ServiceOrderControl('basededados.db')
            service_oreder_control.create_service_order(car_name, car_plate, car_kms)

            make_order = MakeOrder()
            make_order.make_excel()

            delete_service_order_data()
            delete_part_data()
            delete_service_data()

        btn_save_os = customtkinter.CTkButton(
            self.window, text='Salvar', width=150, font=('helvetica', 25), fg_color='DARKRED', command=save_data)
        btn_save_os.place(x=630, y=550)

        btn_save_os = customtkinter.CTkButton(
            self.window, text='voltar', width=150, font=('helvetica', 25), fg_color='DARKRED', command=self.back_to_home)
        btn_save_os.place(x=20, y=550)

        self.window.mainloop()

    def back_to_home(self):
        self.window.destroy()
        home_window = customtkinter.CTk()
        AppHome(home_window)


if __name__ == '__main__':
    database = Database('basededados.db')
    database.create_service_order_table()
    database.create_part_table()
    database.create_service_table()


    root = customtkinter.CTk()
    AppHome(root)


