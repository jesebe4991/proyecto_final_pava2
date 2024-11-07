from datetime import datetime
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from hospital import Hospital
from paciente import Paciente
from medico import Medico
from cita import Cita

console = Console()

def cargar_datos_iniciales():
    hospital = Hospital()
    hospital.cargar_pacientes_desde_csv("data/pacientes.csv")
    hospital.cargar_medicos_desde_json("data/medicos.json")
    hospital.cargar_citas_desde_csv("data/citas.csv")
    return hospital

def mostrar_lista_pacientes(hospital):
    table = Table(title="[bold white]LISTA DE PACIENTES[/bold white]")
    table.add_column("ID", style="cyan")
    table.add_column("NOMBRE COMPLETO", style="magenta")
    table.add_column("CELULAR", style="green")
    table.add_column("CORREO ELECTRÓNICO", style="yellow")

    for paciente in hospital.pacientes:
        table.add_row(paciente.identificacion, paciente.nombre, paciente.celular, paciente.correo)

    console.print(table)

def mostrar_lista_medicos(hospital):
    table = Table(title="[bold white]LISTA DE MÉDICOS[/bold white]")
    table.add_column("ID", style="cyan")
    table.add_column("NOMBRE COMPLETO", style="magenta")
    table.add_column("ESPECIALIDAD", style="green")
    table.add_column("CELULAR", style="yellow")

    for medico in hospital.medicos:
        table.add_row(medico.identificacion, medico.nombre, medico.especialidad, medico.celular)

    console.print(table)

def mostrar_lista_citas(hospital):
    table = Table(title="[bold white]LISTA DE CITAS[/bold white]")
    table.add_column("PACIENTE", style="cyan")
    table.add_column("MÉDICO", style="magenta")
    table.add_column("ESPECIALIDAD", style="green")
    table.add_column("FECHA Y HORA", style="yellow")
    table.add_column("URGENCIAS", style="white")

    for cita in hospital.agenda.citas:
        urgente = "NO" if str(type(cita).__name__) == "Cita" else "SÍ"
        table.add_row(cita.paciente.nombre, cita.medico.nombre, cita.medico.especialidad,
                      cita.fecha_hora.strftime("%Y-%m-%d %H:%M"), urgente)

    console.print(table)

def mostrar_menu_principal():
    console.print(
        Panel.fit(
            "[1] Pacientes\n"
            "[2] Médicos\n"
            "[3] Citas\n"
            "[4] Consultas/Reportes\n"
            "[5] Salir",
            title="SISTEMA DE CITAS MÉDICAS - Menú Principal",
            border_style="bold green",
        )
    )

def mostrar_menu_pacientes():
    console.print(
        Panel.fit(
            "[1] Agregar paciente\n"
            "[2] Ver lista de pacientes\n"
            "[3] Buscar paciente\n"
            "[4] Regresar al menú principal",
            title="Menú de Pacientes",
            border_style="bold cyan",
        )
    )

def mostrar_menu_medicos():
    console.print(
        Panel.fit(
            "[1] Agregar médico\n"
            "[2] Ver lista de médicos\n"
            "[3] Buscar médico\n"
            "[4] Regresar al menú principal",
            title="Menú de Médicos",
            border_style="bold cyan",
        )
    )

def mostrar_menu_citas():
    console.print(
        Panel.fit(
            "[1] Agendar cita\n"
            "[2] Cancelar cita\n"
            "[3] Mover cita\n"
            "[4] Agendar cita urgente\n"
            "[5] Ver citas de un paciente\n"
            "[6] Ver citas de un médico\n"
            "[7] Regresar al menú principal",
            title="Menú de Citas",
            border_style="bold cyan",
        )
    )

def mostrar_menu_reportes():
    console.print(
        Panel.fit(
            "[1] Ver calificaciones de médicos\n"
            "[2] Agregar feedback a una cita\n"
            "[3] Regresar al menú principal",
            title="Menú de Consultas y Reportes",
            border_style="bold cyan",
        )
    )

