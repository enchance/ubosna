import pytz
from typing import Optional, List
from tortoise import fields as f, models, manager
from limeutils import modstr

from app import ic, red, settings as s, cache
from app.pydantic import OptionTemplate
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
    label = f.CharField(max_length=191, default='')
    description = f.CharField(max_length=191, default='')
    sort = f.SmallIntField(default=100)
    parent = f.ForeignKeyField('models.Taxo', related_name='parenttaxos', null=True, on_delete=f.CASCADE)
    taxotype = f.CharField(max_length=10, index=True)

    is_active = f.BooleanField(default=True)
    is_global = f.BooleanField(default=False)
    account = f.ForeignKeyField('models.Account', related_name='account_taxos', null=True, on_delete=f.CASCADE)
    deleted_at = None

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
    optiontype = f.CharField(max_length=10, index=True)
    
    is_active = f.BooleanField(default=True)
    account = f.ForeignKeyField('models.Account', related_name='accountoptions', null=True, on_delete=f.CASCADE)
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
    
    @classmethod
    async def get_templates(cls) -> OptionTemplate:
        partialkey = s.CACHE_OPTION_TEMPLATE
        if d := red.exists(partialkey) and red.get(partialkey) or {}:
            # ic('cache')
            return OptionTemplate(**d)
        # ic('db')
        d = dict(await cls.filter(optiontype='template').values_list('name', 'value'))
        d = OptionTemplate(**d)
        red.set(partialkey, cache.makesafe_dict(d.dict()), clear=True)
        return d
        


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
    account = f.ForeignKeyField('models.Account', related_name='accountmedia', on_delete=f.CASCADE)
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