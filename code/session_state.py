import streamlit as st


def initialize_session_state():
    """
    Initializes the session state variables for the Streamlit app.

    Sets default values for the `selected_persona` and `selected_model` variables if they don't already exist.
    """
    if "selected_persona" not in st.session_state:
        st.session_state.selected_persona = ""

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = ""
