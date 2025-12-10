import streamlit as st
import sys
import os
from datetime import datetime, date
import logging

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.db_utils import init_db
from src.entidades.administrativo.cita import Cita
from src.entidades.administrativo.consulta import Consulta
from src.entidades.administrativo.factura import Factura
from src.entidades.mascotas.mascota import Mascota
from src.entidades.personas.duenos.dueno import Dueno
from src.entidades.personas.empleados.empleado import Empleado

# Configurar logger para este módulo
logger = logging.getLogger('pages.citas')
logger.setLevel(logging.INFO)

st.set_page_config(page_title="Citas - Clínica Veterinaria", page_icon="📅", layout="wide")

logger.info("Accediendo a módulo de Citas")

# Verificar autenticación
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    logger.warning("Intento de acceso no autenticado a Citas")
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
user_role = st.session_state.user_data.get('tipo_empleado', '').lower() if st.session_state.user_type == 'empleado' else 'dueño'
user_id = st.session_state.user_data.get('id_empleado' if st.session_state.user_type == 'empleado' else 'id_dueno', 'N/A')
logger.info(f"Usuario autenticado: rol={user_role}, id={user_id}")

# Conserjes NO tienen acceso a citas
if user_role == 'conserje':
    logger.warning(f"Intento de acceso no autorizado por conserje (id={user_id})")
    st.error("🚫 Acceso restringido. Los conserjes solo pueden acceder a la sección de Empleados.")
    st.stop()

@st.dialog("🏥 Completar Cita y Registrar Consulta")
def modal_completar_cita(cita):
    """Modal para completar una cita y registrar consulta con factura."""
    logger.info(f"Abriendo modal para completar cita ID={cita['id_cita']}")
    
    st.write(f"**Cita #{cita['id_cita']}**")
    st.write(f"**Mascota:** {cita.get('mascota_nombre', 'N/A')}")
    st.write(f"**Motivo:** {cita['motivo']}")
    st.write(f"**Fecha:** {cita['fecha']} {cita['hora']}")
    st.markdown("---")
    
    with st.form("form_completar_cita"):
        st.subheader("📋 Información de Consulta")
        diagnostico = st.text_area("Diagnóstico*", height=120, placeholder="Describa el diagnóstico de la consulta...")
        tratamiento = st.text_area("Tratamiento*", height=120, placeholder="Describa el tratamiento recomendado...")
        observaciones = st.text_area("Observaciones", height=80, placeholder="Observaciones adicionales (opcional)")
        
        st.markdown("---")
        st.subheader("💰 Información de Factura")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            total_factura = st.number_input("Total a Cobrar (€)*", min_value=0.0, max_value=1000000.0, step=5.0, value=50.0)
        with col_f2:
            metodo_pago = st.selectbox("Método de Pago*", ["efectivo", "tarjeta", "transferencia", "paypal"])
        
        submitted = st.form_submit_button("✅ Completar Cita y Generar Factura", use_container_width=True)
        
        if submitted:
            logger.info(f"Procesando completar cita ID={cita['id_cita']}, total={total_factura}, metodo_pago={metodo_pago}")
            
            if diagnostico and tratamiento and total_factura > 0:
                try:
                    db = init_db()
                    if db.connect():
                        logger.info(f"Conexión DB exitosa para completar cita ID={cita['id_cita']}")
                        
                        # 1. Actualizar estado de la cita a completada usando entidad Cita
                        logger.debug(f"Actualizando estado cita ID={cita['id_cita']} a 'completada'")
                        Cita.actualizar_estado(db, cita['id_cita'], "completada")
                        logger.info(f"Cita ID={cita['id_cita']} marcada como completada")
                        
                        # 2. Registrar la consulta usando entidad Consulta
                        logger.debug(f"Creando consulta para cita ID={cita['id_cita']}")
                        id_consulta = Consulta.crear(db, cita['id_cita'], diagnostico, tratamiento, observaciones)
                        
                        if id_consulta:
                            logger.info(f"Consulta ID={id_consulta} creada exitosamente para cita ID={cita['id_cita']}")
                            
                            # 3. Generar factura automáticamente usando entidad Factura
                            fecha_hoy = date.today().strftime("%Y-%m-%d")
                            logger.debug(f"Generando factura para consulta ID={id_consulta}, total={total_factura}")
                            id_factura = Factura.crear(db, id_consulta, total_factura, metodo_pago, fecha_hoy)
                            
                            db.disconnect()
                            
                            if id_factura:
                                logger.info(f"Factura ID={id_factura} generada exitosamente. Proceso completado.")
                                st.success(f"""✅ **CITA COMPLETADA EXITOSAMENTE**
                                
                                - **Consulta ID:** {id_consulta}
                                - **Factura ID:** {id_factura}
                                - **Total:** {total_factura}€
                                - **Método de Pago:** {metodo_pago}
                                """)
                                st.balloons()
                                st.session_state.cita_completada = True
                                st.rerun()
                            else:
                                logger.error(f"Error al generar factura para consulta ID={id_consulta}")
                                st.error("⚠️ Consulta registrada pero error al generar factura")
                        else:
                            logger.error(f"Error al registrar consulta para cita ID={cita['id_cita']}")
                            st.error("Error al registrar la consulta")
                            db.disconnect()
                    else:
                        logger.error("Error al conectar a la base de datos para completar cita")
                        st.error("Error de conexión a la base de datos")
                except Exception as e:
                    logger.exception(f"Excepción al completar cita ID={cita['id_cita']}: {str(e)}")
                    st.error(f"Error: {str(e)}")
            else:
                logger.warning(f"Intento de completar cita ID={cita['id_cita']} con campos obligatorios vacíos")
                st.warning("⚠️ Complete los campos obligatorios y asegúrese de que el total sea mayor a 0")

