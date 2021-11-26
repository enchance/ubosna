from typing import Optional, List
from fastapi_users.db import TortoiseBaseUserModel
from tortoise import models, fields as f, manager
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from limeutils import modstr, listify
from pydantic import UUID4

from app import settings as s, ic, red, cache
from app.authentication.models.common import DTBaseModel, SharedMixin
from app.utils import flatten_query_result
from .manager import CuratorManager

# TODO: Move Account fields to Profile model instead


class Account(SharedMixin, DTBaseModel, TortoiseBaseUserModel):
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
    lang = f.CharField(max_length=2, default='en')
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

    # TODO: Revise as needed
    async def to_dict(self, exclude: Optional[List[str]] = None, prefetch: bool = False) -> dict:
        """
        Converts instance into a dict.
        :param exclude:     Fields not to explicitly include
        :param prefetch:    Query used prefetch_related to save on db hits
        :return:            dict
        """
        d = {}
        exclude = ['created_at', 'deleted_at', 'updated_at', 'hashed_password'] if exclude is None \
            else exclude
        for field in self._meta.db_fields:
            if hasattr(self, field) and field not in exclude:
                d[field] = getattr(self, field)
                if field == 'id':
                    d[field] = str(d[field])
    
        if hasattr(self, 'groups'):
            if prefetch:
                d['groups'] = [i.name for i in self.groups]
            else:
                d['groups'] = await self.groups.all().values_list('name', flat=True)
        if hasattr(self, 'options'):
            if prefetch:
                d['options'] = {i.name: i.value for i in self.options}
            else:
                d['options'] = {
                    i.name: i.value for i in
                    await self.options.all().only('id', 'name', 'value', 'is_active') if i.is_active
                }
        # if hasattr(self, 'permissions'):
        #     if prefetch:
        #         d['permissions'] = [i.code for i in self.permissions]
        #     else:
        #         d['permissions'] = await self.permissions.all().values_list('code', flat=True)
        return d

    @classmethod
    async def get_and_cache(cls, id: UUID4):
        try:
            query = cls.get(pk=id)\
                .prefetch_related(
                    Prefetch('groups', queryset=Group.all().only('id', 'name')),
                    # Prefetch('options', queryset=Option.all().only('user_id', 'name', 'value')),
                    # Prefetch('permissions', queryset=Permission.filter(deleted_at=None).only('id', 'code'))
                )
            account = await query
            
            # if userdb.oauth_account_model is not None:
            #     query = query.prefetch_related("oauth_accounts")
            # usermod = await query.only(*userdb.select_fields)
            
            user_dict = await account.to_dict(prefetch=True)
            partialkey = s.CACHE_USERNAME.format(id)
            user_dict = cache.prepareuser_dict(user_dict)
            red.set(partialkey, cache.prepareuser_dict(user_dict), clear=True)
            return user_dict
        except DoesNotExist:
            pass

    async def add_group(self, *grouplist) -> Optional[set]:
        """
        Add groups to a user and update redis.
        :param grouplist:   Groups to add
        :return:            Set of added groups. Any existing groups are removed from the list.
        """
        if not grouplist:
            return
        
        # TODO: Save to cache
        grouplist = set(grouplist)
        existing = set(await self.get_groups())
        to_add = grouplist - existing
        
        if to_add:
            group_ids = await Group.filter(name__in=to_add).only('id', 'name')
            to_save = [AccountGroups(account=self, group=id, author=self) for id in group_ids]
            await AccountGroups.bulk_create(to_save)
        return to_add
        
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

    async def has_perm(self, codeorgroup: str) -> bool:
        """
        Checks if user has a specific perm or is a part of a group.
        :param codeorgroup: Perm code or group name
        :return:            bool
        """
        # TODO: Use caching
        group_names = await self.get_groups()
        perm_codes = group_names and await Perm.get_perms(*group_names) or []
        return codeorgroup in group_names or codeorgroup in perm_codes
    
    async def get_groups(self) -> List[str]:
        """Get group names assigned to the user."""
        # TODO: Use caching
        groupnames = await Group.filter(group_accounts=self.id).values('name')
        return groupnames and flatten_query_result('name', groupnames) or []
    

