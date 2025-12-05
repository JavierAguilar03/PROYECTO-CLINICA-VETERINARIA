# 📊 Dashboard de la Clínica Veterinaria

## Descripción

El Dashboard es la página principal que ven los empleados al iniciar sesión en el sistema. Proporciona una vista general completa de las métricas y estadísticas más importantes de la clínica veterinaria.

## 🎯 Funcionalidades

### Métricas Principales (KPIs)
- **Citas Totales**: Total de citas registradas en el sistema
- **Citas Pendientes**: Número de citas con estado "pendiente"
- **Mascotas Registradas**: Total de mascotas en el sistema
- **Clientes**: Total de dueños/clientes registrados

### Gráficos Interactivos

1. **Estado de las Citas** (Gráfico de Pastel)
   - Distribución de citas por estado (pendiente, completada, cancelada)
   - Muestra porcentajes de cada estado

2. **Top 5 Especies** (Gráfico de Barras)
   - Las 5 especies más atendidas en la clínica
   - Ordenadas por cantidad de mascotas

3. **Citas por Mes** (Gráfico de Línea)
   - Evolución de citas en los últimos 6 meses
   - Permite identificar tendencias y estacionalidad

4. **Ingresos por Mes** (Gráfico de Barras)
   - Ingresos mensuales de la clínica en euros
   - Últimos 6 meses de facturación

5. **Citas por Veterinario** (Gráfico de Barras Horizontal)
   - Distribución de carga de trabajo entre veterinarios
   - Muestra el número de citas asignadas a cada uno

6. **Edad Promedio por Especie** (Gráfico de Barras)
   - Top 5 especies con su edad promedio en años
   - Útil para análisis demográfico de pacientes

### Tabla de Próximas Citas
- Muestra citas pendientes para hoy y mañana
- Incluye información completa: mascota, dueño, veterinario, motivo
- Permite planificación diaria efectiva

### Estadísticas Adicionales
- **Tasa de Finalización**: Porcentaje de citas completadas vs total
- **Ingreso Promedio**: Promedio de ingresos por consulta
- **Consultas Realizadas**: Total de consultas médicas registradas

## 🔐 Control de Acceso

- **Acceso**: Solo empleados (Veterinarios, Enfermeros, Recepcionistas, Conserjes)
- **Redirección Automática**: Los empleados son redirigidos al Dashboard automáticamente después del login
- **Dueños**: No tienen acceso al Dashboard (son redirigidos a sus páginas específicas)

## 💻 Tecnologías Utilizadas

- **Streamlit**: Framework de la aplicación web
- **Plotly**: Gráficos interactivos y visualizaciones
- **Pandas**: Procesamiento de datos
- **MySQL**: Base de datos (consultas en tiempo real)

## 🚀 Uso

1. **Iniciar sesión** como empleado
2. Serás **redirigido automáticamente** al Dashboard
3. Explora las métricas y gráficos interactivos
4. Usa el **menú lateral** para navegar a otras secciones

## 📝 Notas Técnicas

- Los datos se actualizan en **tiempo real** cada vez que se recarga la página
- Los gráficos son **interactivos**: puedes hacer zoom, hover para ver detalles, etc.
- El Dashboard consulta la base de datos directamente sin caché
- Diseño **responsive** adaptado a diferentes tamaños de pantalla

## 🔧 Mantenimiento

### Agregar Nuevos Gráficos

Para agregar un nuevo gráfico al Dashboard:

1. Abre `pages/Dashboard.py`
2. Crea una consulta SQL para obtener los datos necesarios
3. Procesa los datos con Pandas
4. Crea el gráfico con Plotly Express o Graph Objects
5. Añádelo en una nueva columna o fila

### Ejemplo de Nuevo Gráfico

```python
# Consulta SQL
query_nuevo_grafico = """
    SELECT categoria, COUNT(*) as total
    FROM tabla
    GROUP BY categoria
"""
data = db.fetch_all(query_nuevo_grafico)

# Procesar con Pandas
df = pd.DataFrame(data)

# Crear gráfico con Plotly
fig = px.bar(df, x='categoria', y='total', title='Mi Nuevo Gráfico')
st.plotly_chart(fig, use_container_width=True)
```

## 📊 Estructura del Dashboard

```
Dashboard.py
├── Verificación de autenticación
├── Inicialización de base de datos
├── Título y bienvenida
├── KPIs (4 métricas principales)
├── Fila 1 de gráficos (2 columnas)
│   ├── Estado de Citas
│   └── Top 5 Especies
├── Fila 2 de gráficos (2 columnas)
│   ├── Citas por Mes
│   └── Ingresos por Mes
├── Fila 3 de gráficos (2 columnas)
│   ├── Citas por Veterinario
│   └── Edad Promedio por Especie
├── Tabla de Próximas Citas
└── Estadísticas Adicionales (3 métricas)
```

## 🎨 Personalización

Los colores de los gráficos pueden personalizarse modificando:
- `color_discrete_sequence`: para gráficos de pastel
- `color_continuous_scale`: para gráficos con escala de color continua

Escalas disponibles: 'Blues', 'Greens', 'Oranges', 'Purples', 'Reds', 'Viridis', etc.

---

**Versión**: 1.0  
**Última actualización**: Diciembre 2025
