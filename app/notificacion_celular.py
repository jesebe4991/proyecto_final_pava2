from notificacion import Notificacion


class Celular(Notificacion):
    def enviar_notificacion(self, mensaje, numero):
        print(f"Enviando SMS a {numero} con mensaje: {mensaje}")
