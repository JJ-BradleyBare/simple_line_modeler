import uuid

import streamlit
from utils import SessionStateManager, django_orm_setup, webapp_menu

streamlit.set_page_config(page_title="Device Functions", layout="wide")

django_orm_setup()
webapp_menu()

from django_orm.device.models import Device, Function


def callback_button_edit_table():
    streamlit.session_state["table_is_editable"] = True


def callback_button_cancel_table():
    streamlit.session_state["table_is_editable"] = False


def callback_button_save_table():
    table_data_original = streamlit.session_state["table_data_original"]
    table_data_edited = streamlit.session_state["table_data_edited"]

    edit_indexes = list(streamlit.session_state["table_data_edits"]["edited_rows"].keys())
    addition_data = streamlit.session_state["table_data_edits"]["added_rows"]
    deletion_indexes = streamlit.session_state["table_data_edits"]["deleted_rows"]

    validation_data = [table_data_edited[edit_index] for edit_index in edit_indexes] + addition_data
    validation_error = False

    for data in validation_data:
        try:
            _ = data["Device"]
        except:
            validation_error = True

        try:
            _ = data["Function"]
        except:
            validation_error = True

        try:
            execution_time = str(data["Execution Time Formula (sec)"])
            eval(execution_time.replace("X", "1"))
        except:
            validation_error = True

    if validation_error is True:
        streamlit.error(
            "Validation errors were detected during save. Ensure all columns contain data and 'Execution Time Formula (sec)' contains a capitalized X if it is parameterized.",
        )
        return

    for data in validation_data:
        device_name = data["Device"]
        function_name = data["Function"]
        execution_time = str(data["Execution Time Formula (sec)"])

        device, _ = Device.objects.get_or_create(name=device_name)

        if "id" in data:
            id = uuid.UUID(data["id"])
            function = Function.objects.get(id=id)
            function.device = device
            function.name = function_name
            function.execution_time_formula = execution_time
            function.save()

        else:
            function = Function(name=function_name, device=device, execution_time_formula=execution_time)
            function.save()

    for index in deletion_indexes:
        row = table_data_original[index]
        id = uuid.UUID(row["id"])

        function = Function.objects.get(id=id)
        function.delete()

    for device in Device.objects.all():
        if not Function.objects.filter(device=device).exists():
            device.delete()

    streamlit.session_state["table_is_editable"] = False


with SessionStateManager(
    "table_is_editable",
    "table_data_original",
    "table_data_edited",
    "table_data_edits",
) as session_state_manager:
    streamlit.title("Device Functions")
    with streamlit.container(width=800):
        streamlit.text(
            "The table below describes the functions present on each device and the time required to execute the function in seconds. The execution time can be parameterized with a capitalized X. The parameterization will be taken into account during simulation. Use the buttons below to add / remove functions or to update execution timing. Inputs will be validated when the edits are saved.",
        )

    if streamlit.session_state.get("table_is_editable", False) is False:
        streamlit.button("Edit Table", on_click=callback_button_edit_table)
    else:
        with streamlit.container(horizontal=True):
            streamlit.button("Save Table", on_click=callback_button_save_table)
            streamlit.button("Cancel Edits", on_click=callback_button_cancel_table)

    functions = Function.objects.all()

    data = streamlit.session_state["table_data_original"] = [
        {
            "id": str(function.id),
            "Device": function.device.name,
            "Function": function.name,
            "Execution Time Formula (sec)": function.execution_time_formula,
        }
        for function in Function.objects.prefetch_related("device").all()
    ]

    if streamlit.session_state.get("table_is_editable", False) is False:
        streamlit.dataframe(data, column_order=("Device", "Function", "Execution Time Formula (sec)"))
    else:
        streamlit.session_state["table_data_edited"] = streamlit.data_editor(
            data,
            num_rows="dynamic",
            column_order=("Device", "Function", "Execution Time Formula (sec)"),
            key="table_data_edits",
        )
