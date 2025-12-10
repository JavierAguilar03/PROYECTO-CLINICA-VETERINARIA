import streamlit as st
import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.db_utils import init_db
from src.entidades.mascotas.mascota import Mascota

# Configurar logger
logger = logging.getLogger('pages.mascotas')
logger.setLevel(logging.INFO)

st.set_page_config(page_title="Mascotas", page_icon="🐾", layout="wide")

logger.info("Accediendo a módulo de Mascotas")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    logger.warning("Intento de acceso no autenticado a Mascotas")
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower() if st.session_state.user_type == 'empleado' else 'dueño'
user_id = st.session_state.user_data.get('id_empleado' if st.session_state.user_type == 'empleado' else 'id_dueno', 'N/A')
logger.info(f"Usuario autenticado en Mascotas: rol={user_role}, id={user_id}")

# Conserjes NO tienen acceso a mascotas
if user_role == 'conserje':
    logger.warning(f"Intento de acceso no autorizado por conserje (id={user_id})")
    st.error("🚫 Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados.")
    st.stop()

st.title("🐾 Gestión de Mascotas")
st.markdown("---")

tab1 = st.tabs(["📋 Ver Mascotas"])[0]

with tab1:
    st.subheader("Lista de Mascotas")
    try:
        logger.info(f"Cargando lista de mascotas para rol={user_role}")
        db = init_db()
        if db.connect():
            logger.info("Conexión DB exitosa para listar mascotas")
            # Filtrar según rol
            if user_role == 'dueño':
                # Dueños solo ven sus mascotas
                id_dueno = st.session_state.user_data['id_dueno']
                logger.debug(f"Obteniendo mascotas del dueño id={id_dueno}")
                mascotas = Mascota.obtener_por_dueno(db, id_dueno)
            elif user_role == 'veterinario':
                # Veterinarios solo ven mascotas que atienden (con citas asignadas)
                id_empleado = st.session_state.user_data['id_empleado']
                logger.debug(f"Obteniendo mascotas atendidas por veterinario id={id_empleado}")
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
                logger.debug("Obteniendo todas las mascotas")
                mascotas = Mascota.obtener_todas(db)
            else:
                mascotas = []
            db.disconnect()
            
            if mascotas:
                st.info(f"📊 Total de mascotas: {len(mascotas)}")
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
                            # Obtener nombre del dueño si no está en el resultado
                            if 'dueno_nombre' in mascota and mascota['dueno_nombre']:
                                st.write(f"**Dueño**: {mascota['dueno_nombre']}")
                            elif 'id_dueno' in mascota:
                                # Consultar nombre del dueño
                                from src.entidades.personas.duenos.dueno import Dueno
                                db_temp = init_db()
                                if db_temp.connect():
                                    dueno_info = Dueno.obtener_por_id(db_temp, mascota['id_dueno'])
                                    db_temp.disconnect()
                                    if dueno_info:
                                        st.write(f"**Dueño**: {dueno_info['nombre']}")
                                    else:
                                        st.write(f"**Dueño**: N/A")
                            else:
                                st.write(f"**Dueño**: N/A")
            else:
                st.warning("No hay mascotas registradas")
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("---")
st.info("ℹ️ **Nota**: Para registrar nuevas mascotas, utilice la página de **Citas** → **Nueva Cita**. El sistema le guiará para registrar dueños y mascotas durante el proceso de creación de citas.")
