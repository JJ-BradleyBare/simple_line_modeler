import streamlit
from utils import SessionStateManager, django_orm_setup, webapp_menu

streamlit.set_page_config(page_title="Processes", layout="wide")

django_orm_setup()
webapp_menu()

with SessionStateManager() as session_state_Manager:
    streamlit.title("Processes")
    with streamlit.container(width=800):
        streamlit.text(
            "Processes will be built here using functions defined in the 'Device Functions' table. Processes can also reference other processes. A process will be comprised of a number of swim lanes each containing 1 or more steps.",
        )

    # Inject CSS to make the main content scroll horizontally
    streamlit.markdown(
        """
        <style>
        div.st-key-mykey {
            display: flex;
            flex: 1 1 0%;
            height: 100%;
            max-height: 100%;
            position: relative;
            gap: 0.5rem;
            overflow-x: scroll;
            flex-direction: row;
        }

        div.st-key-mykey>div {
            width: 10000px
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    with streamlit.container(key="mykey", border=True):
        with streamlit.container(width=10000, border=True):
            ...
