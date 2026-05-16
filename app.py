import streamlit as st
import qrcode
from io import BytesIO
import re

# ---------------------------------
# CONFIGURACIÓN
# ---------------------------------

st.set_page_config(
    page_title="EPS SmartQueue",
    page_icon="🏥",
    layout="centered"
)

# ---------------------------------
# ESTILOS
# ---------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

div.stButton > button {
    background-color: #06b6d4;
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    border: none;
    font-size: 16px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #0891b2;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

input {
    border-radius: 10px !important;
}

.css-1d391kg {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# VARIABLES
# ---------------------------------

if 'fila' not in st.session_state:
    st.session_state.fila = []

if 'contador' not in st.session_state:
    st.session_state.contador = 1

if 'turno_actual' not in st.session_state:
    st.session_state.turno_actual = "Ninguno"

# ---------------------------------
# MENÚ
# ---------------------------------

pagina = st.sidebar.selectbox(
    "🏥 Menú EPS",
    [
        "Inicio",
        "Solicitar Turno",
        "Administrador"
    ]
)

# ---------------------------------
# INICIO
# ---------------------------------

if pagina == "Inicio":

    st.title("🏥 EPS SmartQueue")

    st.subheader("Sistema Inteligente de Gestión de Turnos")

    st.write("""
    Bienvenido al sistema digital de turnos de la EPS.

    Aquí podrás:
    - Solicitar turnos
    - Consultar tiempos de espera
    - Escanear códigos QR
    - Mejorar tu experiencia de atención
    """)

    st.info("Atención rápida, moderna y organizada para nuestros pacientes.")

# ---------------------------------
# USUARIO
# ---------------------------------

elif pagina == "Solicitar Turno":

    st.title("🩺 Solicitud de Atención")

    nombre = st.text_input(
        "Nombre completo"
    )

    cedula = st.text_input(
        "Número de cédula"
    )

    motivo = st.selectbox(
        "Motivo de atención",
        [
            "Medicina general",
            "Urgencias",
            "Entrega de medicamentos",
            "Laboratorio",
            "Odontología",
            "Autorizaciones",
            "Vacunación"
        ]
    )

    if st.button("Generar Turno"):

        # VALIDACIONES

        if nombre.strip() == "" or cedula.strip() == "":

            st.error(
                "Debe completar todos los campos"
            )

        elif not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre):

            st.error(
                "El nombre solo puede contener letras"
            )

        elif not cedula.isdigit():

            st.error(
                "La cédula solo debe contener números"
            )

        else:

            # VALIDAR SI YA EXISTE

            usuario_existente = False

            for persona in st.session_state.fila:

                if persona["cedula"] == cedula:

                    usuario_existente = True
                    break

            if usuario_existente:

                st.warning(
                    "⚠️ El usuario ya se encuentra registrado en la fila"
                )

            else:

                turno = f"E{st.session_state.contador}"

                st.session_state.fila.append(
                    {
                        "turno": turno,
                        "nombre": nombre,
                        "cedula": cedula,
                        "motivo": motivo
                    }
                )

                st.session_state.contador += 1

                personas = len(st.session_state.fila)

                tiempo_estimado = personas * 7

                # LINK QR
                link = (
                    f"http://localhost:8501/Consulta"
                    f"?personas={personas}"
                    f"&tiempo={tiempo_estimado}"
                    f"&turno={turno}"
                )

                # GENERAR QR
                qr = qrcode.make(link)

                buffer = BytesIO()

                qr.save(buffer)

                st.success(
                    "✅ Turno generado exitosamente"
                )

                st.markdown(f"""
                ### 📋 Información del Turno

                - 👤 Paciente: **{nombre}**
                - 🪪 Cédula: **{cedula}**
                - 🎫 Turno: **{turno}**
                - 🩺 Servicio: **{motivo}**
                """)

                st.image(
                    buffer.getvalue(),
                    caption="Escanee el QR para consultar su turno"
                )

# ---------------------------------
# ADMINISTRADOR
# ---------------------------------

# ---------------------------------
# ADMINISTRADOR
# ---------------------------------

elif pagina == "Administrador":

    st.title("🔐 Panel Administrativo EPS")

    # VARIABLE LOGIN
    if "admin_logueado" not in st.session_state:
        st.session_state.admin_logueado = False

    # ------------------------------
    # LOGIN
    # ------------------------------

    if not st.session_state.admin_logueado:

        usuario = st.text_input("Usuario")

        password = st.text_input(
            "Contraseña",
            type="password"
        )

        if st.button("Ingresar"):

            if usuario == "admin" and password == "1234":

                st.session_state.admin_logueado = True

                st.rerun()

            else:

                st.error(
                    "Credenciales incorrectas"
                )

    # ------------------------------
    # PANEL ADMIN
    # ------------------------------

    else:

        st.success("Acceso autorizado")

        st.subheader("📑 Pacientes en espera")

        if len(st.session_state.fila) == 0:

            st.warning("No hay pacientes en espera")

        else:

            for persona in st.session_state.fila:

                st.markdown(f"""
                ---
                ### 🎫 {persona['turno']}

                👤 **Paciente:** {persona['nombre']}

                🪪 **Cédula:** {persona['cedula']}

                🩺 **Servicio:** {persona['motivo']}
                """)

            # ------------------------------
            # BOTÓN LLAMAR
            # ------------------------------

            if st.button("📢 Llamar siguiente paciente"):

                siguiente = st.session_state.fila.pop(0)

                st.session_state.turno_actual = (
                    siguiente['turno']
                )

                st.success(
                    f"Atendiendo turno {siguiente['turno']}"
                )

                st.rerun()

            # ------------------------------
            # BOTÓN REINICIAR
            # ------------------------------

            if st.button("🗑️ Reiniciar fila"):

                st.session_state.fila = []

                st.session_state.turno_actual = "Ninguno"

                st.warning("Fila reiniciada")

                st.rerun()

        st.info(
            f"Turno actual: {st.session_state.turno_actual}"
        )

        # ------------------------------
        # CERRAR SESIÓN
        # ------------------------------

        if st.button("🚪 Cerrar sesión"):

            st.session_state.admin_logueado = False

            st.rerun()