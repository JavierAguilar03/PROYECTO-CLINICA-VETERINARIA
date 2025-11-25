import streamlit as st
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Dueños - Clínica Veterinaria", page_icon="👥", layout="wide")

# Verificar autenticación (solo empleados)
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

if st.session_state.user_type != "empleado":
    st.error("🚫 Acceso restringido. Solo empleados pueden acceder a esta sección.")
    st.stop()

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
tab1, tab2, tab3 = st.tabs(["📋 Ver Dueños", "➕ Nuevo Dueño", "🔍 Buscar"])

# TAB 1: Ver Dueños
with tab1:
    st.subheader("Lista de Dueños Registrados")
    
    try:
        db = init_db()
        if db.connect():
            duenos = db.obtener_todos_duenos()
            db.disconnect()
            
            if duenos:
                st.info(f"📊 Total de dueños registrados: {len(duenos)}")
                
                for dueno in duenos:
                    with st.expander(f"👤 {dueno['nombre']} - DNI: {dueno['dni']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**ID**: {dueno['id_dueño']}")
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

# TAB 2: Nuevo Dueño
with tab2:
    st.subheader("Registrar Nuevo Dueño")
    
    with st.form("nuevo_dueno"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre completo*")
            dni = st.text_input("DNI*")
            telefono = st.text_input("Teléfono*")
        
        with col2:
            email = st.text_input("Email*")
            fecha_nacimiento = st.date_input("Fecha de nacimiento*")
            direccion = st.text_area("Dirección*", height=100)
        
        submitted = st.form_submit_button("👤 Registrar Dueño", use_container_width=True)
        
        if submitted:
            if nombre and dni and telefono and email and fecha_nacimiento and direccion:
                try:
                    db = init_db()
                    if db.connect():
                        fecha_str = fecha_nacimiento.strftime("%Y-%m-%d")
                        id_dueno = db.insertar_dueno(nombre, dni, telefono, email, fecha_str, direccion)
                        db.disconnect()
                        
                        if id_dueno:
                            st.success(f"✅ Dueño registrado exitosamente (ID: {id_dueno})")
                        else:
                            st.error("Error al registrar el dueño")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Por favor complete todos los campos obligatorios (*)")

# TAB 3: Buscar
with tab3:
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
