import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Mascotas", page_icon="🐾", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

def init_db():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    return DatabaseConnection(host, user, password, database)

st.title("🐾 Gestión de Mascotas")
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Ver Mascotas", "➕ Nueva Mascota"])

with tab1:
    st.subheader("Lista de Mascotas")
    try:
        db = init_db()
        if db.connect():
            mascotas = db.fetch_all("SELECT m.*, d.nombre as dueno_nombre FROM mascotas m LEFT JOIN duenos d ON m.id_dueno = d.id_dueño")
            db.disconnect()
            
            if mascotas:
                for mascota in mascotas:
                    with st.expander(f"🐶 {mascota['nombre']} - {mascota['especie']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID**: {mascota['id_mascota']}")
                            st.write(f"**Especie**: {mascota['especie']}")
                            st.write(f"**Raza**: {mascota['raza']}")
                        with col2:
                            st.write(f"**Peso**: {mascota['peso']} kg")
                            st.write(f"**Sexo**: {mascota['sexo']}")
                            st.write(f"**Dueño**: {mascota.get('dueno_nombre', 'N/A')}")
            else:
                st.warning("No hay mascotas registradas")
    except Exception as e:
        st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Registrar Nueva Mascota")
    with st.form("nueva_mascota"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre*")
            especie = st.text_input("Especie*")
            raza = st.text_input("Raza*")
        with col2:
            peso = st.number_input("Peso (kg)*", min_value=0.1, step=0.1)
            sexo = st.selectbox("Sexo*", ["Macho", "Hembra"])
            fecha_nac = st.date_input("Fecha de nacimiento*")
        
        id_dueno = st.number_input("ID del Dueño*", min_value=1, step=1)
        
        if st.form_submit_button("🐾 Registrar Mascota", use_container_width=True):
            if nombre and especie and raza and peso and id_dueno:
                try:
                    db = init_db()
                    if db.connect():
                        fecha_str = fecha_nac.strftime("%Y-%m-%d")
                        id_mascota = db.insertar_mascota(nombre, especie, raza, fecha_str, peso, sexo, id_dueno)
                        db.disconnect()
                        if id_mascota:
                            st.success(f"✅ Mascota registrada (ID: {id_mascota})")
                        else:
                            st.error("Error al registrar")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Complete todos los campos")
