"""
Working List of Signals

All signal development is done in this file
"""

import numpy as np
import pandas as pd


# Indicator functions.
# priceSeries is a pandas Series object.
def meanReversion(priceSeries, period = 5, mulFactor = 1, addFactor = 0):
    frame = pd.DataFrame(priceSeries)
    frame.columns = ['price']
    frame['change'] = priceSeries.diff()
    frame['sd'] = pd.rolling_std(frame['price'], period)
    frame['signal'] = np.where(frame['change'] < (mulFactor*frame['sd']+addFactor), 1, -1)
    frame['signal'][0:(period-1)] = 0

    return frame['signal']

def maCrossover(priceSeries, period = 3):
    return 0

# General Indicator Classes
    
