import streamlit
from utils import SessionStateManager, django_orm_setup, webapp_menu

streamlit.set_page_config(page_title="Processes", layout="wide")

django_orm_setup()
webapp_menu()

from django_orm.device.models import Function
from django_orm.process.models import Process, SwimLane

functions: dict[str, Function] = {
    f"{function.device.name} {function.name}": function for function in Function.objects.all()
}
processes: dict[str, Process] = {f"{process.name}": process for process in Process.objects.all()}

with SessionStateManager() as session_state_manager:
    streamlit.title("Processes")
    with streamlit.container(width=800):
        streamlit.text(
            "Processes will be built here using functions defined in the 'Device Functions' table. Processes can also reference other processes. A process will be comprised of a number of swim lanes each containing 1 or more steps.",
        )
        streamlit.selectbox("Select A Process", [])

        with streamlit.container(horizontal=True):
            streamlit.button("Edit Process")

    streamlit.divider()

    with streamlit.container(horizontal=True):
        with streamlit.container(width=300, border=True):
            with streamlit.container(gap=None):
                with streamlit.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
                    streamlit.button(
                        "",
                        icon=":material/arrow_back_ios:",
                        type="tertiary",
                        help="Move swimlane left",
                        key="button_move_swimlane_left",
                    )
                    streamlit.text_input("Swimlane Name", help="Name for the swimlane")
                    streamlit.button(
                        "",
                        icon=":material/arrow_forward_ios:",
                        type="tertiary",
                        help="Move swimlane right",
                        key="button_move_swimlane_right",
                    )

                streamlit.divider()

                with streamlit.container(gap=None):
                    with streamlit.container(horizontal_alignment="center"):
                        streamlit.button(
                            "",
                            icon=":material/add_diamond:",
                            type="tertiary",
                            help="Add step",
                            key="button_add_step",
                        )
                    with streamlit.container(border=True, gap=None):
                        step_type = streamlit.selectbox(
                            "Step Type",
                            ["Device Function", "Process"],
                            help="A step can reference either a single device function or a process made up of a set of complex swimlanes and steps.",
                        )
                        streamlit.markdown("<br>", unsafe_allow_html=True)
                        streamlit.text_input(
                            "Step Synchronization Key",
                            help="Optional key to synchronize steps across swim lanes.",
                        )

                        streamlit.divider()

                        if step_type == "Device Function":
                            function = streamlit.selectbox("Function", sorted(functions.keys()))
                        else:
                            process = streamlit.selectbox("Process", sorted(processes.keys()))

                            swim_lanes: dict[str, SwimLane] = {
                                f"{swim_lane.name}": swim_lane
                                for swim_lane in SwimLane.objects.filter(process=processes[process]).all()
                            }
                            streamlit.markdown("<br>", unsafe_allow_html=True)
                            dependent_swim_lanes = streamlit.multiselect(
                                "Dependent Swim Lanes",
                                sorted(swim_lanes.keys()),
                                help="Swim lanes in the selected process that must complete before this step can be executed.",
                            )
