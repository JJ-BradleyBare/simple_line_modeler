import uuid

from django.db import models

from .device import Device


class Function(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)

    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)

    execution_time_formula = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"device=[{self.device}] | name={self.name}"
