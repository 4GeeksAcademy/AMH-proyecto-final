import streamlit as st
from funciones import cargar_css
from streamlit_extras.switch_page_button import switch_page
import os

#Directorio actual
base_dir = os.path.dirname(__file__)

# Cargar DataFrames
cargar_css(os.path.join(base_dir, '..','streamlit', 'style', 'styles.css'))

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
