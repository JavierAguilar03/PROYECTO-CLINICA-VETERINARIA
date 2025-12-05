import streamlit as st
import sys
import os
from datetime import datetime, timedelta, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Dashboard - Clínica Veterinaria", page_icon="📊", layout="wide")

# Verificar autenticación
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Solo empleados pueden acceder al dashboard
if st.session_state.user_type != 'empleado':
    st.error("🚫 Acceso restringido. El dashboard es solo para empleados.")
    st.stop()

def init_db():
    """Inicializa la conexión a la base de datos."""
    host = ""
    user = ""
    password = ""
    database = ""
    db = DatabaseConnection(host, user, password, database)
    return db

# Título principal
st.title("📊 Dashboard - Clínica Veterinaria")
user_name = st.session_state.user_data.get('nombre', 'Usuario')
user_role = st.session_state.user_data.get('tipo_empleado', 'N/A')
st.markdown(f"**Bienvenido, {user_name}** ({user_role})")
st.markdown("---")

# Obtener datos de la base de datos
try:
    db = init_db()
    if db.connect():
        
        # ===========================
        # MÉTRICAS PRINCIPALES (KPIs)
        # ===========================
        st.subheader("📈 Métricas Principales")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Total de Citas
        query_total_citas = "SELECT COUNT(*) as total FROM citas"
        total_citas = db.fetch_one(query_total_citas)['total']
        
        # Citas pendientes
        query_citas_pendientes = "SELECT COUNT(*) as total FROM citas WHERE estado = 'pendiente'"
        citas_pendientes = db.fetch_one(query_citas_pendientes)['total']
        
        # Total de Mascotas
        query_total_mascotas = "SELECT COUNT(*) as total FROM mascotas"
        total_mascotas = db.fetch_one(query_total_mascotas)['total']
        
        # Total de Clientes (Dueños)
        query_total_duenos = "SELECT COUNT(*) as total FROM duenos"
        total_duenos = db.fetch_one(query_total_duenos)['total']
        
        with col1:
            st.metric(label="📅 Citas Totales", value=total_citas)
        
        with col2:
            st.metric(label="⏳ Citas Pendientes", value=citas_pendientes)
        
        with col3:
            st.metric(label="🐾 Mascotas Registradas", value=total_mascotas)
        
        with col4:
            st.metric(label="👥 Clientes", value=total_duenos)
        
        st.markdown("---")
        
        # ===========================
        # GRÁFICOS EN DOS COLUMNAS
        # ===========================
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            # GRÁFICO 1: Estado de Citas (Pie Chart)
            st.subheader("🗓️ Estado de las Citas")
            query_estado_citas = """
                SELECT estado, COUNT(*) as cantidad
                FROM citas
                GROUP BY estado
            """
            estado_citas_data = db.fetch_all(query_estado_citas)
            
            if estado_citas_data:
                df_estado = pd.DataFrame(estado_citas_data)
                fig_estado = px.pie(
                    df_estado,
                    names='estado',
                    values='cantidad',
                    title='Distribución de Citas por Estado',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_estado.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_estado, use_container_width=True)
            else:
                st.info("No hay datos de citas disponibles")
        
        with col_right:
            # GRÁFICO 2: Top 5 Especies más atendidas
            st.subheader("🐕 Top 5 Especies")
            query_especies = """
                SELECT especie, COUNT(*) as cantidad
                FROM mascotas
                GROUP BY especie
                ORDER BY cantidad DESC
                LIMIT 5
            """
            especies_data = db.fetch_all(query_especies)
            
            if especies_data:
                df_especies = pd.DataFrame(especies_data)
                fig_especies = px.bar(
                    df_especies,
                    x='especie',
                    y='cantidad',
                    title='Top 5 Especies Más Atendidas',
                    color='cantidad',
                    color_continuous_scale='Blues',
                    labels={'cantidad': 'Número de Mascotas', 'especie': 'Especie'}
                )
                fig_especies.update_layout(showlegend=False)
                st.plotly_chart(fig_especies, use_container_width=True)
            else:
                st.info("No hay datos de mascotas disponibles")
        
        # ===========================
        # SEGUNDA FILA DE GRÁFICOS
        # ===========================
        
        col_left2, col_right2 = st.columns(2)
        
        with col_left2:
            # GRÁFICO 3: Citas por mes (últimos 6 meses)
            st.subheader("📆 Citas por Mes")
            query_citas_mes = """
                SELECT 
                    DATE_FORMAT(fecha, '%Y-%m') as mes,
                    COUNT(*) as cantidad
                FROM citas
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY DATE_FORMAT(fecha, '%Y-%m')
                ORDER BY mes
            """
            citas_mes_data = db.fetch_all(query_citas_mes)
            
            if citas_mes_data:
                df_citas_mes = pd.DataFrame(citas_mes_data)
                fig_citas_mes = px.line(
                    df_citas_mes,
                    x='mes',
                    y='cantidad',
                    title='Evolución de Citas (Últimos 6 Meses)',
                    markers=True,
                    labels={'cantidad': 'Número de Citas', 'mes': 'Mes'}
                )
                fig_citas_mes.update_traces(line_color='#1f77b4', line_width=3)
                st.plotly_chart(fig_citas_mes, use_container_width=True)
            else:
                st.info("No hay datos de citas recientes")
        
        with col_right2:
            # GRÁFICO 4: Ingresos por mes (últimos 6 meses)
            st.subheader("💰 Ingresos por Mes")
            query_ingresos = """
                SELECT 
                    DATE_FORMAT(f.fecha, '%Y-%m') as mes,
                    SUM(f.total) as ingresos
                FROM facturas f
                WHERE f.fecha >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY DATE_FORMAT(f.fecha, '%Y-%m')
                ORDER BY mes
            """
            ingresos_data = db.fetch_all(query_ingresos)
            
            if ingresos_data:
                df_ingresos = pd.DataFrame(ingresos_data)
                fig_ingresos = px.bar(
                    df_ingresos,
                    x='mes',
                    y='ingresos',
                    title='Ingresos Mensuales (€)',
                    color='ingresos',
                    color_continuous_scale='Greens',
                    labels={'ingresos': 'Ingresos (€)', 'mes': 'Mes'}
                )
                st.plotly_chart(fig_ingresos, use_container_width=True)
            else:
                st.info("No hay datos de ingresos disponibles")
        
        # ===========================
        # TERCERA FILA DE GRÁFICOS
        # ===========================
        
        col_left3, col_right3 = st.columns(2)
        
        with col_left3:
            # GRÁFICO 5: Citas por Veterinario
            st.subheader("👨‍⚕️ Citas por Veterinario")
            query_citas_vet = """
                SELECT 
                    e.nombre as veterinario,
                    COUNT(c.id_cita) as cantidad
                FROM empleados e
                LEFT JOIN citas c ON e.id_empleado = c.id_empleado
                WHERE e.tipo_empleado = 'Veterinario'
                GROUP BY e.id_empleado, e.nombre
                ORDER BY cantidad DESC
            """
            citas_vet_data = db.fetch_all(query_citas_vet)
            
            if citas_vet_data:
                df_citas_vet = pd.DataFrame(citas_vet_data)
                fig_citas_vet = px.bar(
                    df_citas_vet,
                    y='veterinario',
                    x='cantidad',
                    orientation='h',
                    title='Citas Asignadas por Veterinario',
                    color='cantidad',
                    color_continuous_scale='Oranges',
                    labels={'cantidad': 'Número de Citas', 'veterinario': 'Veterinario'}
                )
                st.plotly_chart(fig_citas_vet, use_container_width=True)
            else:
                st.info("No hay datos de veterinarios disponibles")
        
        with col_right3:
            # GRÁFICO 6: Edad promedio de mascotas por especie
            st.subheader("🎂 Edad Promedio por Especie")
            query_edad_especie = """
                SELECT 
                    especie,
                    AVG(TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE())) as edad_promedio
                FROM mascotas
                WHERE fecha_nacimiento IS NOT NULL
                GROUP BY especie
                HAVING edad_promedio > 0
                ORDER BY edad_promedio DESC
                LIMIT 5
            """
            edad_especie_data = db.fetch_all(query_edad_especie)
            
            if edad_especie_data:
                df_edad_especie = pd.DataFrame(edad_especie_data)
                df_edad_especie['edad_promedio'] = df_edad_especie['edad_promedio'].round(1)
                
                fig_edad = px.bar(
                    df_edad_especie,
                    x='especie',
                    y='edad_promedio',
                    title='Edad Promedio por Especie (años)',
                    color='edad_promedio',
                    color_continuous_scale='Purples',
                    labels={'edad_promedio': 'Edad Promedio (años)', 'especie': 'Especie'}
                )
                st.plotly_chart(fig_edad, use_container_width=True)
            else:
                st.info("No hay datos de edad disponibles")
        
        # ===========================
        # TABLA: PRÓXIMAS CITAS
        # ===========================
        
        st.markdown("---")
        st.subheader("📅 Próximas Citas (Hoy y mañana)")
        
        query_proximas_citas = """
            SELECT 
                c.id_cita,
                c.fecha,
                c.hora,
                m.nombre as mascota,
                m.especie,
                d.nombre as dueño,
                e.nombre as veterinario,
                c.motivo,
                c.estado
            FROM citas c
            LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
            LEFT JOIN duenos d ON m.id_dueno = d.id_dueno
            LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
            WHERE c.fecha BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 1 DAY)
            AND c.estado = 'pendiente'
            ORDER BY c.fecha, c.hora
        """
        proximas_citas = db.fetch_all(query_proximas_citas)
        
        if proximas_citas:
            df_proximas = pd.DataFrame(proximas_citas)
            # Formatear fecha y hora
            df_proximas['fecha'] = pd.to_datetime(df_proximas['fecha']).dt.strftime('%Y-%m-%d')
            df_proximas['hora'] = df_proximas['hora'].astype(str)
            
            st.dataframe(
                df_proximas,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id_cita": "ID",
                    "fecha": "Fecha",
                    "hora": "Hora",
                    "mascota": "Mascota",
                    "especie": "Especie",
                    "dueño": "Dueño",
                    "veterinario": "Veterinario",
                    "motivo": "Motivo",
                    "estado": "Estado"
                }
            )
        else:
            st.info("No hay citas pendientes para hoy o mañana")
        
        # ===========================
        # ESTADÍSTICAS ADICIONALES
        # ===========================
        
        st.markdown("---")
        st.subheader("📊 Estadísticas Adicionales")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            # Tasa de finalización de citas
            query_tasa = """
                SELECT 
                    (SUM(CASE WHEN estado = 'completada' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as tasa
                FROM citas
            """
            tasa_data = db.fetch_one(query_tasa)
            tasa_completadas = tasa_data['tasa'] if tasa_data['tasa'] else 0
            st.metric(
                label="✅ Tasa de Finalización",
                value=f"{tasa_completadas:.1f}%"
            )
        
        with col_stat2:
            # Promedio de ingresos por consulta
            query_promedio = """
                SELECT AVG(total) as promedio
                FROM facturas
                WHERE total > 0
            """
            promedio_data = db.fetch_one(query_promedio)
            promedio_ingreso = promedio_data['promedio'] if promedio_data['promedio'] else 0
            st.metric(
                label="💵 Ingreso Promedio",
                value=f"{promedio_ingreso:.2f} €"
            )
        
        with col_stat3:
            # Total de consultas realizadas
            query_consultas = "SELECT COUNT(*) as total FROM consultas"
            total_consultas = db.fetch_one(query_consultas)['total']
            st.metric(
                label="🏥 Consultas Realizadas",
                value=total_consultas
            )
        
        db.disconnect()
        
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {str(e)}")
    st.info("Por favor, verifique la conexión a la base de datos.")

# Footer
st.markdown("---")
st.caption("💡 **Tip**: Los datos se actualizan en tiempo real cada vez que recarga la página")