st.title("📅 Gestión de Citas")
st.markdown("---")

# Verificar si se completó una cita y limpiar el flag
if 'cita_completada' in st.session_state and st.session_state.cita_completada:
    st.success("✅ Cita completada exitosamente. Consulta y factura registradas.")
    del st.session_state.cita_completada

# Inicializar el índice del tab activo
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["📋 Ver Citas", "➕ Nueva Cita", "🔍 Buscar"])

# TAB 1: Ver Citas
with tab1:
    st.subheader("Lista de Citas")
    
    # Mostrar mensaje de éxito si se acaba de crear una cita
    if 'cita_creada_id' in st.session_state:
        info = st.session_state.cita_creada_info
        st.success(f"""
        ✅ **CITA REGISTRADA EXITOSAMENTE**
        
        - **ID Cita:** {st.session_state.cita_creada_id}
        - **Dueño:** {info['dueno']}
        - **Mascota ID:** {info['mascota_id']}
        - **Fecha:** {info['fecha']} a las {info['hora']}
        """)
        st.balloons()
        # Limpiar el mensaje después de mostrarlo
        del st.session_state.cita_creada_id
        del st.session_state.cita_creada_info
    
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_estado = st.selectbox(
            "Filtrar por estado:",
            ["Todas", "pendiente", "completada", "cancelada"]
        )
    
    try:
        db = init_db()
        if db.connect():
            # Filtrar según el rol del usuario
            if user_role == 'dueño':
                # Dueños solo ven citas de sus mascotas
                id_dueno = st.session_state.user_data['id_dueno']
                if filter_estado == "Todas":
                    query = """
                        SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                        FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE m.id_dueno = %s
                        ORDER BY c.fecha DESC, c.hora DESC
                    """
                    citas = Cita.obtener_todas_filtradas(db, query, (id_dueno,))
                else:
                    query = """
                        SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                        FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE m.id_dueno = %s AND c.estado = %s
                        ORDER BY c.fecha DESC, c.hora DESC
                    """
                    citas = Cita.obtener_todas_filtradas(db, query, (id_dueno, filter_estado))
            elif user_role == 'veterinario':
                # Veterinarios solo ven citas asignadas a ellos
                id_empleado = st.session_state.user_data['id_empleado']
                if filter_estado == "Todas":
                    query = """
                        SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                        FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE c.id_empleado = %s
                        ORDER BY c.fecha DESC, c.hora DESC
                    """
                    citas = Cita.obtener_todas_filtradas(db, query, (id_empleado,))
                else:
                    query = """
                        SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                        FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE c.id_empleado = %s AND c.estado = %s
                        ORDER BY c.fecha DESC, c.hora DESC
                    """
                    citas = Cita.obtener_todas_filtradas(db, query, (id_empleado, filter_estado))
            elif user_role in ['enfermero', 'recepcionista']:
                # Enfermeros y recepcionistas ven todas las citas
                if filter_estado == "Todas":
                    query = """
                        SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                        FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        ORDER BY c.fecha DESC, c.hora DESC
                    """
                    citas = Cita.obtener_todas_filtradas(db, query)
                else:
                    query = """
                        SELECT c.*, m.nombre as mascota_nombre, e.nombre as empleado_nombre
                        FROM citas c
                        LEFT JOIN mascotas m ON c.id_mascota = m.id_mascota
                        LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
                        WHERE c.estado = %s
                        ORDER BY c.fecha DESC, c.hora DESC
                    """
                    citas = Cita.obtener_todas_filtradas(db, query, (filter_estado,))
            else:
                citas = []
            
            db.disconnect()
            
            if citas:
                logger.info(f"Se encontraron {len(citas)} citas para el filtro: {filter_estado}, rol: {user_role}")
                st.info(f"📊 Total de citas: {len(citas)}")
                
                for cita in citas:
                    with st.expander(f"🗓️ Cita #{cita['id_cita']} - {cita['fecha']} {cita['hora']} - {cita['estado'].upper()}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Mascota**: {cita.get('mascota_nombre', 'N/A')} (ID: {cita['id_mascota']})")
                            st.write(f"**Empleado**: {cita.get('empleado_nombre', 'N/A')} (ID: {cita['id_empleado']})")
                            st.write(f"**Motivo**: {cita['motivo']}")
                        
                        with col2:
                            st.write(f"**Estado**: {cita['estado']}")
                            st.write(f"**Fecha**: {cita['fecha']}")
                            st.write(f"**Hora**: {cita['hora']}")
                        
                        # Acciones (solo para empleados y solo si la cita está pendiente)
                        if st.session_state.user_type == "empleado" and cita['estado'].lower() == "pendiente":
                            col_btn1, col_btn2, col_btn3 = st.columns(3)
                            with col_btn1:
                                if st.button("✅ Completar", key=f"complete_{cita['id_cita']}"):
                                    modal_completar_cita(cita)
                            
                            with col_btn2:
                                if st.button("❌ Cancelar", key=f"cancel_{cita['id_cita']}"):
                                    logger.info(f"Cancelando cita ID={cita['id_cita']}")
                                    db2 = init_db()
                                    if db2.connect():
                                        Cita.actualizar_estado(db2, cita['id_cita'], "cancelada")
                                        db2.disconnect()
                                        logger.info(f"Cita ID={cita['id_cita']} cancelada exitosamente")
                                        st.success("Cita cancelada")
                                        st.rerun()
                                    else:
                                        logger.error(f"Error de conexión al intentar cancelar cita ID={cita['id_cita']}")
            else:
                logger.info(f"No se encontraron citas para el filtro: {filter_estado}, rol: {user_role}")
                st.warning("No hay citas registradas")
    
    except Exception as e:
        logger.exception(f"Error al cargar citas: {str(e)}")
        st.error(f"Error al cargar citas: {str(e)}")

