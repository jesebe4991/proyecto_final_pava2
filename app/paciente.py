from persona import Persona


class Paciente(Persona):
    # nos muestra los datos de los pacientes
    def __init__(self, identificacion, nombre, celular, correo):
        super().__init__(identificacion, nombre, celular)
        self.correo = correo
