from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from hospital import Hospital
from paciente import Paciente
from medico import Medico
from cita import Cita
import csv
from cita_urgente import CitaUrgente
from io import StringIO

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
@app.route('/pacientes')
def mostrar_lista_pacientes():
    buscar_id = request.args.get('buscar_id', '')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    if buscar_id:
        # busqueda por identificacion del paciente
        pacientes_filtrados = [p for p in hospital.pacientes if buscar_id in p.identificacion]
        total = len(pacientes_filtrados)
        pacientes = pacientes_filtrados[start:end]
        return jsonify([{'identificacion': p.identificacion, 'nombre': p.nombre, 'celular': p.celular, 'correo': p.correo} for p in pacientes])
    else:
        total = len(hospital.pacientes)
        pacientes = hospital.pacientes[start:end]

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    return render_template('pacientes.html', pacientes=pacientes, pagination=pagination)

@app.route("/pacientes/agregar", methods=["GET", "POST"])
def agregar_paciente():
    # datos para crear el paciente en la agenda
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
    # permite uicar facilmente el paciente
    if request.method == "POST":
        paciente_id = request.form["identificacion"]
        paciente = hospital.buscar_paciente(paciente_id)
        return render_template("buscar_paciente.html", paciente=paciente)
    return render_template("buscar_paciente.html", paciente=None)

# Rutas para Médicos
@app.route('/medicos')
def mostrar_lista_medicos():
    buscar_id = request.args.get('buscar_id', '')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    if buscar_id:
        # nos muestra el medico en especifico que se necesita
        medicos_filtrados = [m for m in hospital.medicos if buscar_id in m.identificacion]
        total = len(medicos_filtrados)
        medicos = medicos_filtrados[start:end]
        return jsonify([{'identificacion': m.identificacion, 'nombre': m.nombre, 'especialidad': m.especialidad, 'celular': m.celular} for m in medicos])
    else:
        total = len(hospital.medicos)
        medicos = hospital.medicos[start:end]

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    return render_template('medicos.html', medicos=medicos, pagination=pagination)

@app.route("/medicos/agregar", methods=["GET", "POST"])
def agregar_medico():
    # nos permite crear nuevos medicos en la base de datos 
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
    # rutas para ubicar medicos 
    if request.method == "POST":
        medico_id = request.form["identificacion"]
        medico = hospital.buscar_medico(medico_id)
        return render_template("buscar_medico.html", medico=medico)
    return render_template("buscar_medico.html", medico=None)

# Rutas para Citas
@app.route('/citas')
def mostrar_lista_citas():
    buscar_fecha = request.args.get('buscar_fecha', '')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    if buscar_fecha:
        # permite filtrar las fechas que el paciente necesita o que el medico ordena para la cita
        citas_filtradas = [c for c in hospital.citas if buscar_fecha in c.fecha_hora.strftime('%Y-%m-%d')]
        total = len(citas_filtradas)
        citas = citas_filtradas[start:end]
        return jsonify([{'id': c.id, 'fecha': c.fecha_hora.strftime('%Y-%m-%d'), 'hora': c.fecha_hora.strftime('%H:%M'), 'paciente': c.paciente.nombre, 'medico': c.medico.nombre} for c in citas])
    else:
        total = len(hospital.agenda.citas)
        citas = hospital.agenda.citas[start:end]

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    return render_template('citas.html', citas=citas, pagination=pagination)

@app.route("/citas/agendar",  methods=["GET", "POST"])
def agendar_cita():
    # ruta para agendar las citas 
    if request.method == "POST":
        es_urgente = 'urgente' in request.form 
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
                cita = Cita(len(hospital.citas) + 1, paciente, medico, fecha_hora)
                if es_urgente:
                    cita = CitaUrgente(len(hospital.citas) + 1, paciente, medico, fecha_hora)
                hospital.agenda.agendar_cita(cita)
                flash("Cita agendada exitosamente!")
                return redirect(url_for("mostrar_lista_citas"))
            else:
                flash("No hay médicos disponibles para la especialidad seleccionada.")
        else:
            flash("Paciente no encontrado.")
    
    nombre_paciente = request.args.get('nombre_paciente', '')
    nombre_medico = request.args.get('nombre_medico', '')
    pacientes = hospital.listar_pacientes(nombre_paciente)
    medicos = hospital.listar_medicos(nombre_medico)
    return render_template('agendar_cita.html', pacientes=pacientes, medicos=medicos, nombre_paciente=nombre_paciente, nombre_medico=nombre_medico, especialidades=hospital.especialidades_disponibles())

@app.route("/citas/cancelar", methods=["POST"])
def cancelar_cita():
    # rutas para cancelar citas 
    cita_id = request.form["cita_id"]
    motivo = request.form["motivo"]
    exito = hospital.agenda.cancelar_cita(cita_id, motivo)
    if exito:
        flash("Cita cancelada exitosamente.")
    else:
        flash("No se encontró la cita con ese ID.")
    return redirect(url_for("mostrar_lista_citas"))

@app.route("/citas/mover", methods=["POST"])
def mover_cita():
    # rutas para mover las citas 
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
@app.route('/reportes')
def mostrar_reportes():
    return render_template('reportes.html')

@app.route('/reportes/pacientes')
def reporte_pacientes():
    # Lógica para generar el reporte de pacientes
    pacientes = hospital.pacientes
    return render_template('reporte_pacientes.html', pacientes=pacientes)

@app.route('/reportes/medicos')
def reporte_medicos():
    # Lógica para generar el reporte de médicos
    medicos = hospital.medicos
    return render_template('reporte_medicos.html', medicos=medicos)

@app.route('/reportes/citas')
def reporte_citas():
    # Lógica para generar el reporte de citas
    citas = hospital.agenda.citas
    return render_template('reporte_citas.html', citas=citas)

@app.route('/reportes/citas/descargar')
def descargar_reporte_citas():
    citas = hospital.agenda.citas
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Fecha', 'Hora', 'Paciente', 'Médico'])
    for cita in citas:
        cw.writerow([cita.fecha_hora.strftime('%Y-%m-%d'), cita.fecha_hora.strftime('%H:%M'), cita.paciente.nombre, cita.medico.nombre])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=reporte_citas.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/reportes/pacientes/descargar')
def descargar_reporte_pacientes():
    pacientes = hospital.pacientes
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Nombre Completo', 'Celular', 'Correo Electrónico'])
    for paciente in pacientes:
        cw.writerow([paciente.identificacion, paciente.nombre, paciente.celular, paciente.correo])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=reporte_pacientes.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/reportes/medicos/descargar')
def descargar_reporte_medicos():
    medicos = hospital.medicos
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Nombre Completo', 'Especialidad', 'Celular'])
    for medico in medicos:
        cw.writerow([medico.identificacion, medico.nombre, medico.especialidad, medico.celular])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=reporte_medicos.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
