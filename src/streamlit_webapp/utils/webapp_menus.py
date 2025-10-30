import streamlit


def webapp_menu():
    with streamlit.sidebar:
        streamlit.page_link(page="home.py", label="Home")
        streamlit.page_link(page="pages/device_functions.py", label="Device Functions")
        streamlit.page_link(page="pages/process_builder.py", label="Process Builder")
