from datetime import datetime
from pydantic import BaseModel

from app import settings as s



class OptionSite(BaseModel):
    sitename: str
    siteurl: str
    author: str
    last_update: datetime
    

class OptionAdmin(BaseModel):
    max_upload_size: int
    

class OptionTemplate(BaseModel):
    theme: str = s.THEME
    email_notifications: bool = False
    show_currency_symbol: bool = True
    date_format: str = s.DATE_FORMAT
    
    access_token: int = ''
    refresh_token: int = ''
    refresh_token_cutoff: int = s.REFRESH_TOKEN_CUTOFF
    verify_email: bool = True
    exchange: str = ''
    broker: str = ''