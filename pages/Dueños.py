import streamlit as st
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Dueños - Clínica Veterinaria", page_icon="👥", layout="wide")

# Verificar autenticación
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower() if st.session_state.user_type == 'empleado' else 'dueño'

# Dueños pueden ver solo su información, conserjes no tienen acceso, otros empleados ven según permiso
if user_role == 'conserje':
    st.error("🚫 Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados.")
    st.stop()

if user_role == 'dueño':
    # Dueños solo ven su propia información
    is_owner_view = True
elif user_role in ['veterinario', 'enfermero']:
    st.error("🚫 Acceso restringido. Solo recepcionistas pueden gestionar información de dueños.")
    st.stop()
else:
    # Recepcionistas tienen acceso completo
    is_owner_view = False

def init_db():
    """Inicializa la conexión a la base de datos."""
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    
    db = DatabaseConnection(host, user, password, database)
    return db

st.title("👥 Gestión de Dueños")
st.markdown("---")

# Tabs
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
                dueno = db.obtener_dueno(id_dueno)
                duenos = [dueno] if dueno else []
            else:
                # Recepcionistas ven todos los dueños
                duenos = db.obtener_todos_duenos()
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

# TAB 2: Buscar
with tab3:
    if is_owner_view:
        st.info("ℹ️ Puede ver su información en la pestaña 'Ver Dueños'.")
    else:
        st.subheader("Buscar Dueño")
        
        id_buscar = st.number_input("ID del dueño", min_value=1, step=1)
        if st.button("🔍 Buscar"):
            try:
                db = init_db()
                if db.connect():
                    dueno = db.obtener_dueno(id_buscar)
                    db.disconnect()
                    
                    if dueno:
                        st.success("Dueño encontrado")
                        st.json(dueno)
                    else:
                        st.warning("No se encontró el dueño")
            except Exception as e:
                st.error(f"Error: {str(e)}")
