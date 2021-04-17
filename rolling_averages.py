import csv
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

''' example.csv contains the values for the system. The thing to note about the file
    is that the sampling periods are not every 1 second. So there might be a value at 
    t = 0s of 200, and then the next value at t = 3s of 210 watts. We can assume that
    the power value for times 1s, and 2s are also 200 watts. (So the power profile is a step
    function)

    Example call
    ===========
    dataframe = load_csv()
    dataframe_with_rolling = calculate_rolling_average(dataframe, averaging_period=600)
'''


def load_csv():
    """ load the CSV containing the values.

    Returns:
        pd.DataFrame: [index, time, value]
    """
    return pd.read_csv('example.csv')


def calculate_rolling_average(data: pd.DataFrame, averaging_period=600):
    """Summary
    Calculate a rolling average

    Args:
        data (pd.DataFrame): contains two columns for time and power
        averaging_period (int): (optional) default 10 minutes (600s)

    Returns:
        DataFrame:  [time, value, moving_average]
    """
    data["moving_average"] = data.rolling(averaging_period, on="time").mean()

    return data


def preprocess(data: pd.DataFrame):
    """
    Process the data
     - Add in missing time steps
     - Fill missing values with previous valid value (I assume the data follows a step function)
    """
    processed = data.drop(axis=1, labels=["index"])  # drop unneeded column

    # add in missing times
    new_index = pd.Index(np.arange(0, data["time"].max(), 1), name="time")
    processed = processed.set_index("time").reindex(new_index).reset_index()

    # fill missing values
    processed["value"].replace(0, np.nan, inplace=True)  # convert all 0's to NaN
    processed["value"].fillna(method="ffill", inplace=True)  # forward fill all NaN (eg, use previous value)
    processed["value"].replace(np.nan, 0, inplace=True)  # change any values that dont have a previous value to 0

    return processed


def plot_chart(data):
    plt.figure(figsize=(10, 8), dpi=300)

    plt.plot(data["time"], data["value"], 'g-', label="original data", linewidth="0.5")
    plt.plot(data["time"], data["moving_average"], "b-", label="moving average", linewidth=3)

    plt.title("Rolling Average Power (w)")
    plt.xlabel("Time")
    plt.ylabel("Power (w)")
    plt.legend()

    plt.savefig(f"rolling_average_{str(datetime.now()).split(' ')[1].split('.')[0].replace(':', '_')}.png",
                bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    values = preprocess(load_csv())
    d = calculate_rolling_average(values)
    plot_chart(d)
