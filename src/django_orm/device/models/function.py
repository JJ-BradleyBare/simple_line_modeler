from django.db import models

from django_orm.timed_item.models import BaseTimedItem

from .device import Device


class Function(BaseTimedItem):
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)

    execution_time_formula = models.CharField(max_length=255)

    # class Meta:
    #    unique_together = ["device", "name"]

    def __str__(self) -> str:
        return f"device=[{self.device}] | name={self.name}"

    def get_execution_time(self, sample_number: int) -> int:
        formula = self.execution_time_formula.replace("X", str(sample_number))
        return eval(formula)
