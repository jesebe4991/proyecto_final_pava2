from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de las clases Hospital y Agenda sin rich
class Hospital:
    def __init__(self, nombre):
        self.nombre = nombre

class Agenda:
    def __init__(self):
        self.citas = []

    def agendar_cita(self, cita, es_urgente):
        self.citas.append({'cita': cita, 'urgente': es_urgente})

hospital = Hospital("Hospital General")
agenda = Agenda()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        cita = request.form['cita']
        es_urgente = 'urgente' in request.form
        agenda.agendar_cita(cita, es_urgente)
        return redirect(url_for('index'))
    return render_template('agendar.html')

if __name__ == '__main__':
    app.run(debug=True)