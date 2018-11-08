# Quantative-Trading-Models

## Introduction 
These are serveral trading results and arbitrage models from Southern China Center for Statistical Science (SC2S2), Sun Yat-sen University

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/logo.png" height="200">

## Research Details
We have completed designed the algorithm of **intraday volatile mean reversion strategy** and run it on *RB1805*,*RB1810* object on [vnpy](https://github.com/vnpy/vnpy). 

See `strategyIntraVolMeanRev.py` for more details trading algorithm.

Meantime, we have implemented various statistical arbitrage model including

1. Cross-star Arbitrage
2. Hidden Markov Model based on Fama-French Three Factors Decomposition
3. Paired Cointegrative Arbitrage

## Results

+ **intraday volatile mean reversion strategy** on *RB1810*

1. ***Backtesting***

Trading results from 05/2017 to 07/2017 on *RB1805*
<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Strategy/Partial%20Results.png" height="600" align=center>

see `backtesting_strategyIntraVolMeanRev.ipynb` for more details

2. ***Minic Panel***
<div align="center">
<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Strategy/MinicPanel_0605_0.png" height="330">
<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Strategy/MinicPanel_0605_1.png" height="330">
</div>

+ Cross-star Arbitrage on dominant futures *Pb*
Pb Futures Duration
start end symbol
2017/10/19 2017/10/23 PB1711
2017/10/24 2017/11/16 PB1712
2017/11/17 2017/12/19 PB1801
2017/12/20 2018/1/17 PB1802
2018/1/18 2018/2/14 PB1803
2018/2/22 2018/3/14 PB1804
2018/3/15 2018/4/17 PB1805
2018/4/18 2018/5/23 PB1806
2018/5/24 2018/6/26 PB1807
2018/6/27 2018/7/23 PB1808
2018/7/24 2018/8/20 PB1809
2018/8/21 2018/9/19 PB1810
2018/9/20 2018/10/19 PB1811
## Set up
+ [***vnpy***](https://github.com/vnpy/vnpy)(vnpy-1.8)
+ ***numpy*** 
+ ***pandas*** 
+ ***matplotlib***

## Contact
+ gaochy5@mail2.sysu.edu.cn
