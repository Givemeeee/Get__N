import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon , QFont
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import twstock
import csv

#建立主程式的類別
class StockIndicatorApp(QWidget):
    def __init__(self):
        super().__init__()
        #設定主程式的名稱及窗口大小
        self.setWindowTitle("股票指標N")
        self.setGeometry(600, 250, 250, 200)
        self.setWindowIcon(QIcon('bullish.png'))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 主程式標題
        title_label = QLabel("股票指標")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Microsoft JhengHei', 22, QFont.Weight.DemiBold))
        layout.addWidget(title_label)

        # 股票代號輸入
        self.stock_code_label = QLabel("請輸入股票代碼")  
        self.stock_code_input = QLineEdit(self)
        self.stock_code_input.setStyleSheet("height: 22px;")
        self.stock_code_label.setFont( QFont('Microsoft JhengHei', 14, QFont.Weight.Light) )
        layout.addWidget(self.stock_code_label)
        layout.addWidget(self.stock_code_input)

        # 設定輸入按鈕並連結Enter做輸入
        calculate_button = QPushButton("計算指標")
        calculate_button.clicked.connect(self.calculate_indicators)
        self.stock_code_input.returnPressed.connect(self.calculate_indicators)
        layout.addWidget(calculate_button)

        #設定清除鍵
        clear_button = QPushButton("清除輸入")
        clear_button.clicked.connect(self.clear_input)
        layout.addWidget(clear_button)
    
        self.setLayout(layout)

        # 程式主要內容抓取twstock資料下來後的csv檔進行顯示
    def calculate_indicators(self):
        stock_code = self.stock_code_input.text()

        output_path_2_months = 'stock_data_2_months.csv'
        output_path_3_months = 'stock_data_3_months.csv'

        num_of_months_2 = 1
        num_of_months_3 = 2

        self.get_stock_data(stock_code, output_path_2_months, num_of_months_2)
        result1 = self.calculate_average_N(output_path_2_months, num_of_months_2)

        self.get_stock_data(stock_code, output_path_3_months, num_of_months_3)
        result2 = self.calculate_average_N(output_path_3_months, num_of_months_3)

        # 創建並顯示結果視窗
        self.result_window = ResultWindow(result1, result2)

    #清除輸入的功能。
    def clear_input(self):
        self.stock_code_input.clear()
    #抓取股票資料的功能。
    def get_stock_data(self, stock_code, output_path, num_of_months):
        
        #設定抓取的時間，為當日的前一個月天數都設為1
        today = datetime.today()
        last_month = today - relativedelta(months=num_of_months)
        last_month = last_month.replace(day=1)
        
        #因為twstock內資料所以設置表頭為datetime,open,high,low,close,change
        headers = ['datetime', 'open', 'high', 'low', 'close', 'change']

        #抓取資料後寫成csv檔做計算
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            stock = twstock.Stock(stock_code)
            for i in range(num_of_months):
                target_date = last_month + relativedelta(months=i)
                target_year, target_month = target_date.year, target_date.month
                data = stock.fetch(target_year, target_month)

                for stock_data in data:
                    writer.writerow([
                        str(stock_data.date),
                        stock_data.open,
                        stock_data.high,
                        stock_data.low,
                        stock_data.close,
                        stock_data.change
                    ])
    #計算平均
    def calculate_average_N(self, file_path, num_of_months):
        max_high = float('-inf')
        min_low = float('inf')
        # 讀取csv檔並計算N值
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            #找到最高價與最低價
            for row in reader:
                stock_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").date()
                high_price = float(row[2])
                low_price = float(row[3])

                if stock_date.month == datetime.today().month:
                    continue  # Skip the current month

                if high_price > max_high:
                    max_high = high_price
                if low_price < min_low:
                    min_low = low_price
            #計算N值
            if max_high != float('-inf') and min_low != float('inf'):
                N = (max_high + min_low) / 2
                N_rounded = round(N, 2)  # 四捨五入到小數點後兩位
                print(f'前{num_of_months}個月的N：', N_rounded)
                return N_rounded  # 返回四捨五入後的結果
            else:
                print(f'前{num_of_months}個月無有效數據可計算 N')
                return None  # 或者返回一個指示沒有數據的值
#製作輸出值視窗
class ResultWindow(QWidget):
    def __init__(self, data1, data2):
        super().__init__()
        self.data1 = data1
        self.data2 = data2
        self.initUI()

        self.setWindowIcon(QIcon('key.ico'))

    def initUI(self):  
        #在分頁顯示計算結果
        self.setWindowTitle('計算結果')
        self.setGeometry(850, 250, 250, 100)
        #UI字體調整
        self.label1 = QLabel('2個月的N: ' + str(self.data1), self)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setFont(QFont('Microsoft JhengHei', 14, QFont.Weight.Medium))
        self.label1.resize(230, 30)  # 設置適當的大小
        self.label1.move((self.width() - self.label1.width()) // 2, 10)  # 水平居中
        #UI字體調整
        self.label2 = QLabel('3個月的N: ' + str(self.data2), self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setFont(QFont('Microsoft JhengHei', 14, QFont.Weight.Medium))
        self.label2.resize(230, 30)  # 設置適當的大小
        self.label2.move((self.width() - self.label2.width()) // 2, 50)  # 水平居中

        self.show()

#啟動主程式
def main():
    app = QApplication(sys.argv)
    window = StockIndicatorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
