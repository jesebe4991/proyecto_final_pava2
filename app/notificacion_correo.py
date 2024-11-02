from notificacion import Notificacion


class Correo(Notificacion):
    def enviar_notificacion(self, mensaje, correo):
        print(f"Enviando correo a {correo} con mensaje: {mensaje}")
