from django.db import models

from django_orm.device.models import Function

from .base_step import BaseStep


class FunctionStep(BaseStep):
    function = models.ForeignKey(to=Function, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"swimlane=[{self.swimlane}] | function=[{self.function}]"
