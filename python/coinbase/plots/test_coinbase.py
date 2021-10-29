import pandas as pd
import matplotlib.pyplot as plt
import requests

url = "https://api.exchange.coinbase.com/products/BTC-USDT/candles"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

values = response.json()
print(values)
df = pd.DataFrame(values)
print(df)
df[3].plot()
plt.show()

