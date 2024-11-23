from notificacion import Notificacion


class Correo(Notificacion):
     # nos permite enviar notificaciones al correo del paciente respecto a cambios en su cita o recordatorio de la misma 
    def enviar_notificacion(self, mensaje, correo):
        print(f"Enviando correo a {correo} con mensaje: {mensaje}")
