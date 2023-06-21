# Tumi Palace App

<img src="./src/tumipalace.gif">


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


## Estructura del proyecto
### Backend/
..

### Frontend/


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

## Endpoints
1. Index: `'/'`
   - Sección principal, que muestra los juegos más populares, el call action para que el usuario se registre y demás.
2. Home: `'/home'`
   - Sólo se accede si el usuario está registrado.
   - Muestra los juegos disponibles en conjunto con una barra de navegación personalizada: `navbar_auth.html`.
3. Config: `'/config/'`
   - Sólo se accede si el usuario está registrado.
   - Muestra la configuración disponible para el usuario. De esta forma es posible cambiar nombre, actualizar datos, eliminar usuario, añadir/cambiar foto de perfil, etc.
4. Ruleta: `'/roulette'`
   - Sólo se accede si el usuario está registrado.
   - Juego de la ruleta que maneja POST, GET, de tal forma que muestra el saldo del usuario y lo actualiza dependiendo si el usuario acerta la apuesta o caso contrario lo descuenta.
5. Slots: `'/slots'`
   - Sólo se accede si el usuario está registrado.
   - Juego de tragamonedas, que cuenta con 3 botones interactivos, hace petición POST y GET.
6. Store `'/store'`
   - Sólo se accede si el usuario está registrado.
   - Permite al current_user cargar nuevo dinero a su cuenta actual, y lo actualiza usando la base de datos POSTGRES.
7. Support: `'/support'`
   - Sólo se accede si el usuario está registrado.
   - Muestra una pagina HTML tal que, el usuario cuenta con preguntas frecuentes y número de ayuda.
8. Logout: `'/logout'`
   - Sólo se accede si el usuario está registrado.
   - Se cierra la sesión y se redirige al inicio.
9.  Msg: `'/msg'`
   - Sólo se accede si el usuario está registrado.
   - Muestra mensajes: 404, Advertencia, Error, etc.
10. Login: `'/login'`
    - Formulario que permite al usuario iniciar sesión en su cuenta, se encuentra afectado por parámetros: Verificar nombre, verificar contraseña, etc.
11. Register: `'/register'`
    - Formulario que permite al usuario crear una cuenta, se encuentra afectado por parámetros: verificar edad, verificar nombre, verificar correo, etc.


## 🚀 Desplegar aplicación
<p align="justify">
    Para correr la aplicación <strong>TumiPalaceApp</strong>, es necesario instalar los módulos de python necesarios. Estos están detallados dentro del archivo requirements.txt, que muestra el nombre del módulo, seguido de su versión. Por otro lado, al usar librerías generadoras de código como <strong>uuid</strong>, es necesario colocar comandos en nuestro postgresql. Para ello hemos detallado la siguiente lista de puntos a considerar:
</p>

1. Crear un ambiente virtual para correr nuestro servidor. Podemos realizarlo a partir de instalar el módulo `pip install virtualenv`. Posteriormente lo creamos con `python3 -m venv env`, siendo `env` el nombre designado.
2. Instalar módulos usando la herramienta pip, seguido de la flag `-r` que apunta a nuestro archivo de requerimientos, `pip install -r requirements.txt`.
3. Acceder a postgresql por terminal mediante el comando: `sudo psql -U postgres`.
4. Crear la tabla de base de datos necesaria, en este caso `tumipalace_db`, utilizando el comando `CREATE DATABASE tumipalace_db;`.
5. Conectarnos a nuestra tabla `\c tumipalace_db;`. Recordar que con `\dt` listamos las relaciones.
6. Correr el programa principal `python3 server.py`.

> Si obtenemos un error parecido a `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`, es por que debemos añadir la siguiente extensión dentro de postgresql (fijarnos que estamos conectados a nuestra tabla).
