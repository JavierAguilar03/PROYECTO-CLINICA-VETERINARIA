import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Consultas", page_icon="🏥", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

if st.session_state.user_type != "empleado":
    st.error("🚫 Acceso restringido. Solo empleados.")
    st.stop()

def init_db():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    return DatabaseConnection(host, user, password, database)

st.title("🏥 Gestión de Consultas")
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Ver Consultas", "➕ Nueva Consulta"])

with tab1:
    st.subheader("Lista de Consultas")
    try:
        db = init_db()
        if db.connect():
            consultas = db.fetch_all("SELECT * FROM consultas ORDER BY id_consulta DESC")
            db.disconnect()
            
            if consultas:
                for consulta in consultas:
                    with st.expander(f"📋 Consulta #{consulta['id_consulta']} - Cita #{consulta['id_cita']}"):
                        st.write(f"**Diagnóstico**: {consulta.get('diagnostico', 'N/A')}")
                        st.write(f"**Tratamiento**: {consulta.get('tratamiento', 'N/A')}")
                        st.write(f"**Observaciones**: {consulta.get('observaciones', 'N/A')}")
            else:
                st.warning("No hay consultas registradas")
    except Exception as e:
        st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Registrar Nueva Consulta")
    with st.form("nueva_consulta"):
        id_cita = st.number_input("ID de la Cita*", min_value=1, step=1)
        diagnostico = st.text_area("Diagnóstico*", height=100)
        tratamiento = st.text_area("Tratamiento*", height=100)
        observaciones = st.text_area("Observaciones", height=80)
        
        if st.form_submit_button("🏥 Registrar Consulta", use_container_width=True):
            if id_cita and diagnostico and tratamiento:
                try:
                    db = init_db()
                    if db.connect():
                        id_consulta = db.insertar_consulta(id_cita, diagnostico, tratamiento, observaciones)
                        db.disconnect()
                        if id_consulta:
                            st.success(f"✅ Consulta registrada (ID: {id_consulta})")
                        else:
                            st.error("Error al registrar")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Complete los campos obligatorios")
