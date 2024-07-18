import logging
import time

from _logging import set_loglevel
from modules.upbit_modules import UpbitModules
from modules.analyze_modules import AnalyzeModules
from modules.scheduler import SafeScheduler
from config import Config


def main(ticker):
    config = Config()

    upbit = UpbitModules(ticker, config)
    analyze = AnalyzeModules()

    # while True:

    data = upbit.get_ohlcv("minute1", 360)

    current_stage = analyze.analyze_stage(data['sma20'].iloc[-1], data['sma60'].iloc[-1], data['sma120'].iloc[-1])

    functions = analyze.get_functions_map()

    if current_stage in functions:
        functions[current_stage](data['close'], data['sma20'], data['sma60'], data['sma120'])


if __name__ == '__main__':
    set_loglevel("D")

    logger = logging.Logger("root")

    logging.info("START TRADING BOT....")

    ticker = "BTC"

    main(ticker)

    schedule = SafeScheduler(logger)
    schedule.every(1).minutes.do(main, ticker)

    while True:
        schedule.run_pending()
        time.sleep(1)
