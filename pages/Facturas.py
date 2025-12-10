import streamlit as st
import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.db_utils import init_db
from src.entidades.administrativo.factura import Factura

# Configurar logger
logger = logging.getLogger('pages.facturas')
logger.setLevel(logging.INFO)

st.set_page_config(page_title="Facturas", page_icon="💰", layout="wide")

logger.info("Accediendo a módulo de Facturas")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    logger.warning("Intento de acceso no autenticado a Facturas")
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
if st.session_state.user_type != "empleado":
    logger.warning(f"Intento de acceso a Facturas por usuario tipo: {st.session_state.user_type}")
    st.error("🚫 Acceso restringido. Solo empleados.")
    st.stop()

user_role = st.session_state.user_data.get('tipo_empleado', '').lower()
user_id = st.session_state.user_data.get('id_empleado', 'N/A')
logger.info(f"Usuario autenticado en Facturas: rol={user_role}, id={user_id}")

# Solo recepcionistas tienen acceso completo a facturas
if user_role not in ['recepcionista']:
    logger.warning(f"Intento de acceso no autorizado a Facturas por rol={user_role}")
    st.error("🚫 Acceso restringido. Solo recepcionistas pueden gestionar facturas.")
    st.stop()

st.title("💰 Gestión de Facturas")
st.markdown("---")

tab1 = st.tabs(["📋 Ver Facturas"])[0]

with tab1:
    st.subheader("Lista de Facturas")
    try:
        db = init_db()
        if db.connect():
            facturas = Factura.obtener_todas(db)
            db.disconnect()
            
            if facturas:
                for factura in facturas:
                    with st.expander(f"💰 Factura #{factura['id_factura']} - {factura['total']} €"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Consulta ID**: {factura['id_consulta']}")
                            st.write(f"**Total**: {factura['total']} €")
                        with col2:
                            st.write(f"**Método de pago**: {factura.get('metodo_pago', 'N/A')}")
                            st.write(f"**Fecha**: {factura.get('fecha', 'N/A')}")
            else:
                st.warning("No hay facturas registradas")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    st.info("ℹ️ **Nota**: Las facturas se generan automáticamente desde la página de **Consultas** después de completar una consulta médica.")
