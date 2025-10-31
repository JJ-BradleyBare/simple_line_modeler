import uuid

from django.db import models
from polymorphic.models import PolymorphicModel


class BaseTimedItem(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
