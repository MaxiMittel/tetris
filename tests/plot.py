import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.window import rolling

RED = "#EF3E36"
PURPLE = "#950952"

load_distribution = pd.read_csv("../load-balancer/request_log.csv", names=["latency","name","method", "path"])
grouped = load_distribution.groupby("name").size().reset_index(name='count')

fig = plt.figure(figsize = (10, 5))
plt.bar(grouped["name"], grouped["count"], color=RED, width=0.4)
 
plt.ylabel("Distribution of API requests")
plt.show()

ping_test = pd.read_csv("api_log.csv", names=["latency"])

fiq = plt.figure(figsize = (10, 5))
plt.plot(ping_test["latency"].rolling(window=4).mean(), color=PURPLE)
plt.ylabel("Latency in ms")
plt.show()
