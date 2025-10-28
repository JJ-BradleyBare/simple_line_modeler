import uuid

from django.db import models

from .swim_lane import SwimLane


class SwimLaneIndex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    swim_lane = models.ForeignKey(to=SwimLane, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"swim_lane=[{self.swim_lane}] | index={self.index}"
