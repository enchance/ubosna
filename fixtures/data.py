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
        'show_currency_symbol': True,
        'date_format': '%Y-%m-%d %H:%M:%S',
        
        'access_token': s.ACCESS_TOKEN_EXPIRE,
        'refresh_token': s.REFRESH_TOKEN_EXPIRE,
        'refresh_token_cutoff': s.REFRESH_TOKEN_CUTOFF,
        'verify_email': s.VERIFY_EMAIL,
        'exchange': '',
        'broker': '',
    },
    'admin': {
        'max_upload_size': 5,        # MB
    },
}
optionsdb_list = ['exchange', 'broker']
taxos_dict = {
    'site': {
        'tags': [],
        'category': []
    },
    'global': {
        'tags': ['apple', 'pear'],
        'category': ['bird', 'dog']
    },
    'fiat': {
        'USD': 'US Dollar', 'EUR': 'Euro', 'AUS': 'Australian Dollar'
    },
    'crypto': {
        'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance Coin', 'USDT': 'Tether', 'SOL': 'Solana', 'ADA': 'Cardano', 'XRP': 'XRP', 'USDC': 'USD Coin', 'DOT': 'Polkadot', 'DOGE': 'Dogecoin', 'AVAX': 'Avalanche', 'SHIB': 'SHIBA INU', 'LUNA': 'Terra', 'CRO': 'Crypto.com Coin', 'WBTC': 'Wrapped Bitcoin', 'LTC': 'Litecoin', 'BUSD': 'Binance USD', 'UNI': 'Uniswap', 'MATIC': 'Polygon', 'LINK': 'ChainLink', 'ALGO': 'Algorand', 'BCH': 'Bitcoin Cash', 'MANA': 'Decentraland', 'AXS': 'Axie Infinity', 'EGLD': 'Elrond', 'XLM': 'Stellar', 'ICP': 'Internet Computer', 'VET': 'VeChain', 'FIL': 'Filecoin', 'FTT': 'FTX Token', 'SAND': 'SAND', 'TRX': 'TRON', 'THETA': 'Theta Token', 'DAI': 'Dai', 'ETC': 'Ethereum Classic', 'ATOM': 'Cosmos', 'HBAR': 'Hedera Hashgraph', 'FTM': 'Fantom', 'GALA': 'Gala', 'NEAR': 'NEAR Protocol', 'GRT': 'The Graph', 'XMR': 'Monero', 'HNT': 'Helium', 'XTZ': 'Tezos', 'LRC': 'Loopring', 'FLOW': 'Flow Protocol', 'EOS': 'EOS', 'MIOTA': 'IOTA', 'KLAY': 'Klaytn', 'CAKE': 'PancakeSwap', 'LEO': 'LEO Tokens', 'ZEC': 'Zcash', 'ENJ': 'Enjin Coin', 'AAVE': 'Aave', 'MKR': 'Maker', 'KSM': 'Kusama', 'XEC': 'eCash', 'RUNE': 'THORChain', 'BSV': 'Bitcoin SV', 'AMP': 'Amp', 'STX': 'Stacks', 'NEO': 'NEO', 'CHZ': 'Chiliz', 'ONE': 'Harmony', 'QNT': 'Quant', 'BAT': 'Basic Attention Token', 'WAVES': 'Waves', 'HOT': 'Holo', 'CRV': 'Curve DAO Token', 'BTT': 'BitTorrent', 'KCS': 'KuCoin', 'AR': 'Arweave', 'DASH': 'Dash', 'COMP': 'Compound Coin', 'CELO': 'Celo', 'TFUEL': 'Theta Fuel', 'HT': 'Huobi Token', 'XEM': 'NEM', 'IOTX': 'IoTeX', 'IMX': 'Impact', 'QTUM': 'Qtum', 'CEL': 'Celsius', 'MINA': 'Mina', 'OKB': 'OKB', 'NEXO': 'Nexo', 'DCR': 'Decred', 'BIT': 'First Bitcoin', 'ANKR': 'Ankr', 'SC': 'Siacoin', 'TUSD': 'True USD', 'ZEN': 'Horizen', 'ICX': 'ICON', 'LPT': 'Livepeer', 'AUDIO': 'Audius', 'RNDR': 'Render Token', 'OMG': 'OmiseGo', 'RVN': 'Ravencoin', 'ROSE': 'Oasis Network', 'VGX': 'Voyager Token', 'XDC': 'XDC Network', 'ZIL': 'Zilliqa', 'YFI': 'yearn.finance', 'ILV': 'Illuvium', 'STORJ': 'Storj', 'RLY': 'Rally', 'SUSHI': 'Sushi', 'RENBTC': 'renBTC', 'BTG': 'Bitcoin Gold', 'ZRX': '0x', 'SCRT': 'SecretCoin', 'BNT': 'Bancor', 'USDP': 'USDP Stablecoin', 'CKB': 'Nervos Network', 'HIVE': 'Hive', 'DFI': 'DeFiChain', 'REN': 'REN', 'UMA': 'UMA', 'SNX': 'Synthetix Network Token', 'ONT': 'Ontology', 'PERP': 'Perpetual Protocol', 'OMI': 'ECOMI', 'TEL': 'Telcoin', 'TTT': 'TrustNote', 'VLX': 'Velas', 'SKL': 'SKALE Network', 'ELON': 'Dogelon Mars', 'RAY': 'Raydium', 'IOST': 'IOST', 'RPL': 'Rocket Pool', 'GNT': 'Golem', 'POLY': 'Polymath Network', 'KAVA': 'Kava', 'DYDX': 'dYdX', 'DGB': 'DigiByte', 'XYO': 'XYO Network', 'SRM': 'Serum', 'CHSB': 'SwissBorg', 'CELR': 'Celer Network', 'XWC': 'WhiteCoin', 'OCEAN': 'Ocean Protocol', '1INCH': '1inch', 'UOS': 'Ultra', 'ALICE': 'MyNeighborAlice', 'NANO': 'Nano', 'SUPER': 'SuperFarm', 'GNO': 'Gnosis', 'TRAC': 'OriginTrail', 'CHR': 'Chromia', 'RSR': 'Reserve Rights', 'XDB': 'DigitalBits', 'FET': 'Fetch.ai', 'C98': 'Coin98', 'USDN': 'Neutrino Dollar', 'REQ': 'Request Network', 'YGG': 'Yield Guild Games', 'WOO': 'Wootrade', 'INJ': 'Injective Protocol', 'MDX': 'Mdex', 'GT': 'GateToken', 'WARP': 'WARP', 'MBOX': 'MOBOX', 'DENT': 'Dent', 'KEEP': 'Keep Network', 'SAN': 'Santiment Network Token', 'LSK': 'Lisk', 'CTSI': 'Cartesi', 'SYS': 'SysCoin', 'MASK': 'Mask Network', 'DVI': 'Dvision Network', 'XPRT': 'Persistence', 'SXP': 'Swipe', 'ALPHA': 'Alpha Finance Lab', 'TRIBE': 'Tribe', 'FEI': 'Fei Protocol', 'REEF': 'Reef', 'XVG': 'Verge', 'CVC': 'Civic', 'OGN': 'Origin Protocol', 'SNT': 'Status', 'WRX': 'WazirX', 'NKN': 'NKN', 'TLM': 'Alien Worlds', 'RFOX': 'RedFOX Labs', 'TWT': 'Trust Wallet Token', 'KNC': 'Kyber Network', 'BTCST': 'Bitcoin Standard Hashrate Token', 'VTHO': 'VeThor Token', 'OXT': 'Orchid', 'ARDR': 'Ardor', 'KAI': 'KardiaChain', 'PUNDIX': 'Pundi X[new]', 'COTI': 'COTI', 'ACH': 'Alchemy Pay', 'ARRR': 'Pirate Chain', 'XCH': 'Chia', 'SFUND': 'Seedify.fund', 'CFX': 'Conflux Network'
    },
    'exchange': {
        'crypto': 'Crypto',
        'pse': 'PSE',
        'nyse': 'NYSE',
        'nasdaq': 'NASDAQ',
    },
    'broker': {
        'binance': 'Binance',
        'col': 'COL',
    }
}
broker_dict = {
}

# Update as needed
groups_init = s.USER_GROUPS + ['ModGroupSet', 'AdminGroupSet']


