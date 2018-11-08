from hmmlearn.hmm import GaussianHMM
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import datetime

# Set up
beginDate = '2005-01-01'
endDate = '2015-12-31'
n = 6 # preset status
data = get_price('CSI300.INDX',start_date=beginDate, end_date=endDate,frequency='1d')
data.iloc[0:9,]
Factor1 = np.log(np.array(data['High'])) - np.log(np.array(data['Low']))
Factor2 = np.log(np.array(data['High'][5:])) - np.log(np.array(data['High'][5:]))
Factor3 = np.log(np.array(data['Volume'][5:])) - np.log(np.array(data['Volume'][5:]))
Factors = np.column_stack([Factor1,Factor2,Factor3])

# Prediction
model = GaussianHMM(n_components= n, covariance_type="full", n_iter=2000).fit(Factors)
hidden_states = model.predict(A)
plt.figure(figsize=(30, 18)) 
for i in range(model.n_components):
    pos = (hidden_states==i)
    plt.plot_date(Date[pos],close[pos],'o',label='hidden state %d'%i,lw=2)
    plt.legend(loc="upper left",
              fontsize=30)

# Validation
res = pd.DataFrame({'Date':Date,'logRet_1':logRet_1,'state':hidden_states}).set_index('Date')
plt.figure(figsize=(25, 18)) 
for i in range(model.n_components):
    pos = (hidden_states==i)
    pos = np.append(0,pos[:-1])#Buy in next day
    df = res.logRet_1
    res['state_ret%s'%i] = df.multiply(pos)
    plt.plot_date(Date,np.exp(res['state_ret%s'%i].cumsum()),'-',label='hidden state %d'%i)
    plt.legend(loc="upper left",
              fontsize=30)


# Trading
Long = (hidden_states==0) + (hidden_states == 1) # Long
Short = (hidden_states==3) + (hidden_states == 5)  # Short
Long = np.append(0,long[:-1]) 
Short = np.append(0,short[:-1]) 

# Return Results
res['ret'] =  df.multiply(long) - df.multiply(short)  
plt.plot_date(Date,np.exp(res['ret'].cumsum()),'r-')