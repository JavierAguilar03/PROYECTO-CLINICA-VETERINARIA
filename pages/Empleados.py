import streamlit as st
import sys
import os
from datetime import date
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.db_utils import init_db
from src.entidades.personas.empleados.empleado import Empleado

# Configurar logger
logger = logging.getLogger('pages.empleados')
logger.setLevel(logging.INFO)

st.set_page_config(page_title="Empleados", page_icon="👨‍⚕️", layout="wide")

logger.info("Accediendo a módulo de Empleados")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    logger.warning("Intento de acceso no autenticado a Empleados")
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

if st.session_state.user_type != "empleado":
    logger.warning(f"Intento de acceso a Empleados por usuario tipo: {st.session_state.user_type}")
    st.error("🚫 Acceso restringido. Solo empleados.")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower()
user_id = st.session_state.user_data.get('id_empleado', 'N/A')
logger.info(f"Usuario autenticado en Empleados: rol={user_role}, id={user_id}")

# Determinar nivel de acceso
if user_role == 'conserje':
    # Conserjes solo ven su propia información
    is_limited_view = True
    can_register = False
    logger.info(f"Conserje id={user_id} con vista limitada")
elif user_role == 'recepcionista':
    # Recepcionistas tienen acceso completo
    is_limited_view = False
    can_register = True
    logger.info(f"Recepcionista id={user_id} con acceso completo")
else:
    # Veterinarios y enfermeros ven todos pero no pueden registrar
    is_limited_view = False
    can_register = False
    logger.info(f"Empleado rol={user_role} con vista de solo lectura")

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
                empleado = Empleado.obtener_por_id(db, id_empleado)
                empleados = [empleado] if empleado else []
            else:
                # Otros empleados ven todos
                empleados = Empleado.obtener_todos(db)
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
                fecha_nac = st.date_input("Fecha de nacimiento*", min_value=date(1900, 1, 1), max_value=date.today())
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
                            id_emp = Empleado.crear(db, nombre, dni, telefono, email, fecha_str, salario, tipo, usuario, password)
                            db.disconnect()
                            if id_emp:
                                st.success(f"✅ Empleado registrado (ID: {id_emp})")
                            else:
                                st.error("Error al registrar")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("⚠️ Complete todos los campos obligatorios")
