from notificacion import Notificacion


class Whatsapp(Notificacion):
     # nos permite enviar notificaciones al whatsapp del paciente respecto a cambios en su cita o recordatorio de la misma 
    def enviar_notificacion(self, mensaje, numero):
        print(f"Enviando Whatsapp a {numero} con mensaje: {mensaje}")
