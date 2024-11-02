from notificacion import Notificacion


class Whatsapp(Notificacion):
    def enviar_notificacion(self, mensaje, numero):
        print(f"Enviando Whatsapp a {numero} con mensaje: {mensaje}")
