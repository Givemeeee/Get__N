import datetime
import twstock
import pandas as pd
from ta.momentum import rsi

end = datetime.datetime.now()
start = end - datetime.timedelta(days=30)

stock = twstock.Stock("2330")
monthly_data = stock.fetch(start.year, start.month)

# 將 twstock 的資料轉換為 pandas DataFrame
df = pd.DataFrame(monthly_data)

class RSIIndicator(object):
    def __init__(self, data, period=4, threshold=77):
        self.data = data
        self.period = period  
        self.threshold = threshold

    def calculate(self):
        # 計算 RSI
        rsi_month = rsi(self.data['close'], window=self.period)

        if rsi_month.iloc[-1] > self.threshold:
            dir = "上升"
        else:
            dir = "下降"

        print(f"目前月線 RSI: {rsi_month.iloc[-1]}, 方向: {dir}")

ind = RSIIndicator(df)
ind.calculate()
