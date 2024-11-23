# Issues

- un super-menú con todas las opciones es poco práctico, tener un menú donde tengas citas, consultas/reportes, pacientes, médicos (por ejemplo) funciona mejor.
- al agendar una cita, debes digitar el nombre exacto de la especialidad, podría buscar la especialidad más parecida ignorando mayúsculas/minúsculas/tildes, o listar las especialidades disponibles (por eso decía "selecciona").
- no deberías tener opciones separadas para agendar citas y citas urgentes, al agendar cita (opción 3) solo era necesario preguntar si la cita es urgente o no.
- del mismo modo, una sub-clase para citas urgentes no es necesaria dado, si usas un atributo "urgente: bool" puede manejarlas ambas, y no necesitas validar con isinstance() en la creación.
- más importante que eso, es que en ambos casos (3, 12) permite agendar citar para fechas del pasado (1999-01-01) y no está validando que las citas van en intervalos de 20 minutos (0, 20, 40).
- como tienes una única agenda debes hacer muchas validaciones para agregar una cita, si tienes una agenda por médico y es diccionario, eso sería más sencillo.
- entiendo lo que quieres hacer con la calificación, pero debería estar solo asociada a la cita y no al médico (otra razón para que la agenda sea del médico), pero no se válida que la cita ya fuera calificada y permite calificar varias veces la misma cita.
- el código aunque en general es fácil de leer, carece de documentación y comentarios.
- las clases hospital y agenda utilizan "rich", eso hace más difícil usar el mismo código en una interfaz web o de otro tipo