import requests
import time
import urllib3
import datetime

urllib3.disable_warnings()

# ===== 設定 =====
stock_id = "3481"   # 群創
buy_price = 26.6

CHANNEL_ACCESS_TOKEN = "8OkXLg74ebWlmb0HWBhYpKrPrh1iIf+oU7hKw3qFOyL7KN5PZ9lsV7YBwctJzmkBDS3ci4yptwM1PWqLs2yLwrH6o00qPebbJ8t/jclC9iGbyOBsqh8yXo8ZeNXPURJIB+vIc2SfpDhQPhHBxY5yfQdB04t89/1O/w1cDnyilFU="
USER_ID = "U052d1bc982d25e1dcea9c896ee22991f"

# ===== 設定時間段 =====
def is_trading_time():
    now = datetime.datetime.now()
    
    # 星期一=0，星期五=4
    if now.weekday() > 4:
        return False
    
    # 時間 9:00 ~ 13:30
    start = now.replace(hour=9, minute=0, second=0)
    end = now.replace(hour=13, minute=30, second=0)
    
    return start <= now <= end

# ===== 發LINE通知 =====
def send_line(msg):
    url = "https://api.line.me/v2/bot/message/push"
    
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": msg
            }
        ]
    }

    requests.post(url, headers=headers, json=data, verify=False)

# ===== 抓即時股價 =====
def get_price():
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers, verify=False).json()
    
    price = data["msgArray"][0]["z"]
    return float(price) if price != "-" else None

# ===== 主程式 =====
alerted = False

if __name__ == "__main__":
    while True:
        if is_trading_time():
            price = get_price()
            
            if price:
                print(f"現在價格: {price}")

                if price >= buy_price and not alerted:
                    send_line(f"{stock_id} 已達 {price}！")
                    alerted = True
        else:
            print("非交易時間")

        time.sleep(30)

