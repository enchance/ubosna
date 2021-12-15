from typing import Union
from tortoise import fields as f, manager
from limeutils import modstr, reverse_choices

from app import settings as s
from app.auth import DTBaseModel, SharedMixin, CuratorManager, Media, Taxo, Account
from .pydantic import BuyCryptoPM
from .choices import ActionChoices

from . import get_quotecurr
from .pydantic import TradePM


class Broker(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=191, unique=True)
    label = f.CharField(max_length=191, default='')
    brokerno = f.CharField(max_length=191, default='')
    logo = f.ForeignKeyField('models.Media', related_name='logobrokers', on_delete=f.CASCADE)
    site = f.CharField(max_length=255, default='')
    currency = f.CharField(max_length=5, default=s.CURRENCY_BROKER)
    
    is_active = f.BooleanField(default=True)
    metadata = f.JSONField(null=True)

    og = manager.Manager()
    
    class Meta:
        table = 'trades_broker'
        manager = CuratorManager()


    def __str__(self):
        return modstr(self, 'name')
    
    
class AccountBrokers(SharedMixin, DTBaseModel):
    account = f.ForeignKeyField('models.Account', related_name='accountbrokers', on_delete=f.CASCADE)
    broker = f.ForeignKeyField('models.Broker', related_name='accountbrokers', on_delete=f.CASCADE)
    wallet = f.DecimalField(max_digits=19, decimal_places=8, default=0)
    traded = f.DecimalField(max_digits=19, decimal_places=8, default=0)
    status = f.CharField(max_length=20, default='active')
    
    is_primary = f.BooleanField(default=False)
    metadata = f.JSONField(null=True)
    
    og = manager.Manager()
    
    class Meta:
        table = 'trades_xaccountbrokers'
        manager = CuratorManager()
        

class Ticker(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=10)
    label = f.CharField(max_length=191, default='')
    tickertype = f.CharField(max_length=10, default='crypto')
    exchange = f.ForeignKeyField('models.Taxo', related_name='exchangetickers', on_delete=f.CASCADE)
    metadata = f.JSONField(null=True)

    og = manager.Manager()

    class Meta:
        table = 'trades_security'
        manager = CuratorManager()


class Archiver(DTBaseModel):
    amount = f.DecimalField(max_digits=20, decimal_places=8)
    pool = f.ForeignKeyField('models.Pool', related_name='poolarchives', on_delete=f.CASCADE)
    

class Pool(SharedMixin, DTBaseModel):
    currency = f.CharField(max_length=20, index=True)
    amount = f.DecimalField(max_digits=20, decimal_places=8)
    costave = f.DecimalField(max_digits=23, decimal_places=8)
    account = f.ForeignKeyField('models.Account', related_name='accountpools', on_delete=f.CASCADE)

    og = manager.Manager()

    class Meta:
        table = 'trades_pool'
        manager = CuratorManager()
        
    # INCOMPLETE: Work in progress...
    async def add(self):
        pass
        
        
class Trade(SharedMixin, DTBaseModel):
    action = f.SmallIntField(index=True)  # 1: buy, 2: sell
    price = f.DecimalField(max_digits=23, decimal_places=8)
    basecurr = f.CharField(max_length=20, index=True)   # ETH/usdt
    quotecurr = f.CharField(max_length=20, index=True)   # eth/USDT
    
    buyamount = f.DecimalField(max_digits=23, decimal_places=8)
    storedamount = f.DecimalField(max_digits=23, decimal_places=8)
    gross = f.DecimalField(max_digits=23, decimal_places=8)   # quotecurr
    feesmain = f.DecimalField(max_digits=23, decimal_places=8, default=None, null=True)
    feescurr = f.CharField(max_length=10)   # basecurr
    total = f.DecimalField(max_digits=23, decimal_places=8, default=0, null=True)
    leverage = f.SmallIntField(default=None, null=True)
    
    tradetype = f.CharField(max_length=20, index=True)      # crypto, stock
    status = f.CharField(max_length=20, default='')  # complete, ongoing?
    note = f.CharField(max_length=255, default='')
    
    pool = f.ForeignKeyField('models.Pool', related_name='pooltrades', on_delete=f.CASCADE)
    broker = f.ForeignKeyField('models.Broker', related_name='brokertrades', on_delete=f.CASCADE)
    exchange = f.ForeignKeyField('models.Taxo', related_name='exchangetrades', on_delete=f.CASCADE)
    
    is_closed = f.BooleanField(default=False, index=True)   # closing your position resets the pool
    account = f.ForeignKeyField('models.Account', related_name='accounttrades', on_delete=f.CASCADE)
    metadata = f.JSONField(null=True)

    tags = f.ManyToManyField('models.Taxo', related_name='tagtrades', through='trades_xtradetags',
                             backward_key='trade_id', forward_key='taxo_id')
    og = manager.Manager()
    
    class Meta:
        table = 'trades_trade'
        manager = CuratorManager()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    
    def __str__(self):
        if self.tradetype == 'crypto':
            name = f'{self.basecurr.upper()}{self.quotecurr.upper()}'
        else:
            name = self.basecurr.upper()
        actionstr = reverse_choices(ActionChoices, self.action)         # noqa
        return f'{actionstr.capitalize()} {name}@{self.price}'
    
    
    @classmethod
    async def trade(cls, trade_data: TradePM):
        # d = {
        #     'leverage': kwargs.get('leverage', 0),
        #     'status': kwargs.get('status', 'ongoing'),
        #     'note': kwargs.get('note', ''),
        #     'is_closed': kwargs.get('is_closed', False),
        #     'metadata': kwargs.get('metadata', {}),
        #     'tags': kwargs.get('tags', None),
        # }
        return await cls.create(**trade_data.dict())

    @classmethod
    def _buy(cls):
        pass
    
    @classmethod
    def _sell(cls):
        pass
    
    # INCOMPLETE: Work in progress...
    @classmethod
    def buycrypto(cls, trade: BuyCryptoPM):
        pass

    # INCOMPLETE: Work in progress...
    @classmethod
    def sellcrypto(cls, trade: BuyCryptoPM):
        pass

    # INCOMPLETE: Work in progress...
    @classmethod
    def buystock(cls, trade: BuyCryptoPM):
        pass

    # INCOMPLETE: Work in progress...
    @classmethod
    def sellstock(cls, trade: BuyCryptoPM):
        pass
