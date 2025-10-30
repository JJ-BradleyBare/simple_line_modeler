from __future__ import annotations

from django.db import models

from .base_step import BaseStep
from .process import Process
from .swimlane import Swimlane


class ProcessStep(BaseStep):
    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)

    swimlanes_constraint: models.ManyToManyField[Swimlane, ProcessStep] = models.ManyToManyField(
        to=Swimlane,
        blank=True,
    )

    def __str__(self) -> str:
        return f"swimlane=[{self.swimlane}] | process=[{self.process}] | swimlanes_constraint=[{list(self.swimlanes_constraint.all())}]"
