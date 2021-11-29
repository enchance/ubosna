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
        

class Ticker(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=10)
    label = f.CharField(max_length=191, default='')
    tickertype = f.CharField(max_length=10, default='crypto')
    metadata = f.JSONField(null=True)

    og = manager.Manager()

    class Meta:
        table = 'trades_security'
        manager = CuratorManager()


# INCOMPLETE: Work in progress...
class Pool(SharedMixin, DTBaseModel):
    amount = f.IntField(max_digits=18, decimal_places=8, null=True)
    currency = f.CharField(max_length=3, null=True)
    account = f.ForeignKeyField('models.Account', related_name='accountpools', on_delete=f.CASCADE)
    # divider = f.SmallIntField(default=1)    # Impt for getting the average

    og = manager.Manager()

    class Meta:
        table = 'trades_pool'
        manager = CuratorManager()
        
    # INCOMPLETE: Work in progress...
    @classmethod
    async def add(cls):
        pass
        
        
class Trade(SharedMixin, DTBaseModel):
    base = f.ForeignKeyField('models.Taxo', related_name='basetrades',
                             on_delete=f.CASCADE)   # ETH/usdt
    quote = f.ForeignKeyField('models.Taxo', related_name='quotetrades',
                              on_delete=f.CASCADE)  # eth/USDT
    pool = f.ForeignKeyField('models.Pool', related_name='pooltrades', on_delete=f.CASCADE)
    broker = f.ForeignKeyField('models.Broker', related_name='brokertrades', on_delete=f.CASCADE)
    # tradegroup = f.UUIDField(generated=False)
    
    action = f.CharField(max_length=10, index=True)  # buy, sell
    price = f.DecimalField(max_digits=16, decimal_places=8, null=True)
    amount = f.IntField(max_digits=18, decimal_places=8, null=True)
    gross = f.DecimalField(max_digits=12, decimal_places=4, default=0, null=True)
    basefees = f.DecimalField(max_digits=12, decimal_places=4, default=None, null=True)
    quotefees = f.DecimalField(max_digits=12, decimal_places=4, default=None, null=True)
    total = f.DecimalField(max_digits=10, decimal_places=4, default=0, null=True)
    tradetype = f.CharField(max_length=20)      # crypto, stock
    status = f.CharField(max_length=20, default='')  # complete, partial?
    note = f.CharField(max_length=255, default='')
    leverage = f.SmallIntField(default=None, null=True)
    exchange = f.CharField(max_length=191)
    
    account = f.ForeignKeyField('models.Account', related_name='accounttrades', on_delete=f.CASCADE)
    metadata = f.JSONField(null=True)
    tags = f.ManyToManyField('models.Taxo', related_name='tag_trades', through='trades_xtradetags',
                             backward_key='trade_id', forward_key='taxo_id')

    og = manager.Manager()
    
    class Meta:
        table = 'trades_trade'
        manager = CuratorManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        div = '' if self.tradetype == 'crypto' else '/'
        name = f'{self.base.name.upper()}{div}{self.quote.name.upper()}'
        return f'{self.action.capitalize()} {name}@{self.price}'