def agregar_paciente(hospital):
    identificacion = Prompt.ask("Ingrese la identificación del paciente")
    nombre = Prompt.ask("Ingrese el nombre del paciente")
    celular = Prompt.ask("Ingrese el celular del paciente")
    correo = Prompt.ask("Ingrese el correo del paciente")
    paciente = Paciente(identificacion, nombre, celular, correo)
    hospital.agregar_paciente(paciente)

def agregar_medico(hospital):
    identificacion = Prompt.ask("Ingrese la identificación del médico")
    nombre = Prompt.ask("Ingrese el nombre del médico")
    celular = Prompt.ask("Ingrese el celular del médico")
    especialidad = Prompt.ask("Ingrese la especialidad del médico")
    medico = Medico(identificacion, nombre, celular, especialidad)
    hospital.agregar_medico(medico)

def buscar_paciente(hospital):
    paciente_id = Prompt.ask("Ingrese la identificación del paciente")
    paciente = hospital.buscar_paciente(paciente_id)
    if paciente:
        table = Table(title="[bold white]PACIENTE ENCONTRADO[/bold white]")
        table.add_column("ID", style="cyan")
        table.add_column("NOMBRE COMPLETO", style="magenta")
        table.add_column("CELULAR", style="green")
        table.add_column("CORREO ELECTRÓNICO", style="yellow")
        table.add_row(paciente.identificacion, paciente.nombre, paciente.celular, paciente.correo)
        console.print(table)
    else:
        print("Paciente no encontrado.")

def buscar_medico(hospital):
    medico_id = Prompt.ask("Ingrese la identificación del médico")
    medico = hospital.buscar_medico(medico_id)
    if medico:
        table = Table(title="[bold white]MÉDICO ENCONTRADO[/bold white]")
        table.add_column("ID", style="cyan")
        table.add_column("NOMBRE COMPLETO", style="magenta")
        table.add_column("ESPECIALIDAD", style="green")
        table.add_column("CELULAR", style="yellow")
        table.add_row(medico.identificacion, medico.nombre, medico.especialidad, medico.celular)
        console.print(table)
    else:
        print("Médico no encontrado.")

def agendar_cita(hospital):
    paciente_id = Prompt.ask("Ingrese la identificación del paciente")
    paciente = hospital.buscar_paciente(paciente_id)

    if paciente:
        especialidad = Prompt.ask("Ingrese la especialidad requerida")
        medicos_disponibles = hospital.buscar_medicos_por_especialidad(especialidad)
        
        if not medicos_disponibles:
            print(f"No se encontró la especialidad '{especialidad}'. Las especialidades disponibles son:")
            for especialidad in hospital.especialidades_disponibles():
                print(f"- {especialidad}")
            especialidad = Prompt.ask("Por favor, ingrese una especialidad de la lista anterior")
            medicos_disponibles = hospital.buscar_medicos_por_especialidad(especialidad)

        if medicos_disponibles:
            print("Médicos disponibles:")
            for i, medico in enumerate(medicos_disponibles, 1):
                print(f"{i}. Dr. {medico.nombre}")
            medico_index = int(Prompt.ask("Seleccione el número del médico")) - 1
            medico = medicos_disponibles[medico_index]
            fecha = Prompt.ask("Ingrese la fecha de la cita (YYYY-MM-DD)")
            hora = Prompt.ask("Ingrese la hora de la cita (HH:MM)")
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            cita = Cita(paciente, medico, fecha_hora)
            hospital.agenda.agendar_cita(cita)
        else:
            print(f"No hay médicos disponibles para la especialidad '{especialidad}'")
    else:
        print("Paciente no encontrado")

def cancelar_cita(hospital):
    cita_id = Prompt.ask("Ingrese el ID de la cita a cancelar")
    exito = hospital.agenda.cancelar_cita(cita_id)
    if exito:
        print("Cita cancelada exitosamente.")
    else:
        print("No se encontró la cita con ese ID.")

