import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os
from datetime import datetime

# Configuración inicial
FILE_PATH = "reportes_jalisco.csv"
CENTRO_JALISCO = [20.6597, -103.3496]
ZOOM_INICIAL = 12

# Configurar geocodificador
geolocator = Nominatim(user_agent="jalisco_app", domain="nominatim.openstreetmap.org")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Cargar o crear DataFrame
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=["fecha", "lat", "lon", "direccion", "tipo", "descripcion"])

if "reportes" not in st.session_state:
    st.session_state.reportes = df



# =============================================
# CONFIGURACIÓN INICIAL Y ESTILOS
# =============================================
def configurar_pagina(pagina_actual):
    st.set_page_config(page_title="ALINTOX",page_icon='https://i.imgur.com/4UO1NPS.jpeg',layout="wide" )
    aplicar_estilos(pagina_actual)

def aplicar_estilos(pagina_actual):
    """Define estilos CSS con fondo dinámico"""
    if pagina_actual == "Página Principal":
        fondo_css = """
        .stApp {
            background-image: url('https://i.imgur.com/TQ0btBE.jpeg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        """
    else:
        fondo_css = """
        .stApp {
            background-color: white !important;
        }
        """

    st.markdown(f"""
    <style>
    {fondo_css}

    .stButton > button {{
        background-color: #632D33 !important;
        border: none !important;
        padding: 15px 40px !important;
        border-radius: 8px !important;
        font-family: Arial !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: background-color 0.3s !important;
    }}
    .stButton > button:hover {{
        background-color: #4a2126 !important;
    }}

    .footer-section {{
        color: #632D33;
        font-family: Arial;
        margin-right: 50px;
    }}

    .circle-btn-container {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 10px;
    }}

    .social-button {{
        background-color: white;
        border: none;
        color: black;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-left: auto;
        margin: 5px 0;
    }}

    .button-container {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .circle-button {{
        background-color: #DCE2B0;
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        border: none;
    }}

    .button-text {{
        font-family: Arial;
        font-size: 20px;
        font-weight: bold;
        color: #868E7F;
    }}
    /* Elimina padding y margen extra del contenedor principal */
    .stApp, .main, .block-container {{
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }}

    /* Ajusta el iframe de st_folium */
    iframe {{
        display: block;
        height: 450px !important;
        width: 100% !important;
        margin: 0 auto;
        padding: 0 !important;
        border: none !important;
    }}

    /* Opcional: evitar scroll si queda espacio extra */
    html, body {{
        overflow-x: hidden;
    }}


    </style>
    """, unsafe_allow_html=True)

# =============================================
# COMPONENTES REUTILIZABLES
# =============================================
def mostrar_navegacion():
    """Barra de navegación superior"""

    cols = st.columns([3, 3, 1.7, 1.2, 1.2, 1.2])

    # Logo
    cols[0].image("https://i.imgur.com/UzkFH3g.jpeg", width=300)

    # Botones de navegación
    nav_items = {
        "Página Principal":2,
        "Tienda": 3,
        "Log In": 4,
        "Sign In": 5
    }

    for pagina, col_index in nav_items.items():
        if cols[col_index].button(pagina, key=f"nav_{pagina}"):
            st.session_state.pagina_actual = pagina
            st.rerun()

