from main import main
from _logging import set_loglevel
import logging
import time
from modules.scheduler import SafeScheduler

if __name__ == "__main__":
    try:
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

    except KeyboardInterrupt as kbi:
        pass
