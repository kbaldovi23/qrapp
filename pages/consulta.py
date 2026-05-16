import streamlit as st

# ------------------------------
# CONFIG
# ------------------------------

st.set_page_config(
    page_title="Consulta QR",
    page_icon="📱",
    layout="centered"
)

# ------------------------------
# OCULTAR SIDEBAR
# ------------------------------

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# LEER DATOS DEL QR
# ------------------------------

params = st.query_params

personas = params.get("personas", "0")
tiempo = params.get("tiempo", "0")
turno = params.get("turno", "Sin turno")

# ------------------------------
# INTERFAZ
# ------------------------------

st.title("📱 Estado de la Fila")

st.metric(
    "Tu turno",
    turno
)

st.metric(
    "Personas en espera",
    personas
)

st.metric(
    "Tiempo estimado",
    f"{tiempo} minutos"
)

if int(personas) == 0:

    st.success("No hay personas esperando")

else:

    st.warning(
        "Por favor espere su turno"
    )