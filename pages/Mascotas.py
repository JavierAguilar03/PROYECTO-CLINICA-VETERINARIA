import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.db_utils import init_db
from src.entidades.mascotas.mascota import Mascota

st.set_page_config(page_title="Mascotas", page_icon="🐾", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower() if st.session_state.user_type == 'empleado' else 'dueño'

# Conserjes NO tienen acceso a mascotas
if user_role == 'conserje':
    st.error("🚫 Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados.")
    st.stop()

st.title("🐾 Gestión de Mascotas")
st.markdown("---")

tab1 = st.tabs(["📋 Ver Mascotas"])[0]

with tab1:
    st.subheader("Lista de Mascotas")
    try:
        db = init_db()
        if db.connect():
            # Filtrar según rol
            if user_role == 'dueño':
                # Dueños solo ven sus mascotas
                id_dueno = st.session_state.user_data['id_dueno']
                mascotas = Mascota.obtener_por_dueno(db, id_dueno)
            elif user_role == 'veterinario':
                # Veterinarios solo ven mascotas que atienden (con citas asignadas)
                id_empleado = st.session_state.user_data['id_empleado']
                query = """
                    SELECT DISTINCT m.*, d.nombre as dueno_nombre 
                    FROM mascotas m 
                    LEFT JOIN duenos d ON m.id_dueno = d.id_dueno
                    INNER JOIN citas c ON m.id_mascota = c.id_mascota
                    WHERE c.id_empleado = %s
                """
                mascotas = db.fetch_all(query, (id_empleado,))
            elif user_role in ['enfermero', 'recepcionista']:
                # Enfermeros y recepcionistas ven todas las mascotas
                mascotas = Mascota.obtener_todas(db)
            else:
                mascotas = []
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

st.markdown("---")
st.info("ℹ️ **Nota**: Para registrar nuevas mascotas, utilice la página de **Citas** → **Nueva Cita**. El sistema le guiará para registrar dueños y mascotas durante el proceso de creación de citas.")
