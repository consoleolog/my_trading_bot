import pyupbit
import logging
import json

from _logging import set_loglevel
from config import *
from modules.smtp_module import SMTPModule


class UpbitModules:
    set_loglevel("D")

    def __init__(self, ticker):
        self.ticker = ticker
        self.upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
        self.smtp = SMTPModule()

    def get_balances(self, ticker):
        balances = self.upbit.get_balances()
        for b in balances:
            if b['currency'] == ticker:
                if b['balance'] is not None:
                    logging.info(float(b['balance']))
                    return float(b['balance'])
                else:
                    return 0
        return 0

    def _buy(self, ticker, amount, price):
        try:
            if amount == 0:
                msg = self.upbit.buy_market_order(ticker, price)
                if msg is None:
                    return "already_buy"
                msg = json.loads(''.join(map(lambda x: '"' if x == "'" else x, msg)).strip())
                inputs = self.smtp.write_email("업비트 매매 결과 보고", ticker, msg['created_at'],"매수", price)
                self.smtp.send_email(inputs)
                return msg
        except Exception as e:
            logging.error(e)
            raise

    def _sell(self, ticker, amount):
        try:
            msg = self.upbit.sell_market_order(f"KRW-{ticker}", amount)
            for m in msg:
                if m == 'error':
                    return "already_sell"
            msg = json.loads(''.join(map(lambda x: '"' if x == "'" else x, msg)).strip())
            inputs = self.smtp.write_email("업비트 매매 결과 보고", ticker, msg['created_at'], "매도", msg['volume'])
            self.smtp.send_email(inputs)
            return msg
        except Exception as e:
            logging.error(e)
            raise

    def get_ohlcv(self, interval, count):
        try:
            data = pyupbit.get_ohlcv(ticker=f"KRW-{self.ticker}", interval=interval, count=count)
            data['close'] = data['close'].astype(int)
            data['sma20'] = data['close'].astype(int).rolling(20).mean()
            data['sma60'] = data['close'].astype(int).rolling(60).mean()
            data['sma120'] = data['close'].astype(int).rolling(120).mean()

            return data
        except TypeError as type_error:
            logging.error(type_error)
            pass

