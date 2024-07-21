import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "your stock endpoint"
NEWS_ENDPOINT = "your news endpoint"
STOCK_API_KEY = "your stock api key"
NEWS_API_KEY = "your news api key"
TWILIO_SID = "your twilio acc sid "
TWILIO_AUTH_TOKEN = "your twilio auth token"
TWILIO_PHONE_NUMBER = "your twilio phone no"

stock_params = {
    'apikey': STOCK_API_KEY,
    'symbol': STOCK_NAME,
    'function': 'TIME_SERIES_DAILY',
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

stock_difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if stock_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

stock_diff_percent = round((abs(stock_difference) / float(yesterday_closing_price)) * 100)

if stock_diff_percent > 2:

    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    articles = news_data['articles']

    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{stock_diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE_NUMBER,
            to="+918383077299"
        )

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

