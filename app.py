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

base_dir = os.path.dirname(__file__)


class AppHome:
    def __init__(self, window):
        self.window = window
        self.home()
        self.service_order_manager()
        self.report()

    def home(self):
        self.window.geometry('800x600')
        self.window.title('Painel de navegação')
        icon_path = os.path.join(base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_left = customtkinter.CTkFrame(self.window, width=200, height=720)
        frame_left.pack(side=LEFT)

        frame_right = customtkinter.CTkFrame(self.window, width=1200, height=720)
        frame_right.pack(side=RIGHT)

        image_path = os.path.join(base_dir, 'img', 'painel2.png')

        image_bg = customtkinter.CTkImage(dark_image=Image.open(image_path), size=(998, 720))
        lbl_image = customtkinter.CTkLabel(frame_right, image=image_bg, text="")
        lbl_image.place(relx=0.01, rely=0.01, relwidth=1.0, relheight=1.0)

        image_path = os.path.join(base_dir, 'img', 'logo.png')

        logo_bg = customtkinter.CTkImage(dark_image=Image.open(image_path), size=(195, 195))
        lbl_image = customtkinter.CTkLabel(frame_left, image=logo_bg, text="")
        lbl_image.place(x=5, y=20)

        btn_windonw_service_order = customtkinter.CTkButton(
            frame_left, text='Odem de serviço', width=50, font=('helvetica', 20), fg_color='DARKRED', command=self.service_order_manager)
        btn_windonw_service_order.place(x=20, y=250)

        btn_windonw_report = customtkinter.CTkButton(
            frame_left, text='Relatorio', width=165, font=('helvetica', 20), fg_color='DARKRED', command=self.report)
        btn_windonw_report.place(x=20, y=300)

        def switch():
            if switch_var.get() == 'ON':
                customtkinter.set_appearance_mode("light")
            else:
                customtkinter.set_appearance_mode("Dark")

        switch_var = customtkinter.StringVar(value="OFF")
        switch_mode = customtkinter.CTkSwitch(
            frame_left, text="Modo claro", height=40, variable=switch_var, onvalue="ON", offvalue="OFF", command=switch)
        switch_mode.place(x=20, y=560)

        self.window.mainloop()

    def service_order_manager(self):
        self.window.destroy()
        new_window = customtkinter.CTk()
        AppServiceOrderManager(new_window)

    def report(self):
        self.window.destroy()
        report_window = customtkinter.CTk()
        AppReport(report_window)


class AppServiceOrder:
    def __init__(self, window):
        self.window = window
        self.service_order()

    def service_order(self):
        self.window.geometry('800x600')
        self.window.title('Ordem de Serviço')
        icon_path = os.path.join(base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_title = customtkinter.CTkFrame(self.window, width=1200, height=80, bg_color='DARKRED', fg_color='DARKRED')
        frame_title.pack(side=TOP)

        logo_path = os.path.join(base_dir, 'img', 'logo1.png')
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

        btn_save_os_back = customtkinter.CTkButton(
            self.window, text='voltar', width=150, font=('helvetica', 25), fg_color='DARKRED', command=self.back_to_home)
        btn_save_os_back.place(x=20, y=550)

        self.window.mainloop()

    def back_to_home(self):
        self.window.destroy()
        home_window = customtkinter.CTk()
        AppHome(home_window)


class AppServiceOrderManager:
    def __init__(self, window):
        self.window = window
        self.service_order_manager()
        self.new_order()

    def service_order_manager(self):
        self.window.geometry('800x600')
        self.window.title('Gerenciamento de Ordem de Serviço')
        icon_path = os.path.join(base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_title = customtkinter.CTkFrame(self.window, width=1200, height=80, bg_color='DARKRED', fg_color='DARKRED')
        frame_title.pack(side=TOP)

        logo_path = os.path.join(base_dir, 'img', 'logo1.png')
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

        entry_part_item = customtkinter.CTkEntry(self.window, placeholder_text='Buscar OS', width=350,
                                                 font=('helvetica', 25))
        entry_part_item.place(x=20, y=190)

        btn_new_order = customtkinter.CTkButton(
            self.window, text='Nova Os', width=150, font=('helvetica', 25), fg_color='DARKRED',
            command=self.new_order)
        btn_new_order.place(x=600, y=190)

        btn_pesquisar = customtkinter.CTkButton(
            self.window, text='Pesquisar', width=150, font=('helvetica', 25), fg_color='DARKRED',
            command=self.back_to_home)
        btn_pesquisar.place(x=380, y=190)

        cols = ('service_order', 'plate', 'total_part', 'total_service', 'total_value', 'date')
        treeview_part = ttk.Treeview(self.window, show='headings', columns=cols, height=16)

        treeview_part.column('service_order', width=156, minwidth=10, stretch=NO)
        treeview_part.heading('#1', text='Ordem de Serviço')
        treeview_part.column('plate', width=156, minwidth=50, stretch=NO)
        treeview_part.heading('#2', text='Placa')
        treeview_part.column('total_part', width=157, minwidth=50, stretch=NO)
        treeview_part.heading('#3', text='Total de Peças')
        treeview_part.column('total_service', width=157, minwidth=10, stretch=NO)
        treeview_part.heading('#4', text='Total de Serviço')
        treeview_part.column('total_value', width=157, minwidth=50, stretch=NO)
        treeview_part.heading('#5', text='Total Geral')
        treeview_part.column('date', width=157, minwidth=50, stretch=NO)
        treeview_part.heading('#6', text='Data')

        treeview_part.place(x=20, y=300)

        part_scrollbar = Scrollbar(self.window, orient='vertical')
        treeview_part.configure(yscrollcommand=part_scrollbar.set)
        part_scrollbar.place(x=960, y=300, relheight=0.46)


        btn_save_os_back = customtkinter.CTkButton(
            self.window, text='voltar', width=150, font=('helvetica', 25), fg_color='DARKRED',
            command=self.back_to_home)
        btn_save_os_back.place(x=20, y=550)

        self.window.mainloop()

    def new_order(self):
        self.window.destroy()
        service_order_window = customtkinter.CTk()
        AppServiceOrder(service_order_window)

    def back_to_home(self):
        self.window.destroy()
        home_window = customtkinter.CTk()
        AppHome(home_window)


class AppReport:
    def __init__(self, window):
        self.window = window
        self.report()

    def report(self):
        self.window.title('Relatorio')
        self.window.geometry('810x600')
        icon_path = os.path.join(base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        frame_1 = customtkinter.CTkFrame(
            self.window, width=600, height=600, bg_color='DARKRED')
        frame_1.pack(side=RIGHT)

        frame_2 = customtkinter.CTkFrame(self.window, width=200, height=600)
        frame_2.pack(side=LEFT)

        image_path = os.path.join(base_dir, 'img', 'logo.png')

        logo_bg = customtkinter.CTkImage(dark_image=Image.open(image_path), size=(195, 195))
        lbl_image = customtkinter.CTkLabel(frame_2, image=logo_bg, text="")
        lbl_image.place(x=5, y=20)

        tab_moths = customtkinter.CTkTabview(frame_1, width=600, height=800, corner_radius=10, segmented_button_selected_color='DARKRED')
        tab_moths.pack(side=TOP)

        tab_moths.add("JAN")
        tab_moths.add("FEV")
        tab_moths.add("MAR")
        tab_moths.add("ABR")
        tab_moths.add("MAI")
        tab_moths.add("JUN")
        tab_moths.add("JUL")
        tab_moths.add("AGO")
        tab_moths.add("SET")
        tab_moths.add("OUT")
        tab_moths.add("NOV")
        tab_moths.add("DEZ")

        # Janeiro

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("JAN"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("JAN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_jan_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_jan_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_jan_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_jan_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_jan_1.set(f'{0}')
                txt_var_value_jan_2.set(f'{0}')
                txt_var_value_jan_3.set(f'{0}')
                txt_var_value_jan_4.set(f'{0}')
            else:
                txt_var_value_jan_1.set(f'{valor_1}')
                txt_var_value_jan_2.set(f'{valor_2:.2f}')
                txt_var_value_jan_3.set(f'{valor_3:.2f}')
                txt_var_value_jan_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "JAN"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED',  dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_jan_1, font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_jan_2, font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_jan_3, font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_jan_4, font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Fevereiro

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("FEV"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("FEV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 65
        valor_2 = 1500.00
        valor_3 = 2600.00
        valor_4 = 4100.00

        txt_var_value_fev_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_fev_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_fev_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_fev_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_fev_1.set(f'{0}')
                txt_var_value_fev_2.set(f'{0}')
                txt_var_value_fev_3.set(f'{0}')
                txt_var_value_fev_4.set(f'{0}')
            else:
                txt_var_value_fev_1.set(f'{valor_1}')
                txt_var_value_fev_2.set(f'{valor_2:.2f}')
                txt_var_value_fev_3.set(f'{valor_3:.2f}')
                txt_var_value_fev_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "FEV"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_fev_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_fev_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_fev_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_fev_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Março

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("MAR"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("MAR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_mar_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_mar_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_mar_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_mar_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_mar_1.set(f'{0}')
                txt_var_value_mar_2.set(f'{0}')
                txt_var_value_mar_3.set(f'{0}')
                txt_var_value_mar_4.set(f'{0}')
            else:
                txt_var_value_mar_1.set(f'{valor_1}')
                txt_var_value_mar_2.set(f'{valor_2:.2f}')
                txt_var_value_mar_3.set(f'{valor_3:.2f}')
                txt_var_value_mar_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "MAR"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_mar_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_mar_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_mar_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_mar_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Abril

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("ABR"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("ABR"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_abr_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_abr_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_abr_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_abr_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_abr_1.set(f'{0}')
                txt_var_value_abr_2.set(f'{0}')
                txt_var_value_abr_3.set(f'{0}')
                txt_var_value_abr_4.set(f'{0}')
            else:
                txt_var_value_abr_1.set(f'{valor_1}')
                txt_var_value_abr_2.set(f'{valor_2:.2f}')
                txt_var_value_abr_3.set(f'{valor_3:.2f}')
                txt_var_value_abr_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "ABR"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_abr_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_abr_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_abr_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_abr_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Maio

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("MAI"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("MAI"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_mai_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_mai_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_mai_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_mai_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_mai_1.set(f'{0}')
                txt_var_value_mai_2.set(f'{0}')
                txt_var_value_mai_3.set(f'{0}')
                txt_var_value_mai_4.set(f'{0}')
            else:
                txt_var_value_mai_1.set(f'{valor_1}')
                txt_var_value_mai_2.set(f'{valor_2:.2f}')
                txt_var_value_mai_3.set(f'{valor_3:.2f}')
                txt_var_value_mai_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "MAI"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_mai_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_mai_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_mai_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_mai_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Junho

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("JUN"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("JUN"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_jun_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_jun_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_jun_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_jun_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_jun_1.set(f'{0}')
                txt_var_value_jun_2.set(f'{0}')
                txt_var_value_jun_3.set(f'{0}')
                txt_var_value_jun_4.set(f'{0}')
            else:
                txt_var_value_jun_1.set(f'{valor_1}')
                txt_var_value_jun_2.set(f'{valor_2:.2f}')
                txt_var_value_jun_3.set(f'{valor_3:.2f}')
                txt_var_value_jun_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "JUN"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_jun_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_jun_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_jun_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_jun_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Julho

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("JUL"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("JUL"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_jul_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_jul_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_jul_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_jul_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_jul_1.set(f'{0}')
                txt_var_value_jul_2.set(f'{0}')
                txt_var_value_jul_3.set(f'{0}')
                txt_var_value_jul_4.set(f'{0}')
            else:
                txt_var_value_jul_1.set(f'{valor_1}')
                txt_var_value_jul_2.set(f'{valor_2:.2f}')
                txt_var_value_jul_3.set(f'{valor_3:.2f}')
                txt_var_value_jul_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "JUL"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_jul_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_jul_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_jul_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_jul_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Agosto

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("AGO"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("AGO"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_ago_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_ago_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_ago_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_ago_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_ago_1.set(f'{0}')
                txt_var_value_ago_2.set(f'{0}')
                txt_var_value_ago_3.set(f'{0}')
                txt_var_value_ago_4.set(f'{0}')
            else:
                txt_var_value_ago_1.set(f'{valor_1}')
                txt_var_value_ago_2.set(f'{valor_2:.2f}')
                txt_var_value_ago_3.set(f'{valor_3:.2f}')
                txt_var_value_ago_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "AGO"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_ago_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_ago_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_ago_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_ago_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Setembro

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("SET"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("SET"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_set_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_set_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_set_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_set_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_set_1.set(f'{0}')
                txt_var_value_set_2.set(f'{0}')
                txt_var_value_set_3.set(f'{0}')
                txt_var_value_set_4.set(f'{0}')
            else:
                txt_var_value_set_1.set(f'{valor_1}')
                txt_var_value_set_2.set(f'{valor_2:.2f}')
                txt_var_value_set_3.set(f'{valor_3:.2f}')
                txt_var_value_set_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "SET"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_set_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_set_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_set_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_set_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Outubro

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("OUT"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("OUT"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_out_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_out_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_out_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_out_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_out_1.set(f'{0}')
                txt_var_value_out_2.set(f'{0}')
                txt_var_value_out_3.set(f'{0}')
                txt_var_value_out_4.set(f'{0}')
            else:
                txt_var_value_out_1.set(f'{valor_1}')
                txt_var_value_out_2.set(f'{valor_2:.2f}')
                txt_var_value_out_3.set(f'{valor_3:.2f}')
                txt_var_value_out_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "OUT"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_out_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_out_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_out_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_out_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Novembro

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("NOV"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("NOV"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_nov_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_nov_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_nov_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_nov_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_nov_1.set(f'{0}')
                txt_var_value_nov_2.set(f'{0}')
                txt_var_value_nov_3.set(f'{0}')
                txt_var_value_nov_4.set(f'{0}')
            else:
                txt_var_value_nov_1.set(f'{valor_1}')
                txt_var_value_nov_2.set(f'{valor_2:.2f}')
                txt_var_value_nov_3.set(f'{valor_3:.2f}')
                txt_var_value_nov_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "NOV"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_nov_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_nov_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_nov_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_nov_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

        # Dezembro

        lbl_title = customtkinter.CTkLabel(tab_moths.tab("DEZ"), text="Valores", font=('ROBOT', 50))
        lbl_title.place(x=5, y=5)

        frame_tab_1 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_1.place(x=10, y=110)

        frame_tab_2 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_2.place(x=270, y=110)

        frame_tab_3 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_3.place(x=10, y=170)

        frame_tab_4 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_4.place(x=270, y=170)

        frame_tab_5 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_5.place(x=10, y=230)

        frame_tab_6 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_6.place(x=270, y=230)

        frame_tab_7 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='yellow')
        frame_tab_7.place(x=10, y=290)

        frame_tab_8 = customtkinter.CTkFrame(
            tab_moths.tab("DEZ"), width=250, height=50, corner_radius=20, fg_color='red')
        frame_tab_8.place(x=270, y=290)

        lbl_title_frame_tab_1 = customtkinter.CTkLabel(
            frame_tab_1, text='Atendimentos', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_1.place(x=5, y=5)

        lbl_title_frame_tab_2 = customtkinter.CTkLabel(
            frame_tab_3, text='Total Serviços', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_2.place(x=5, y=5)

        lbl_title_frame_tab_3 = customtkinter.CTkLabel(
            frame_tab_5, text='Total Peças', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_3.place(x=5, y=5)

        lbl_title_frame_tab_4 = customtkinter.CTkLabel(
            frame_tab_7, text='Faturamento', font=('helvetica', 30), text_color='black')
        lbl_title_frame_tab_4.place(x=5, y=5)

        valor_1 = 50
        valor_2 = 1000.00
        valor_3 = 2000.00
        valor_4 = 3000.00

        txt_var_value_dez_1 = customtkinter.StringVar(value=f'{valor_1}')
        txt_var_value_dez_2 = customtkinter.StringVar(value=f'{valor_2}')
        txt_var_value_dez_3 = customtkinter.StringVar(value=f'{valor_3}')
        txt_var_value_dez_4 = customtkinter.StringVar(value=f'{valor_4}')

        def period(choice):
            if choice == "Diario":
                txt_var_value_dez_1.set(f'{0}')
                txt_var_value_dez_2.set(f'{0}')
                txt_var_value_dez_3.set(f'{0}')
                txt_var_value_dez_4.set(f'{0}')
            else:
                txt_var_value_dez_1.set(f'{valor_1}')
                txt_var_value_dez_2.set(f'{valor_2:.2f}')
                txt_var_value_dez_3.set(f'{valor_3:.2f}')
                txt_var_value_dez_4.set(f'{valor_4:.2f}')

        menu_period = customtkinter.CTkOptionMenu(tab_moths.tab(
            "DEZ"), values=["Mensal", "Diario"], height=30, fg_color='DARKRED', command=period, corner_radius=50,
            button_color='DARKRED', dropdown_hover_color='DARKRED')
        menu_period.place(x=420, y=5)

        lbl_value_frame_tab_1 = customtkinter.CTkLabel(frame_tab_2, textvariable=txt_var_value_dez_1,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_1.place(x=5, y=5)

        lbl_value_frame_tab_2 = customtkinter.CTkLabel(frame_tab_4, textvariable=txt_var_value_dez_2,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_2.place(x=5, y=5)

        lbl_value_frame_tab_3 = customtkinter.CTkLabel(frame_tab_6, textvariable=txt_var_value_dez_3,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_3.place(x=5, y=5)

        lbl_value_frame_tab_4 = customtkinter.CTkLabel(frame_tab_8, textvariable=txt_var_value_dez_4,
                                                       font=('helvetica', 30), text_color='black')
        lbl_value_frame_tab_4.place(x=5, y=5)

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
    database.create_report_service_order()

    root = customtkinter.CTk()
    AppHome(root)


