import pandas as pd
from fbprophet import Prophet
import time
import datetime as dt
import matplotlib.pyplot as plt

# 1. Read in Data and Process Dates

df = pd.read_csv('ElonCryptoTweets.csv')
dfInitial = pd.read_csv('ElonCryptoTweets.csv')

df.drop(['Date', 'Tweets'], axis=1)
df.columns = ['y', 'ds']

df['ds'] = pd.to_datetime(dfInitial['Date'], errors='coerce')
df['y'] = dfInitial['Tweets']
df.head()

# 2. Train Model

m = Prophet(interval_width=0.95, daily_seasonality=True)
model = m.fit(df)


# 3. Forecast

future = m.make_future_dataframe(periods=100, freq='D')
forecast = m.predict(future)
forecast.head()

x = forecast['ds']
y = forecast['trend']
z = forecast['yhat']
print(x, y, z)

plot1 = m.plot(forecast)

plt2 = m.plot_components(forecast)

plt.show()

def calculate_group(epoch_time, yhat):
    day = time.strftime('%A', time.localtime(epoch_time))
    day_points = {
        "Monday": 30,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 10,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 20
    }
    day_score = day_points.get(day, "Invalid day.")

    if yhat < 2:
        yhat_score = 10
    elif 2 < yhat < 3:
        yhat_score = 30
    elif 3 < yhat < 4:
        yhat_score = 50
    else:
        yhat_score = 70

    total_score = day_score + yhat_score
    print("Total Score: " + str(total_score))
    if total_score < 33:
        return 0
    elif 33 < total_score < 66:
        return 1
    else:
        return 2

df = pd.DataFrame(forecast._data, columns= ['ds', 'yhat'])

df['ds'] = (df['ds'] - dt.datetime(1970,1,1)).dt.total_seconds().astype('int64')
print(df)

df['yhat'] = df.apply(lambda x: calculate_group(x['ds'], x['yhat']), axis=1)
df.to_json(r'Df.json', orient="records")
