import argparse

from datetime import datetime
from termcolor import colored
from lumibot.strategies import Strategy


class MyStrategy(Strategy):
    def on_trading_iteration(self):
        if self.first_iteration:
            aapl_price = self.get_last_price("AAPL")
            quantity = self.portfolio_value // aapl_price
            order = self.create_order("AAPL", quantity, "buy")
            self.submit_order(order)


def run_strat(use_bt: bool):
    if use_bt:
        from lumibot.backtesting import YahooDataBacktesting

        # Pick the dates that you want to start and end your backtest
        backtesting_start = datetime(2020, 11, 1)
        backtesting_end = datetime(2020, 12, 31)

        # Run the backtest
        MyStrategy.backtest(
            YahooDataBacktesting,
            backtesting_start,
            backtesting_end,
        )
        pass
    else:
        from lumibot.brokers import Alpaca
        from lumibot.traders import Trader
        from lumibot.credentials import ALPACA_CONFIG

        print(colored(ALPACA_CONFIG, "cyan"))
        trader = Trader()
        broker = Alpaca(ALPACA_CONFIG)
        strategy = MyStrategy(broker=broker)

        # Run the strategy live
        trader.add_strategy(strategy)
        trader.run_all()
    pass


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "--live",
            help="live mode",
            action="store_true",
        )
    parser.add_argument(
        "--print",
        help="print config",
        action="store_true",
    )
    args = parser.parse_args()
    use_bt = not args.live

    run_strat(use_bt=use_bt)
    pass


if __name__ == "__main__":
    main()
    pass
