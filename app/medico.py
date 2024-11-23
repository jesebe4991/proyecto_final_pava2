from persona import Persona


class persona:
    # nos permite identificar un paciente
    def __init__(self, identificacion, nombre, celular):
        self.identificacion = identificacion
        self.nombre = nombre
        self.celular = celular

class Medico(Persona):
    # nos permite identificar un medico
    def __init__(self, identificacion, nombre, celular, especialidad):
        super().__init__(identificacion, nombre, celular)
        self.especialidad = especialidad
        self.citas = [] # Lista para almacenar citas

    def agregar_cita(self, cita):
        self.citas.append(cita)

    def calificacion_promedio(self):
        # nos permite calificar la atencion recibida en la cita 
        calificaciones = [cita.calificacion for cita in self.citas if cita.calificacion is not  None]
        if not calificaciones:
            return 0
        return sum(calificaciones) / len(calificaciones)
    
    def __repr__(self):
        return f"Dr. {self.nombre}, Especialidad: {self.especialidad}"
