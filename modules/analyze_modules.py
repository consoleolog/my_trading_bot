import logging

from _logging import set_loglevel


class AnalyzeModules:
    set_loglevel("D")

    def gradient(self, value, rolling):
        return (value.iloc[-2].astype(int) - value.iloc[-1].astype(int)) / rolling

    def analyze_stage(self, short, middle, long):
        if short >= middle >= long:  # 단 중 장
            return "stage1"

        elif middle >= short >= long:  # 중 단 장
            return "stage2"

        elif middle >= long >= short:  # 중 장 단
            return "stage3"

        elif long >= middle >= short:  # 장  중 단
            return "stage4"

        elif long >= short >= middle:  # 장 단 중
            return "stage5"

        elif short >= long >= middle:  # 단 장 중
            return "stage6"

    def _stage_1(self, value, short, middle, long):  # 단 중 장
        logging.info(f" stage1 : {value.iloc[-1]} 안정하게 상승 중.")

        short_gradient = self.gradient(short, 20)

        middle_gradient = self.gradient(middle, 60)

        long_gradient = self.gradient(long, 120)

        if short_gradient > 0 and middle_gradient > 0 and long_gradient > 0:
            logging.info(" 매수에 엣지 발생. ")

        elif short_gradient < 0 and middle_gradient < 0 and long_gradient < 0:
            logging.info(" 매도에 엣지 발생. ")

        elif short.iloc[-1] == middle.iloc[-1]:
            logging.info(f" 단기 중기 교차. ")

        elif middle.iloc[-1] == long.iloc[-1]:
            logging.info(f" 중기 장기 교차.")

        elif short.iloc[-1] == long.iloc[-1]:
            logging.info(f" 단기 장기 교차. ")

    def _stage_2(self, value, short, middle, long):  # 중 단 장
        logging.info(f" stage2 : {value.iloc[-1]} 상승 추세의 끝. ")

        if middle.iloc[-1] == short.iloc[-1]:
            logging.info(f" 중기 단기 교차. ")

        if short.iloc[-1] == long.iloc[-1]:
            logging.info(f" 단기 장기 교차. ")

        if middle.iloc[-1] == long.iloc[-1]:
            logging.info(f" 즁기 장기 교차. ")

    def _stage_3(self, value, short, middle, long):  # 중 장 단
        logging.info(f" stage3 : {value.iloc[-1]} 하락 추세의 시작. ")

        if middle.iloc[-1] == long.iloc[-1]:
            logging.info(f" 중기 장기 교차. ")

        if long.iloc[-1] == short.iloc[-1]:
            logging.info(f" 장기 단기 교차. ")

        if middle.iloc[-1] == short.iloc[-1]:
            logging.info(f" 중기 단기 교차. ")

    def _stage_4(self, value, short, middle, long):  # 장 중 단
        logging.info(f" stage4 : {value.iloc[-1]} 안정하게 하락 중. ")

        if long.iloc[-1] == middle.iloc[-1]:
            logging.info(f" 장기 중기 교차. ")

        if middle.iloc[-1] == short.iloc[-1]:
            logging.info(f" 중기 단기 교차. ")

        if long.iloc[-1] == short.iloc[-1]:
            logging.info(f" 장기 단기 교차. ")

    def _stage_5(self, value, short, middle, long):  # 장 단 중
        logging.info(f" stage5 : {value.iloc[-1]} 하락 추세의 끝. ")

        if long.iloc[-1] == short.iloc[-1]:
            logging.info(f" 장기 단기 교차. ")

        if short.iloc[-1] == middle.iloc[-1]:
            logging.info(f" 단기 중기 교차.  ")

        if long.iloc[-1] == middle.iloc[-1]:
            logging.info(f" 장기 중기 교차.  ")

    def _stage_6(self, value, short, middle, long):  # 단 장 중
        logging.info(f" stage6 : {value.iloc[-1]} 상승 추세의 시작. ")

        if short.iloc[-1] == long.iloc[-1]:
            logging.info(f" 단기 장기 교차.  ")

        if long.iloc[-1] == middle.iloc[-1]:
            logging.info(f" 장기 중기 교차. ")

        if short.iloc[-1] == middle.iloc[-1]:
            logging.info(f" 단기 중기 교차. ")

    def get_functions_map(self):
        return {
            'stage1': self._stage_1,
            'stage2': self._stage_2,
            'stage3': self._stage_3,
            'stage4': self._stage_4,
            'stage5': self._stage_5,
            'stage6': self._stage_6
        }
