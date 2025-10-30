import typing

import streamlit
from utils import SessionStateManager, django_orm_setup, webapp_menu

streamlit.set_page_config(page_title="Processes", layout="wide")

django_orm_setup()
webapp_menu()

from django_orm.device.models import Function
from django_orm.process.models import FunctionStep, Process, ProcessStep, StepIndex, Swimlane, SwimlaneIndex

functions: dict[str, Function] = {
    f"{function.device.name} {function.name}": function for function in Function.objects.all()
}
processes: dict[str, Process] = {f"{process.name}": process for process in Process.objects.all()}


def callback_selectbox_select_process():
    streamlit.session_state["process_is_editable"] = False


def callback_button_edit_process():
    streamlit.session_state["process_is_editable"] = True


def callback_button_cancel_process():
    streamlit.session_state["process_is_editable"] = False


def callback_button_save_process():
    selected_process = processes[str(streamlit.session_state["selected_process_key"])]
    new_process_name = str(streamlit.session_state["text_input_process_name"])

    selected_process.name = new_process_name
    selected_process.save()

    streamlit.session_state["selected_process_key"] = new_process_name

    streamlit.session_state["process_is_editable"] = False


def callback_button_move_swimlane_left(index: int):
    process_swimlanes = streamlit.session_state["process_swimlanes"]

    swimlane = process_swimlanes.pop(index)
    process_swimlanes.insert(index - 1 if (index - 1) != 0 else 0, swimlane)


def callback_button_move_swimlane_right(index: int):
    process_swimlanes = streamlit.session_state["process_swimlanes"]

    swimlane = process_swimlanes.pop(index)
    process_swimlanes.insert(index + 1, swimlane)


