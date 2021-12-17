from ast import literal_eval
from typing import Optional, List, Union
from fastapi_users.db import TortoiseBaseUserModel
from tortoise import models, fields as f, manager
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from limeutils import modstr, listify
from pydantic import UUID4

from app import settings as s, ic, red, cache, utils
from app.pydantic import OptionTemplate
from app.authentication.models.common import DTBaseModel, SharedMixin, Option
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

    groups = f.ManyToManyField('models.Group', related_name='groupaccounts',
                               through='auth_xaccountgroups',
                               backward_key='account_id', forward_key='group_id')
    
    perms = f.ManyToManyField('models.Perm', related_name='permaccounts',
                              through='auth_xaccountperms',
                              backward_key='account_id', forward_key='perm_id')
    
    brokers = f.ManyToManyField('models.Broker', related_name='brokeraccounts',
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
                    d[field] = str(d[field])                                        # noqa
    
        if hasattr(self, 'groups'):
            d['groups'] = prefetch and [i.name for i in self.groups] or \
                          await self.groups.all().values_list('name', flat=True)

        if hasattr(self, 'perms'):
            d['perms'] = prefetch and [i.code for i in self.perms] or \
                         await self.perms.all().values_list('code', flat=True)

        if hasattr(self, 'options'):
            if prefetch:
                d['options'] = {i.name: i.value for i in self.options}
            else:
                rowlist = await self.options.all().values_list('name', 'value')
                d['options'] = dict(rowlist)
            d['options'] = OptionTemplate(**d['options']).dict()
        return d

    @classmethod
    async def get_and_cache(cls, id: UUID4, parsed: bool = True):
        """
        Get account data and save them to redis for easy access.
        :param id:      Account id
        :param parsed:  Return parsed data instead of caching data
        :return:    dict of data saved to cache
        """
        # TODO: Include options in Prefetch
        cached_fields = ['id', 'email', 'is_active', 'is_superuser', 'is_verified', *s.INCLUDE_FIELDS]
        try:
            query = cls.get(pk=str(id)) \
                .prefetch_related(
                    Prefetch('groups', queryset=Group.all().only('id', 'name')),
                    Prefetch('perms', queryset=Perm.all().only('id', 'code')),
                    Prefetch('accountoptions', queryset=Option.all()\
                             .only('id', 'name', 'value', 'account_id'), to_attr='options')
                ).only(*cached_fields)
            account = await query
            
            # if userdb.oauth_account_model is not None:
            #     query = query.prefetch_related("oauth_accounts")
            # usermod = await query.only(*userdb.select_fields)
            
            partialkey = s.CACHE_ACCOUNT.format(id)
            user_dict = await account.to_dict(prefetch=True)
            for_caching = cache.prepareuser_dict(user_dict)
            red.set(partialkey, for_caching, clear=True)
            
            return parsed and user_dict or for_caching
        
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

    async def has_perm(self, perm: str) -> bool:
        """
        Checks if user has a specific perm or is a part of a group.
        :param perm:    Check if user has this perm
        :return:        bool
        """
        permlist, missing = set(), []
        grouplist = await self.get_groups()
        for name in grouplist:
            partialkey = s.CACHE_GROUPNAME.format(name)
            if red.exists(partialkey):
                perms = set(red.get(partialkey))
                permlist = permlist.union(perms)
            else:
                missing.append(name)
        
        # Resave to cache if group cache is missing
        if missing:
            perms_dict = await Perm.filter(permgroups__name__in=missing)\
                                   .values('code', group='permgroups__name')
            d = {}
            for i in perms_dict:
                name, code = i['group'], i['code']
                d.setdefault(name, set())
                d[name].add(code)
                permlist.add(code)
                
                # Save to cache
                partialkey = s.CACHE_GROUPNAME.format(name)
                red.set(partialkey, list(d[name]), clear=True)
        #     ic(d)
        # ic(permlist)
        return perm in permlist
    
    async def has_group(self, group: str):
        pass
    
    async def get_groups(self) -> list:
        """Get group names assigned to the user. Updates cache if not exists."""
        if cachedata := self.get_cache('groups'):
            return cachedata['groups']
        grouplist = await Group.filter(groupaccounts=self.id).values_list('name', flat=True)
        await Account.get_and_cache(self.id)
        return grouplist or []

    async def update_cache(self):
        pass
        
    def get_cache(self, *keys) -> dict:
        """Get specific keys or just get all of them. Assumes cache exists."""
        partialkey = s.CACHE_ACCOUNT.format(self.id)
        if red.exists(partialkey):
            account_dict = red.get(partialkey)
            account_dict = cache.restoreuser_dict(account_dict)
            if keys:
                valid_keys = set(keys) & set(account_dict.keys())
                return {k: v for k, v in account_dict.items() if k in valid_keys}
            return account_dict
    

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