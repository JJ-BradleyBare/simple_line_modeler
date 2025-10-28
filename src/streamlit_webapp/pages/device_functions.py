import streamlit
from utils import django_orm_setup, webapp_menu

django_orm_setup()
webapp_menu()

streamlit.set_page_config(page_title="Device Functions", layout="wide")
