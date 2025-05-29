Sistema de Marcación para Control de Asistencia - Eno Bronstrup S.A.

======================================================================
1. INFORMACIÓN GENERAL
======================================================================

Este documento README proporciona una descripción general del Sistema de Marcación para Control de Asistencia y Gestion de Marcaciones y Empleados desarrollado para Eno Bronstrup S.A.

El objetivo principal de este sistema es automatizar y optimizar el registro de entradas y salidas de los empleados, eliminando métodos manuales y proporcionando una gestión más eficiente de la asistencia.

======================================================================
2. CARACTERÍSTICAS PRINCIPALES
======================================================================

El sistema de marcación está diseñado para cumplir con las siguientes funciones clave:

* **Registro de Marcaciones:** Permite a los empleados registrar su hora de entrada y salida a través de un marcador de asistencia físico.
* **Almacenamiento de Datos Centralizado:** Todas las marcaciones se almacenan de forma segura en una base de datos MySQL.
* **Gestión de Empleados:** Permite al personal autorizado añadir, modificar y gestionar la información de los empleados dentro del sistema.
* **Visualización de Marcaciones:** Proporciona una interfaz web para consultar las marcaciones de todos los empleados, con opciones de filtrado por fecha y empleado.
* **Generación de Informes:** Permite crear informes detallados sobre la asistencia, incluyendo horas trabajadas, ausencias y tardanzas.
* **Exportación de Informes:** Los informes generados pueden ser impresos o exportados a formato PDF para su archivo y distribución.
* **Acceso Web:** La administración y consulta del sistema se realiza a través de una aplicación web, accesible desde cualquier navegador.

======================================================================
3. TECNOLOGÍAS UTILIZADAS
======================================================================

El sistema ha sido desarrollado utilizando las siguientes tecnologías:

* **Lenguaje de Programación Backend:** Python
* **Framework Web Backend:** Flask
* **Base de Datos:** MySQL
* **Tecnologías Frontend: HTML, CSS, Boostrap
* **Dispositivo de Marcación:** Marcador de asistencia electrónico: ZKTeco

======================================================================
4. REQUERIMIENTOS DEL SISTEMA
======================================================================

Para el correcto funcionamiento del sistema, se requieren los siguientes componentes:

* **Servidor:** Un servidor (físico o virtual) con un sistema operativo compatible (Linux o Windows Server) y los recursos necesarios para ejecutar el intérprete de Python, el framework web y el servidor MySQL.
* **Marcadores de Asistencia:** Los dispositivos físicos que los empleados utilizarán para registrar su entrada y salida.
* **Red Local (LAN):** Conectividad de red para que los marcadores puedan comunicarse con el servidor y las estaciones de trabajo puedan acceder a la aplicación web.
* **Estaciones de Trabajo:** Computadoras con un navegador web actualizado para acceder a la interfaz de administración del sistema.
* **Software de Base de Datos:** MySQL Server instalado y configurado en el servidor.
* **Entorno Python:** Intérprete de Python y las librerías necesarias (ej: PyMySQL, Flask/Django, librerías para PDF como ReportLab/FPDF) instaladas en el servidor.

======================================================================
5. INSTALACIÓN Y CONFIGURACIÓN (Guía Preliminar)
======================================================================


1.  **Configuración del Servidor:**
    * Instalar el sistema operativo: Windows u otros
    * Instalar Python y las dependencias del proyecto (pip install -r ).
    * Instalar Visual Studio Code
    * Instalar las siguientes las librerias (PYMYSQL, PyZK)
    * Instalar un servidor web(XAMP).
    * Configurar el entorno virtual de Python.

2.  **Configuración de la Base de Datos MySQL:**
    * Instalar MySQL Server.
    * Crear la base de datos para el sistema de marcación.
    * Crear un usuario de base de datos con los permisos adecuados.
    * Importar el esquema de la base de datos (se proporcionará un archivo .sql).

3.  **Despliegue de la Aplicación Web:**
    * Copiar los archivos de la aplicación Python al servidor.
    * Configurar el servidor web para servir la aplicación Python.
    * Asegurar la conectividad entre la aplicación y la base de datos.

4.  **Configuración de los Marcadores de Asistencia:**
    * Instalar los marcadores físicos en las ubicaciones designadas.
    * Configurar los marcadores para que se conecten al servidor y envíen los datos de marcación según el protocolo definido.
    * Realizar pruebas de comunicación.

5.  **Carga Inicial de Datos:**
    * Introducir la información inicial de los empleados (nombres, IDs, etc.) en el sistema.

======================================================================
6. USO BÁSICO
======================================================================

* **Para Empleados:** Los empleados solo necesitan acercar su método de identificación (tarjeta, huella, etc.) al marcador de asistencia en la entrada y salida.
* **Para Administradores:** Acceder a la aplicación web a través de un navegador utilizando la URL proporcionada. Se requerirán credenciales de usuario y contraseña.

======================================================================
7. LIMITACIONES DEL SISTEMA (Alcance Actual)
======================================================================

Es importante destacar que esta versión del sistema de marcación se enfoca exclusivamente en el control de asistencia. No incluye funcionalidades para:

* Gestión de Tareas o Proyectos.
* Cálculo Automático de Horas Extras Complejas.
* Generación de Informes de Productividad.
* Personalización Extrema de Informes.

======================================================================
8. SOPORTE Y CONTACTO
======================================================================

Para cualquier consulta, problema técnico o solicitud de mejora, por favor contacte al equipo de soporte de TI de Eno Bronstrup S.A. o al desarrollador del sistema.

[luisluismm727@gmail.com]

======================================================================
9. AGRADECIMIENTOS
======================================================================

Agradecemos a Eno Bronstrup S.A. por la oportunidad de desarrollar e implementar esta solución.

======================================================================
[30/05/25 | 30/05/25]