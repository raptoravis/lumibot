from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.backtesting import PolygonDataBacktesting
from lumibot.strategies import Strategy

from lumibot.brokers import Alpaca
from lumibot.traders import Trader

from lumibot.credentials import IS_BACKTESTING
from lumibot.credentials import ALPACA_CONFIG
from lumibot.credentials import POLYGON_CONFIG


# pip install git+https://github.com/Lumiwealth/quantstats_lumi@main

IS_BT = IS_BACKTESTING


# A simple strategy that buys AAPL on the first day and holds it
class MyStrategy(Strategy):
    def on_trading_iteration(self):
        if self.first_iteration:
            aapl_price = self.get_last_price("AAPL")
            quantity = self.portfolio_value // aapl_price
            order = self.create_order("AAPL", quantity, "buy")
            self.submit_order(order)


if IS_BT:
    # Pick the dates that you want to start and end your backtest
    backtesting_start = datetime(2020, 11, 1)
    backtesting_end = datetime(2020, 12, 31)

    use_yahoo = True

    data_source = YahooDataBacktesting if use_yahoo else PolygonDataBacktesting
    polygon_api_key = None if use_yahoo else POLYGON_CONFIG['API_KEY']
    sleep_time = 1 if use_yahoo else 10

    # Run the backtest
    MyStrategy.backtest(
        data_source,
        backtesting_start,
        backtesting_end,
        polygon_api_key=polygon_api_key,
        sleeptime=sleep_time,
    )
else:
    alpaca_config = ALPACA_CONFIG

    trader = Trader()
    broker = Alpaca(alpaca_config)
    strategy = MyStrategy(broker=broker)

    # Run the strategy live
    trader.add_strategy(strategy)
    trader.run_all()
    pass
