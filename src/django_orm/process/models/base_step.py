import uuid

from django.db import models
from polymorphic.models import PolymorphicModel

from .swim_lane import SwimLane


class BaseStep(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    swim_lane = models.ForeignKey(to=SwimLane, on_delete=models.CASCADE)
