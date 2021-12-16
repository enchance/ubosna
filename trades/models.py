from typing import Union
from tortoise import fields as f, manager
from tortoise.exceptions import BaseORMException, DoesNotExist
from limeutils import modstr, reverse_choices

from app import settings as s
from app.auth import DTBaseModel, SharedMixin, CuratorManager, Media, Taxo, Account
from . import *
# from .pydantic import TradePM
# from .choices import ActionChoices



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
        unique_together = (('account', 'currency'),)
    
    def __str__(self):
        return self.id                                                                  # noqa
        
        
class Trade(SharedMixin, DTBaseModel):
    action = f.SmallIntField(index=True)  # 1: buy, 2: sell
    price = f.DecimalField(max_digits=23, decimal_places=8)
    basecurr = f.CharField(max_length=20, index=True)   # ETH/usdt
    quotecurr = f.CharField(max_length=20, index=True)   # eth/USDT
    
    amount = f.DecimalField(max_digits=23, decimal_places=8)
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

    def __str__(self):
        if self.tradetype == 'crypto':
            name = f'{self.basecurr.upper()}{self.quotecurr.upper()}'
        else:
            name = self.basecurr.upper()
        actionstr = reverse_choices(ActionChoices, self.action)         # noqa
        return f'{actionstr.capitalize()} {name}@{self.price}'


    # TESTME: Untested
    async def trade(self, trade_data: TradePM, action: ActionChoices):
        """
        Make a new trade with your trading data. You can use this directly but it's recommended to
        any of the buy/sell class methods instead which are easier.
        :param trade_data:  TradePM instance
        :param action:      Buy/Sell value via ActionChoices
        :return:            Trade
        """
        currency = action == ActionChoices.buy and trade_data.quotecurr or trade_data.basecurr
        trade_data.pool = get_pool(trade_data.account, currency)
        trade_data.exchange = trade_data.exchange or ''
        trade_data.broker = trade_data.broker or self
        trade_data.tags = trade_data.tags or None
        trade_data.leverage = trade_data.leverage or None
        # trade = self._compute_missing(trade_data)
        # return await self.create(**trade.dict())

    # # @classmethod
    # # def _compute_missing(cls, trade: TradePM) -> TradePM:
    # #     # TODO: Fill in values
    # #     d = {
    # #         'storeamount': trade.storeamount or 0,
    # #         'gross': trade.gross or 0,
    # #         'feesmain': trade.feesmain or 0,
    # #         'feescurr': trade.feescurr or '',
    # #         'total': trade.total or 0,
    # #         'tradetype': trade.tradetype or '',
    # #         'status': trade.status or '',
    # #         'is_closed': trade.is_closed or False,
    # #     }
    # #     trade = TradePM(**trade.dict(), **d)
    # #     return trade

    # TESTME: Untested
    async def buy_crypto(self, trade_data: TradePM):
        """
        Buy crypto.
        :param trade_data:  Refer to TradePM
        :return:            Trade
        """
        try:
            return await self.trade(trade_data, ActionChoices.buy)
        except BaseORMException as e:
            raise e

    # TODO: buy/sell method for stock
    # TODO: buy/sell method for forex