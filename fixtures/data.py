from app import settings as s



# Update pydantic models if you edit this
options_dict = {
    'site': {
        'sitename': s.SITE_NAME,
        'siteurl': s.SITE_URL,
        'author': s.PROGRAM_OVERLORDS,
        'last_update': '',
    },
    # For each user
    'template': {
        'theme': 'light',
        'email_notifications': True,
        'language': 'en',
        'show_currency_symbol': True,
        'date_format': '%Y-%m-%d %H:%M:%S',
        
        'currency': s.CURRENCY_ACCOUNT,
        'access_token': s.ACCESS_TOKEN_EXPIRE,
        'refresh_token': s.REFRESH_TOKEN_EXPIRE,
        'refresh_token_cutoff': s.REFRESH_TOKEN_CUTOFF,
        'verify_email': s.VERIFY_EMAIL
    },
    'admin': {
        'max_upload_size': 5,        # MB
    }
}
taxos_dict = {
    'site': {
        'tags': [],
        'category': []
    },
    'global': {
        'tags': ['apple', 'pear'],
        'category': ['bird', 'dog']
    }
}

# Update as needed
groups_init = s.USER_GROUPS + ['ModGroupSet', 'AdminGroupSet']


