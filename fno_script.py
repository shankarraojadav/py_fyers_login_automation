import pandas as pd
from fyers_apiv3 import fyersModel
# from fyers_apiv3 import accessToken
import requests
import json
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fyers API credentials
client_id = "MHL1D4GVKO-100"
client_secret = "73TRE2LOLQ"
redirect_url = "https://google.com"
authorization_code = "YOUR_AUTH_CODE"

# Function to read stock list from an Excel sheet
file_path = "sorted_stocks_by_market_cap.csv.csv"
def read_fno_stocks_from_excel(file_path):
    df = pd.read_excel(file_path)
    # Assuming the stock symbols are in a column named 'Symbol' in the Excel sheet
    fno_stocks = df['Symbol'].tolist()
    return fno_stocks

# Function to authenticate Fyers API
def authenticate_fyers():
    session = accessToken.SessionModel(client_id=client_id, secret_key=client_secret, redirect_uri=redirect_url, response_type="code", grant_type="authorization_code")
    session.set_token(authorization_code)
    response = session.generate_token()
    access_token = response["access_token"]
    
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="log_path/")
    return fyers

# Function to get news for FNO stocks
def get_stock_news(fyers, stock_symbol):
    news_url = f"https://api.fyers.in/v2/news?symbol=NSE:{stock_symbol}"
    headers = {
        "Authorization": f"Bearer {fyers.access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(news_url, headers=headers)
    news_data = response.json()
    
    # Return important news articles
    important_news = []
    if news_data.get('data'):
        for article in news_data['data']:
            if any(keyword in article['headline'].lower() for keyword in ['results', 'announcement', 'earnings']):
                important_news.append((article['headline'], article['link']))
    return important_news

# Function to check and notify about important news
def check_for_important_news(fyers, fno_stocks):
    all_news = {}
    
    for stock in fno_stocks:
        news = get_stock_news(fyers, stock)
        if news:
            all_news[stock] = news
    
    if all_news:
        send_notification(all_news)

# Function to send email notification
def send_notification(news):
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    subject = "Important Stock News Alert"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Compose the email content
    body = "Here is the latest important news for your FNO stocks:\n\n"
    for stock, news_items in news.items():
        body += f"{stock}:\n"
        for headline, link in news_items:
            body += f"{headline}\nRead more: {link}\n\n"
    
    msg.attach(MIMEText(body, 'plain'))

    # Email server setup (example: Gmail)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, "your_email_password")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)

# Function to schedule the script every 1 hour
def schedule_script(file_path):
    fno_stocks = read_fno_stocks_from_excel(file_path)
    fyers = authenticate_fyers()
    
    schedule.every(1).hours.do(check_for_important_news, fyers, fno_stocks)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Run the scheduler
if __name__ == "__main__":
    file_path = 'path_to_your_excel_file.xlsx'  # Replace with the path to your Excel file
    schedule_script(file_path)
