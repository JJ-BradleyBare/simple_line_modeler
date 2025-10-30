import uuid

from django.db import models

from .process import Process


class Swimlane(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)

    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"name={self.name} | process=[{self.process}]"
