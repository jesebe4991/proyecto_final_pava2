from notificacion import Notificacion


class Celular(Notificacion):
    # nos permite enviar notificaciones al celular del paciente respecto a cambios en su cita o recordatorio de la misma 
    def enviar_notificacion(self, mensaje, numero):
        print(f"Enviando SMS a {numero} con mensaje: {mensaje}")
