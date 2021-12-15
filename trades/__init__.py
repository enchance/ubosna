from .settings import TradeSettings


tsettings = TradeSettings()


def get_quotecurr():
    return dict(
        crypto=tsettings.BASEQUOTE_CRYPTO,
        stock=tsettings.BASEQUOTE_STOCK,
        forex=tsettings.BASEQUOTE_FOREX,
    )