def mover_cita(hospital):
    cita_id = Prompt.ask("Ingrese el ID de la cita a mover")
    nueva_fecha = Prompt.ask("Ingrese la nueva fecha de la cita (YYYY-MM-DD)")
    nueva_hora = Prompt.ask("Ingrese la nueva hora de la cita (HH:MM)")
    nueva_fecha_hora = datetime.strptime(f"{nueva_fecha} {nueva_hora}", "%Y-%m-%d %H:%M")
    exito = hospital.agenda.mover_cita(cita_id, nueva_fecha_hora)
    if exito:
        print("Cita movida exitosamente.")
    else:
        print("No se encontró la cita con ese ID.")

def ver_citas_paciente(hospital):
    paciente_id = Prompt.ask("Ingrese la identificación del paciente")
    citas = hospital.agenda.obtener_citas_por_paciente(paciente_id)
    if citas:
        table = Table(title=f"[bold white]CITAS PARA EL PACIENTE {paciente_id}[/bold white]")
        table.add_column("ID CITA", style="cyan")
        table.add_column("FECHA Y HORA", style="yellow")
        table.add_column("MÉDICO", style="magenta")
        table.add_column("ESPECIALIDAD", style="green")
        for cita in citas:
            table.add_row(cita.id, cita.fecha_hora.strftime("%Y-%m-%d %H:%M"), cita.medico.nombre, cita.medico.especialidad)
        console.print(table)
    else:
        print("No se encontraron citas para ese paciente.")

def ver_citas_medico(hospital):
    medico_id = Prompt.ask("Ingrese la identificación del médico")
    citas = hospital.agenda.obtener_citas_por_medico(medico_id)
    if citas:
        table = Table(title=f"[bold white]CITAS PARA EL MÉDICO {medico_id}[/bold white]")
        table.add_column("ID CITA", style="cyan")
        table.add_column("FECHA Y HORA", style="yellow")
        table.add_column("PACIENTE", style="magenta")
        table.add_column("ESPECIALIDAD", style="green")
        for cita in citas:
            table.add_row(cita.id, cita.fecha_hora.strftime("%Y-%m-%d %H:%M"), cita.paciente.nombre, cita.medico.especialidad)
        console.print(table)
    else:
        print("No se encontraron citas para ese médico.")

def main():
    hospital = cargar_datos_iniciales()

    while True:
        mostrar_menu_principal()
        opcion_principal = Prompt.ask("Seleccione una categoría", choices=["1", "2", "3", "4", "5"])

        if opcion_principal == "1":  
            while True:
                mostrar_menu_pacientes()
                opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
                if opcion == "1":
                    agregar_paciente(hospital)
                elif opcion == "2":
                    mostrar_lista_pacientes(hospital)
                elif opcion == "3":
                    buscar_paciente(hospital)
                elif opcion == "4":
                    break

        elif opcion_principal == "2":  
            while True:
                mostrar_menu_medicos()
                opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
                if opcion == "1":
                    agregar_medico(hospital)
                elif opcion == "2":
                    mostrar_lista_medicos(hospital)
                elif opcion == "3":
                    buscar_medico(hospital)
                elif opcion == "4":
                    break

        elif opcion_principal == "3":  
            while True:
                mostrar_menu_citas()
                opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7"])
                if opcion == "1":
                    agendar_cita(hospital)
                elif opcion == "2":
                    cancelar_cita(hospital)
                elif opcion == "3":
                    mover_cita(hospital)
                elif opcion == "4":
                    print("Función para agendar cita urgente (a implementar)")
                elif opcion == "5":
                    ver_citas_paciente(hospital)
                elif opcion == "6":
                    ver_citas_medico(hospital)
                elif opcion == "7":
                    break

        elif opcion_principal == "4":  
            while True:
                mostrar_menu_reportes()
                opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3"])
                if opcion == "1":
                    print("Función para ver calificaciones de médicos")
                elif opcion == "2":
                    print("Función para agregar feedback a una cita")
                elif opcion == "3":
                    break

        elif opcion_principal == "5":
            print("Saliendo del sistema. Hasta luego!")
            break

if __name__ == "__main__":
    main()
