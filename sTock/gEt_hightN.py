import csv
import datetime

max_high = float('-inf') 
min_low = float('inf')
data=r'C:\Users\s1010\Documents\python\sTock\stock_data2m.csv'
with open(data,'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # 略過標題行
    for row in reader:
        date = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') 
        open_price = float(row[1])
        high_price = float(row[2])
        low_price = float(row[3])
        close_price = float(row[4])
        
        if high_price > max_high:
            max_high = high_price
        if low_price < min_low:
            min_low = low_price
            
N = (max_high + min_low)/2
print('N：',N)