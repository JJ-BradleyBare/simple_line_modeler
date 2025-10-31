from __future__ import annotations

import uuid

from django.db import models

from .step import Step


class StepParallelization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    steps: models.ManyToManyField[Step, StepParallelization] = models.ManyToManyField(to=Step)

    def __str__(self) -> str:
        return f"steps=[{list(self.steps.all())}]"
