class WalletError(Exception):
    pass


class WalletNotFound(WalletError):
    pass


class InsufficientBalance(WalletError):
    pass


class DuplicateTransaction(WalletError):
    pass


class InvalidTransaction(WalletError):
    pass
