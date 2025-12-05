import streamlit as st
from src.database_conn.db_conn import DatabaseConnection
from src.logging.log_config import setup_logging
import os

# Configurar logging
setup_logging()

# Configuración de la página
st.set_page_config(
    page_title="Clínica Veterinaria - Sistema de Gestión",
    page_icon="🐾",
    layout="wide"
)

# Inicializar session_state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

def init_db_connection():
    """Inicializa la conexión a la base de datos."""
    host = ""
    user = ""
    password = ""
    database = ""
    db = DatabaseConnection(host, user, password, database)
    return db

def authenticate_employee(username: str, password: str):
    """Autentica a un empleado."""
    try:
        db = init_db_connection()
        if db.connect():
            if db.validate_user(username, password):
                # Obtener datos del empleado
                query = "SELECT * FROM empleados WHERE usuario = %s"
                user_data = db.fetch_one(query, (username,))
                db.disconnect()
                return True, user_data
            db.disconnect()
    except Exception as e:
        st.error(f"Error al autenticar: {str(e)}")
    return False, None

def login_page():
    """Página de inicio de sesión."""
    st.title("🐾 Sistema de Gestión de Clínica Veterinaria")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Inicio de Sesión")
        
        # Selector de tipo de usuario
        user_type = st.radio(
            "Seleccione tipo de usuario:",
            ["Empleado", "Dueño de Mascota"],
            horizontal=True
        )
        
        if user_type == "Empleado":
            st.info("👨‍⚕️ **Empleados**: Ingrese sus credenciales para acceso completo al sistema")
            
            with st.form("employee_login"):
                username = st.text_input("Usuario", placeholder="usuario_empleado")
                password = st.text_input("Contraseña", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Iniciar Sesión", use_container_width=True)
                
                if submit:
                    if username and password:
                        with st.spinner("Autenticando..."):
                            success, user_data = authenticate_employee(username, password)
                            if success:
                                st.session_state.authenticated = True
                                st.session_state.user_type = "empleado"
                                st.session_state.user_data = user_data
                                st.success("✅ Autenticación exitosa")
                                st.rerun()
                            else:
                                st.error("❌ Credenciales incorrectas")
                    else:
                        st.warning("⚠️ Por favor complete todos los campos")
        
        else:  # Dueño
            st.info("🏠 **Dueños**: Acceso limitado para registro de citas")
            
            with st.form("owner_login"):
                dni = st.text_input("DNI", placeholder="12345678A")
                email = st.text_input("Email", placeholder="correo@ejemplo.com")
                submit = st.form_submit_button("Acceder", use_container_width=True)
                
                if submit:
                    if dni and email:
                        # Verificar dueño en la base de datos
                        try:
                            db = init_db_connection()
                            if db.connect():
                                query = "SELECT * FROM duenos WHERE dni = %s AND email = %s"
                                owner_data = db.fetch_one(query, (dni, email))
                                db.disconnect()
                                
                                if owner_data:
                                    st.session_state.authenticated = True
                                    st.session_state.user_type = "dueño"
                                    st.session_state.user_data = owner_data
                                    st.success("✅ Acceso concedido")
                                    st.rerun()
                                else:
                                    st.error("❌ DNI o email no encontrados")
                        except Exception as e:
                            st.error(f"Error al verificar: {str(e)}")
                    else:
                        st.warning("⚠️ Por favor complete todos los campos")
        
        st.markdown("---")
        st.caption("💡 **Nota**: Si es un nuevo dueño, contacte con la recepción para registrarse.")

def main_app():
    """Aplicación principal después del login."""
    
    # Redirigir a empleados al Dashboard automáticamente
    if st.session_state.user_type == "empleado":
        st.switch_page("pages/Dashboard.py")
    
    # Sidebar con información del usuario
    with st.sidebar:
        st.title("👤 Usuario")
        
        if st.session_state.user_type == "empleado":
            user_role = st.session_state.user_data.get('tipo_empleado', 'N/A')
            st.success(f"**Empleado**: {st.session_state.user_data.get('nombre', 'Usuario')}")
            st.caption(f"Tipo: {user_role}")
        else:
            st.info(f"**Dueño**: {st.session_state.user_data.get('nombre', 'Usuario')}")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.rerun()
        
        st.markdown("---")
        
        # Mostrar páginas disponibles según el rol
        st.caption("**Páginas disponibles:**")
        if st.session_state.user_type == "empleado":
            user_role = st.session_state.user_data.get('tipo_empleado', '').lower()
            
            st.caption("• 📊 Dashboard (vista general)")
            if user_role == 'conserje':
                st.caption("• 👨‍⚕️ Empleados (solo tu info)")
            elif user_role == 'veterinario':
                st.caption("• 📅 Citas (solo las tuyas)")
                st.caption("• 🐾 Mascotas (solo las que atiendes)")
                st.caption("• 🏥 Consultas (solo las tuyas)")
                st.caption("• 👨‍⚕️ Empleados (info general)")
            elif user_role == 'enfermero':
                st.caption("• 📅 Citas (todas)")
                st.caption("• 🐾 Mascotas (todas)")
                st.caption("• 🏥 Consultas (todas)")
                st.caption("• 👨‍⚕️ Empleados (info general)")
            elif user_role == 'recepcionista':
                st.caption("• 📅 Citas (todas)")
                st.caption("• 🐾 Mascotas (todas)")
                st.caption("• 🏥 Consultas (todas)")
                st.caption("• 💰 Facturas (todas)")
                st.caption("• 👥 Dueños (todos)")
                st.caption("• 👨‍⚕️ Empleados (todos + registro)")
        else:  # Dueño
            st.caption("• 📅 Citas (solo las de tus mascotas)")
            st.caption("• 🐾 Mascotas (solo las tuyas)")
            st.caption("• 👥 Dueños (solo tu info)")
        
        st.markdown("---")
        st.caption("Sistema de Gestión v1.0")
    
    # Contenido principal
    st.title("🐾 Sistema de Gestión de Clínica Veterinaria")
    
    if st.session_state.user_type == "empleado":
        user_role = st.session_state.user_data.get('tipo_empleado', '').lower()
        
        st.markdown(f"""
        ### Panel de Empleado - {st.session_state.user_data.get('tipo_empleado', 'N/A')}
        
        Bienvenido al sistema de gestión.
        """)
        
        # Mostrar accesos según rol
        if user_role == 'conserje':
            st.info("""
            **Acceso Limitado - Conserje**
            
            Como conserje, solo tienes acceso a:
            - 👨‍⚕️ **Empleados**: Ver tu información personal y salario
            
            👈 Accede desde el menú lateral.
            """)
            
        elif user_role == 'veterinario':
            st.markdown("""
            **Accesos disponibles:**
            
            - 📋 **Citas**: Ver y gestionar solo las citas asignadas a ti
            - 🐕 **Mascotas**: Ver información de las mascotas que atiendes
            - 🏥 **Consultas**: Registrar diagnósticos y tratamientos de tus citas
            - 👨‍💼 **Empleados**: Ver información general del equipo
            
            👈 **Use el menú lateral** para navegar entre secciones.
            """)
            
        elif user_role == 'enfermero':
            st.markdown("""
            **Accesos disponibles:**
            
            - 📋 **Citas**: Ver todas las citas de la clínica
            - 🐕 **Mascotas**: Acceso completo a información de todas las mascotas
            - 🏥 **Consultas**: Ver todas las consultas médicas
            - 👨‍💼 **Empleados**: Ver información del equipo
            
            👈 **Use el menú lateral** para navegar entre secciones.
            """)
            
        elif user_role == 'recepcionista':
            st.markdown("""
            **Acceso Completo - Recepcionista**
            
            Como recepcionista, tienes acceso total a:
            
            - 📋 **Gestionar Citas**: Ver, crear y modificar todas las citas
            - 🏥 **Consultas**: Ver todas las consultas médicas
            - 💰 **Facturas**: Generar y gestionar facturas
            - 🐕 **Mascotas**: Gestionar información de todas las mascotas
            - 👥 **Dueños**: Registrar y gestionar información de clientes
            - 👨‍💼 **Empleados**: Administrar todo el personal
            
            👈 **Use el menú lateral** para navegar entre las diferentes secciones.
            """)
        
        st.info("💡 **Consejo**: Las páginas están disponibles en el menú lateral izquierdo según tus permisos.")
        
    else:  # Dueño
        st.markdown("""
        ### Panel de Cliente
        
        Bienvenido. Desde aquí puede:
        
        - 📅 **Registrar Citas**: Solicitar nuevas citas para sus mascotas
        - 🐾 **Ver Mascotas**: Consultar y registrar información de sus mascotas
        - 📜 **Historial**: Ver citas previas de sus mascotas
        - 👤 **Mi Perfil**: Ver su información personal
        
        👈 **Use el menú lateral** para acceder a las opciones disponibles.
        """)
        
        st.warning("⚠️ **Acceso Limitado**: Como dueño, solo tiene acceso a información relacionada con sus mascotas.")
        
        # Botón rápido para citas
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📅 Ir a Citas", use_container_width=True, type="primary"):
                st.switch_page("pages/Citas.py")

# Flujo principal
if st.session_state.authenticated:
    main_app()
else:
    login_page()
