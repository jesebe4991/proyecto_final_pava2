import csv
import json
import unicodedata
from agenda import Agenda
from paciente import Paciente
from cita import Cita
from cita_urgente import CitaUrgente
from medico import Medico
from datetime import datetime
from rich import print
from rich.console import Console

console = Console()

class Hospital:
    # nos muestra el lugar de la cita 
    def __init__(self):
        self.pacientes = []
        self.medicos = []
        self.citas = []
        self.agenda = Agenda()

    def agregar_paciente(self, paciente):
        # nos muestra la informacion para agendar una cita a un paciente
        self.pacientes.append(paciente)
        print(f"[green]Paciente {paciente.nombre} agregado al hospital.[/green]")

    def agregar_medico(self, medico):
        # nos muestra la informacion para agregar los medicos 
        self.medicos.append(medico)

    def buscar_paciente(self, identificacion):
        # nos permie ubicar los pacienes agregados
        return next(
            (p for p in self.pacientes if p.identificacion == identificacion), None
        )

    def buscar_medico(self, identificacion):
        # nos permite consultar los medicos agregados 
        return next(
            (m for m in self.medicos if m.identificacion == identificacion), None
        )

    def normalizar_texto(self, texto):
        # Eliminar tildes y convertir a minúsculas
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        ).lower()

    def especialidades_disponibles(self):
        # Lista de especialidades únicas en el hospital, normalizadas
        especialidades = set(self.normalizar_texto(m.especialidad) for m in self.medicos)
        return sorted(especialidades)

    def buscar_medicos_por_especialidad(self, especialidad):
        especialidad_normalizada = self.normalizar_texto(especialidad)
        
        # Priorizar médicos cuyas especialidades contienen la palabra buscada
        medicos_filtrados = [
            m for m in self.medicos
            if especialidad_normalizada in self.normalizar_texto(m.especialidad)
        ]
        
        # Ordenar los médicos según la coincidencia: especialidades que empiezan con el término tienen prioridad
        medicos_ordenados = sorted(
            medicos_filtrados,
            key=lambda m: self.normalizar_texto(m.especialidad).startswith(especialidad_normalizada),
            reverse=True
        )
        
        return medicos_ordenados

    def cargar_pacientes_desde_csv(self, archivo):
        try:
            with open(archivo, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    paciente = Paciente(
                        row["identificación"],
                        row["nombre_completo"],
                        row["celular"],
                        row["correo"],
                    )
                    self.agregar_paciente(paciente)
            console.print(
                "[bold][green]Pacientes cargados exitosamente desde el archivo CSV.[/green][/bold]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo CSV.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar pacientes: {str(e)}[/red]")

    def cargar_medicos_desde_json(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as jsonfile:
                medicos_data = json.load(jsonfile)
                for medico_data in medicos_data:
                    # Asegurarse de que todos los campos necesarios estén presentes
                    if all(
                        key in medico_data
                        for key in ["id", "nombre", "celular", "especialidad"]
                    ):
                        medico = Medico(
                            medico_data["id"],
                            medico_data["nombre"],
                            medico_data["celular"],
                            medico_data["especialidad"],
                        )
                        self.agregar_medico(medico)
                    else:
                        console.print(
                            f"[yellow]Advertencia: Datos incompletos para el médico {medico_data.get('nombre', 'desconocido')}[/yellow]"
                        )
            console.print(
                "[bold][green]Médicos cargados exitosamente desde el archivo JSON.[/green][/bold]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo JSON.[/red]")
        except json.JSONDecodeError:
            console.print("[red]Error: El archivo JSON está mal formateado.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar médicos: {str(e)}[/red]")

    def cargar_citas_desde_csv(self, archivo):
        # nos permie consultar las citas 
        try:
            with open(archivo, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    id = row['id']
                    paciente = self.buscar_paciente(row["paciente"])
                    medico = self.buscar_medico(row["medicos"])
                    if paciente and medico:
                        fecha_hora = datetime.strptime(
                            row["fecha_hora"], "%Y-%m-%d %H:%M:%S"
                        )
                        cita = Cita(id, paciente, medico, fecha_hora)
                        self.agenda.agendar_cita(cita)
                    else:
                        if not paciente:
                            console.print(
                                f"[yellow]Advertencia: No se encontró el paciente con ID {row['paciente']}[/yellow]"
                            )
                        if not medico:
                            console.print(
                                f"[yellow]Advertencia: No se encontró el médico con ID {row['medicos']}[/yellow]"
                            )
            console.print(
                "[bold][green]Citas cargadas exitosamente desde el archivo CSV.[/green][/bold]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo CSV de citas.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar citas: {str(e)}[/red]")
            
    def listar_medicos(self, nombre=None):
        # nos muestra los medicos disponibles 
        if nombre:
            return [medico for medico in self.medicos if nombre.lower() in medico.nombre.lower()]
        return self.medicos

    def listar_pacientes(self, nombre=None):
        # nos muestra los datos del paciente que solicita la cita 
        if nombre:
            return [paciente for paciente in self.pacientes if nombre.lower() in paciente.nombre.lower()]
        return self.pacientes

    def agendar_cita_urgente(self, paciente, medico, fecha_hora):
        # nos muestra las fechas mas cercanas disponibles para agendar una cita
        cita_urgente = CitaUrgente(paciente, medico, fecha_hora)
        self.agenda.agendar_cita(cita_urgente)

    def agregar_feedback_cita(self, cita, calificacion, comentario):
        # nos muestra los datos de la cita 
        if cita in self.agenda.citas:
            cita.agregar_feedback(calificacion, comentario)
            console.print(
                f"[green]Feedback agregado a la cita de {cita.paciente.nombre}[/green]"
            )
        else:
            console.print("[red]La cita no existe en la agenda.[/red]")
