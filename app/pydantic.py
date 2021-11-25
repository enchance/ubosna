from datetime import datetime
from pydantic import BaseModel



class OptionSite(BaseModel):
    sitename: str
    siteurl: str
    author: str
    last_update: datetime
    

class OptionAdmin(BaseModel):
    max_upload_size: int
    

class OptionTemplate(BaseModel):
    theme: str
    email_notifications: bool
    language: str
    show_currency_symbol: bool
    date_format: str
    
    currency: str
    access_token: int
    refresh_token: int
    refresh_token_cutoff: int
    verify_email: bool