# Sistema de Permisos por Rol - Clínica Veterinaria

## Resumen de Permisos

### 🩺 VETERINARIOS
**Acceso Limitado a sus Pacientes**

#### Páginas Accesibles:
- ✅ **Citas** - Solo citas asignadas a ellos
- ✅ **Mascotas** - Solo mascotas que atienden (con citas asignadas)
- ✅ **Consultas** - Solo consultas de sus citas (pueden registrar nuevas)
- ✅ **Empleados** - Ver información general del equipo (sin registrar)
- ❌ **Facturas** - Sin acceso
- ❌ **Dueños** - Sin acceso

#### Funcionalidades:
- Ver y gestionar solo las citas donde están asignados como veterinario
- Ver información de las mascotas que tienen citas con ellos
- Registrar diagnósticos y tratamientos en sus consultas
- Ver lista completa de empleados
- NO pueden completar/cancelar citas (solo ver)

---

### 💉 ENFERMEROS
**Acceso Completo a Información de Animales**

#### Páginas Accesibles:
- ✅ **Citas** - Todas las citas (pueden completar/cancelar)
- ✅ **Mascotas** - Todas las mascotas (sin registrar nuevas)
- ✅ **Consultas** - Todas las consultas (solo lectura)
- ✅ **Empleados** - Ver información general del equipo (sin registrar)
- ❌ **Facturas** - Sin acceso
- ❌ **Dueños** - Sin acceso

#### Funcionalidades:
- Ver todas las citas de la clínica
- Modificar estados de citas (completar/cancelar)
- Ver información completa de todas las mascotas
- Ver todas las consultas médicas (sin registrar)
- Ver lista completa de empleados
- NO pueden registrar nuevas mascotas ni consultas

---

### 📝 RECEPCIONISTAS
**Acceso Total al Sistema**

#### Páginas Accesibles:
- ✅ **Citas** - Todas las citas (gestión completa)
- ✅ **Mascotas** - Todas las mascotas (puede registrar)
- ✅ **Consultas** - Todas las consultas (solo lectura)
- ✅ **Facturas** - Todas las facturas (gestión completa)
- ✅ **Dueños** - Todos los dueños (gestión completa)
- ✅ **Empleados** - Todos los empleados (gestión completa + registro)

#### Funcionalidades:
- Gestión completa de citas (ver, crear, modificar, cancelar)
- Registrar nuevas mascotas para cualquier dueño
- Ver todas las consultas médicas
- Generar y gestionar facturas
- Registrar y gestionar información de dueños
- Registrar nuevos empleados y ver información de todos
- Acceso administrativo completo

---

### 🧹 CONSERJES
**Acceso Mínimo - Solo Información Personal**

#### Páginas Accesibles:
- ✅ **Empleados** - Solo su propia información y salario
- ❌ **Citas** - Sin acceso
- ❌ **Mascotas** - Sin acceso
- ❌ **Consultas** - Sin acceso
- ❌ **Facturas** - Sin acceso
- ❌ **Dueños** - Sin acceso

#### Funcionalidades:
- Ver únicamente su información personal
- Ver su salario
- NO tienen acceso a ninguna otra sección del sistema
- Mensaje de error al intentar acceder a páginas restringidas

---

### 🏠 DUEÑOS DE MASCOTAS
**Acceso a sus Datos y Mascotas**

#### Páginas Accesibles:
- ✅ **Citas** - Solo citas de sus mascotas (pueden crear)
- ✅ **Mascotas** - Solo sus mascotas (pueden registrar)
- ✅ **Dueños** - Solo su propia información
- ❌ **Consultas** - Sin acceso
- ❌ **Facturas** - Sin acceso
- ❌ **Empleados** - Sin acceso

#### Funcionalidades:
- Ver citas de sus mascotas
- Registrar nuevas citas para sus mascotas
- Ver información de sus mascotas
- Registrar nuevas mascotas (auto-asignadas a su ID)
- Ver su información personal
- NO pueden ver información de otros dueños o mascotas ajenas

---

## Tabla Resumen de Permisos

| Página/Función | Veterinario | Enfermero | Recepcionista | Conserje | Dueño |
|----------------|-------------|-----------|---------------|----------|-------|
| **Citas** | Ver solo suyas | Ver todas | Gestión total | ❌ | Ver solo suyas |
| **Mascotas** | Ver solo las que atiende | Ver todas | Gestión total | ❌ | Ver solo suyas |
| **Consultas** | Registrar suyas | Ver todas | Ver todas | ❌ | ❌ |
| **Facturas** | ❌ | ❌ | Gestión total | ❌ | ❌ |
| **Dueños** | ❌ | ❌ | Gestión total | ❌ | Ver solo su info |
| **Empleados** | Ver todos | Ver todos | Gestión total | Ver solo su info | ❌ |

---

## Implementación Técnica

### Control de Acceso en Cada Página

Cada página verifica:
1. **Autenticación**: Usuario debe estar logueado
2. **Tipo de usuario**: Empleado vs Dueño
3. **Rol específico**: Tipo de empleado (veterinario, enfermero, etc.)
4. **Filtrado de datos**: Consultas SQL filtradas según el rol

### Variables de Sesión

```python
st.session_state.authenticated  # Boolean: ¿está logueado?
st.session_state.user_type      # String: "empleado" o "dueño"
st.session_state.user_data      # Dict: Información del usuario
```

### Determinación del Rol

```python
user_role = st.session_state.user_data.get('tipo_empleado', '').lower() 
            if st.session_state.user_type == 'empleado' 
            else 'dueño'
```

### Mensajes de Error

- **Conserjes**: "Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados."
- **Veterinarios/Enfermeros**: "Acceso restringido. Solo recepcionistas pueden..."
- **Dueños**: "Acceso restringido. Solo empleados pueden..."

---

## Notas de Seguridad

1. **Filtrado en Backend**: Todas las consultas SQL están filtradas por ID de usuario/empleado
2. **Sin bypass**: No es posible acceder a datos ajenos mediante URLs o formularios
3. **Validación consistente**: Control de acceso en todas las páginas
4. **Mensajes claros**: Usuarios saben qué pueden y no pueden hacer

---

## Casos de Uso

### Veterinario Dr. García
- Inicia sesión → Ve solo sus 12 citas asignadas
- Accede a Mascotas → Ve solo las 8 mascotas que atiende
- Completa una consulta → Registra diagnóstico y tratamiento
- Intenta ver Facturas → Error: "Acceso restringido"

### Enfermera María
- Inicia sesión → Ve todas las 51 citas de la clínica
- Accede a Mascotas → Ve las 30 mascotas registradas
- Marca cita como completada → OK
- Intenta registrar consulta → Advertencia: "Solo veterinarios"

### Recepcionista Ana
- Inicia sesión → Acceso total a todo el sistema
- Registra nuevo dueño → OK
- Genera factura → OK
- Registra nuevo empleado → OK

### Conserje Juan
- Inicia sesión → Solo ve su información
- Intenta ver Citas → Error: "Los conserjes solo pueden..."
- Ve su salario: 1200€ → OK
- No puede acceder a ninguna otra página

### Dueño Pedro
- Inicia sesión con DNI + email
- Ve sus 2 mascotas: Max y Luna
- Registra cita para Max → OK
- Intenta ver otras mascotas → No aparecen
- Ve su información personal → OK
