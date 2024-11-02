# SISTEMA DE GESTIÓN DE CITAS MÉDICAS

Este proyecto es un sistema de gestión de citas médicas diseñado para permitir a los pacientes solicitar citas, a los médicos gestionar sus agendas y generar reportes detallados. El sistema incluye funciones para notificaciones, verificación de disponibilidad y cancelación de citas, además de permitir agendar citas para el área de urgencias. Está basado en los requerimientos obtenidos del cliente.

## Funcionalidades Principales

- **Gestión de Agenda**: Los médicos tienen una agenda donde se almacenan las citas pendientes y realizadas.
- **Notificaciones**: Se envían notificaciones a los pacientes para recordar sus citas a través de llamadas, mensajes de texto o correo electrónico.
- **Cancelación y Reprogramación de Citas**: Los pacientes pueden cancelar y reprogramar citas según la disponibilidad de los médicos.
- **Gestión eficaz de los pacientes del hospital**: Se pueden agregar pacientes de manera libre al hospital.
- **Agendamiento de citas**: Para todos y cada uno de los pacientes existentes en el hospital, se ofrece la posibilidad de agendar citas de la especialidad requerida con el médico de su preferencia.
- **Información de las citas**: Los pacientes pueden buscar las citas que tienen agendadas en el hospital simplemente digitando su número de cédula. El sistema le mostrará una lista de todas las citas que tiene agendadas, especificando el doctor que le va a atender, la fecha y la hora.
- **Cancelación de citas**: Los pacientes tienen la posibilidad las citas que tengan agendadas. Simplemente digitando su número de cédula el sistema le arrojará una lista de citas, donde cancelar una de estas será tan sencillo como digitar el número que tiene la cita que desea cancelar.
- **Reprogramación de citas**: Cada paciente puede elegir qué cita desea reagendar y para qué fecha y horario.
- **Agenda para los médicos**: Los médicos también pueden verificar fácilmente su agenda de citas programadas, esto simplemente con su número de cédula.
- **Urgencias**: ¿Estás presentando una urgencia? No te preocupes, puedes agendar una cita con dicha área fácilmente.
- **Calificación de las citas**: Cada paciente tiene la oportunidad de calificar la atención recibida en alguna cita. Para esto, es tan sencillo como digitar su número de cédula y seleccionar la cita que desea puntuar, para luego calificarla en una escala de 0 a 5.
- **Calificación promedio de los médicos**: Todos los usuarios pueden ver cuáles son los médicos que tienen mejor promedio de calificación por parte de los pacientes.

## Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python ./app/main.py
```
