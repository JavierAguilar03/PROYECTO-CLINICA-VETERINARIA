# 🔐 CREDENCIALES DE PRUEBA - Clínica Veterinaria

## 📋 Instrucciones de Configuración

### 1. Ejecutar el script SQL
```bash
# En MySQL Workbench o desde línea de comandos:
mysql -u root -p < database_setup.sql

# O ejecutar cada sección del archivo database_setup.sql manualmente
```

### 2. Configurar variables de entorno (opcional)
```powershell
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_PASSWORD = "tu_password_mysql"
$env:DB_NAME = "clinica_veterinaria"
```

---

## 👨‍⚕️ EMPLEADOS (Acceso Completo)

### Veterinario
- **Usuario**: `carlos`
- **Contraseña**: `admin123`
- **Nombre**: Dr. Carlos Martínez
- **Email**: carlos@clinica.com

### Recepcionista
- **Usuario**: `ana`
- **Contraseña**: `recep123`
- **Nombre**: Ana García López
- **Email**: ana@clinica.com

### Enfermero
- **Usuario**: `luis`
- **Contraseña**: `enfer123`
- **Nombre**: Luis Fernández
- **Email**: luis@clinica.com

### Conserje
- **Usuario**: `maria`
- **Contraseña**: `conse123`
- **Nombre**: María Rodríguez
- **Email**: maria@clinica.com

---

## 🏠 DUEÑOS (Acceso Limitado - Solo Citas)

### Dueño 1
- **DNI**: `11111111A`
- **Email**: `juan.perez@email.com`
- **Nombre**: Juan Pérez González
- **Mascotas**: Max (Labrador), Luna (Siamés)

### Dueño 2
- **DNI**: `22222222B`
- **Email**: `laura.sanchez@email.com`
- **Nombre**: Laura Sánchez Ruiz
- **Mascotas**: Rocky (Pastor Alemán), Michi (Persa)

### Dueño 3
- **DNI**: `33333333C`
- **Email**: `pedro.gomez@email.com`
- **Nombre**: Pedro Gómez Torres
- **Mascotas**: Toby (Golden Retriever)

---

## 🐾 MASCOTAS EN EL SISTEMA

1. **Max** - Labrador, 25.5kg (Dueño: Juan)
2. **Luna** - Siamés, 4.2kg (Dueño: Juan)
3. **Rocky** - Pastor Alemán, 32.0kg (Dueño: Laura)
4. **Michi** - Persa, 3.8kg (Dueño: Laura)
5. **Toby** - Golden Retriever, 28.3kg (Dueño: Pedro)

---

## 📅 CITAS CREADAS

- **26/11/2025 10:00** - Max - Revisión y vacunación (Pendiente)
- **26/11/2025 11:30** - Rocky - Control de peso (Pendiente)
- **27/11/2025 09:00** - Luna - Consulta por tos (Pendiente)
- **25/11/2025 15:00** - Toby - Revisión anual (Completada) ✅

---

## 🚀 Cómo Probar

### Paso 1: Ejecutar la aplicación
```powershell
streamlit run app.py
```

### Paso 2: Hacer login
**Como Empleado:**
1. Seleccionar "Empleado"
2. Usuario: `carlos` | Contraseña: `admin123`
3. Tendrás acceso a todas las páginas

**Como Dueño:**
1. Seleccionar "Dueño de Mascota"
2. DNI: `11111111A` | Email: `juan.perez@email.com`
3. Solo tendrás acceso a Citas

### Paso 3: Explorar funcionalidades
- Ver citas existentes
- Crear nuevas citas
- Gestionar mascotas
- Registrar consultas (solo empleados)
- Generar facturas (solo empleados)

---

## ⚠️ NOTAS IMPORTANTES

1. **Contraseñas en texto plano**: Para producción, usar hashing (bcrypt, etc.)
2. **Datos de prueba**: Estos datos son solo para desarrollo/testing
3. **Base de datos**: Asegúrate de que MySQL esté corriendo
4. **Puerto por defecto**: MySQL usa puerto 3306
5. **Tablas**: El script crea automáticamente todas las tablas necesarias

---

## 🔄 Reiniciar Base de Datos

Si necesitas limpiar y volver a empezar:

```sql
DROP DATABASE IF EXISTS clinica_veterinaria;
-- Luego ejecutar database_setup.sql nuevamente
```

---

## 📧 Envío de Emails

Para probar el envío de facturas por email:

```python
# En la aplicación o consola Python
from src.entidades.administrativo.factura import Factura

factura = Factura(1, 1)
servicios = [{'descripcion': 'Consulta', 'precio': 50.0}]
factura.calcular_total(servicios, impuestos=0.16)

# Configurar con tu email
factura.enviar_por_email(
    email_cliente='destinatario@email.com',
    email_remitente='tu_email@gmail.com',
    password_remitente='tu_app_password',
    adjuntar_pdf=True
)
```

**Nota**: Para Gmail, necesitas una [contraseña de aplicación](https://support.google.com/accounts/answer/185833)

---

## ✅ Checklist de Verificación

- [ ] MySQL instalado y corriendo
- [ ] Base de datos `clinica_veterinaria` creada
- [ ] Script `database_setup.sql` ejecutado
- [ ] Variables de entorno configuradas (opcional)
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] Aplicación corriendo con `streamlit run app.py`
- [ ] Login exitoso como empleado o dueño
- [ ] Navegación por las diferentes páginas

---

**¡Listo para usar!** 🎉
