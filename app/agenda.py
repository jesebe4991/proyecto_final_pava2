from cita_urgente import CitaUrgente
from rich.console import Console

console = Console()


class Agenda:
    # permite agendar citas para saber el horario de disponibilidad de los medicos y llevar un orden en las citas
    def __init__(self):
        self.citas = []

    def agendar_cita(self, cita):
        # Verificar si hay conflicto de horarios
        for c in self.citas:
            if c.medico == cita.medico and c.fecha_hora == cita.fecha_hora:
                if isinstance(cita, CitaUrgente) and not isinstance(c, CitaUrgente):
                    # Mover la cita existente si la nueva es urgente
                    nueva_fecha = self.encontrar_siguiente_horario_disponible(
                        c.medico, c.fecha_hora
                    )
                    c.fecha_hora = nueva_fecha
                    console.print(
                        f"[yellow]La cita existente ha sido movida a {nueva_fecha} debido a una urgencia.[/yellow]"
                    )
                else:
                    raise ValueError(
                        "Ya existe una cita en ese horario para este médico."
                    )

        self.citas.append(cita)
        # permite asignar una fecha y hora a cada paciente
        console.print(f"[green]Cita agendada: {cita}[/green]")

    def encontrar_siguiente_horario_disponible(self, medico, fecha_hora):
        # Lógica simple: buscar el siguiente horario disponible en intervalos de 1 hora
        nueva_fecha = fecha_hora
        while True:
            nueva_fecha = nueva_fecha.replace(hour=(nueva_fecha.hour + 1) % 24)
            if not any(
                c.medico == medico and c.fecha_hora == nueva_fecha for c in self.citas
            ):
                return nueva_fecha

    def cancelar_cita(self, cita_id, motivo):
        #permite cancelar la cita 
        for cita in self.citas:
            if cita.id == cita_id:
                self.citas.remove(cita)
                print(f"Cita cancelada. Motivo: {motivo}")
                return True
        return False

    def mover_cita(self, cita_id, nueva_fecha_hora):
        #permite escoger una nueva fecha para la cita sin cancelarla 
        for cita in self.citas:
            if cita.id == cita_id:
                cita.fecha_hora = nueva_fecha_hora
                return True
        return False

    def buscar_citas_paciente(self, paciente):
        # permite ubicar la fecha y hora de una cita de un paciente
        return [cita for cita in self.citas if cita.paciente == paciente]

    def buscar_citas_medico(self, medico):
        # permite ubicar la disponibilidad de cada medico 
        return [cita for cita in self.citas if cita.medico == medico]