def mostrar_footer():
    """Sección footer de la página"""

    # Estilos: insertarlos antes de las columnas
    st.markdown("""
    <style>
    .social-button-link {
        display: inline-block;
        width: 40px;
        height: 40px;
        background-color: #f2f2f2;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        margin: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: background-color 0.3s;
    }

    .social-button-link:hover {
        background-color: #e0e0e0;
    }

    .social-button-icon {
        width: 20px;
        height: 20px;
        vertical-align: middle;
    }

    .social-button {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #f2f2f2;
        border: none;
        margin: 5px;
        font-size: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    cols = st.columns([1, 1, 1, 1, 1])

    # Columnas del footer
    cols[0].markdown("""
    <div class="footer-section">
        <h3 style='font-size: 24px; margin-bottom: 12px;'>ALINTOX</h3>
        <p style='color: #959191; font-size: 16px;'>Sientete segur@ al alcance de tus manos.</p>
        <p style='color: #959191; font-size: 16px;'>Ayuda/Preguntas Frecuentes</p>
    </div>
    """, unsafe_allow_html=True)

    cols[1].markdown("""
    <div class="footer-section">
        <h3 style='color: #080809; font-weight: bold; font-size: 17px; margin-bottom: 15px;'>COMPAÑÍA</h3>
        <p style='color: #959191; font-size: 16px;'>Sobre nosotros</p>
    </div>
    """, unsafe_allow_html=True)

    cols[2].markdown("""
    <div class="footer-section">
        <h3 style='color: #080809; font-weight: bold; font-size: 17px; margin-bottom: 15px;'>CONTACTO</h3>
        <p style='color: #959191; font-size: 16px;'>Tel: 33 3837 6000</p>
        <p style='color: #959191; font-size: 16px;'>reporte@alintox.mx</p>
    </div>
    """, unsafe_allow_html=True)

    cols[3].markdown("""
    <div class="footer-section">
        <h3 style='color: #080809; font-weight: bold; font-size: 17px; margin-bottom: 15px;'>ENLACES</h3>
        <p style='color: #959191; font-size: 16px;'>Términos y condiciones</p>
        <p style='color: #959191; font-size: 16px;'>Política de privacidad</p>
        <p style='color: #959191; font-size: 16px;'>Soporte técnico</p>
    </div>
    """, unsafe_allow_html=True)

    cols[4].markdown("""
    <div class="circle-btn-container">
        <a href="https://www.instagram.com/alintox" target="_blank" class="social-button-link">
            <img src="https://1000marcas.net/wp-content/uploads/2019/11/insta-logo.png" alt="icono1" class="social-button-icon">
        </a>
        <button class="social-button">✓</button>
        <a href="https://www.tiktok.com/@_alintox" target="_blank" class="social-button-link">
            <img src="https://icones.pro/wp-content/uploads/2021/03/logo-icone-tiktok-simbolo-noir.png" alt="icono2" class="social-button-icon">
        </a>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# PÁGINAS DE LA APLICACIÓN
# =============================================

#pagina principal----------

def pagina_principal():

    """Contenido de la página principal"""
    cols_principal = st.columns([1, 1])

    with cols_principal[0]:
        st.markdown("""
        <div style='margin-left: 50px;'>
            <h1 style='color: #632D33; font-size: 26px;'>Somos jóvenes y no queremos desaparecer</h1>
            <h2 style='color: #40292B; font-size: 106px;'>¡Defensa que deja huella!</h2>
            <p style='color: #5E6282; font-size: 22px;'>
            El dispositivo está basado en compuestos bioactivos naturales extraídos del ajo y la cebolla,
            conocidos por sus propiedades irritantes en mucosas y vías respiratorias. Además, se incorpora
            un pigmento natural que permite marcar al agresor, facilitando su posterior identificación.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with cols_principal[1]:
        st.image("https://i.imgur.com/lB6NbVP.png", width=1200)

    mostrar_seccion_botones()
    mostrar_seccion_telefonos()
#------------------------

#mapa--------------------
def pagina_mapa():

    m = folium.Map(location=CENTRO_JALISCO, zoom_start=ZOOM_INICIAL, tiles="CartoDB positron")

    # Añadir marcadores existentes
    for _, reporte in st.session_state.reportes.iterrows():
        folium.Marker(
            location=[reporte.lat, reporte.lon],
            popup=f"""
            <b> {reporte.tipo}</b><br>
            <hr>
            <i>Fecha: {reporte.fecha}</i><br>
            <i>{reporte.direccion}</i><br>
             {reporte.descripcion}
            """,
            icon=folium.Icon(color="red" if reporte.tipo == "Robo" else "blue")
        ).add_to(m)

    # Interactividad del mapa
    map_data = st_folium(
        m,
        height=500,
        returned_objects=["last_clicked"],
        key="main_map",
        use_container_width=True
    )

    # Estilos personalizados aplicados directamente aquí
    st.markdown("""
    <style>
    /* Cambiar color del texto general debajo del mapa */
    .stForm h2, .stForm h3, .stForm label, .stForm p {
        color: black !important;
    }

    /* Estilos para el input de texto (ubicación) */
    input[type="text"] {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        border-radius: 5px;
    }

    /* Estilos para el área de texto (descripción) */
    textarea {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        border-radius: 5px;
    }

    /* Estilos para el selectbox */
    div[data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid black !important;
        border-radius: 5px !important;
    }

    div[data-baseweb="select"] input {
        color: black !important;
    }

    div[data-baseweb="select"] div {
        background-color: white !important;
        color: black !important;
    }

    div[role="listbox"] div {
        background-color: white !important;
        color: black !important;
    }

    /* Opciones del dropdown */
    div[role="option"] {
        background-color: white !important;
        color: black !important;
    }

    div[role="option"]:hover {
        background-color: #f0f0f0 !important;
    }

    </style>
    """, unsafe_allow_html=True)
    # Formulario fijo en 4 columnas
    form = st.form(key="report_form")

    # Crear 4 columnas
    col1, col2, col3, col4 = form.columns(4)

    with col1:
        fecha = st.date_input("Fecha del incidente", datetime.now())

    with col2:
        tipo = st.selectbox("Tipo de Agresión",
                          ["Robo", "Agresión física", "Acoso", "Vandalismo", "Otro"],
                          key="tipo_select")

    with col3:
        if 'direccion_input' not in st.session_state:
            st.session_state.direccion_input = ""

        direccion = st.text_area(
            "Ubicación exacta",
            value=st.session_state.direccion_input,
            placeholder="Click en el mapa o ingresa dirección",
            key="ubicacion_input"
        )

    with col4:
        descripcion = st.text_area(
            "Descripción del incidente",
            placeholder="Ej. Persona sospechosa observando vehículos",
            key="descripcion_input"
        )

    # Estilos CSS
    st.markdown("""
    <style>
    ::placeholder {
        color: #999999 !important;
        opacity: 1 !important;
    }

    input::placeholder, textarea::placeholder {
        color: #999999 !important;
    }

    /* Forzar altura visual del text_input para que se parezca al text_area */
    input[type="text"] {
        height: 68px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Espacio para el botón - ocupará columnas 2-4 (3 columnas a la derecha)
    a_, btn_col, = form.columns([1, 3])  # 1 columna vacía, 3 para el botón, 1 vacía
    with a_:
        st.markdown(""" """)
    with btn_col:
        submitted = form.form_submit_button("Agregar Reporte")

        st.markdown("""
        <style>
        /* Selector de alta especificidad */
        div[data-testid="stFormSubmitButton"] > button > div > p {
            color: white !important;
            font-weight: bold !important;
        }

        /* Estilo base del botón */
        div[data-testid="stFormSubmitButton"] button {
            background-color: #632D33 !important;
            border: 1px solid #632D33 !important;
            width: 100%;
        }

        /* Hover state */
        div[data-testid="stFormSubmitButton"] button:hover {
            background-color: #4a2126 !important;
            border-color: #4a2126 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if submitted:
            if direccion:
                try:
                    if ":" in direccion:  # Coordenadas
                        lat, lon = map(float, direccion.split(":")[1].strip().split(","))
                        nuevo_reporte = pd.DataFrame([{
                            "fecha": fecha.strftime("%Y-%m-%d"),
                            "lat": lat,
                            "lon": lon,
                            "direccion": direccion,
                            "tipo": tipo,
                            "descripcion": descripcion
                        }])
                    else:  # Dirección textual
                        location = geocode(f"{direccion}, Jalisco, México")
                        if location:
                            nuevo_reporte = pd.DataFrame([{
                                "fecha": fecha.strftime("%Y-%m-%d"),
                                "lat": location.latitude,
                                "lon": location.longitude,
                                "direccion": direccion,
                                "tipo": tipo,
                                "descripcion": descripcion
                            }])
                        else:
                            st.error("Dirección no encontrada")
                            st.stop()

                    st.session_state.reportes = pd.concat([st.session_state.reportes, nuevo_reporte], ignore_index=True)
                    st.success("Reporte agregado correctamente!")
                    st.session_state.direccion_input = ""
                    st.rerun()

                except Exception as e:
                    st.error(f"Error al procesar la ubicación: {str(e)}")
            else:
                st.warning("Por favor ingresa una ubicación")

    # Actualizar dirección con coordenadas del mapa
    if map_data["last_clicked"]:
        coords = map_data["last_clicked"]
        st.session_state.direccion_input = f"Coordenadas: {coords['lat']:.5f}, {coords['lng']:.5f}"
        st.rerun()

    st.session_state.reportes.to_csv(FILE_PATH, index=False)


#------------------------------

#Tienda------------------------
def pagina_tienda():

    st.markdown("""
    <style>
    /* 1) Quita el recuadro del contenedor de todos los forms */
    div[data-testid="stForm"] {
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    /* 2) Estilo de los botones dentro del form */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #cccccc !important;
        color: #333333 !important;
        border: none !important;
        font-size: 20px !important;
        padding: 4px 10px !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #aaaaaa !important;
    }
    /* 3) Quita el outline azul al hacer foco */
    div[data-testid="stFormSubmitButton"] button:focus {
        outline: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


    # Inicializar estado
    if 'cantidad' not in st.session_state:
        st.session_state.cantidad = 1
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    # Layout en dos columnas
    col1, col_relleno, col2 = st.columns([1,0.1, 1])

    with col1:
        st.image(
        'https://i.imgur.com/Zm3ROYf.png',
        use_container_width=True,
        )
        st.image(
            'https://i.imgur.com/Q4p8coG.png',
            width=250,
        )


    with col2:
        st.markdown("<h1 style='color: #632D33; font-family: Arial;'>GAS DEFENSA PERSONAL</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #40292B; font-family: Arial;'>Alintox</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:inline-block; vertical-align:middle;">
            <span style="color:#FFD700; font-size:24px;">⭐⭐⭐⭐⭐</span>
            <span style="color:#5E6282; font-size:16px; margin-left:8px;">(4.9/5.0)</span>
        </div>
        """, unsafe_allow_html=True)

        # Precio
        st.markdown(f"""
        <div style="color: #515151; font-size: 16px; margin: 10px 0; font-family: Arial;">
            Total<br>
            <span style="font-size: 36px; color: #632D33; font-weight: bold;">${299 * st.session_state.cantidad}.00 MXN</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color: #632D33; font-family: Arial;'>Detalles del producto</h3>", unsafe_allow_html=True)
        st.markdown("""
        <span style="color: black;">
            <strong>Tamaño:</strong> 100 ml<br>
            <strong>Color:</strong> Negro
        </span>
        """, unsafe_allow_html=True)

        # Columnas para botones +, -, y cantidad
        col_relleno, col_a, col_b, col_c = st.columns([1, 0.1, 0.1, 0.3])

        with col_a:
            with st.form("form_restar"):
                btn_restar = st.form_submit_button("－")
                if btn_restar:
                    if st.session_state.cantidad > 1:
                        st.session_state.cantidad -= 1
                    st.rerun()

        with col_b:
            st.markdown(f"""
            <div style="text-align: center; font-size: 20px; color: black; margin: 10px 0; font-family: Arial;">
                {st.session_state.cantidad}
            </div>
            """, unsafe_allow_html=True)

        with col_c:
            with st.form("form_sumar"):
                btn_sumar = st.form_submit_button("＋")
                if btn_sumar:
                    st.session_state.cantidad += 1
                    st.rerun()


        # --- Botón AGREGAR AL CARRITO (centrado) ---
        col2, col3 = st.columns([3, 1])
        with col2:
            if st.button('  Agregar al carrito  ', key='add_cart'):
                st.session_state.carrito.append({
                    "producto": "Gas Defensa Personal",
                    "cantidad": st.session_state.cantidad,
                    "precio": 299 * st.session_state.cantidad
                })
                st.success("¡Producto añadido!")
                st.rerun()

        # --- Botón DEVOLUCIONES en formulario gris, pequeño, alineado a la izquierda ---
        col_left, _ = st.columns([1 , 3])
        with col_left:
            with st.form("form_devoluciones"):
                devolver = st.form_submit_button("Devoluciones")
                if devolver:
                    st.session_state.pagina_actual = "Devoluciones"
                    st.rerun()


    # Descripción
    st.markdown("""
        <div style="margin-top: 30px;">
            <h3 style="color: #632D33; font-size: 20px; margin-bottom: 15px; font-family: Arial;">Descripción</h3>
            <p style="color: #515151; font-size: 16px; line-height: 1.6; font-family: Arial;">
            El dispositivo está basado en compuestos bioactivos naturales extraídos del ajo (Allium sativum) y la cebolla (Allium cepa), conocidos por sus propiedades irritantes en mucosas y vías respiratorias. Formulado con ingredientes naturales y concentraciones controladas, este spray desorienta temporalmente al agresor, sin provocar daños permanentes en la piel ni en los pulmones y adornas de dejar un pigmento en la piel por las propiedades de la jamaica.
            </p>
        </div>
        """, unsafe_allow_html=True)


    # Comentarios
    st.markdown('<p style="color: #632D33; font-size: 24px; font-weight: bold; text-align: left;">Comentarios</p>', unsafe_allow_html=True)

    # Crear dos columnas para los comentarios y la imagen
    col_comentarios, col_imagen = st.columns([2, 1])

    with col_comentarios:
        st.markdown('<p style="color: #5E6282; font-size: 18px; text-align: left;">A**** L****  ⭐⭐⭐⭐⭐</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #999999; font-size: 14px; text-align: left;">14/04/25</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: black; font-size: 16px; text-align: left;">Muchas gracias, excelente artículo, me ha hecho sentir más comod@ mientras voy caminando por la calle.</p>', unsafe_allow_html=True)

        st.markdown("###")

        st.markdown('<p style="color: #5E6282; font-size: 18px; text-align: left;">M***** G**  ⭐⭐⭐⭐⭐</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #999999; font-size: 14px; text-align: left;">20/04/25</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: black; font-size: 16px; text-align: left;">Gracias por el artículo, me siento más segur@ al salir en mi ciudad.</p>', unsafe_allow_html=True)

    with col_imagen:
        st.image(
        'https://i.imgur.com/baXZcze.png',
          width=500
        )


#-----------------------------

#Pagina de devoluciones-------
def pagina_devoluciones():
    # Inyectar estilos CSS personalizados (incluye override para el botón gris)
    st.markdown("""
    <style>
    .title { text-align: center; color: #5b1f2e; font-size: 40px; font-weight: bold; margin-bottom: 30px; }
    .note  { font-size: 14px; color: #333; margin-top: 20px; }
    .product-detail { font-size: 16px; line-height: 1.5; }
    .product-detail a { text-decoration: none; color: #5b1f2e; font-weight: bold; }

    /* Botón de enviar solicitud en gris */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #cccccc !important;
        color: #333333 !important;
        border: none !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #aaaaaa !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Título
    st.markdown("<div class='title'>Devoluciones</div>", unsafe_allow_html=True)

    # Columnas: formulario vs. detalles
    col1, _, col2 = st.columns([1.5, 0.5, 1])

    with col1:
        with st.form("devolucion_form"):
            # Nuevo campo: cantidad a devolver
            cantidad_dev = st.number_input(
                "¿Cuántos productos deseas devolver?",
                min_value=1, value=1, step=1
            )
            nombre   = st.text_input("Nombre", placeholder="Ingresa tu nombre completo")
            direccion= st.text_input("Dirección", placeholder="Ingresa tu dirección")
            correo   = st.text_input("Correo electrónico", placeholder="usuario@ejemplo.com")
            telefono = st.text_input("Número telefónico", placeholder="+52 33 1234 5678")
            motivo   = st.text_area("¿Por qué devuelves el producto?", placeholder="Motivo de la devolución...")

            st.markdown(
                "<p class='note'>En Alintox nos preocupa tu seguridad y tu opinión; con tu solicitud te daremos una respuesta lo más breve posible. Agradecemos tu paciencia.*El tiempo de devolución puede variar de 15 a 30 días </p>",
                unsafe_allow_html=True
            )

            enviado = st.form_submit_button("Enviar solicitud")
            if enviado:
                st.success(f"¡Solicitud enviada para {cantidad_dev} producto(s)! Pronto nos pondremos en contacto contigo.")

        # Botón regresar
        if st.button("← Regresar a Tienda"):
            st.session_state.pagina_actual = "Tienda"
            st.rerun()

    with col2:
        st.image("https://i.imgur.com/ApPqvRp.png", width=250)
        st.markdown("### Detalles del producto:")
        st.markdown("""
        <div class='product-detail'>
            <strong>Gas defensa personal</strong><br>
            Marca: <a href='#'>Alintox</a><br>
            Tamaño: <strong>100 ml</strong><br>
            Color: <strong>Negro</strong><br>
            Cantidad: <strong>1</strong>
        </div>
        """, unsafe_allow_html=True)

#----------------------------------

#Pagina Log In---------------------

def pagina_login():
    # --- CSS personalizado ---
    st.markdown("""
    <style>
    /* Título grande y con sombra */
    .login-title {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px #bbbbbb;
    }

    /* Centrar el formulario y limitar su ancho */
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px 0;
    }

    /* Inputs de ancho completo y bordes redondeados */
    .login-container .stTextInput input {
        width: 100% !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 20px !important;
        box-sizing: border-box;
    }

    /* Botón principal ancho completo y burdeos */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background-color: #632D33 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: background-color 0.3s !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #4a2126 !important;
    }

    /* Enlace de "¿Olvidaste tu contraseña?" alineado a la izquierda */
    .forgot-password {
        text-align: left;
        margin: 10px 0 0 0 !important;
        font-size: 14px;
    }
    .forgot-password a {
        color: #0066CC !important;
        text-decoration: underline !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Título
    st.markdown("<div class='login-title'>Inicio de Sesión</div>", unsafe_allow_html=True)

    # Contenedor único que agrupa todo
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    with st.form("login_form"):
        usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="login_usuario")
        contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="login_contrasena")
        submitted = st.form_submit_button("Inicio de sesión")

    # Lógica de ejemplo
    if submitted:
        if usuario and contrasena:
            st.success("Inicio de sesión exitoso!")
        else:
            st.error("Por favor ingresa usuario y contraseña")

    st.markdown("""
            <p class="forgot-password">
                <a href="#">¿Olvidaste tu contraseña?</a>
            </p>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


#------------------------------------

#Pagina Sing In----------------------

def pagina_signin():
    # --- CSS personalizado para Sign Up ---
    st.markdown("""
    <style>
    /* Título grande y con sombra */
    .signin-title {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px #bbbbbb;
    }

    /* Centrar el formulario y limitar su ancho */
    .signin-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px 0;
    }

    /* Inputs de ancho completo y bordes redondeados */
    .signin-container .stTextInput input {
        width: 100% !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 20px !important;
        box-sizing: border-box;
    }

    /* Botón principal ancho completo y burdeos */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background-color: #632D33 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: background-color 0.3s !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #4a2126 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Título
    st.markdown("<div class='signin-title'>Registro de Usuario</div>", unsafe_allow_html=True)

    # Contenedor centrado
    st.markdown("<div class='signin-container'>", unsafe_allow_html=True)
    with st.form("signin_form"):
        usuario     = st.text_input("Usuario", placeholder="Elige un nombre de usuario", key="signin_usuario")
        correo      = st.text_input("Correo electrónico", placeholder="usuario@ejemplo.com", key="signin_correo")
        contrasena1 = st.text_input("Contraseña", type="password", placeholder="Crea una contraseña", key="signin_pass1")
        contrasena2 = st.text_input("Confirmar contraseña", type="password", placeholder="Repite tu contraseña", key="signin_pass2")

        submitted = st.form_submit_button("REGISTRARSE")
    st.markdown("</div>", unsafe_allow_html=True)

    # Lógica de ejemplo
    if submitted:
        if not usuario or not correo or not contrasena1 or not contrasena2:
            st.error("Por favor completa todos los campos.")
        elif contrasena1 != contrasena2:
            st.error("Las contraseñas no coinciden.")
        else:
            st.success(f"¡Bienvenid@, {usuario}! Tu registro ha sido exitoso.")

#------------------------------------

#Pagina Como se usa------------------

def pagina_comousar():

    st.markdown("<h1 style='color: #632D33; font-family: Arial;'>¿Cómo usar el spray?</h1>", unsafe_allow_html=True)
    col1, col2, col3= st.columns([6, 4, 1])

    with col1:
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <img src="https://i.imgur.com/VjNFa47.png" width="300">
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("""
        <style>
            .paso {
                font-size: 25px;
                font-weight: bold;
                color: #632D33;
            }
            .aviso {
              font-weight: bold;
                font-size: 20px;
                color: #1E1E1E;
            }
        </style>
        <div>
            <span class="paso">PASO 1:</span>
            <span class="aviso">Desactivar el seguro de la parte posterior del gas.</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div>
            <span class="texto"></span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
            .paso {
                margin-top: 20px;
                font-size: 25px;
                font-weight: bold;
                color: #632D33;
            }
            .aviso {
                font-weight: bold;
                font-size: 20px;
                color: #1E1E1E;
            }
        </style>
        <div>
            <span class="paso">PASO 2:</span>
            <span class="aviso">Activar el pulverizador con presión sobre el botón.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <style>
            .texto {
                font-size: 15px;
                color: #959191;
            }
        </style>
        <div>
            <span class="texto">Siempre úsese solamente en casos de defensa personal de riesgo inminente</span>
        </div>
        """, unsafe_allow_html=True)

#---------------------------


# =============================================
# SECCIONES COMPARTIDAS
# =============================================
def mostrar_seccion_botones():
    """Botones interactivos inferiores"""
    cols = st.columns([1.2, 4.1, 4, 7.2])

    with cols[1]:
        if st.button("Mapa de Incidentes", key="mapa_incidentes"):
            st.session_state.pagina_actual = "Mapa"
            st.rerun()

    with cols[2]:
        if st.button("¿Cómo se usa?", key="btn_ayuda"):
            st.session_state.pagina_actual = "Como se usa"
            st.rerun()

def mostrar_seccion_telefonos():
    """Sección de teléfonos de emergencia"""
    st.markdown("""
    <div style='margin-left: 100px;'>
        <div style="display: inline-block; text-align: center; margin-right: 150px;">
            <p style="font-size: 15px; font-weight: bold; color: #632D33; margin-top: 20px; margin-bottom: 1px;">
                Tel. Centro Atencion Ciudadana:</p>
            <p style="font-size: 30px; font-weight: bold; color: black; margin-top: 1px;">800 911 2000</p>
        </div>
        <div style="display: inline-block; text-align: center;">
            <p style="font-size: 15px; font-weight: bold; color: #632D33; margin-top: 20px; margin-bottom: 1px;">
                Linea S.O.S Mujeres</p>
            <p style="font-size: 30px; font-weight: bold; color: black; margin-top: 1px;">*765</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# CONFIGURACIÓN PRINCIPAL
# =============================================
def main():
    if "pagina_actual" not in st.session_state:
        st.session_state["pagina_actual"] = "Página Principal"

    configurar_pagina(st.session_state.pagina_actual)
    mostrar_navegacion()

    # Manejo de navegación
    if st.session_state.pagina_actual == "Página Principal":
        pagina_principal()
    elif st.session_state.pagina_actual == "Mapa":
        pagina_mapa()
    elif st.session_state.pagina_actual == "Como se usa":
        pagina_comousar()
    elif st.session_state.pagina_actual == "Tienda":
        pagina_tienda()
    elif st.session_state.pagina_actual == 'Devoluciones':
        pagina_devoluciones()
    elif st.session_state.pagina_actual == "Log In":
        pagina_login()
    elif st.session_state.pagina_actual == "Sign In":
        pagina_signin()


    mostrar_footer()

if __name__ == "__main__":
    main()
