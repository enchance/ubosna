from typing import Optional
from fastapi_users.db import TortoiseBaseUserModel
from tortoise import models, fields as f, manager
from limeutils import modstr

from app import settings as s
from app.authentication.models.common import DTBaseModel, SharedMixin
from .manager import CuratorManager


class Account(DTBaseModel, TortoiseBaseUserModel):
    username = f.CharField(max_length=50, default='')
    display = f.CharField(max_length=50, default='')
    firstname = f.CharField(max_length=191, default='')
    midname = f.CharField(max_length=191, default='')
    lastname = f.CharField(max_length=191, default='')

    civil = f.CharField(max_length=20, default='')
    bday = f.DateField(null=True)
    status = f.CharField(max_length=20, default='')
    bio = f.CharField(max_length=191, default='')
    country = f.CharField(max_length=2, default='')
    zipcode = f.CharField(max_length=20, default='')
    timezone = f.CharField(max_length=10, default=s.USER_TIMEZONE)
    currency = f.CharField(max_length=5, default=s.CURRENCY_ACCOUNT)
    metadata = f.JSONField(null=True)

    groups = f.ManyToManyField('models.Group', related_name='group_accounts',
                               through='auth_xaccountgroups',
                               backward_key='account_id', forward_key='group_id')
    perms = f.ManyToManyField('models.Perm', related_name='perm_accounts',
                              through='auth_xaccountperms',
                              backward_key='account_id', forward_key='perm_id')
    # Project
    brokers = f.ManyToManyField('models.Broker', related_name='broker_users',
                                through='trades_xaccountbrokers',
                                backward_key='account_id', forward_key='broker_id')

    og = manager.Manager()
    
    class Meta:
        table = 'auth_account'
        manager = CuratorManager()
        
    def __str__(self):
        return modstr(self, 'id')
    
    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'.strip()
    
    async def to_dict(self):
        pass

    async def add_group(self, *groups) -> Optional[list]:
        """
        Add groups to a user and update redis
        :param groups:  Groups to add
        :return:        list The user's groups
        """
        # Get the ids of the groups
        
        
        # from app.auth import userdb
        #
        # groups = list(filter(None, groups))
        # groups = list(filter(valid_str_only, groups))
        # if not groups:
        #     return
        #
        # groups = await Group.filter(name__in=groups).only('id', 'name')
        # if not groups:
        #     return
        #
        # await self.groups.add(*groups)
        # names = await Group.filter(group_users__id=self.id) \
        #     .values_list('name', flat=True)
        #
        # partialkey = s.CACHE_USERNAME.format(self.id)
        # if user_dict := red.get(partialkey):
        #     user_dict = cache.restoreuser_dict(user_dict)
        #     user = userdb.usercomplete(**user_dict)
        # else:
        #     user = await UserMod.get_and_cache(self.id)
        #
        # user.groups = names
        # red.set(partialkey, cache.prepareuser_dict(user.dict()))
        # return user.groups
        pass
    

class AccountGroups(models.Model):
    account = f.ForeignKeyField('models.Account', related_name='accountgroups')
    group = f.ForeignKeyField('models.Group', related_name='accountgroups')
    author = f.ForeignKeyField('models.Account', related_name='author_accountgroups')
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()

    class Meta:
        table = 'auth_xaccountgroups'
        manager = CuratorManager()

    def __str__(self):
        return f'{self.account}:{self.group}'

class AccountPerms(models.Model):
    account = f.ForeignKeyField('models.Account', related_name='accountperms')
    perm = f.ForeignKeyField('models.Perm', related_name='accountperms')
    author = f.ForeignKeyField('models.Account', related_name='author_accountperms')
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_xaccountperms'
        manager = CuratorManager()

    def __str__(self):
        return f'{self.account}:{self.perm}'
    

class GroupPerms(models.Model):
    group = f.ForeignKeyField('models.Account', related_name='groupperms')
    perm = f.ForeignKeyField('models.Perm', related_name='groupperms')
    author = f.ForeignKeyField('models.Account', related_name='author_groupperms')
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_xgroupperms'
        manager = CuratorManager()
        
    def __str__(self):
        return f'{self.group}:{self.perm}'
    

# INCOMPLETE: Work in progress...
class Perm(SharedMixin, models.Model):
    code = f.CharField(max_length=30, unique=True)
    description = f.CharField(max_length=191, default='')
    author = f.ForeignKeyField('models.Account', related_name='author_perms')
    updated_at = f.DatetimeField(auto_now=True)
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_perm'
        ordering = ['code']
        manager = CuratorManager()
        
    def __str__(self):
        return modstr(self, 'code')


# INCOMPLETE: Work in progress...
class Group(SharedMixin, models.Model):
    name = f.CharField(max_length=191, unique=True)
    description = f.CharField(max_length=191, default='')
    author = f.ForeignKeyField('models.Account', related_name='author_groups')
    updated_at = f.DatetimeField(auto_now=True)
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_group'
        ordering = ['name']
        manager = CuratorManager()
        
    def __str__(self):
        return modstr(self, 'name')


class Token(SharedMixin, models.Model):
    token = f.CharField(max_length=128, unique=True)
    expires = f.DatetimeField(index=True)
    is_blacklisted = f.BooleanField(default=False)
    account = f.ForeignKeyField('models.Account', related_name='account_tokens')
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_token'
        ordering = ['created_at']
        manager = CuratorManager()
    
    def __str__(self):
        return modstr(self, 'token')