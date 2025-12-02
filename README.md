# 🐾 Sistema de Gestión de Clínica Veterinaria

Sistema completo de gestión para clínica veterinaria desarrollado en Python con Streamlit, MySQL y arquitectura orientada a objetos.

## ✨ Características Implementadas

### 🔐 Sistema de Autenticación
- ✅ Login diferenciado para empleados y dueños
- ✅ Empleados: acceso completo con usuario/contraseña
- ✅ Dueños: acceso limitado (solo citas) con DNI/email
- ✅ Control de sesión persistente

### 📋 Módulos Principales

#### Gestión de Citas
- Crear, ver, modificar y cancelar citas
- Filtros por estado (pendiente, completada, cancelada)
- Búsqueda por ID de cita o mascota
- Asignación de empleados

#### Gestión de Mascotas
- Registro completo (especie, raza, peso, edad)
- Historial de consultas
- Vinculación con dueños

#### Gestión de Dueños
- Datos personales completos
- Visualización de mascotas asociadas
- Búsqueda por ID o DNI

#### Gestión de Consultas
- Diagnósticos y tratamientos
- Observaciones médicas
- Vinculación con citas

#### Gestión de Facturas
- ✅ **Generación de PDF** con reportlab
- ✅ **Envío por email** con smtplib
- Cálculo con descuentos e impuestos
- Múltiples métodos de pago

#### Gestión de Empleados
- Registro de personal
- Control de salarios
- Credenciales de acceso

### 💾 Base de Datos
- Conexión MySQL con métodos CRUD específicos
- Queries parametrizadas seguras
- Transacciones con rollback
- Métodos: `insertar_*`, `obtener_*`, `actualizar_*`, `eliminar_*`

### 📊 Sistema de Logging
- Configuración centralizada (`logging.conf`)
- Logs por módulo
- Niveles: DEBUG, INFO, WARNING, ERROR
- Salida a consola y archivo

### 🧪 Tests Unitarios
- Tests con unittest para db_conn
- Tests para entidades
- Mocking de conexiones
- Cobertura de casos exitosos y errores

## 🚀 Instalación

### Requisitos
- Python 3.8+
- MySQL 5.7+
- pip

### Pasos

1. **Clonar el repositorio**
```powershell
git clone <repo-url>
cd PROYECTO-CLINICA-VETERINARIA
```

2. **Crear entorno virtual**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

3. **Instalar dependencias**
```powershell
pip install -r requirements.txt
```

4. **Configurar base de datos** (opcional)
```powershell
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_PASSWORD = "tu_password"
$env:DB_NAME = "clinica_veterinaria"
```

5. **Ejecutar aplicación**
```powershell
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
PROYECTO-CLINICA-VETERINARIA/
├── app.py                      # Aplicación principal con autenticación
├── requirements.txt            # Dependencias
├── LICENSE                     # Licencia MIT
├── README.md                   # Este archivo
├── .gitignore                  # Archivos ignorados
│
├── pages/                      # Páginas Streamlit
│   ├── Citas.py
│   ├── Consultas.py
│   ├── Facturas.py
│   ├── Mascotas.py
│   ├── Dueños.py
│   └── Empleados.py
│
├── src/                        # Código fuente
│   ├── database_conn/          # Conexión MySQL
│   │   └── db_conn.py
│   ├── entidades/              # Clases de dominio
│   │   ├── administrativo/     # Cita, Consulta, Factura
│   │   ├── mascotas/          # Mascota
│   │   └── personas/          # Persona, Dueño, Empleado
│   ├── logging/               # Sistema de logging
│   │   ├── logging.conf
│   │   └── log_config.py
│   └── utils/                 # Utilidades
│
├── test/                      # Tests unitarios
│   ├── test_database_conn/
│   └── test_entidades/
│
├── logs/                      # Archivos de log
└── facturas/                  # PDFs generados
```

## 🔧 Uso Avanzado

### Generación de PDF
```python
from src.entidades.administrativo.factura import Factura

factura = Factura(1, 1)
servicios = [{'descripcion': 'Consulta', 'precio': 50.0}]
factura.calcular_total(servicios, impuestos=0.16)
factura.generar_pdf(ruta='facturas/factura_1.pdf')
```

### Envío de Email
```python
factura.enviar_por_email(
    email_cliente='cliente@email.com',
    email_remitente='clinica@email.com',
    password_remitente='app_password',
    adjuntar_pdf=True
)
```

**Nota**: Para Gmail, usar [contraseña de aplicación](https://support.google.com/accounts/answer/185833)

## 🧪 Tests

Ejecutar tests:
```powershell
# Con pytest
python -m pytest test/ -v

# Con unittest
python -m unittest discover -s test -p "test_*.py"
```

## 🏗️ Arquitectura

- **Patrón MVC**: Separación de modelo (entidades), vista (pages) y controlador (db_conn)
- **SOLID**: Principios aplicados en diseño de clases
- **Logging**: Centralizado y configurable
- **Type Hints**: Para mejor mantenibilidad

## 📝 Próximas Mejoras

- [ ] Dashboard con métricas
- [ ] Exportación a Excel
- [ ] Calendario visual de citas
- [ ] Notificaciones automáticas
- [ ] Búsqueda avanzada con filtros
- [ ] Más cobertura de tests

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Añadir nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

## 👥 Autores

- Repositorio: [JavierAguilar03](https://github.com/JavierAguilar03)

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
