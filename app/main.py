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

    # Cargar pacientes iniciales
    hospital.cargar_pacientes_desde_csv("data/pacientes.csv")

    # Cargar médicos iniciales
    hospital.cargar_medicos_desde_json("data/medicos.json")

    # Cargar citas iniciales
    hospital.cargar_citas_desde_csv("data/citas.csv")

    return hospital


def mostrar_lista_pacientes(hospital):
    table = Table(title="[bold white]LISTA DE PACIENTES[/bold white]")
    table.add_column("ID", style="cyan")
    table.add_column("NOMBRE COMPLETO", style="magenta")
    table.add_column("CELULAR", style="green")
    table.add_column("CORREO ELECTRÓNICO", style="yellow")

    for paciente in hospital.pacientes:
        table.add_row(
            paciente.identificacion, paciente.nombre, paciente.celular, paciente.correo
        )

    console.print(table)


def mostrar_lista_medicos(hospital):
    table = Table(title="[bold white]LISTA DE MÉDICOS[/bold white]")
    table.add_column("ID", style="cyan")
    table.add_column("NOMBRE COMPLETO", style="magenta")
    table.add_column("ESPECIALIDAD", style="green")
    table.add_column("CELULAR", style="yellow")

    for medico in hospital.medicos:
        table.add_row(
            medico.identificacion, medico.nombre, medico.especialidad, medico.celular
        )

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

        table.add_row(
            cita.paciente.nombre,
            cita.medico.nombre,
            cita.medico.especialidad,
            cita.fecha_hora.strftime("%Y-%m-%d %H:%M"),
            urgente,
        )

    console.print(table)


def mostrar_menu():
    console.print(
        Panel.fit(
            "1. Agregar paciente.\n"
            "2. Agregar médico.\n"
            "3. Agendar cita.\n"
            "4. Cancelar cita.\n"
            "5. Mover cita.\n"
            "6. Ver citas de un paciente.\n"
            "7. Ver citas de un médico.\n"
            "8. Ver lista de pacientes.\n"
            "9. Ver lista de médicos.\n"
            "10. Buscar un paciente.\n"
            "11. Buscar un médico.\n"
            "12. Agendar cita urgente.\n"
            "13. Agregar feedback a una cita.\n"
            "14. Ver calificaciones de médicos.\n"
            "15. Salir",
            title="SISTEMA DE CITAS MÉDICAS",
            border_style="bold green",
        )
    )


