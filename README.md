<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>Simulación de Concurrencia con Niveles de Aislamiento en PostgreSQL</h1>

  <p>Este proyecto simula múltiples usuarios intentando reservar la misma localidad en una base de datos PostgreSQL, usando diferentes niveles de aislamiento de transacciones: <strong>READ COMMITTED</strong>, <strong>REPEATABLE READ</strong> y <strong>SERIALIZABLE</strong>.</p>

  <h2>Requisitos</h2>
  <ul>
    <li>Python 3.7 o superior</li>
    <li>PostgreSQL</li>
    <li>Paquetes de Python:
      <ul>
        <li>psycopg2</li>
        <li>python-dotenv</li>
      </ul>
    </li>
  </ul>

  <h2>Instalación</h2>
  <ol>
    <li>Clona este repositorio:
      <pre><code>git clone https://github.com/diegoanro22/Proyect2_BD.git</code></pre>
    </li>
    <li>Ingresa al directorio del proyecto:
      <pre><code>cd Proyect2_BD</code></pre>
    </li>
    <li>Instala las dependencias necesarias:
      <pre><code>pip install psycopg2</code></pre>
      <pre><code>pip install dotenv</code></pre>
    </li>
    <li>Copia el archivo <code>.env.example</code> y configura tus credenciales:
      <pre><code>cp .env.example .env</code></pre>
      Edita el archivo <code>.env</code> y coloca tus datos de conexión a PostgreSQL:
      <pre><code>
DB_NAME=Proyect2_Isolation
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
      </code></pre>
    </li>
  </ol>

  <h2>Inicialización de la Base de Datos</h2>
  <p>Antes de ejecutar la simulación, crea la base de datos y las tablas con los siguientes archivos SQL que se incluyen en el repositorio:</p>
  <ol>
    <li><code>ddl.sql</code>: crea las tablas necesarias.</li>
    <li><code>data.sql</code>: inserta datos iniciales.</li>
  </ol>

  <h2>Ejecutar la Simulación</h2>
  <p>Corre el archivo <code>concurrency.py</code> para simular las reservas concurrentes:</p>
  <pre><code>python concurrency.py</code></pre>
  <p>El script mostrará los resultados por cada nivel de aislamiento, incluyendo:</p>
  <ul>
    <li>Cantidad de reservas exitosas</li>
    <li>Cantidad de reservas fallidas</li>
    <li>Tiempo promedio de ejecución</li>
  </ul>

</body>
</html>
