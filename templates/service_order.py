import os

from AutoTechDecktop.templates.home import HomeTemplate



class ServiceOrderTemplate:
    def __init__(self, ct):
        self.window = ct.CTk()
        self.ct = ct
        self.base_dir = os.path.dirname(__file__)

    def back_to_home(self):
        window = HomeTemplate(self.ct)
        window.home_template()

    def service_order_template(self):
        self.window.geometry('1200x720')
        self.window.title('Ordem de Serviço')
        icon_path = os.path.join(self.base_dir, 'img', 'icon.ico')
        self.window.iconbitmap(icon_path)

        btn_back_to_home = self.ct.CTkButton(
            self.window, text='voltar', width=165, font=('helvetica', 20), fg_color='DARKRED', command=self.back_to_home)
        btn_back_to_home.place(x=20, y=250)

        return self.window.mainloop()
