from cita import Cita


class CitaUrgente(Cita):
    # nos muestra las citas prioritarias 
    def __init__(self, paciente, medico, fecha_hora):
        super().__init__(paciente, medico, fecha_hora)

    def __repr__(self):
        return f"Cita URGENTE del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
