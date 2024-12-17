import requests
import datetime as dt
from twilio.rest import Client # Twilio requires this

# CONSTANT
# ------------------- CHANGE YOUR STOCK API DETAILS HERE ----------------------------- #
STOCK = "TSLA"
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = ""
# ------------------- CHANGE YOUR NEWS API DETAILS HERE ----------------------------- #
COMPANY_NAME = "Tesla Inc"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = ""
# ------------------- CHANGE YOUR TWILIO API DETAILS HERE ----------------------------- #
ACC_SID = ""
AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
TARGET_PHONE_NUMBER = ""

# --------------------------- STOCK SETUP ---------------------------------- #
stock_parameters = {
	"function": "TIME_SERIES_DAILY",
	"symbol": STOCK,
	"apikey": STOCK_API_KEY
}

stock_response = requests.get(url=STOCK_API_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_dict = stock_response.json()["Time Series (Daily)"]

# Change dict to list
stock_list = [value for key, value in stock_dict.items()]
yesterday_closing_price = float(stock_list[0]["4. close"])
before_yesterday_closing_price = float(stock_list[1]["4. close"])

# # Calculate percent changes
price_change_percent = round((yesterday_closing_price - before_yesterday_closing_price) / yesterday_closing_price * 100)
print(price_change_percent)
# Setup emoji whether rise or fall
emoji_up_down = None
if price_change_percent < 0:
	emoji_up_down = "📈"
else:
	emoji_up_down = "📉"

# --------------- CHANGE STOCK PERCENT CHANGE NOTIFIER HERE ------------------- #
if abs(price_change_percent) > 5:

	# -------------------- NEWS SETUP -------------------------- #
	news_parameters = {
		"q": COMPANY_NAME,
		"apiKey": NEWS_API_KEY,
		"sortBy": "publishedAt",
		"pageSize": "3",
	}

	news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_parameters)
	news_response.raise_for_status()
	news_list = news_response.json()["articles"]

	formatted_news_list = [f"{STOCK}: {emoji_up_down}{price_change_percent}%\nHeadline: {content["title"]}.\nSummary: {content["description"]}" for content in news_list]

	# ------------------- TWILIO SETUP ---------------------- #
	client = Client(ACC_SID, AUTH_TOKEN)
	for article in formatted_news_list:
		message = client.messages.create(
			body=article,
			from_=TWILIO_PHONE_NUMBER,
			to=TARGET_PHONE_NUMBER
			)
		print(message.status)
