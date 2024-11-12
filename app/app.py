from flask import Flask, render_template, request, redirect, url_for, flash
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from hospital import Hospital
from paciente import Paciente
from medico import Medico
from cita import Cita

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Para manejar los mensajes flash en la aplicación web
hospital = Hospital()

# Cargar datos iniciales cuando se inicia la aplicación
def cargar_datos_iniciales():
    hospital.cargar_pacientes_desde_csv("data/pacientes.csv")
    hospital.cargar_medicos_desde_json("data/medicos.json")
    hospital.cargar_citas_desde_csv("data/citas.csv")

cargar_datos_iniciales()

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Rutas para Pacientes
@app.route("/pacientes")
def mostrar_lista_pacientes():
    return render_template("pacientes.html", pacientes=hospital.pacientes)

@app.route("/pacientes/agregar", methods=["GET", "POST"])
def agregar_paciente():
    if request.method == "POST":
        identificacion = request.form["identificacion"]
        nombre = request.form["nombre"]
        celular = request.form["celular"]
        correo = request.form["correo"]
        paciente = Paciente(identificacion, nombre, celular, correo)
        hospital.agregar_paciente(paciente)
        flash("Paciente agregado exitosamente!")
        return redirect(url_for("mostrar_lista_pacientes"))
    return render_template("agregar_paciente.html")

@app.route("/pacientes/buscar", methods=["GET", "POST"])
def buscar_paciente():
    if request.method == "POST":
        paciente_id = request.form["identificacion"]
        paciente = hospital.buscar_paciente(paciente_id)
        return render_template("buscar_paciente.html", paciente=paciente)
    return render_template("buscar_paciente.html", paciente=None)

# Rutas para Médicos
@app.route("/medicos")
def mostrar_lista_medicos():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    medicos = hospital.medicos[start:end]
    pagination = Pagination(page=page, total=len(hospital.medicos), per_page=per_page, css_framework='bootstrap4')
    return render_template('medicos.html', medicos=medicos, pagination=pagination)

@app.route("/medicos/agregar", methods=["GET", "POST"])
def agregar_medico():
    if request.method == "POST":
        identificacion = request.form["identificacion"]
        nombre = request.form["nombre"]
        celular = request.form["celular"]
        especialidad = request.form["especialidad"]
        medico = Medico(identificacion, nombre, celular, especialidad)
        hospital.agregar_medico(medico)
        flash("Médico agregado exitosamente!")
        return redirect(url_for("mostrar_lista_medicos"))
    return render_template("agregar_medico.html")

@app.route("/medicos/buscar", methods=["GET", "POST"])
def buscar_medico():
    if request.method == "POST":
        medico_id = request.form["identificacion"]
        medico = hospital.buscar_medico(medico_id)
        return render_template("buscar_medico.html", medico=medico)
    return render_template("buscar_medico.html", medico=None)

# Rutas para Citas
@app.route("/citas")
def mostrar_lista_citas():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    citas = hospital.agenda.citas[start:end]
    pagination = Pagination(page=page, total=len(hospital.agenda.citas), per_page=per_page, css_framework='bootstrap4')
    return render_template('citas.html', citas=citas, pagination=pagination)

@app.route("/citas/agendar", methods=["GET", "POST"])
def agendar_cita():
    if request.method == "POST":
        es_urgente = request.form["urgente"] == "s"
        paciente_id = request.form["paciente_id"]
        especialidad = request.form["especialidad"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        paciente = hospital.buscar_paciente(paciente_id)
        
        if paciente:
            medicos_disponibles = hospital.buscar_medicos_por_especialidad(especialidad)
            if medicos_disponibles:
                medico = medicos_disponibles[0]  # Elegimos el primer médico disponible para simplificar
                fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
                cita = Cita(paciente, medico, fecha_hora)
                hospital.agenda.agendar_cita(cita)
                flash("Cita agendada exitosamente!")
                return redirect(url_for("mostrar_lista_citas"))
            else:
                flash("No hay médicos disponibles para esa especialidad")
        else:
            flash("Paciente no encontrado")
    
    return render_template("agendar_cita.html", especialidades=hospital.especialidades_disponibles())

@app.route("/citas/cancelar", methods=["POST"])
def cancelar_cita():
    cita_id = request.form["cita_id"]
    exito = hospital.agenda.cancelar_cita(cita_id)
    if exito:
        flash("Cita cancelada exitosamente.")
    else:
        flash("No se encontró la cita con ese ID.")
    return redirect(url_for("mostrar_lista_citas"))

@app.route("/citas/mover", methods=["POST"])
def mover_cita():
    cita_id = request.form["cita_id"]
    nueva_fecha = request.form["nueva_fecha"]
    nueva_hora = request.form["nueva_hora"]
    nueva_fecha_hora = datetime.strptime(f"{nueva_fecha} {nueva_hora}", "%Y-%m-%d %H:%M")
    exito = hospital.agenda.mover_cita(cita_id, nueva_fecha_hora)
    if exito:
        flash("Cita movida exitosamente.")
    else:
        flash("No se encontró la cita con ese ID.")
    return redirect(url_for("mostrar_lista_citas"))

# Ruta para Consultas y Reportes
@app.route("/reportes")
def mostrar_reportes():
    return render_template("reportes.html")

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
