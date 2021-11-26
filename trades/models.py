from tortoise import fields as f, manager
from limeutils import modstr

from app import settings as s
from app.auth import DTBaseModel, SharedMixin, CuratorManager, Media



class Broker(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=191, unique=True)
    short = f.CharField(max_length=10, default='')
    brokerno = f.CharField(max_length=191, default='')
    logo = f.ForeignKeyField('models.Media', related_name='logobrokers')
    site = f.CharField(max_length=255, default='')
    currency = f.CharField(max_length=5, default=s.CURRENCY_BROKER)
    
    is_active = f.BooleanField(default=True)
    metadata = f.JSONField(null=True)
    author = f.ForeignKeyField('models.Account', related_name='author_brokers', on_delete=f.CASCADE)

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
        

class Security(SharedMixin, DTBaseModel):
    ticker = f.CharField(max_length=10)
    label = f.CharField(max_length=191)
    securitytype = f.CharField(max_length=10, default='stock')

    og = manager.Manager()

    class Meta:
        table = 'trades_security'
        manager = CuratorManager()


class Trade(SharedMixin, DTBaseModel):
    security = f.ForeignKeyField('models.Security', related_name='securitytrades',
                                 on_delete=f.SET_NULL, null=True)
    action = f.CharField(max_length=10)  # ActionChoices
    price = f.DecimalField(max_digits=16, decimal_places=8, null=True)
    amount = f.IntField(max_digits=18, decimal_places=8, null=True)
    gross = f.DecimalField(max_digits=12, decimal_places=4, default=0, null=True)
    fees = f.DecimalField(max_digits=12, decimal_places=4, default=0, null=True)
    total = f.DecimalField(max_digits=10, decimal_places=4, default=0, null=True)
    status = f.CharField(max_length=20, default='')  # Not sure what it's for right now
    currency = f.CharField(max_length=3, null=True)
    broker = f.ForeignKeyField('models.Broker', related_name='brokertrades',
                               on_delete=f.SET_NULL, null=True)
    note = f.CharField(max_length=255, default='')
    tradetype = f.CharField(max_length=20)      # crypto, stock
    leverage = f.SmallIntField(default=None, null=True)
    
    account = f.ForeignKeyField('models.Account', related_name='accounttrades', on_delete=f.CASCADE)
    metadata = f.JSONField(null=True)
    # stash = f.ForeignKeyField('models.Stash', related_name='trades')
    #
    #
    # basetrade: FKRel['Trade'] = f.ForeignKeyField('models.Trade', related_name='basetrade_trades',
    #                                       null=True)
    #
    # is_resolved = f.BooleanField(default=True, index=True)
    # author: FKRel['UserMod'] = f.ForeignKeyField('models.UserMod', related_name='author_trades')
    #
    tags = f.ManyToManyField('models.Taxo', related_name='tag_trades', through='trades_xtradetags',
                             backward_key='trade_id', forward_key='taxo_id')

    og = manager.Manager()
    
    class Meta:
        table = 'trades_trade'
        manager = CuratorManager()
        
    def __str__(self):
        div = '' if self.tradetype == 'crypto' else '/'
        name = f'{self.security.ticker.upper()}{div}{self.currency.upper()}'
        return f'{self.action.capitalize()} {name} @{self.price}'
