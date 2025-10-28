from __future__ import annotations

from django.db import models

from .base_step import BaseStep
from .process import Process
from .swim_lane import SwimLane


class ProcessStep(BaseStep):
    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)

    swim_lanes_constraint: models.ManyToManyField[SwimLane, ProcessStep] = models.ManyToManyField(
        to=SwimLane,
        blank=True,
    )

    def __str__(self) -> str:
        return f"swim_lane=[{self.swim_lane}] | process=[{self.process}] | swim_lanes_constraint=[{list(self.swim_lanes_constraint.all())}]"
