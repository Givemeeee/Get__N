import twstock
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_one_month():
    # 獲取當前日期
    today = datetime.today()
    # 計算前一個月的日期
    last_month = today - relativedelta(months=1)
    # 設置日期為1號
    last_month = last_month.replace(day=1)
    getNewyear = int(last_month.strftime("%Y"))
    getNewmonth = int(last_month.strftime("%m"))
    print(getNewyear, ',', getNewmonth)
    return getNewyear,getNewmonth

def get_two_month():
    #獲取當前日期
    today = datetime.today()
    # 計算前一個月的日期
    last_month = today - relativedelta(months=2)
    # 設置日期為1號
    last_month = last_month.replace(day=1)
    get2Newyear = int(last_month.strftime("%Y"))
    get2Newmonth = int(last_month.strftime("%m"))
    return get2Newyear,get2Newmonth

def get_three_month():
    #獲取當前日期
    today = datetime.today()
    # 計算前一個月的日期
    last_month = today - relativedelta(months=3)
    # 設置日期為1號
    last_month = last_month.replace(day=1)
    get3Newyear = int(last_month.strftime("%Y"))
    get3Newmonth = int(last_month.strftime("%m"))
    return get3Newyear,get3Newmonth

# 獲取前一個月的日期
getNewyear,getNewmonth= get_one_month()
get2Newyear,get2Newmonth= get_two_month()

#儲存資料創建空串列
month_one_ago = []
month_two_ago = []

# 使用 twstock 模組獲取三個月前股票資料
stock = twstock.Stock((input("請輸入股票代碼：")))
month_one_ago.append(stock.fetch(getNewyear,getNewmonth))
month_two_ago.append(stock.fetch(get2Newyear,get2Newmonth))

print(month_one_ago)

# 將三個串列儲存到CSV檔案

# 定義欄位名稱 
headers = ['datetime', 'open','high','low','close','change']
output_path = r'C:\Users\s1010\Documents\python\sTock\stock_data2m.csv'

# 打開csv檔案進行寫入
with open(output_path,'w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)

    # 寫入欄位名稱
    writer.writerow(headers)
    
    # 寫入股票資料 
    for stock_data in month_one_ago[0]:
        writer.writerow([
            str(stock_data.date),
            stock_data.open,
            stock_data.high,
            stock_data.low, 
            stock_data.close,
            stock_data.change
        ])
    for stock_data in month_two_ago[0]:
        writer.writerow([
            str(stock_data.date),
            stock_data.open,
            stock_data.high,
            stock_data.low, 
            stock_data.close,
            stock_data.change
        ])
