import pytz
from typing import Optional, List
from tortoise import fields as f, models
from limeutils import modstr



class DTmixin(object):
    deleted_at = f.DatetimeField(null=True)
    updated_at = f.DatetimeField(auto_now=True)
    created_at = f.DatetimeField(auto_now_add=True)


# INCOMPLETE: Work in progress...
class SharedMixin(object):
    # TODO: See if there is a pydantic solution
    # def to_dict(self, *, exclude: Optional[List[str]] = None, only: Optional[List[str]] = None):
    #     """
    #     Convert an object to a dict
    #     :param exclude: Field names to exclude. If empty then all fields are taken.
    #     :param only:    Only use these names. If empty then the object's fields are used.
    #     :return:        dict
    #     """
    #     d = {}
    #     exclude = ['created_at', 'deleted_at', 'updated_at'] if exclude is None else exclude
    #     fieldlist = self._meta.db_fields if only is None else only                      # noqa
    #     for field in fieldlist:      # noqa
    #         if hasattr(self, field):
    #             if (only and field in only) or field not in exclude:
    #                 d[field] = getattr(self, field)
    #     return d
    
    async def soft_delete(self):
        self.deleted_at = datetime.now(tz=pytz.UTC)                 # noqa
        await self.save(update_fields=['deleted_at'])               # noqa


class Taxo(DTmixin, SharedMixin, models.Model):
    name = f.CharField(max_length=50)
    display = f.CharField(max_length=50, default='')
    description = f.CharField(max_length=191, default='')
    taxotype = f.SmallIntField(default=1, index=True)
    sort = f.SmallIntField(default=100)
    parent = f.ForeignKeyField('models.Taxo', related_name='parent_taxos', null=True)

    is_active = f.BooleanField(default=True)
    is_global = f.BooleanField(default=False)
    account = f.ForeignKeyField('models.Account', related_name='account_taxos', null=True)
    author = f.ForeignKeyField('models.Account', related_name='author_taxos')

    class Meta:
        table = 'core_taxo'
        unique_together = (('name', 'taxotype'),)
        # TODO: Add manager

    def __str__(self):
        return modstr(self, 'name')