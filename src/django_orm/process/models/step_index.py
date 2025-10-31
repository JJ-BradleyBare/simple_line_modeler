import uuid

from django.db import models

from .step import Step


class StepIndex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    step = models.ForeignKey(to=Step, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"step=[{self.step}] | index={self.index}"