class AccountGroups(models.Model):
    account = f.ForeignKeyField('models.Account', related_name='accountgroups', on_delete=f.CASCADE)
    group = f.ForeignKeyField('models.Group', related_name='accountgroups', on_delete=f.CASCADE)
    author = f.ForeignKeyField('models.Account', related_name='author_accountgroups', on_delete=f.CASCADE)
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()

    class Meta:
        table = 'auth_xaccountgroups'
        manager = CuratorManager()

    def __str__(self):
        return f'{self.account}:{self.group}'


class AccountPerms(models.Model):
    account = f.ForeignKeyField('models.Account', related_name='accountperms', on_delete=f.CASCADE)
    perm = f.ForeignKeyField('models.Perm', related_name='accountperms', on_delete=f.CASCADE)
    author = f.ForeignKeyField('models.Account', related_name='author_accountperms', on_delete=f.CASCADE)
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_xaccountperms'
        manager = CuratorManager()

    def __str__(self):
        return f'{self.account}:{self.perm}'
    

class GroupPerms(models.Model):
    group = f.ForeignKeyField('models.Group', related_name='groupperms', on_delete=f.CASCADE)
    perm = f.ForeignKeyField('models.Perm', related_name='groupperms', on_delete=f.CASCADE)
    created_at = f.DatetimeField(auto_now_add=True)

    og = manager.Manager()
    
    class Meta:
        table = 'auth_xgroupperms'
        manager = CuratorManager()
        
    def __str__(self):
        return f'{self.group}:{self.perm}'
    

class Perm(DTBaseModel):
    code = f.CharField(max_length=30, unique=True)
    description = f.CharField(max_length=191, default='')
    deleted_at = None

    og = manager.Manager()
    
    class Meta:
        table = 'auth_perm'
        ordering = ['code']
        manager = CuratorManager()
        
    def __str__(self):
        return modstr(self, 'code')

    @classmethod
    async def get_perms(cls, *groupnames) -> List[str]:
        """
        Get a consolidated list of perms of the groupnames
        :param groupnames:  name of groups
        :return:            list
        """
        if not groupnames:
            return []

        in_db = []
        perms = []

        for name in groupnames:
            # Check cache
            partialkey = s.CACHE_GROUPNAME.format(name)
            if cacheperms := red.exists(partialkey) and red.get(partialkey):
                perms.extend(cacheperms)
            else:
                in_db.append(name)

        # Check db if not in cache
        if in_db:
            dbperms = await cls.filter(permgroups__name__in=in_db).values_list('code', flat=True)
            perms.extend(dbperms)
        return perms


class Group(DTBaseModel):
    name = f.CharField(max_length=191, unique=True)
    description = f.CharField(max_length=191, default='')
    deleted_at = None
    
    perms = f.ManyToManyField('models.Perm', related_name='permgroups',
                              through='auth_xgroupperms',
                              backward_key='group_id', forward_key='perm_id')

    og = manager.Manager()
    
    class Meta:
        table = 'auth_group'
        ordering = ['name']
        manager = CuratorManager()
        
    def __str__(self):
        return modstr(self, 'name')

    @classmethod
    async def get_and_cache(cls, group: str) -> list:
        """
        Get a group's permissions and cache it for future use. Replaces data if exists.
        Only one group must be given so each can be cached separately.
        :param group:   Group name
        :return:        list
        """
    
        if perms := await Perm.get_perms(group):
            # Cache perms of the group
            partialkey = s.CACHE_GROUPNAME.format(group)
            red.set(partialkey, perms, ttl=-1, clear=True)
            
            # Cache list of all groups
            grouplist = red.exists('groups') and red.get('groups') or []
            if group not in grouplist:
                grouplist.append(group)
                red.set('groups', grouplist, clear=True)
        return perms


class Token(DTBaseModel):
    token = f.CharField(max_length=128, unique=True)
    expires = f.DatetimeField(index=True)
    is_blacklisted = f.BooleanField(default=False)
    account = f.ForeignKeyField('models.Account', related_name='accounttokens', on_delete=f.CASCADE)
    deleted_at = None

    og = manager.Manager()
    
    class Meta:
        table = 'auth_token'
        ordering = ['created_at']
        manager = CuratorManager()
    
    def __str__(self):
        return modstr(self, 'token')