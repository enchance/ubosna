from tortoise import fields as f, manager
from limeutils import modstr

from app import settings as s
from app.authentication.models.common import DTBaseModel, SharedMixin
from app.authentication.models.manager import CuratorManager



class Broker(SharedMixin, DTBaseModel):
    name = f.CharField(max_length=191, unique=True)
    short = f.CharField(max_length=10, default='')
    brokerno = f.IntField(null=True)
    logo = f.CharField(max_length=255, default='')
    site = f.CharField(max_length=255, default='')
    currency = f.CharField(max_length=5, default=s.CURRENCY_BROKER)
    
    is_active = f.BooleanField(default=True)
    metadata = f.JSONField(null=True)
    author = f.ForeignKeyField('models.Account', related_name='author_brokers')
    
    og = manager.Manager()
    
    class Meta:
        table = 'trades_broker'
        manager = CuratorManager()


    def __str__(self):
        return modstr(self, 'name')
    
    
class AccountBrokers(SharedMixin, DTBaseModel):
    account = f.ForeignKeyField('models.Account', related_name='accountbrokers')
    broker = f.ForeignKeyField('models.Broker', related_name='accountbrokers')
    wallet = f.DecimalField(max_digits=19, decimal_places=8, default=0)
    traded = f.DecimalField(max_digits=19, decimal_places=8, default=0)
    status = f.CharField(max_length=20, default='active')
    
    is_primary = f.BooleanField(default=False)
    metadata = f.JSONField(null=True)
    
    og = manager.Manager()
    
    class Meta:
        table = 'trades_xaccountbrokers'
        manager = CuratorManager()