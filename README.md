# 🐾 Sistema de Gestión de Clínica Veterinaria

Sistema integral de gestión para clínicas veterinarias desarrollado con Python y Streamlit. Permite administrar dueños, mascotas, citas, consultas médicas, facturas y personal de la clínica con un sistema de autenticación y control de acceso basado en roles.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelo de Datos](#-modelo-de-datos)
- [Sistema de Logging](#-sistema-de-logging)
- [Testing](#-testing)
- [Roles y Permisos](#-roles-y-permisos)
- [Contribución](#-contribución)

## ✨ Características

### Gestión de Entidades
- **Dueños**: Registro y administración de propietarios de mascotas
- **Mascotas**: Control de pacientes animales con historial completo
- **Citas**: Programación y seguimiento de citas veterinarias
- **Consultas**: Registro de diagnósticos, tratamientos y observaciones médicas
- **Facturas**: Gestión de pagos y comprobantes
- **Empleados**: Administración de personal de la clínica

### Funcionalidades Principales
- 🔐 **Sistema de autenticación** con control de acceso basado en roles
- 📊 **Dashboard interactivo** con métricas en tiempo real
- 🔍 **Búsqueda y filtrado** avanzado de registros
- 📝 **CRUD completo** para todas las entidades
- 🎨 **Interfaz intuitiva** desarrollada con Streamlit
- 📋 **Logging exhaustivo** para auditoría y debugging
- ✅ **Cobertura de tests** para calidad del código

### Control de Acceso por Roles
- **Dueño**: Vista de sus mascotas y citas propias
- **Veterinario**: Gestión de consultas y visualización de citas
- **Enfermero**: Apoyo en consultas y acceso a información médica
- **Recepcionista**: Acceso completo a gestión administrativa
- **Conserje**: Acceso limitado a información propia

## 🛠 Tecnologías

### Backend
- **Python 3.x**: Lenguaje principal
- **MySQL**: Base de datos relacional
- **mysql-connector-python 9.5.0**: Conector de base de datos

### Frontend
- **Streamlit 1.51.0**: Framework de interfaz web
- **Plotly 5.24.1**: Visualización de datos
- **Pandas 2.3.3**: Procesamiento de datos

### Testing y Calidad
- **pytest 9.0.0**: Framework de testing
- **logging**: Sistema de logs integrado

### Otras Dependencias
- **FastAPI 0.121.1**: Framework web asíncrono
- **Pydantic 2.12.4**: Validación de datos
- **ReportLab 4.2.5**: Generación de PDFs
- **GitPython 3.1.45**: Integración con Git

## 🏗 Arquitectura

El proyecto sigue una arquitectura en capas con separación de responsabilidades:

```
┌─────────────────────────────────────┐
│         Capa de Presentación        │
│        (Streamlit Pages)            │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         Capa de Entidades           │
│    (Lógica de Negocio - Modelos)   │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      Capa de Acceso a Datos         │
│      (DatabaseConnection)           │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         Base de Datos MySQL         │
└─────────────────────────────────────┘
```

### Principios de Diseño
- **Separación de Responsabilidades**: Cada módulo tiene una función específica
- **Inyección de Dependencias**: Las entidades reciben la conexión DB como parámetro
- **Logging Centralizado**: Sistema de logs configurable en toda la aplicación
- **Testing**: Cobertura de tests unitarios con mocks

## 📦 Requisitos

- **Python**: 3.8 o superior
- **MySQL**: 5.7 o superior
- **pip**: Gestor de paquetes de Python
- **Sistema Operativo**: Windows, Linux o macOS

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JavierAguilar03/PROYECTO-CLINICA-VETERINARIA.git
cd PROYECTO-CLINICA-VETERINARIA
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/macOS
python3 -m venv env
source env/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

#### Crear la base de datos

```sql
CREATE DATABASE clinica_veterinaria;
USE clinica_veterinaria;
```

#### Crear las tablas

```sql
-- Tabla de Dueños
CREATE TABLE duenos (
    id_dueno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_nacimiento DATE,
    direccion VARCHAR(200)
);

-- Tabla de Mascotas
CREATE TABLE mascotas (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(50),
    fecha_nacimiento DATE,
    peso DECIMAL(5,2),
    sexo VARCHAR(10),
    id_dueno INT,
    FOREIGN KEY (id_dueno) REFERENCES duenos(id_dueno) ON DELETE CASCADE
);

-- Tabla de Empleados
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_nacimiento DATE,
    salario DECIMAL(10,2),
    tipo_empleado VARCHAR(50) NOT NULL,
    usuario VARCHAR(50) UNIQUE,
    contraseña VARCHAR(255)
);

-- Tabla de Citas
CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(200),
    id_mascota INT,
    id_empleado INT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota) ON DELETE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE SET NULL
);

-- Tabla de Consultas
CREATE TABLE consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT UNIQUE,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE CASCADE
);

-- Tabla de Facturas
CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT UNIQUE,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50),
    fecha DATE,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE
);
```

#### Insertar datos de prueba (opcional)

```sql
-- Insertar empleados de ejemplo
INSERT INTO empleados (nombre, dni, telefono, email, fecha_nacimiento, salario, tipo_empleado, usuario, contraseña)
VALUES 
    ('Dr. Carlos Ruiz', '11223344A', '600111222', 'carlos@veterinaria.com', '1980-04-10', 2500.00, 'Veterinario', 'carlos_vet', '1234'),
    ('Ana Martínez', '55667788B', '600333444', 'ana@veterinaria.com', '1992-08-25', 1800.00, 'Recepcionista', 'ana_recep', '1234');

-- Insertar dueños de ejemplo
INSERT INTO duenos (nombre, dni, telefono, email, fecha_nacimiento, direccion)
VALUES 
    ('Juan Pérez', '12345678A', '600123456', 'juan@email.com', '1985-03-20', 'Calle Mayor 1'),
    ('María García', '87654321B', '600654321', 'maria@email.com', '1990-07-15', 'Avenida Principal 45');
```

## ⚙️ Configuración

### Configurar Conexión a Base de Datos

Edita el archivo `src/database_conn/db_conn.py` o usa variables de entorno:

```python
# Configuración directa en db_conn.py
def __init__(self, host: str, user: str, password: str, database: str):
    self.host = "localhost"        # Tu host
    self.user = "root"              # Tu usuario
    self.password = "tu_password"   # Tu contraseña
    self.database = "clinica_veterinaria"
```

O usa variables de entorno:

```bash
# Windows PowerShell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="tu_password"
$env:DB_NAME="clinica_veterinaria"

# Linux/macOS
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="tu_password"
export DB_NAME="clinica_veterinaria"
```

### Configurar Logging

El sistema de logging está configurado en `src/logging/logging.conf`. Personaliza los niveles y handlers según necesites:

```ini
[logger_root]
level=INFO              # Cambia a DEBUG para más detalle
handlers=consoleHandler,fileHandler

[handler_fileHandler]
level=DEBUG
args=('logs/app.log', 'a')  # Ubicación del archivo de log
```

## 🎮 Uso

### Iniciar la Aplicación

```bash
streamlit run Página_de_Inicio.py
```

La aplicación se abrirá en `http://localhost:8501`

### Flujo de Trabajo Típico

#### 1. Login
- Accede con credenciales de empleado o dueño
- Sistema valida y asigna permisos según rol

#### 2. Dashboard (Empleados)
- Visualiza métricas: citas pendientes, consultas del día, ingresos
- Acceso rápido a funcionalidades principales

#### 3. Gestión de Dueños (Recepcionista)
- Registrar nuevo dueño con datos personales
- Buscar y editar información existente
- Visualizar mascotas asociadas

#### 4. Gestión de Mascotas
- Registrar mascota vinculada a dueño
- Actualizar datos (peso, información médica)
- Ver historial de citas

#### 5. Programación de Citas
- Crear cita: seleccionar mascota, veterinario, fecha/hora
- Estados: Pendiente → Completada/Cancelada
- Filtrar por estado, fecha, mascota

#### 6. Registro de Consultas (Veterinario)
- Al completar cita, registrar diagnóstico y tratamiento
- Añadir observaciones médicas
- Generar factura asociada

#### 7. Gestión de Facturas (Recepcionista)
- Visualizar todas las facturas
- Filtrar por fecha, método de pago
- Actualizar estado de pago

## 📁 Estructura del Proyecto

```
PROYECTO-CLINICA-VETERINARIA/
├── pages/                          # Páginas de Streamlit
│   ├── Citas.py                   # Gestión de citas
│   ├── Consultas.py               # Registro de consultas
│   ├── Dashboard.py               # Dashboard principal
│   ├── Dueños.py                  # Gestión de dueños
│   ├── Empleados.py               # Gestión de empleados
│   ├── Facturas.py                # Gestión de facturas
│   └── Mascotas.py                # Gestión de mascotas
│
├── src/                           # Código fuente
│   ├── database_conn/             # Capa de acceso a datos
│   │   └── db_conn.py            # Clase DatabaseConnection
│   │
│   ├── entidades/                 # Modelos de negocio
│   │   ├── administrativo/
│   │   │   ├── cita.py           # Clase Cita
│   │   │   ├── consulta.py       # Clase Consulta
│   │   │   └── factura.py        # Clase Factura
│   │   │
│   │   ├── mascotas/
│   │   │   └── mascota.py        # Clase Mascota
│   │   │
│   │   └── personas/
│   │       ├── duenos/
│   │       │   └── dueno.py      # Clase Dueno
│   │       │
│   │       ├── empleados/
│   │       │   ├── empleado.py   # Clase Empleado
│   │       │   ├── veterinario.py
│   │       │   ├── enfermero.py
│   │       │   ├── recepcionista.py
│   │       │   └── conserje.py
│   │       │
│   │       └── persona.py        # Clase base Persona
│   │
│   ├── excepciones/              # Excepciones personalizadas
│   │   └── excepciones.py
│   │
│   ├── logging/                  # Configuración de logging
│   │   ├── logging.conf          # Configuración de loggers
│   │   └── log_config.py         # Setup de logging
│   │
│   └── utils/                    # Utilidades
│       └── db_utils.py           # Utilidades de BD
│
├── test/                         # Tests unitarios
│   ├── test_database_conn/
│   │   └── test_db_conn.py
│   │
│   └── test_entidades/
│       ├── test_administrativo/
│       │   ├── test_cita.py
│       │   ├── test_consulta.py
│       │   └── test_factura.py
│       │
│       ├── test_mascotas/
│       │   └── test_mascota.py
│       │
│       └── test_personas/
│           ├── test_dueno.py
│           └── test_empleado.py
│
├── logs/                         # Archivos de log (generados)
│   └── app.log
│
├── env/                          # Entorno virtual (generado)
├── Página_de_Inicio.py          # Punto de entrada principal
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
```

## 🗄 Modelo de Datos

### Diagrama de Relaciones

```
┌─────────────┐         ┌──────────────┐
│   DUENOS    │◄───────┤   MASCOTAS   │
├─────────────┤ 1    * ├──────────────┤
│ id_dueno PK │         │ id_mascota PK│
│ nombre      │         │ nombre       │
│ dni         │         │ especie      │
│ telefono    │         │ raza         │
│ email       │         │ id_dueno FK  │
└─────────────┘         └──────┬───────┘
                               │ 1
                               │
                          *    │
                        ┌──────┴───────┐       ┌──────────────┐
                        │    CITAS     │◄──────┤  EMPLEADOS   │
                        ├──────────────┤ *   1 ├──────────────┤
                        │ id_cita PK   │       │ id_empleado  │
                        │ fecha        │       │ nombre       │
                        │ hora         │       │ tipo_empleado│
                        │ estado       │       │ usuario      │
                        │ id_mascota FK│       │ contraseña   │
                        │ id_empleado  │       └──────────────┘
                        └──────┬───────┘
                               │ 1
                               │
                               │ 1
                        ┌──────┴──────────┐
                        │   CONSULTAS     │
                        ├─────────────────┤
                        │ id_consulta PK  │
                        │ id_cita FK      │
                        │ diagnostico     │
                        │ tratamiento     │
                        │ observaciones   │
                        └──────┬──────────┘
                               │ 1
                               │
                               │ 1
                        ┌──────┴──────────┐
                        │   FACTURAS      │
                        ├─────────────────┤
                        │ id_factura PK   │
                        │ id_consulta FK  │
                        │ total           │
                        │ metodo_pago     │
                        │ fecha           │
                        └─────────────────┘
```

### Entidades Principales

#### Dueno
- Propietarios de mascotas
- Pueden tener múltiples mascotas
- Acceso limitado a su información

#### Mascota
- Pacientes de la clínica
- Vinculadas a un dueño
- Tienen historial de citas

#### Empleado
- Personal de la clínica
- Tipos: Veterinario, Enfermero, Recepcionista, Conserje
- Sistema de credenciales para login

#### Cita
- Programación de visitas
- Estados: pendiente, completada, cancelada
- Vincula mascota con empleado

#### Consulta
- Registro médico de la cita
- Diagnóstico, tratamiento, observaciones
- Una por cita completada

#### Factura
- Comprobante de pago
- Vinculada a consulta
- Métodos: efectivo, tarjeta, transferencia, paypal

## 📊 Sistema de Logging

### Configuración

El sistema de logging está configurado en `src/logging/logging.conf` con múltiples loggers:

- **db_conn**: Operaciones de base de datos (nivel DEBUG)
- **entidades**: Lógica de negocio (nivel INFO)
- **pages**: Interacciones de usuario (nivel INFO)
- **utils**: Utilidades (nivel INFO)
- **test**: Ejecución de tests (nivel INFO)

### Niveles de Log

| Nivel | Uso | Ejemplos |
|-------|-----|----------|
| **DEBUG** | Detalles técnicos | Queries SQL, parámetros |
| **INFO** | Operaciones normales | Creación de entidades, accesos |
| **WARNING** | Situaciones inusuales | Accesos no autorizados, validaciones |
| **ERROR** | Errores recuperables | Fallos de BD, operaciones fallidas |
| **EXCEPTION** | Errores con stack trace | Excepciones no controladas |

### Ubicación de Logs

Los logs se guardan en `logs/app.log` con formato:

```
2025-12-10 14:30:45 - pages.citas - INFO - crear_cita:123 - Creando cita para mascota 5
2025-12-10 14:30:45 - entidades.cita - INFO - crear:25 - Cita creada exitosamente con ID: 42
2025-12-10 14:30:46 - db_conn - DEBUG - execute_insert:67 - INSERT ejecutado, ID: 42
```

### Ejemplos de Logs por Módulo

```python
# En páginas
logger.warning("Intento de acceso no autorizado a Facturas por rol=veterinario")

# En entidades
logger.info(f"Creando mascota 'Max' (Perro) para dueño {id_dueno}")

# En database_conn
logger.debug(f"Ejecutando query: {query} con params: {params}")

# En tests
logger.info("Ejecutando test: test_crear_cita")
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Tests específicos
pytest test/test_entidades/test_administrativo/test_cita.py

# Con verbose
pytest -v

# Ver logs durante tests
pytest -s
```

### Estructura de Tests

```
test/
├── test_database_conn/
│   └── test_db_conn.py         # Tests de conexión BD
│
└── test_entidades/
    ├── test_administrativo/
    │   ├── test_cita.py        # Tests de Cita
    │   ├── test_consulta.py    # Tests de Consulta
    │   └── test_factura.py     # Tests de Factura
    │
    ├── test_mascotas/
    │   └── test_mascota.py     # Tests de Mascota
    │
    └── test_personas/
        ├── test_dueno.py       # Tests de Dueno
        └── test_empleado.py    # Tests de Empleado
```

### Cobertura Actual

- **DatabaseConnection**: Conexión, queries, operaciones CRUD
- **Entidades**: Creación, actualización, obtención por ID
- **Validaciones**: Estados de cita, métodos de pago

### Ejemplo de Test

```python
def test_crear_cita(self):
    """Test crear una nueva cita."""
    logger.info("Ejecutando test: test_crear_cita")
    db_mock = MagicMock()
    db_mock.insertar_cita.return_value = 1
    
    id_cita = Cita.crear(
        db_mock,
        fecha="2025-12-15",
        hora="10:30",
        motivo="Vacunación",
        id_mascota=1,
        id_empleado=1,
        estado="pendiente"
    )
    
    assert id_cita == 1
    db_mock.insertar_cita.assert_called_once()
    logger.info("Test test_crear_cita: PASSED")
```

## 👥 Roles y Permisos

### Matriz de Permisos

| Funcionalidad | Dueño | Veterinario | Enfermero | Recepcionista | Conserje |
|---------------|-------|-------------|-----------|---------------|----------|
| **Dashboard** | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Ver Dueños** | 🔒 Propio | ❌ | ❌ | ✅ | ❌ |
| **Registrar Dueño** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Ver Mascotas** | 🔒 Propias | ✅ | ✅ | ✅ | ❌ |
| **Crear Mascota** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Ver Citas** | 🔒 Propias | ✅ | ✅ | ✅ | ❌ |
| **Crear Cita** | 🔒 Solo propias | ✅ | ❌ | ✅ | ❌ |
| **Ver Consultas** | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Crear Consulta** | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Ver Facturas** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Ver Empleados** | ❌ | 👁️ Solo ver | 👁️ Solo ver | ✅ | 🔒 Propio |
| **Crear Empleado** | ❌ | ❌ | ❌ | ✅ | ❌ |

**Leyenda:**
- ✅ Acceso completo
- ❌ Sin acceso
- 🔒 Solo información propia
- 👁️ Solo lectura

### Descripción de Roles

#### 🏠 Dueño
- Propietario de mascotas
- Acceso limitado a su información personal
- Puede ver sus mascotas y citas programadas
- **Puede crear citas** solo para sus propias mascotas
- **No puede registrar nuevos dueños** (seguridad)
- **No puede crear ni modificar** otros registros

#### 🩺 Veterinario
- Profesional médico de la clínica
- Gestiona consultas y diagnósticos
- Visualiza todas las citas y mascotas
- Puede crear citas y registrar consultas
- **No tiene acceso** a gestión administrativa (facturas, empleados)

#### 💉 Enfermero
- Personal de apoyo médico
- Visualiza información médica
- Puede registrar consultas
- Acceso similar al veterinario pero sin crear citas

#### 📋 Recepcionista
- **Acceso administrativo completo**
- Gestiona dueños, mascotas, citas
- Administra facturas y empleados
- Control total del sistema excepto consultas médicas

#### 🧹 Conserje
- Personal de mantenimiento
- **Acceso más limitado**
- Solo puede ver su propia información de empleado
- Sin acceso a gestión de pacientes o administrativo

## 🤝 Contribución

### Guía para Contribuir

1. **Fork** el repositorio
2. Crea una **rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m "Añadir nueva funcionalidad"
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un **Pull Request**

### Estándares de Código

- **PEP 8**: Seguir convenciones de estilo Python
- **Type Hints**: Usar anotaciones de tipo
- **Docstrings**: Documentar clases y métodos
- **Tests**: Incluir tests para nuevas funcionalidades
- **Logging**: Añadir logs apropiados

### Ejemplo de Código Estándar

```python
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger('modulo.clase')

class MiClase:
    """
    Descripción de la clase.
    
    Attributes:
        atributo: Descripción del atributo
    """
    
    def mi_metodo(self, parametro: str) -> Optional[int]:
        """
        Descripción del método.
        
        Args:
            parametro: Descripción del parámetro
            
        Returns:
            Valor de retorno o None
        """
        logger.info(f"Ejecutando mi_metodo con {parametro}")
        try:
            # Lógica del método
            resultado = self._procesar(parametro)
            logger.info(f"Método ejecutado exitosamente: {resultado}")
            return resultado
        except Exception as e:
            logger.exception(f"Error en mi_metodo: {str(e)}")
            raise
```

## 📝 Licencia

Este proyecto es un desarrollo académico para la Universidad Francisco de Vitoria (UFV).

## 👨‍💻 Autores

- **Javier Aguilar** - [JavierAguilar03](https://github.com/JavierAguilar03)
- **Lorenzo Cadenas** - [renzoC18](https://github.com/renzoC18)

## 📞 Soporte

Para reportar bugs o solicitar features:
- Abre un [Issue](https://github.com/JavierAguilar03/PROYECTO-CLINICA-VETERINARIA/issues)
- Contacta al equipo de desarrollo

## 🔄 Historial de Versiones

### v1.0.0 - Release Inicial
- ✅ Sistema completo de gestión veterinaria
- ✅ Autenticación y control de acceso por roles
- ✅ CRUD para todas las entidades
- ✅ Dashboard con métricas
- ✅ Sistema de logging exhaustivo
- ✅ Cobertura de tests unitarios
- ✅ Documentación completa

---

**🐾 Desarrollado con ❤️ para mejorar la gestión de clínicas veterinarias**
