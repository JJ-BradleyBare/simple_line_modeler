from __future__ import annotations

import uuid

from django.db import models

from .base_step import BaseStep


class StepGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    steps: models.ManyToManyField[BaseStep, StepGroup] = models.ManyToManyField(to=BaseStep)

    def __str__(self) -> str:
        return f"steps=[{list(self.steps.all())}]"
