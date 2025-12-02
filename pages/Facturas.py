import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database_conn.db_conn import DatabaseConnection

st.set_page_config(page_title="Facturas", page_icon="💰", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicie sesión primero")
    st.stop()

# Control de acceso por rol
if st.session_state.user_type != "empleado":
    st.error("🚫 Acceso restringido. Solo empleados.")
    st.stop()

user_role = st.session_state.user_data.get('tipo_empleado', '').lower()

# Solo recepcionistas tienen acceso completo a facturas
if user_role not in ['recepcionista']:
    st.error("🚫 Acceso restringido. Solo recepcionistas pueden gestionar facturas.")
    st.stop()

def init_db():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'clinica_veterinaria')
    return DatabaseConnection(host, user, password, database)

st.title("💰 Gestión de Facturas")
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Ver Facturas", "➕ Nueva Factura"])

with tab1:
    st.subheader("Lista de Facturas")
    try:
        db = init_db()
        if db.connect():
            facturas = db.fetch_all("SELECT * FROM facturas ORDER BY id_factura DESC")
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

with tab2:
    st.subheader("Generar Nueva Factura")
    with st.form("nueva_factura"):
        id_consulta = st.number_input("ID de la Consulta*", min_value=1, step=1)
        total = st.number_input("Total (€)*", min_value=0.0, step=0.01)
        metodo_pago = st.selectbox("Método de pago", ["efectivo", "tarjeta", "transferencia", "paypal"])
        fecha = st.date_input("Fecha")
        
        if st.form_submit_button("💰 Generar Factura", use_container_width=True):
            if id_consulta and total:
                try:
                    db = init_db()
                    if db.connect():
                        fecha_str = fecha.strftime("%Y-%m-%d")
                        id_factura = db.insertar_factura(id_consulta, total, metodo_pago, fecha_str)
                        db.disconnect()
                        if id_factura:
                            st.success(f"✅ Factura generada (ID: {id_factura})")
                        else:
                            st.error("Error al generar factura")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Complete los campos obligatorios")