# TAB 2: Nueva Cita
with tab2:
    st.subheader("Registrar Nueva Cita")
    
    # Paso 1: Identificar o registrar dueño
    st.markdown("### 📝 Paso 1: Dueño")
    
    tipo_dueno = st.radio(
        "Seleccione una opción:",
        ["Dueño Existente", "Nuevo Dueño"],
        horizontal=True,
        key="tipo_dueno"
    )
    
    id_dueno_seleccionado = None
    dueno_nombre_display = ""
    
    if tipo_dueno == "Dueño Existente":
        st.markdown("#### Buscar Dueño por DNI y Nombre")
        col_search1, col_search2 = st.columns(2)
        
        with col_search1:
            dni_buscar = st.text_input("DNI del Dueño*", placeholder="12345678A", key="dni_buscar")
        with col_search2:
            nombre_buscar = st.text_input("Nombre del Dueño*", placeholder="Juan Pérez", key="nombre_buscar")
        
        if st.button("🔍 Buscar Dueño", key="btn_buscar_dueno"):
            if dni_buscar and nombre_buscar:
                try:
                    db = init_db()
                    if db.connect():
                        query = "SELECT * FROM duenos WHERE dni = %s AND nombre LIKE %s"
                        duenos_encontrados = Dueno.buscar(db, query, (dni_buscar, f"%{nombre_buscar}%"))
                        db.disconnect()
                        
                        if duenos_encontrados:
                            if len(duenos_encontrados) == 1:
                                st.session_state.dueno_encontrado = duenos_encontrados[0]
                                st.success(f"✅ Dueño encontrado: {duenos_encontrados[0]['nombre']} (DNI: {duenos_encontrados[0]['dni']})")
                            else:
                                st.session_state.duenos_multiples = duenos_encontrados
                                st.warning(f"⚠️ Se encontraron {len(duenos_encontrados)} dueños. Seleccione uno:")
                        else:
                            st.error("❌ No se encontró ningún dueño con ese DNI y nombre")
                            st.session_state.dueno_encontrado = None
                except Exception as e:
                    st.error(f"Error al buscar: {str(e)}")
            else:
                st.warning("⚠️ Ingrese DNI y nombre para buscar")
        
        # Mostrar dueños encontrados
        if 'dueno_encontrado' in st.session_state and st.session_state.dueno_encontrado:
            dueno = st.session_state.dueno_encontrado
            id_dueno_seleccionado = dueno['id_dueno']
            dueno_nombre_display = dueno['nombre']
            
            with st.container(border=True):
                st.markdown("**✅ Dueño Seleccionado:**")
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write(f"**Nombre:** {dueno['nombre']}")
                    st.write(f"**DNI:** {dueno['dni']}")
                with col_info2:
                    st.write(f"**Teléfono:** {dueno['telefono']}")
                    st.write(f"**Email:** {dueno['email']}")
        
        elif 'duenos_multiples' in st.session_state and st.session_state.duenos_multiples:
            dueno_seleccion = st.selectbox(
                "Seleccione el dueño correcto:",
                options=range(len(st.session_state.duenos_multiples)),
                format_func=lambda i: f"{st.session_state.duenos_multiples[i]['nombre']} - {st.session_state.duenos_multiples[i]['dni']} - Tel: {st.session_state.duenos_multiples[i]['telefono']}"
            )
            if st.button("Confirmar Selección"):
                st.session_state.dueno_encontrado = st.session_state.duenos_multiples[dueno_seleccion]
                del st.session_state.duenos_multiples
                st.rerun()
    
    else:  # Nuevo Dueño
        st.markdown("#### Registrar Nuevo Dueño")
        with st.form("form_nuevo_dueno"):
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                nuevo_dueno_nombre = st.text_input("Nombre Completo*", key="nuevo_dueno_nombre")
                nuevo_dueno_dni = st.text_input("DNI*", key="nuevo_dueno_dni", placeholder="12345678A")
                nuevo_dueno_telefono = st.text_input("Teléfono*", key="nuevo_dueno_telefono", placeholder="666777888")
            with col_d2:
                nuevo_dueno_email = st.text_input("Email*", key="nuevo_dueno_email", placeholder="correo@ejemplo.com")
                nuevo_dueno_fecha_nac = st.date_input("Fecha de Nacimiento*", key="nuevo_dueno_fecha_nac", 
                                                       min_value=date(1900, 1, 1), max_value=date.today())
                nuevo_dueno_direccion = st.text_input("Dirección", key="nuevo_dueno_direccion")
            
            submit_dueno = st.form_submit_button("➕ Registrar Dueño", use_container_width=True)
            
            if submit_dueno:
                if nuevo_dueno_nombre and nuevo_dueno_dni and nuevo_dueno_telefono and nuevo_dueno_email:
                    try:
                        db = init_db()
                        if db.connect():
                            fecha_nac_str = nuevo_dueno_fecha_nac.strftime("%Y-%m-%d")
                            id_dueno_nuevo = Dueno.crear(
                                db, nuevo_dueno_nombre, nuevo_dueno_dni, nuevo_dueno_telefono,
                                nuevo_dueno_email, fecha_nac_str, nuevo_dueno_direccion or ""
                            )
                            db.disconnect()
                            
                            if id_dueno_nuevo:
                                st.session_state.dueno_encontrado = {
                                    'id_dueno': id_dueno_nuevo,
                                    'nombre': nuevo_dueno_nombre,
                                    'dni': nuevo_dueno_dni,
                                    'telefono': nuevo_dueno_telefono,
                                    'email': nuevo_dueno_email
                                }
                                st.success(f"✅ Dueño registrado exitosamente (ID: {id_dueno_nuevo})")
                                st.rerun()
                            else:
                                st.error("Error al registrar el dueño")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("⚠️ Complete los campos obligatorios marcados con *")
        
        if 'dueno_encontrado' in st.session_state and st.session_state.dueno_encontrado:
            dueno = st.session_state.dueno_encontrado
            id_dueno_seleccionado = dueno['id_dueno']
            dueno_nombre_display = dueno['nombre']
    
    # Paso 2: Seleccionar o registrar mascota (solo si hay dueño seleccionado)
    if id_dueno_seleccionado:
        st.markdown("---")
        st.markdown("### 🐾 Paso 2: Mascota")
        
        tipo_mascota = st.radio(
            "Seleccione una opción:",
            ["Mascota Existente", "Nueva Mascota"],
            horizontal=True,
            key="tipo_mascota"
        )
        
        id_mascota_seleccionada = None
        
        if tipo_mascota == "Mascota Existente":
            try:
                db = init_db()
                if db.connect():
                    mascotas_dueno = Mascota.obtener_por_dueno(db, id_dueno_seleccionado)
                    db.disconnect()
                    
                    if mascotas_dueno:
                        mascota_options = {
                            f"{m['nombre']} - {m['especie']} ({m['raza']})": m['id_mascota'] 
                            for m in mascotas_dueno
                        }
                        mascota_selected = st.selectbox("Seleccione la Mascota:", list(mascota_options.keys()))
                        id_mascota_seleccionada = mascota_options[mascota_selected]
                        
                        # Mostrar info de la mascota
                        mascota_info = next(m for m in mascotas_dueno if m['id_mascota'] == id_mascota_seleccionada)
                        with st.container(border=True):
                            st.markdown("**Información de la Mascota:**")
                            col_m1, col_m2 = st.columns(2)
                            with col_m1:
                                st.write(f"**Nombre:** {mascota_info['nombre']}")
                                st.write(f"**Especie:** {mascota_info['especie']}")
                                st.write(f"**Raza:** {mascota_info['raza']}")
                            with col_m2:
                                st.write(f"**Peso:** {mascota_info['peso']} kg")
                                st.write(f"**Sexo:** {mascota_info['sexo']}")
                                st.write(f"**Fecha Nac.:** {mascota_info.get('fecha_nacimiento', 'N/A')}")
                    else:
                        st.info(f"ℹ️ El dueño {dueno_nombre_display} no tiene mascotas registradas. Registre una nueva mascota.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        else:  # Nueva Mascota
            st.markdown("#### Registrar Nueva Mascota")
            # Verificar si ya se registró una mascota
            mascota_ya_registrada = 'mascota_registrada' in st.session_state
            
            if mascota_ya_registrada:
                st.info("✅ Mascota ya registrada. Complete los detalles de la cita abajo.")
            
            with st.form("form_nueva_mascota"):
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    nueva_mascota_nombre = st.text_input("Nombre*", key="nueva_mascota_nombre", disabled=mascota_ya_registrada)
                    nueva_mascota_especie = st.text_input("Especie*", key="nueva_mascota_especie", placeholder="Perro, Gato, etc.", disabled=mascota_ya_registrada)
                    nueva_mascota_raza = st.text_input("Raza*", key="nueva_mascota_raza", disabled=mascota_ya_registrada)
                with col_m2:
                    nueva_mascota_peso = st.number_input("Peso (kg)*", min_value=0.1, max_value=500000.0, step=0.1, key="nueva_mascota_peso", disabled=mascota_ya_registrada)
                    nueva_mascota_sexo = st.selectbox("Sexo*", ["Macho", "Hembra"], key="nueva_mascota_sexo", disabled=mascota_ya_registrada)
                    nueva_mascota_fecha_nac = st.date_input("Fecha de Nacimiento*", key="nueva_mascota_fecha_nac",
                                                            min_value=date(1900, 1, 1), max_value=date.today(), disabled=mascota_ya_registrada)
                
                submit_mascota = st.form_submit_button("➕ Registrar Mascota", use_container_width=True, disabled=mascota_ya_registrada)
                
                if submit_mascota:
                    if nueva_mascota_nombre and nueva_mascota_especie and nueva_mascota_raza:
                        try:
                            db = init_db()
                            if db.connect():
                                fecha_nac_str = nueva_mascota_fecha_nac.strftime("%Y-%m-%d")
                                id_mascota_nueva = Mascota.crear(
                                    db, nueva_mascota_nombre, nueva_mascota_especie, nueva_mascota_raza,
                                    fecha_nac_str, nueva_mascota_peso, nueva_mascota_sexo, id_dueno_seleccionado
                                )
                                db.disconnect()
                                
                                if id_mascota_nueva:
                                    st.session_state.mascota_registrada = id_mascota_nueva
                                    st.success(f"✅ Mascota registrada exitosamente (ID: {id_mascota_nueva})")
                                    st.rerun()
                                else:
                                    st.error("Error al registrar la mascota")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Complete los campos obligatorios marcados con *")
            
            if 'mascota_registrada' in st.session_state:
                id_mascota_seleccionada = st.session_state.mascota_registrada
        
        # Paso 3: Detalles de la cita (solo si hay mascota seleccionada)
        if id_mascota_seleccionada:
            st.markdown("---")
            st.markdown("### 📅 Paso 3: Detalles de la Cita")
            
            with st.form("form_cita_final"):
                col_c1, col_c2 = st.columns(2)
                
                with col_c1:
                    fecha_cita = st.date_input("Fecha de la Cita*", min_value=date.today())
                    hora_cita = st.time_input("Hora de la Cita*")
                    motivo_cita = st.text_area("Motivo de la Cita*", height=100, placeholder="Describa el motivo de la consulta...")
                
                with col_c2:
                    # Obtener empleados
                    try:
                        db = init_db()
                        if db.connect():
                            veterinarios = Empleado.obtener_todos(db, tipo='Veterinario')
                            db.disconnect()
                            
                            if veterinarios:
                                veterinario_options = {
                                    f"{v['nombre']} - {v.get('especialidad', 'General')}": v['id_empleado'] 
                                    for v in veterinarios
                                }
                                veterinario_selected = st.selectbox("Veterinario Asignado*", list(veterinario_options.keys()))
                                id_empleado_cita = veterinario_options[veterinario_selected]
                            else:
                                st.warning("No hay veterinarios disponibles")
                                id_empleado_cita = None
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        id_empleado_cita = None
                    
                    estado_cita = st.selectbox("Estado Inicial", ["pendiente", "completada", "cancelada"], index=0)
                
                submit_cita = st.form_submit_button("✅ REGISTRAR CITA COMPLETA", use_container_width=True, type="primary")
                
                if submit_cita:
                    logger.info(f"Procesando registro de nueva cita: mascota_id={id_mascota_seleccionada}, empleado_id={id_empleado_cita}")
                    
                    if motivo_cita and id_empleado_cita:
                        try:
                            db = init_db()
                            if db.connect():
                                logger.info("Conexión DB exitosa para crear cita")
                                fecha_str = fecha_cita.strftime("%Y-%m-%d")
                                hora_str = hora_cita.strftime("%H:%M")
                                
                                logger.debug(f"Creando cita: fecha={fecha_str}, hora={hora_str}, motivo={motivo_cita}, estado={estado_cita}")
                                id_cita = Cita.crear(db, fecha_str, hora_str, motivo_cita, 
                                                    id_mascota_seleccionada, id_empleado_cita, estado_cita)
                                db.disconnect()
                                
                                if id_cita:
                                    logger.info(f"Cita ID={id_cita} registrada exitosamente")
                                    
                                    # Limpiar session_state
                                    if 'dueno_encontrado' in st.session_state:
                                        del st.session_state.dueno_encontrado
                                    if 'mascota_registrada' in st.session_state:
                                        del st.session_state.mascota_registrada
                                    if 'duenos_multiples' in st.session_state:
                                        del st.session_state.duenos_multiples
                                    
                                    # Marcar para mostrar mensaje de éxito en el tab de ver citas
                                    st.session_state.cita_creada_id = id_cita
                                    st.session_state.cita_creada_info = {
                                        'dueno': dueno_nombre_display,
                                        'mascota_id': id_mascota_seleccionada,
                                        'fecha': fecha_str,
                                        'hora': hora_str
                                    }
                                    st.session_state.active_tab = 0  # Cambiar al tab de ver citas
                                    
                                    st.rerun()
                                else:
                                    logger.error("Error al crear cita: no se obtuvo ID")
                                    st.error("Error al registrar la cita")
                            else:
                                logger.error("Error al conectar a la base de datos para crear cita")
                                st.error("Error de conexión a la base de datos")
                        except Exception as e:
                            logger.exception(f"Excepción al registrar cita: {str(e)}")
                            st.error(f"Error: {str(e)}")
                    else:
                        logger.warning("Intento de registrar cita con campos obligatorios vacíos")

                        st.warning("⚠️ Complete todos los campos obligatorios")
    else:
        st.info("👆 Primero seleccione o registre un dueño en el Paso 1")

# TAB 3: Buscar
with tab3:
    st.subheader("Buscar Citas")
    
    buscar_por = st.radio("Buscar por:", ["ID Cita", "ID Mascota"], horizontal=True)
    
    if buscar_por == "ID Cita":
        id_buscar = st.number_input("ID de la cita", min_value=1, step=1)
        if st.button("🔍 Buscar"):
            try:
                db = init_db()
                if db.connect():
                    cita = Cita.obtener_por_id(db, id_buscar)
                    db.disconnect()
                    
                    if cita:
                        st.success("✅ Cita encontrada")
                        with st.container(border=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**📋 ID Cita:** {cita['id_cita']}")
                                st.markdown(f"**📅 Fecha:** {cita['fecha']}")
                                st.markdown(f"**🕐 Hora:** {cita['hora']}")
                                st.markdown(f"**📊 Estado:** {cita['estado']}")
                            with col2:
                                st.markdown(f"**🐾 Mascota:** {cita.get('mascota_nombre', 'N/A')} ({cita.get('especie', 'N/A')})")
                                st.markdown(f"**👤 Dueño:** {cita.get('dueno_nombre', 'N/A')}")
                                st.markdown(f"**👨‍⚕️ Veterinario:** {cita.get('veterinario_nombre', 'N/A')}")
                            st.markdown("---")
                            st.markdown(f"**📝 Motivo:** {cita['motivo']}")
                    else:
                        st.warning("No se encontró la cita")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    else:  # ID Mascota
        id_mascota_buscar = st.number_input("ID de la mascota", min_value=1, step=1)
        if st.button("🔍 Buscar Citas"):
            try:
                db = init_db()
                if db.connect():
                    citas = Cita.obtener_por_mascota(db, id_mascota_buscar)
                    db.disconnect()
                    
                    if citas:
                        st.success(f"✅ Se encontraron {len(citas)} citas")
                        for cita in citas:
                            with st.container(border=True):
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col1:
                                    st.markdown(f"**📋 Cita #{cita['id_cita']}**")
                                    st.markdown(f"📅 {cita['fecha']}")
                                    st.markdown(f"🕐 {cita['hora']}")
                                with col2:
                                    st.markdown(f"**🐾 Mascota:** {cita.get('mascota_nombre', 'N/A')}")
                                    st.markdown(f"**👨‍⚕️ Veterinario:** {cita.get('veterinario_nombre', 'N/A')}")
                                    st.markdown(f"**📝 Motivo:** {cita['motivo'][:50]}..." if len(cita['motivo']) > 50 else f"**📝 Motivo:** {cita['motivo']}")
                                with col3:
                                    estado_emoji = "🟢" if cita['estado'] == 'completada' else "🟡" if cita['estado'] == 'pendiente' else "🔴"
                                    st.markdown(f"{estado_emoji} **{cita['estado'].upper()}**")
                    else:
                        st.warning("No se encontraron citas para esta mascota")
            except Exception as e:
                st.error(f"Error: {str(e)}")
