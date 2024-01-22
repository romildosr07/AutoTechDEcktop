import customtkinter as ct

from AutoTechDecktop.templates.service_order import ServiceOrderTemplate


def open_service_order():
    window = ServiceOrderTemplate(ct)
    window.service_order_template()


