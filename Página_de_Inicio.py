import streamlit as st
from src.database_conn.db_conn import DatabaseConnection
from src.logging.log_config import setup_logging
import os

# Configurar logging
setup_logging()

# Configuración de la página
st.set_page_config(
    page_title="Página de Inicio",
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
    """Aplicación principal después del login - Dashboard personalizado."""
    
    # Sidebar con información del usuario y botón de logout
    with st.sidebar:
        st.title("👤 Usuario")
        
        if st.session_state.user_type == "empleado":
            user_role = st.session_state.user_data.get('tipo_empleado', 'N/A')
            st.success(f"**Empleado**: {st.session_state.user_data.get('nombre', 'Usuario')}")
            st.caption(f"Tipo: {user_role}")
        else:
            st.info(f"**Dueño**: {st.session_state.user_data.get('nombre', 'Usuario')}")
        
        st.markdown("---")
        
        # Botón de logout prominente
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.rerun()
        
        st.markdown("---")
        
        # Mostrar páginas disponibles según el rol
        st.caption("**Páginas disponibles:**")
        if st.session_state.user_type == "empleado":
            user_role = st.session_state.user_data.get('tipo_empleado', '').lower()
            
            st.caption("• 🏠 Página de Inicio")
            st.caption("• 📊 Dashboard (estadísticas)")
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
    
    # Contenido principal - Dashboard personalizado
    st.title("🏠 Página de Inicio")
    st.markdown("---")
    
    if st.session_state.user_type == "empleado":
        user_role = st.session_state.user_data.get('tipo_empleado', '').lower()
        nombre = st.session_state.user_data.get('nombre', 'Usuario')
        
        st.markdown(f"### 👋 Bienvenido/a, {nombre}")
        st.caption(f"Rol: {st.session_state.user_data.get('tipo_empleado', 'N/A')}")
        st.markdown("---")
        
        # Dashboard personalizado según rol
        try:
            db = init_db_connection()
            if db.connect():
                
                if user_role == 'veterinario':
                    st.subheader("📊 Tu Panel de Veterinario")
                    
                    col1, col2, col3 = st.columns(3)
                    id_empleado = st.session_state.user_data['id_empleado']
                    
                    # Métricas del veterinario
                    with col1:
                        citas_hoy = db.fetch_all("""
                            SELECT COUNT(*) as total FROM citas 
                            WHERE id_empleado = %s AND fecha = CURDATE()
                        """, (id_empleado,))
                        total_hoy = citas_hoy[0]['total'] if citas_hoy else 0
                        st.metric("Citas Hoy", total_hoy)
                    
                    with col2:
                        citas_pendientes = db.fetch_all("""
                            SELECT COUNT(*) as total FROM citas 
                            WHERE id_empleado = %s AND estado = 'pendiente'
                        """, (id_empleado,))
                        total_pendientes = citas_pendientes[0]['total'] if citas_pendientes else 0
                        st.metric("Citas Pendientes", total_pendientes)
                    
                    with col3:
                        consultas = db.fetch_all("""
                            SELECT COUNT(*) as total FROM consultas co
                            INNER JOIN citas ci ON co.id_cita = ci.id_cita
                            WHERE ci.id_empleado = %s
                        """, (id_empleado,))
                        total_consultas = consultas[0]['total'] if consultas else 0
                        st.metric("Consultas Realizadas", total_consultas)
                    
                    st.markdown("---")
                    st.subheader("📅 Próximas Citas")
                    proximas = db.fetch_all("""
                        SELECT c.*, m.nombre as mascota FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        WHERE c.id_empleado = %s AND c.estado = 'pendiente'
                        ORDER BY c.fecha, c.hora LIMIT 5
                    """, (id_empleado,))
                    
                    if proximas:
                        for cita in proximas:
                            st.info(f"🗓️ {cita['fecha']} a las {cita['hora']} - {cita.get('mascota', 'N/A')} - {cita['motivo']}")
                    else:
                        st.success("✅ No tienes citas pendientes")
                
                elif user_role == 'recepcionista':
                    st.subheader("📊 Panel de Recepción")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        citas_hoy = db.fetch_all("SELECT COUNT(*) as total FROM citas WHERE fecha = CURDATE()")
                        st.metric("Citas Hoy", citas_hoy[0]['total'] if citas_hoy else 0)
                    
                    with col2:
                        citas_pendientes = db.fetch_all("SELECT COUNT(*) as total FROM citas WHERE estado = 'pendiente'")
                        st.metric("Pendientes", citas_pendientes[0]['total'] if citas_pendientes else 0)
                    
                    with col3:
                        facturas_hoy = db.fetch_all("SELECT COUNT(*) as total FROM facturas WHERE fecha = CURDATE()")
                        st.metric("Facturas Hoy", facturas_hoy[0]['total'] if facturas_hoy else 0)
                    
                    with col4:
                        ingresos_hoy = db.fetch_all("SELECT SUM(total) as total FROM facturas WHERE fecha = CURDATE()")
                        ingresos = ingresos_hoy[0]['total'] if ingresos_hoy and ingresos_hoy[0]['total'] else 0
                        st.metric("Ingresos Hoy", f"{ingresos:.2f}€")
                    
                    st.markdown("---")
                    st.subheader("📅 Citas de Hoy")
                    citas_hoy_list = db.fetch_all("""
                        SELECT c.*, m.nombre as mascota, e.nombre as veterinario FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE c.fecha = CURDATE()
                        ORDER BY c.hora
                    """)
                    
                    if citas_hoy_list:
                        for cita in citas_hoy_list:
                            estado_color = "🟢" if cita['estado'] == 'completada' else "🟡" if cita['estado'] == 'pendiente' else "🔴"
                            st.info(f"{estado_color} {cita['hora']} - {cita.get('mascota', 'N/A')} - Dr. {cita.get('veterinario', 'N/A')} - {cita['estado']}")
                    else:
                        st.info("No hay citas programadas para hoy")
                
                elif user_role == 'enfermero':
                    st.subheader("📊 Panel de Enfermería")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        citas_hoy = db.fetch_all("SELECT COUNT(*) as total FROM citas WHERE fecha = CURDATE()")
                        st.metric("Citas Hoy", citas_hoy[0]['total'] if citas_hoy else 0)
                    
                    with col2:
                        mascotas = db.fetch_all("SELECT COUNT(*) as total FROM mascotas")
                        st.metric("Total Mascotas", mascotas[0]['total'] if mascotas else 0)
                    
                    with col3:
                        consultas = db.fetch_all("SELECT COUNT(*) as total FROM consultas")
                        st.metric("Consultas Totales", consultas[0]['total'] if consultas else 0)
                    
                    st.markdown("---")
                    st.subheader("📅 Citas Pendientes")
                    pendientes = db.fetch_all("""
                        SELECT c.*, m.nombre as mascota, e.nombre as veterinario FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE c.estado = 'pendiente'
                        ORDER BY c.fecha, c.hora LIMIT 10
                    """)
                    
                    if pendientes:
                        for cita in pendientes:
                            st.info(f"🗓️ {cita['fecha']} {cita['hora']} - {cita.get('mascota', 'N/A')} - Dr. {cita.get('veterinario', 'N/A')}")
                    else:
                        st.success("✅ No hay citas pendientes")
                
                elif user_role == 'conserje':
                    st.subheader("👋 Panel de Conserje")
                    st.info("""
                    Bienvenido/a al sistema.
                    
                    Puede acceder a su información personal desde la página de **Empleados**.
                    """)
                    
                    id_empleado = st.session_state.user_data['id_empleado']
                    salario = st.session_state.user_data.get('salario', 0)
                    st.metric("Tu Salario", f"{salario}€")
                
                db.disconnect()
        except Exception as e:
            st.error(f"Error al cargar dashboard: {str(e)}")
        
        st.markdown("---")
        st.info("💡 **Consejo**: Use el menú lateral izquierdo para navegar a otras páginas según sus permisos.")
        
    else:  # Dueño
        nombre = st.session_state.user_data.get('nombre', 'Usuario')
        st.markdown(f"### 👋 Bienvenido/a, {nombre}")
        st.caption("Cliente")
        st.markdown("---")
        
        # Dashboard para dueño
        try:
            db = init_db_connection()
            if db.connect():
                id_dueno = st.session_state.user_data['id_dueno']
                
                st.subheader("📊 Tu Panel")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    mascotas = db.fetch_all("SELECT COUNT(*) as total FROM mascotas WHERE id_dueno = %s", (id_dueno,))
                    st.metric("Tus Mascotas", mascotas[0]['total'] if mascotas else 0)
                
                with col2:
                    citas = db.fetch_all("""
                        SELECT COUNT(*) as total FROM citas c
                        INNER JOIN mascotas m ON c.id_mascota = m.id_mascota
                        WHERE m.id_dueno = %s
                    """, (id_dueno,))
                    st.metric("Citas Totales", citas[0]['total'] if citas else 0)
                
                with col3:
                    pendientes = db.fetch_all("""
                        SELECT COUNT(*) as total FROM citas c
                        INNER JOIN mascotas m ON c.id_mascota = m.id_mascota
                        WHERE m.id_dueno = %s AND c.estado = 'pendiente'
                    """, (id_dueno,))
                    st.metric("Citas Pendientes", pendientes[0]['total'] if pendientes else 0)
                
                st.markdown("---")
                st.subheader("🐾 Tus Mascotas")
                mis_mascotas = db.fetch_all("SELECT * FROM mascotas WHERE id_dueno = %s", (id_dueno,))
                
                if mis_mascotas:
                    for mascota in mis_mascotas:
                        st.success(f"🐶 {mascota['nombre']} - {mascota['especie']} ({mascota['raza']})")
                else:
                    st.info("No tienes mascotas registradas. Registra una desde Citas.")
                
                st.markdown("---")
                st.subheader("📅 Próximas Citas")
                proximas = db.fetch_all("""
                    SELECT c.*, m.nombre as mascota, e.nombre as veterinario FROM citas c
                    INNER JOIN mascotas m ON c.id_mascota = m.id_mascota
                    LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                    WHERE m.id_dueno = %s AND c.estado = 'pendiente'
                    ORDER BY c.fecha, c.hora
                """, (id_dueno,))
                
                if proximas:
                    for cita in proximas:
                        st.info(f"🗓️ {cita['fecha']} a las {cita['hora']} - {cita.get('mascota', 'N/A')} - Dr. {cita.get('veterinario', 'N/A')}")
                else:
                    st.success("✅ No tienes citas pendientes")
                
                db.disconnect()
        except Exception as e:
            st.error(f"Error al cargar información: {str(e)}")
        
        st.markdown("---")
        
        # Botón rápido para registrar cita
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📅 Registrar Nueva Cita", use_container_width=True, type="primary"):
                st.switch_page("pages/Citas.py")

# Flujo principal
if st.session_state.authenticated:
    main_app()
else:
    login_page()
