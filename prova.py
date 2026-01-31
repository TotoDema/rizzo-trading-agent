import os
from hyperliquid_trader import HyperLiquidTrader
from hyperliquid.utils import constants
from hyperliquid.exchange import Exchange
from dotenv import load_dotenv
load_dotenv()  # Carica le variabili dal file .env

trader = HyperLiquidTrader(
    secret_key=os.getenv("SECRET_KEY"),
    account_address=os.getenv("ACCOUNT_ADDRESS"),
    testnet=True
)

resp = trader.place_order(
    name="BTC",
    is_buy=True,
    size=0.00015,
    price=None,          # None → market order
    reduce_only=False,
)
print(resp)





status = trader.get_account_status()

print(status);