def main():
    hospital = cargar_datos_iniciales()

    while True:
        mostrar_menu()
        opcion = Prompt.ask(
            "Seleccione una opción",
            choices=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ],
        )

        if opcion == "1":
            identificacion = Prompt.ask("Ingrese la identificación del paciente")
            nombre = Prompt.ask("Ingrese el nombre del paciente")
            celular = Prompt.ask("Ingrese el celular del paciente")
            correo = Prompt.ask("Ingrese el correo del paciente")
            paciente = Paciente(identificacion, nombre, celular, correo)
            hospital.agregar_paciente(paciente)

        elif opcion == "2":
            identificacion = Prompt.ask("Ingrese la identificación del médico")
            nombre = Prompt.ask("Ingrese el nombre del médico")
            celular = Prompt.ask("Ingrese el celular del médico")
            especialidad = Prompt.ask("Ingrese la especialidad del médico")
            medico = Medico(identificacion, nombre, celular, especialidad)
            hospital.agregar_medico(medico)

        elif opcion == "3":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                especialidad = Prompt.ask("Ingrese la especialidad requerida")
                medicos_disponibles = hospital.buscar_medicos_por_especialidad(
                    especialidad
                )
                if medicos_disponibles:
                    print("Médicos disponibles:")
                    for i, medico in enumerate(medicos_disponibles, 1):
                        print(f"{i}. Dr. {medico.nombre}")
                    medico_index = (
                        int(Prompt.ask("Seleccione el número del médico")) - 1
                    )
                    medico = medicos_disponibles[medico_index]
                    fecha = Prompt.ask("Ingrese la fecha de la cita (YYYY-MM-DD)")
                    hora = Prompt.ask("Ingrese la hora de la cita (HH:MM)")
                    fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
                    cita = Cita(paciente, medico, fecha_hora)
                    hospital.agenda.agendar_cita(cita)
                else:
                    print(
                        f"No hay médicos disponibles para la especialidad {especialidad}"
                    )
            else:
                print("Paciente no encontrado")

        elif opcion == "4":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for i, cita in enumerate(citas_paciente, 1):
                        print(f"{i}. {cita}")
                    cita_index = (
                        int(Prompt.ask("Seleccione el número de la cita a cancelar"))
                        - 1
                    )
                    cita = citas_paciente[cita_index]
                    motivo = Prompt.ask("Ingrese el motivo de la cancelación")
                    hospital.agenda.cancelar_cita(cita, motivo)
                else:
                    print("El paciente no tiene citas programadas")
            else:
                print("Paciente no encontrado")

        elif opcion == "5":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for i, cita in enumerate(citas_paciente, 1):
                        print(f"{i}. {cita}")
                    cita_index = (
                        int(Prompt.ask("Seleccione el número de la cita a mover")) - 1
                    )
                    cita = citas_paciente[cita_index]
                    nueva_fecha = Prompt.ask(
                        "Ingrese la nueva fecha de la cita (YYYY-MM-DD)"
                    )
                    nueva_hora = Prompt.ask("Ingrese la nueva hora de la cita (HH:MM)")
                    nueva_fecha_hora = datetime.strptime(
                        f"{nueva_fecha} {nueva_hora}", "%Y-%m-%d %H:%M"
                    )
                    hospital.agenda.mover_cita(cita, nueva_fecha_hora)
                else:
                    print("El paciente no tiene citas programadas")
            else:
                print("Paciente no encontrado")

        elif opcion == "6":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for cita in citas_paciente:
                        print(cita)
                else:
                    print("El paciente no tiene citas programadas")
            else:
                print("Paciente no encontrado.")

        elif opcion == "7":
            medico_id = Prompt.ask("Ingrese la identificación del médico")
            medico = hospital.buscar_medico(medico_id)
            if medico:
                citas_medico = hospital.agenda.buscar_citas_medico(medico)
                if citas_medico:
                    print("Citas del médico:")
                    for cita in citas_medico:
                        print(cita)
                else:
                    print("El médico no tiene citas programadas")
            else:
                print("Médico no encontrado")

        elif opcion == "8":
            mostrar_lista_pacientes(hospital)

        elif opcion == "9":
            mostrar_lista_medicos(hospital)

        elif opcion == "10":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                table = Table(
                    title="[bold white]PACIENTE ENCONTRADO EN EL HOSPITAL[/bold white]"
                )
                table.add_column("ID", style="cyan")
                table.add_column("NOMBRE COMPLETO", style="magenta")
                table.add_column("CELULAR", style="green")
                table.add_column("CORREO ELECTRÓNICO", style="yellow")

                table.add_row(
                    paciente.identificacion,
                    paciente.nombre,
                    paciente.celular,
                    paciente.correo,
                )

                console.print(table)
            else:
                print("Paciente no encontrado.")

        elif opcion == "11":
            medico_id = Prompt.ask("Ingrese la identificación del médico")
            medico = hospital.buscar_medico(medico_id)
            if medico:
                table = Table(
                    title="[bold white]MÉDICO ENCONTRADO EN EL HOSPITAL[/bold white]"
                )
                table.add_column("ID", style="cyan")
                table.add_column("NOMBRE COMPLETO", style="magenta")
                table.add_column("ESPECIALIDAD", style="green")
                table.add_column("CELULAR", style="yellow")

                table.add_row(
                    medico.identificacion,
                    medico.nombre,
                    medico.especialidad,
                    medico.celular,
                )

                console.print(table)
            else:
                print("Médico no encontrado.")

        elif opcion == "12":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                especialidad = Prompt.ask(
                    "Ingrese la especialidad requerida para la urgencia"
                )
                medicos_disponibles = hospital.buscar_medicos_por_especialidad(
                    especialidad
                )
                if medicos_disponibles:
                    print("Médicos disponibles:")
                    for i, medico in enumerate(medicos_disponibles, 1):
                        print(f"{i}. Dr. {medico.nombre}")
                    medico_index = (
                        int(Prompt.ask("Seleccione el número del médico")) - 1
                    )
                    medico = medicos_disponibles[medico_index]
                    fecha = Prompt.ask(
                        "Ingrese la fecha de la cita urgente (YYYY-MM-DD)"
                    )
                    hora = Prompt.ask("Ingrese la hora de la cita urgente (HH:MM)")
                    fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
                    try:
                        hospital.agendar_cita_urgente(paciente, medico, fecha_hora)
                    except ValueError as e:
                        console.print(
                            f"[red]Error al agendar cita urgente: {str(e)}[/red]"
                        )
                else:
                    print(
                        f"No hay médicos disponibles para la especialidad {especialidad}"
                    )
            else:
                print("Paciente no encontrado")

        elif opcion == "13":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for i, cita in enumerate(citas_paciente, 1):
                        print(f"{i}. {cita}")
                    cita_index = (
                        int(
                            Prompt.ask(
                                "Seleccione el número de la cita para agregar feedback"
                            )
                        )
                        - 1
                    )
                    cita = citas_paciente[cita_index]
                    calificacion = float(Prompt.ask("Ingrese la calificación (0-5)"))
                    comentario = Prompt.ask("Ingrese un comentario sobre la cita")
                    hospital.agregar_feedback_cita(cita, calificacion, comentario)
                else:
                    print("El paciente no tiene citas para calificar")
            else:
                print("Paciente no encontrado")

        elif opcion == "14":
            table = Table(
                title="[bold white]CALIFICACIÓN PROMEDIO POR MÉDICO[/bold white]"
            )
            table.add_column("Nombre del Médico", style="cyan")
            table.add_column("Especialidad", style="magenta")
            table.add_column("Calificación Promedio", style="yellow")

            for medico in hospital.medicos:
                calificacion_promedio = round(medico.calificacion_promedio(), 2)
                table.add_row(
                    medico.nombre, medico.especialidad, str(calificacion_promedio)
                )

            console.print(table)

        elif opcion == "15":
            print("Gracias por usar el Sistema de Citas Médicas. ¡Hasta luego!")
            break

        console.print("\nPresione Enter para continuar...")
        input()


if __name__ == "__main__":
    main()