with SessionStateManager(
    "process_is_editable",
    "selected_process_key",
    "text_input_process_name",
    "selected_process_swimlanes",
    "process_swimlane_steps",
) as session_state_manager:
    process_is_editable = streamlit.session_state.get("process_is_editable", False)

    streamlit.title("Processes")
    with streamlit.container(width=800):
        streamlit.text(
            "Processes will be built here using functions defined in the 'Device Functions' table. Processes can also reference other processes. A process will be comprised of a number of swim lanes each containing 1 or more steps.",
        )
        process_key = streamlit.selectbox(
            "Select A Process",
            sorted(processes.keys()),
            key="selected_process_key",
            on_change=callback_selectbox_select_process,
        )

        if process_is_editable is False:
            streamlit.button("Edit Process", on_click=callback_button_edit_process)
        else:
            with streamlit.container(horizontal=True):
                streamlit.button("Save Process", on_click=callback_button_save_process)
                streamlit.button("Cancel Edits", on_click=callback_button_cancel_process)

    streamlit.divider()

    process = processes[process_key]

    if process_is_editable is True:
        with streamlit.container(horizontal_alignment="center"):
            streamlit.text_input(
                "Process Name",
                width=800,
                label_visibility="collapsed",
                value=process.name,
                key="text_input_process_name",
            )
            streamlit.button("Add Swimlane")

    with streamlit.container(horizontal=True):
        session_state_manager.add_persistent_keys("process_swimlanes")

        if process_is_editable is False:
            streamlit.session_state["process_swimlanes"] = [
                swimlane_index.swimlane
                for swimlane_index in SwimlaneIndex.objects.filter(
                    swimlane__process=process,
                )
                .order_by("index")
                .all()
            ]

        for index, process_swimlane in enumerate(streamlit.session_state["process_swimlanes"]):
            with streamlit.container(width=300, border=True, gap=None):
                with streamlit.container(
                    horizontal=True,
                    horizontal_alignment="center",
                    vertical_alignment="center",
                ):
                    if process_is_editable is True:
                        streamlit.button(
                            "",
                            icon=":material/arrow_back_ios:",
                            type="tertiary",
                            help="Move Swimlane left",
                            key=f"{process_swimlane.id}_button_move_Swimlane_left",
                            on_click=callback_button_move_swimlane_left,
                            args=(index,),
                        )
                    streamlit.text_input(
                        "Swimlane Name",
                        help="Name for the Swimlane",
                        value=process_swimlane.name,
                        key=f"{process_swimlane.id}_text_input_Swimlane_name",
                        disabled=not process_is_editable,
                    )
                    if process_is_editable is True:
                        streamlit.button(
                            "",
                            icon=":material/arrow_forward_ios:",
                            type="tertiary",
                            help="Move Swimlane right",
                            key=f"{process_swimlane.id}_button_move_Swimlane_right",
                            on_click=callback_button_move_swimlane_right,
                            args=(index,),
                        )

                streamlit.divider()

                if process_is_editable is True:
                    with streamlit.container(horizontal_alignment="center"):
                        streamlit.button(
                            "",
                            icon=":material/add_diamond:",
                            type="tertiary",
                            help="Add step",
                            key=f"{process_swimlane.id}_button_add_step_before",
                        )

                session_state_manager.add_persistent_keys(f"process_swimlane_{process_swimlane.id}_steps")

                if process_is_editable is False:
                    streamlit.session_state[f"process_swimlane_{process_swimlane.id}_steps"] = [
                        step_index.step
                        for step_index in StepIndex.objects.filter(step__swimlane=process_swimlane)
                        .order_by("index")
                        .all()
                    ]

                for index, process_swimlane_step in enumerate(
                    streamlit.session_state[f"process_swimlane_{process_swimlane.id}_steps"],
                ):
                    with streamlit.container(border=True, gap=None):
                        step_type = streamlit.selectbox(
                            "Step Type",
                            ["Device Function", "Process"],
                            help="A step can reference either a single device function or a process made up of a set of complex Swimlanes and steps.",
                            index=0 if isinstance(process_swimlane_step, FunctionStep) else 1,
                            key=f"{process_swimlane_step.id}_selectbox_step_type",
                            disabled=not process_is_editable,
                        )
                        streamlit.markdown("<br>", unsafe_allow_html=True)
                        streamlit.text_input(
                            "Step Parallelization Key",
                            help="Optional key that causes steps with the same key to be processes at the same time on the same device.",
                            key=f"{process_swimlane_step.id}_text_input_step_synchronization_key",
                            disabled=not process_is_editable,
                        )

                        streamlit.divider()

                        if step_type == "Device Function":
                            step_function_key = streamlit.selectbox(
                                "Function",
                                sorted(functions.keys()),
                                key=f"{process_swimlane_step.id}_selectbox_function",
                                disabled=not process_is_editable,
                            )
                        else:
                            process_swimlane_step = typing.cast("ProcessStep", process_swimlane_step)

                            step_process_key = streamlit.selectbox(
                                "Process",
                                sorted(processes.keys()),
                                key=f"{process_swimlane_step.id}_selectbox_process",
                                disabled=not process_is_editable,
                            )
                            streamlit.markdown("<br>", unsafe_allow_html=True)

                            step_process_swimlanes: dict[str, Swimlane] = {
                                f"{swimlane.name}": swimlane
                                for swimlane in Swimlane.objects.filter(process=processes[step_process_key]).all()
                            }

                            dependent_step_process_swimlane_keys = streamlit.multiselect(
                                "Dependent Swim Lanes",
                                sorted(step_process_swimlanes.keys()),
                                help="Swim lanes in the selected process that must complete before this step can be executed.",
                                key=f"{process_swimlane_step.id}_multiselect_dependent_swimlanes",
                                default=[
                                    swimlane.name for swimlane in process_swimlane_step.swimlanes_constraint.all()
                                ],
                                disabled=not process_is_editable,
                            )

                    if process_is_editable is True:
                        with streamlit.container(horizontal_alignment="center"):
                            streamlit.button(
                                "",
                                icon=":material/add_diamond:",
                                type="tertiary",
                                help="Add step",
                                key=f"{process_swimlane_step.id}_button_add_step_after",
                            )
                    else:
                        streamlit.markdown("<br>", unsafe_allow_html=True)
