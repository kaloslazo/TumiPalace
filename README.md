# Tumi Palace App

<img src="./src/tumipalace.gif">


## 🫂 Integrantes
- Kalos Lazo Mera *202210184*
- Giancarlo Ferreyra Uribe *202210132*
- Matias Castillo Quincho *202210081*
- Marcelo Azalde Lazo *202210034*


## 📝 Descripción
<p align="justify">
Aplicación web que permite a los usuarios realizar apuestas de distinta índole, su principal atractivo es el Coricancha (Tragamonedas), la web permite a los usuarios mantener sus registros, jugadas, transacciones y muchas mas opciones almacenadas desde cualquier dispositivo tanto en escritorio como en moviles y desde la simple comodidad de su casa.
</p>


## 📌 Objetivos principales
### Misión
<p align="justify">
    Ofrecer a los clientes una experiencia de entretenimiento segura y de alta calidad. Nos esforzamos por ofrecer una amplia gama de emocionantes juegos y servicios. Al mismo tiempo que garantizamos altos estándares de seguridad web y protegemos la seguridad del usuarios con algoritmos encriptación.
</p>

### Visión
<p align="justify">
    Ser reconocidos como el casino virtual lider en el mercado peruano ofreciendo una experiencia de juego única y segura. Nuestro objetivo es favorecer al usuario con ofertas y bonificaciones atractivas y una atención excepcional. Nos esforzamos por estar a la vanguardia en tecnología e innovación de la industria de casinos en línea.
</p>


## 📚 Librerías
- Flask
- UUID
- SQLAlchemy
- WTForms

## 📄 Información acerca de las herramientas utilizadas
- Flask: Framework web ligero y flexible para Python, nos permite construir aplicaciones web de manera sencilla. La utilizamos para manejar las rutas y las solicitudes HTTP en el casino web.
- Flask-Bcrypt: Extensión de Flask, que la utilizamos para que nos facilite el uso de Bcrypt para el hash y verificación de contraseñas en una aplicación Flask.
- Flask-Login: Extensión de Flask que simplifica la gestión de autenticación de usuarios, nos ayuda en las funciones de inicio de sesión, cierre de sesión, recordar contraseñas y proteger rutas específicas de acceso no autorizado.
- Flask-Migrate: Extensión de Flask que facilita la migración de la base de datos utilizando Alembic. nos ayuda a simplificar el proceso de realizar y aplicar cambios en la estructura de la base de datos a medida que evoluciona el programa del casino virtual.
- Flask-SQLAlchemy: Extensión de Flask que proporciona integración con SQLAlchemy, que nos ayuda bastante a interactuar con la base de datos de manera más sencilla y directa.
- UUID: Es una librería que nos ayuda a generar identificadores únicos, es útil dentro del programa porque lo usamos para asignar identificadores únicos a los usuarios, juegos, transacciones, etc.
- SQLAlchemy: Es una librería ORM para python, la utilizamos para interactuar con las bases de datos relacionales de una manera sencilla y orientada a objetos.
- WTForms: Es una librería de Python que facilita la validación y el manejo de formularios, lo utilizamos dentro del programa para crear formularios de registro, inicio de sesión, entre otras.
- Alembic: Herramienta de migración de bases de datos para SQLAlchemy, lo utilizamos para realizar actualizaciones y revisiones de la base de datos de manera controlada y actualizada.
- Bcrypt: Algoritmo de hashing utilizado para el almacenamiento seguro de contraseñas; nos ayuda a generar y verificar hashes de contraseñas, por lo que nos ayuda a aumentar la seguridad y dificulta el acceso no autorizado a las cuentas de los usuarios.
- Blinker: Es una librería de señales y eventos que nos ayuda a facilitar la comunicación entre diferentes componentes de nuestra web, la utilizamos dentro del casino web para notificar eventos como la finalización de un juego, actualización de saldo, etc.
- Click: Es un paquete para crear interfaces de línea de comandos(CLI) de manera sencilla, lo utilizamos para construir herramientas de administración o scripts para automatizar las tareas relacionadascon la gestión del casino web.

## 🚀 Desplegar aplicación
<p align="justify">
    Para correr la aplicación <strong>TumiPalaceApp</strong>, es necesario instalar los módulos de python necesarios. Estos están detallados dentro del archivo requirements.txt, que muestra el nombre del módulo, seguido de su versión. Por otro lado, al usar librerías generadoras de código como <strong>uuid</strong>, es necesario colocar comandos en nuestro postgresql. Para ello hemos detallado la siguiente lista de puntos a considerar:
</p>

1. Crear un ambiente virtual para correr nuestro servidor. Podemos realizarlo a partir de instalar el módulo `pip install virtualenv`. Posteriormente lo creamos con `python3 -m venv env`, siendo `env` el nombre designado.
2. Instalar módulos usando la herramienta pip, seguido de la flag `-r` que apunta a nuestro archivo de requerimientos, `pip install -r requirements.txt`.
3. Acceder a postgresql por terminal mediante el comando: `sudo psql -U postgres`.
4. Crear la tabla de base de datos necesaria, en este caso `tumipalace_db`, utilizando el comando `CREATE DATABASE tumipalace_db;`.
5. Conectarnos a nuestra tabla `\c tumipalace_db;`. Recordar que con `\dt` listamos las relaciones.
6. Correr el programa principal `python3 main.py`.

> Si obtenemos un error parecido a `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`, es por que debemos añadir la siguiente extensión dentro de postgresql (fijarnos que estamos conectados a nuestra tabla): `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`.
