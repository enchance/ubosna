from tortoise.models import Manager
from tortoise.queryset import QuerySet



class CuratorManager(Manager):
    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if 'deleted_at' in self._model._meta.db_fields:
            qs = qs.filter(deleted_at=None)
        # if 'is_active' in self._model._meta.db_fields:
        #     qs = qs.filter(is_active=True)
        return qs