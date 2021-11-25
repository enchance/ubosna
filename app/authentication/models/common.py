import pytz
from typing import Optional, List
from tortoise import fields as f, models, manager
from limeutils import modstr

from .manager import CuratorManager



class DTBaseModel(models.Model):
    deleted_at = f.DatetimeField(null=True, index=True)
    updated_at = f.DatetimeField(auto_now=True)
    created_at = f.DatetimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


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


class Taxo(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=50)
    display = f.CharField(max_length=50, default='')
    description = f.CharField(max_length=191, default='')
    sort = f.SmallIntField(default=100)
    parent = f.ForeignKeyField('models.Taxo', related_name='parent_taxos', null=True, on_delete=f.CASCADE)
    taxotype = f.SmallIntField(default=1, index=True)       # TaxoTypeChoices

    is_active = f.BooleanField(default=True)
    is_global = f.BooleanField(default=False)
    account = f.ForeignKeyField('models.Account', related_name='account_taxos', null=True, on_delete=f.CASCADE)
    author = f.ForeignKeyField('models.Account', related_name='author_taxos')

    og = manager.Manager()
    
    class Meta:
        table = 'core_taxo'
        ordering = ['sort', 'name']
        manager = CuratorManager()

    def __str__(self):
        return modstr(self, 'name')
    
    @classmethod
    async def get_and_cache(cls, taxotype: int, name: str):
        """Get data and force save it to cache."""
        pass
        # INCOMPLETE: Work in progress...


class Option(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=20)
    value = f.CharField(max_length=191)
    optiontype = f.CharField(max_length=10)
    
    is_active = f.BooleanField(default=True)
    account = f.ForeignKeyField('models.Account', related_name='account_options', null=True, on_delete=f.CASCADE)
    deleted_at = None

    og = manager.Manager()
    
    class Meta:
        table = 'core_option'
        ordering = ['name']
        manager = CuratorManager()
    
    def __str__(self):
        return modstr(self, 'name')

    @classmethod
    async def get_and_cache(cls, taxotype: int, name: str):
        """Get data and force save it to cache."""
        pass
        # INCOMPLETE: Work in progress...


class Media(SharedMixin, DTBaseModel):
    url = f.CharField(max_length=256, unique=True)
    filename = f.CharField(max_length=199)
    width = f.SmallIntField(null=True)
    height = f.SmallIntField(null=True)
    label = f.CharField(max_length=191, default='')
    size = f.SmallIntField(null=True)
    status = f.CharField(max_length=20)         # Set original, modified, delete
    mediatype = f.SmallIntField(default=1, index=True)
    
    is_active = f.BooleanField(default=True)
    account = f.ForeignKeyField('models.Account', related_name='account_media', on_delete=f.CASCADE)
    metadata = f.JSONField(null=True)

    og = manager.Manager()
    
    class Meta:
        table = 'core_media'
        ordering = ['url']
        manager = CuratorManager()
    
    def __str__(self):
        return modstr(self, 'filename')

    @classmethod
    async def get_and_cache(cls, taxotype: int, name: str):
        """Get data and force save it to cache."""
        pass
        # INCOMPLETE: Work in progress...