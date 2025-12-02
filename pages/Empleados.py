import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Empleados", page_icon="👨‍⚕️", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

if st.session_state.user_type != "empleado":
    st.error("🚫 Acceso restringido. Solo empleados.")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower()

# Determinar nivel de acceso
if user_role == 'conserje':
    # Conserjes solo ven su propia información
    is_limited_view = True
    can_register = False
elif user_role == 'recepcionista':
    # Recepcionistas tienen acceso completo
    is_limited_view = False
    can_register = True
else:
    # Veterinarios y enfermeros ven todos pero no pueden registrar
    is_limited_view = False
    can_register = False

def init_db():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    return DatabaseConnection(host, user, password, database)

st.title("👨‍⚕️ Gestión de Empleados")
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Ver Empleados", "➕ Nuevo Empleado"])

with tab1:
    if is_limited_view:
        st.subheader("Mi Información")
    else:
        st.subheader("Lista de Empleados")
    
    try:
        db = init_db()
        if db.connect():
            if is_limited_view:
                # Conserjes solo ven su propia información
                id_empleado = st.session_state.user_data['id_empleado']
                query = "SELECT * FROM empleados WHERE id_empleado = %s"
                empleado = db.fetch_one(query, (id_empleado,))
                empleados = [empleado] if empleado else []
            else:
                # Otros empleados ven todos
                empleados = db.obtener_todos_empleados()
            db.disconnect()
            
            if empleados:
                for empleado in empleados:
                    with st.expander(f"👤 {empleado['nombre']} - {empleado['tipo_empleado']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID**: {empleado['id_empleado']}")
                            st.write(f"**DNI**: {empleado['dni']}")
                            st.write(f"**Teléfono**: {empleado['telefono']}")
                        with col2:
                            st.write(f"**Email**: {empleado['email']}")
                            st.write(f"**Salario**: {empleado['salario']} €")
                            st.write(f"**Usuario**: {empleado.get('usuario', 'N/A')}")
            else:
                st.warning("No hay empleados registrados")
    except Exception as e:
        st.error(f"Error: {str(e)}")

with tab2:
    if not can_register:
        st.warning("⚠️ Solo recepcionistas pueden registrar nuevos empleados.")
    else:
        st.subheader("Registrar Nuevo Empleado")
        with st.form("nuevo_empleado"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo*")
                dni = st.text_input("DNI*")
                telefono = st.text_input("Teléfono*")
                email = st.text_input("Email*")
            with col2:
                fecha_nac = st.date_input("Fecha de nacimiento*")
                salario = st.number_input("Salario*", min_value=0.0, step=100.0)
                tipo = st.selectbox("Tipo*", ["Veterinario", "Recepcionista", "Enfermero", "Conserje"])
                usuario = st.text_input("Usuario (opcional)")
            
            password = st.text_input("Contraseña (opcional)", type="password")
            
            if st.form_submit_button("👨‍⚕️ Registrar Empleado", use_container_width=True):
                if nombre and dni and telefono and email and salario and tipo:
                    try:
                        db = init_db()
                        if db.connect():
                            fecha_str = fecha_nac.strftime("%Y-%m-%d")
                            id_emp = db.insertar_empleado(nombre, dni, telefono, email, fecha_str, salario, tipo, usuario, password)
                            db.disconnect()
                            if id_emp:
                                st.success(f"✅ Empleado registrado (ID: {id_emp})")
                            else:
                                st.error("Error al registrar")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("⚠️ Complete todos los campos obligatorios")
