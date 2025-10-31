from django_orm.timed_item.models import BaseTimedItem


class Process(BaseTimedItem):
    def __str__(self) -> str:
        return f"name={self.name}"
