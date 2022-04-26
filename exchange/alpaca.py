"""Alpaca Markets: https://app.alpaca.markets/"""

import alpaca_trade_api as tradeapi
from dotenv import load_dotenv


class Alpaca:
    """Alpaca Markets: https://app.alpaca.markets/"""

    def __init__(self):
        """Initialize Alpaca Class."""
        load_dotenv()
        self.api = tradeapi.REST(api_version="v2")

    def get_account(self):
        """Get account information."""
        return self.api.get_account()

    def submit_order(self, **kwargs):
        """Submit an order."""
        return self.api.submit_order(**kwargs)

    def get_assets(self):
        """Get assets."""
        return self.api.list_assets(status="active")


if __name__ == "__main__":
    alpaca = Alpaca()
    print(alpaca.get_account())
