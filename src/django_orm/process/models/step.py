from __future__ import annotations

import uuid

from django.db import models
from polymorphic.models import PolymorphicModel

from django_orm.timed_item.models import BaseTimedItem

from .swimlane import Swimlane


class Step(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    swimlane = models.ForeignKey(to=Swimlane, on_delete=models.CASCADE)

    timed_item = models.ForeignKey(to=BaseTimedItem, on_delete=models.CASCADE)

    swimlanes_constraint: models.ManyToManyField[Swimlane, Step] = models.ManyToManyField(
        to=Swimlane,
        blank=True,
    )

    def __str__(self) -> str:
        return f"swimlane=[{self.swimlane}] | timed_item=[{self.timed_item}] | swimlanes_constraint=[{list(self.swimlanes_constraint.all())}]"
