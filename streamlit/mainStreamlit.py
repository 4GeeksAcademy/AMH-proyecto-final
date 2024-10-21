import streamlit as st
from funciones import cargar_css
from streamlit_extras.switch_page_button import switch_page

# Aplicamos el CSS personalizado y el fondo
cargar_css('style/styles.css')

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    if st.session_state["page"] == "home":
        switch_page('pagina_principal')
    elif st.session_state["page"] == "residencial":
        switch_page('pagina_residencial')
    elif st.session_state["page"] == "servicios":
        switch_page('pagina_servicios')
    elif st.session_state["page"] == "industrial":
        switch_page('pagina_industrial')
if __name__ == "__main__":
    main()
