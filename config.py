import os
import dotenv

dotenv.load_dotenv()


class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        self.UPBIT_ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
        self.UPBIT_SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')

        self.NAVER_ID = os.getenv('NAVER_ID')
        self.NAVER_PASSWORD = os.getenv('NAVER_PASSWORD')

        self.SMTP_FROM = os.getenv('SMTP_FROM')
        self.SMTP_TO = os.getenv('SMTP_TO')

        self.NEO4J_URI = os.getenv('NEO4J_URI')
        self.NEO4J_USER = os.getenv('NEO4J_USER')
        self.NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
