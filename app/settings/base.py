import os
from typing import List
from pydantic import BaseSettings, Field, EmailStr
from dotenv import load_dotenv



load_dotenv(override=True)

class Base(BaseSettings):
    DEBUG: bool = os.getenv('DEBUG')
    ENV: str = os.getenv('ENV')
    SITE_NAME: str = os.getenv('SITE_NAME')
    APPCODE: str = os.getenv('APPCODE')   # No space
    
    # General
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    SECRET_KEY_EMAIL: str = os.getenv('SECRET_KEY_EMAIL')
    USE_TZ: bool = True
    TIMEZONE: str = 'UTC'
    LANGUAGE_CODE: str = 'en-us'
    CURRENCY_ACCOUNT: str = os.getenv('CURRENCY_ACCOUNT')
    CURRENCY_BROKER: str = os.getenv('CURRENCY_BROKER', 'USD')
    
    # Authentication
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE: int = 60 * 15  # seconds (15 mins)
    REFRESH_TOKEN_EXPIRE: int = 3600 * 24 * 15  # seconds (15 days)
    REFRESH_TOKEN_CUTOFF: int = ACCESS_TOKEN_EXPIRE  # minutes
    SESSION_COOKIE_AGE: int = 3600 * 24 * 15  # seconds
    VERIFY_EMAIL_TTL: int = 3600 * 3    # seconds
    VERIFY_TOKEN_EXPIRE: int = 3600     # seconds
    RESET_PASSWORD_TTL: int = 60 * 30   # seconds
    REQUIRES_VERIFICATION: bool = True
    
    # Database
    # Refer to app.settings.db.py
    
    # Cache
    USE_CACHE: bool = True
    CACHE_TTL: int = 3600 * 24 * 15
    CACHE_CONFIG: dict = {
        "default": {
            'pre': os.getenv('CACHE_PREFIX', APPCODE),
            'ver': os.getenv('CACHE_VERSION'),
            'ttl': os.getenv('CACHE_TTL', CACHE_TTL),
        }
    }
    CACHE_GROUPNAME: str = 'group-{}'
    CACHE_USERNAME: str = 'account-{}'
    CACHE_TAXONOMY: str = 'tax-{}-{}'
    CACHE_TAXONOMY_SEARCH: str = 'tax-{}-*'
    CACHE_OPTION_SITE: str = 'option-site'
    CACHE_OPTION_ADMIN: str = 'option-admin'
    CACHE_OPTION_TEMPLATE: str = 'option-template'
    CACHE_TAXO_TAG_TEMPLATE: str = 'taxo-tags'
    CACHE_TAXO_CAT_TEMPLATE: str = 'taxo-cats'
    CACHE_TAXO_FIAT: str = 'taxo-fiat'
    CACHE_TAXO_CRYPTO: str = 'taxo-crypto'
    
    # Account
    USERNAME_MIN: int = Field(4, ge=4, le=10)
    PASSWORD_MIN: int = Field(10, ge=10, le=20)
    AUTO_VERIFY: bool = False
    VERIFY_EMAIL: bool = True
    EMAIL_SENDER: EmailStr = os.getenv('EMAIL_HOST_USER')
    USER_TIMEZONE: str = os.getenv('USER_TIMEZONE', '+08:00')
    USER_GROUPS: List[str] = ['AccountGroup', 'TradeGroup']
    
    # Email
    EMAIL_PORT: int = os.getenv('EMAIL_PORT')
    EMAIL_HOST: str = os.getenv('EMAIL_HOST')
    EMAIL_HOST_USER: str = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASS: str = os.getenv('EMAIL_HOST_PASS')
    
    # Others
    PROGRAM_OVERLORDS: str = 'DropkickDev'
    
    # API
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    COINMARKETCAP_KEY = os.getenv('COINMARKETCAP_KEY')
    
    # Form/Notice URLs
    # NOTICE_HEADER: dict = {'X-Allow-Notice': 'true'}
    # FORM_RESET_PASSWORD: str = os.getenv('FORM_RESET_PASSWORD', '/reset-password-form')
    # NOTICE_VERIFY_REGISTER_OK: str = os.getenv('NOTICE_VERIFY_REGISTER_OK', '/n/verify-register-ok')
    # NOTICE_VERIFY_REGISTER_FAIL: str = os.getenv('NOTICE_VERIFY_REGISTER_FAIL',
    #                                              '/n/verify-register-fail')
    # NOTICE_TOKEN_EXPIRED: str = os.getenv('NOTICE_TOKEN_EXPIRED', '/n/token-expired')
    # NOTICE_TOKEN_BAD: str = os.getenv('NOTICE_TOKEN_BAD', '/n/token-bad')
    # NOTICE_USER_ALREADY_VERIFIED: str = os.getenv('NOTICE_USER_ALREADY_VERIFIED',
    #                                               '/n/user-already-verified')
    
    TESTDATA: str = 'This is base data'
    
    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'