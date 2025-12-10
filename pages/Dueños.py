import streamlit as st
import sys
import os
import logging

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.db_utils import init_db
from src.entidades.personas.duenos.dueno import Dueno

# Configurar logger
logger = logging.getLogger('pages.duenos')
logger.setLevel(logging.INFO)

st.set_page_config(page_title="Dueños - Clínica Veterinaria", page_icon="👥", layout="wide")

logger.info("Accediendo a módulo de Dueños")

# Verificar autenticación
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    logger.warning("Intento de acceso no autenticado a Dueños")
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower() if st.session_state.user_type == 'empleado' else 'dueño'
user_id = st.session_state.user_data.get('id_empleado' if st.session_state.user_type == 'empleado' else 'id_dueno', 'N/A')
logger.info(f"Usuario autenticado en Dueños: rol={user_role}, id={user_id}")

# Dueños pueden ver solo su información, conserjes no tienen acceso, otros empleados ven según permiso
if user_role == 'conserje':
    logger.warning(f"Intento de acceso no autorizado por conserje (id={user_id})")
    st.error("🚫 Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados.")
    st.stop()

if user_role == 'dueño':
    # Dueños solo ven su propia información
    is_owner_view = True
    logger.info(f"Dueño id={user_id} con vista de solo su información")
elif user_role in ['veterinario', 'enfermero']:
    logger.warning(f"Intento de acceso no autorizado a Dueños por rol={user_role}")
    st.error("🚫 Acceso restringido. Solo recepcionistas pueden gestionar información de dueños.")
    st.stop()
else:
    # Recepcionistas tienen acceso completo
    is_owner_view = False
    logger.info(f"Recepcionista id={user_id} con acceso completo a Dueños")

st.title("👥 Gestión de Dueños")
st.markdown("---")

# Solo mostrar tab de ver para dueños, tabs completos para recepcionistas
if is_owner_view:
    # Dueños solo ven su información, sin opción de editar
    tab1 = st.tabs(["📋 Ver Mi Información"])[0]
    tab3 = None  # No hay tab de búsqueda para dueños
else:
    # Recepcionistas tienen todas las funcionalidades
    tab1, tab3 = st.tabs(["📋 Ver Dueños", "🔍 Buscar"])

# TAB 1: Ver Dueños
with tab1:
    if is_owner_view:
        st.subheader("Mi Información")
    else:
        st.subheader("Lista de Dueños Registrados")
    
    try:
        db = init_db()
        if db.connect():
            if is_owner_view:
                # Dueños solo ven su propia información
                id_dueno = st.session_state.user_data['id_dueno']
                dueno = Dueno.obtener_por_id(db, id_dueno)
                duenos = [dueno] if dueno else []
            else:
                # Recepcionistas ven todos los dueños
                duenos = Dueno.obtener_todos(db)
            db.disconnect()
            
            if duenos:
                st.info(f"📊 Total de dueños registrados: {len(duenos)}")
                
                for dueno in duenos:
                    with st.expander(f"👤 {dueno['nombre']} - DNI: {dueno['dni']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**ID**: {dueno['id_dueno']}")
                            st.write(f"**Nombre**: {dueno['nombre']}")
                            st.write(f"**DNI**: {dueno['dni']}")
                            st.write(f"**Teléfono**: {dueno['telefono']}")
                        
                        with col2:
                            st.write(f"**Email**: {dueno['email']}")
                            st.write(f"**Fecha Nac.**: {dueno['fecha_nacimiento']}")
                            st.write(f"**Dirección**: {dueno['direccion']}")
            else:
                st.warning("No hay dueños registrados")
    
    except Exception as e:
        st.error(f"Error al cargar dueños: {str(e)}")
    
    if not is_owner_view:
        st.markdown("---")
        st.info("ℹ️ **Nota**: Para registrar nuevos dueños, utilice la página de **Citas** → **Nueva Cita**. El sistema le guiará para registrar dueños durante el proceso de creación de citas.")

# TAB 2: Buscar (solo para recepcionistas)
if tab3 is not None:
    with tab3:
        st.subheader("Buscar Dueño")
        
        id_buscar = st.number_input("ID del dueño", min_value=1, step=1)
        if st.button("🔍 Buscar"):
            try:
                db = init_db()
                if db.connect():
                    dueno = Dueno.obtener_por_id(db, id_buscar)
                    db.disconnect()
                    
                    if dueno:
                        st.success("✅ Dueño encontrado")
                        with st.container(border=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**👤 ID:** {dueno['id_dueno']}")
                                st.markdown(f"**📛 Nombre:** {dueno['nombre']}")
                                st.markdown(f"**🆔 DNI:** {dueno['dni']}")
                                st.markdown(f"**📞 Teléfono:** {dueno['telefono']}")
                            with col2:
                                st.markdown(f"**📧 Email:** {dueno['email']}")
                                st.markdown(f"**🎂 Fecha Nacimiento:** {dueno.get('fecha_nacimiento', 'N/A')}")
                                st.markdown(f"**🏠 Dirección:** {dueno.get('direccion', 'N/A')}")
                    else:
                        st.warning("No se encontró el dueño")
            except Exception as e:
                st.error(f"Error: {str(e)}")
