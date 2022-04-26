"""Libertex Metatrader Account"""

import os

import requests
from dotenv import load_dotenv


class Libertex:
    """Libertex Metatrader Account"""

    def __init__(self):
        """Initialize Alpaca Class."""
        load_dotenv()

        self.account_id = os.getenv("METAAPI_ACCOUNT_ID")
        self.base_url = "https://mt-client-api-v1.agiliumtrade.agiliumtrade.ai"
        self.account_url = self.base_url + f"/users/current/accounts/{self.account_id}"
        self.headers = {
            "Accept": "application/json",
            "auth-token": os.getenv("METAAPI_TOKEN"),
        }
        self.symbol_mapping = {
            "gold": "XAUUSD",
            "dax": "FDAX",
            "dow": "YM",
            "brent": "BRN",
            "eur/usd": "EURUSD",
            "eur/jpy": "EURJPY",
            "eur/gpb": "EURGBP",
            "bitcoin": "BTCUSD",
        }

    def get_symbol_specification(self, symbol):
        """Get specification for a symbol."""
        symbol = self.symbol_mapping.get(symbol)
        url = self.account_url + f"/symbols/{symbol}/specification"
        return requests.get(url, headers=self.headers).json()

    def get_symbol_price(self, symbol):
        """Get the actual price of a symbol."""
        symbol = self.symbol_mapping.get(symbol)
        url = self.account_url + f"/symbols/{symbol}/current-price"
        response = requests.get(url, headers=self.headers).json()
        return response.get("bid", 0)

    def check_symbols(self):
        """Check if all symbols are available."""
        print("Active symbols:")
        for k, v in self.symbol_mapping.items():
            price = self.get_symbol_price(k)
            min_volume = self.get_symbol_specification(k).get("minVolume")
            print(f"{v} -> Price: {price}, Min volume: {min_volume}")

    def find_symbol(self, symbol):
        """Map symbol to Libertex symbol."""
        if self.symbol_mapping.get(symbol):
            return self.symbol_mapping.get(symbol)
        return None

    def get_account_info(self):
        """Get account information."""
        url = self.account_url + "/accountInformation"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_positions(self):
        """Get positions."""
        url = self.account_url + "/positions"
        response = requests.get(url, headers=self.headers).json()
        return response

    def open_position(self, symbol, action):
        """Buy a currency."""

        text_symbol = symbol
        symbol = self.find_symbol(symbol)

        if symbol:

            if action == "SELL":
                action = "ORDER_TYPE_SELL"
            else:
                action = "ORDER_TYPE_BUY"

            # get min volume
            min_volume = self.get_symbol_specification(text_symbol).get("minVolume")

            data = {
                "actionType": action,
                "symbol": symbol,
                "volume": min_volume,
                "stopLoss": 10,  # percentage / leverage, i. e. 10/2 = 5
                "takeProfit": 10,  # percentage / leverage, i. e. 10/2 = 5
                "stopLossUnits": "RELATIVE_BALANCE_PERCENTAGE",
                "takeProfitUnits": "RELATIVE_BALANCE_PERCENTAGE",
            }

            url = self.account_url + "/trade"
            response = requests.post(url, headers=self.headers, json=data).json()
            return response

        return {"message": "Invalid symbol"}

    def close_positions(self, symbol):
        """Close all positions with the symbol."""

        if self.find_symbol(symbol):

            data = {
                "actionType": "POSITIONS_CLOSE_SYMBOL",
                "symbol": self.find_symbol(symbol),
            }

            url = self.account_url + "/trade"
            response = requests.post(url, headers=self.headers, json=data).json()
            return response

        return {"message": "Invalid symbol"}


if __name__ == "__main__":
    libertex = Libertex()
    print(f"Account balance: {libertex.get_account_info().get('balance')}")
    print(f"Open positions: {len(libertex.get_positions())}")
    # print(libertex.check_symbols())

    # print(libertex.open_position("brent", "BUY"))
    # print(libertex.open_position("gold", "SELL"))
    # print(libertex.close_positions("brent"))
    # print(libertex.get_positions())
    # print(libertex.get_account())
