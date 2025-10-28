import os
import pathlib
import sys

import django
import streamlit


def django_orm_setup():
    sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

    if not streamlit.session_state.get("django_orm_setup", False):
        streamlit.session_state["django_orm_setup"] = True

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_orm.django_config.settings")
        django.setup()
    # Only want to run once if not setup. Otherwise weird DB stuff can occur.
