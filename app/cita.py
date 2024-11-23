class Cita:
    # nos muestra los datos de la cita 
    def __init__(self, id, paciente, medico, fecha_hora):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.motivo_cancelacion = None
        self.calificacion = None
        self.comentario = None
        self.id = id

    def __repr__(self):
        return f"Cita del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

    def agregar_feedback(self, calificacion, comentario):
        # nos permite realizar la calificacion al medico 
        if self.calificacion is not None:
            print("Esta cita ya ha sido calificada.")
            return
        
        self.calificacion = calificacion
        self.comentario = comentario
        self.medico.calificaciones.append(calificacion)
        print ("Claificación y comentario agregados con éxito.")