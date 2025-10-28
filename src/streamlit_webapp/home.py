import streamlit
from utils import SessionStateManager, django_orm_setup, webapp_menu

streamlit.set_page_config(page_title="Home", layout="wide")

django_orm_setup()
webapp_menu()

with SessionStateManager() as session_state_Manager:
    pass
