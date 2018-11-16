# Quantative-Trading-Models 
![vnpy](https://img.shields.io/badge/vnpy-1.8.1-orange.svg)
![Python 3x](https://img.shields.io/badge/python-3.x-blue.svg)
![hmm](https://img.shields.io/badge/hmm-0.0.1.dist--info-green.svg)


These are trading results and arbitrage models from Southern China Center for Statistical Science (SC2S2), Sun Yat-sen University

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/logo.png" height="200">

## Research Details
We have completed designed the algorithm of **intraday volatile mean reversion strategy** and run it on *RB1805*,*RB1810* object on [vnpy](https://github.com/vnpy/vnpy). 

See `strategyIntraVolMeanRev.py` for more details trading algorithm.

Meantime, we have implemented various statistical arbitrage model including




1. **Cross-star Arbitrage**
2. **Hidden Markov Model** based on Factors Decomposition
3. **Paired Cointegrative Arbitrage**

## Results

+ **intraday volatile mean reversion strategy** on *RB1810*

1. Backtesting

Trading results from 05/2017 to 07/2017 on *RB1805*

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Strategy/Partial%20Results.png" height="800" align=center>

see `backtesting_strategyIntraVolMeanRev.ipynb` for more details

2. Minic Panel

Minic trading results on 05/06/2018 on *RB1810*

<div align="center">
<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Strategy/MinicPanel_0605_0.png" height="330">
<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Strategy/MinicPanel_0605_1.png" height="330">
</div>

---
+ **Hidden Markov Model arbitrage** on *CSI300*

First, we illustrate the basic conception of HMM and write the augmented expected log-likelihood as 

<img src="https://latex.codecogs.com/gif.latex?\begin{aligned}&space;Q(\theta,\theta^*)&=\sum_Z&space;\log&space;f&space;(X,Z|\theta)f(Z|X,\theta^*)\\&space;&=\sum_Z&space;\log[f(Z|\theta)P(X|Z,\theta)]f(Z|X,\theta^*)\\&space;&=\sum_Z&space;\log[f(z_1|\theta)\prod_{n=2}^Nf(z_n|z_{n-1},\theta)\prod_{n=1}^Nf(x_n|z_n,\theta)]f(Z|X,\theta^*)&space;\end{aligned}" title="\begin{aligned} Q(\theta,\theta^*)&=\sum_Z \log f (X,Z|\theta)f(Z|X,\theta^*)\\ &=\sum_Z \log[f(Z|\theta)P(X|Z,\theta)]f(Z|X,\theta^*)\\ &=\sum_Z \log[f(z_1|\theta)\prod_{n=2}^Nf(z_n|z_{n-1},\theta)\prod_{n=1}^Nf(x_n|z_n,\theta)]f(Z|X,\theta^*) \end{aligned}" /></a>

* <img src="https://latex.codecogs.com/gif.latex?f(z_1|\theta)" title="f(z_1|\theta)" /></a> is the prior state probabilities
* <img src="https://latex.codecogs.com/gif.latex?f(z_n|z_{n-1})" title="f(z_n|z_{n-1})" /></a> is the state transition probabilities
* <img src="https://latex.codecogs.com/gif.latex?f(x_n|z_n)" title="f(x_n|z_n)" /></a> is the output probabilities

A example for the probabilistic parameters of a hidden Markov model is presented as below(Omit partial output probabilities for simplicity)

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Model/HMM/Prob.png" height="330">

Based on [RiceQuant](https://www.ricequant.com/profile/352568), we obtain daliy open,high,low,close and volume of *CSI300* (`data`) from 01/01/2005 to 31/12/2015 and denoted three feature-factors as,

1. Computing logged daliy spread
```Python
Factor1 = np.log(np.array(data['High'])) - np.log(np.array(data['Low']))
```
2. Computing each 5 days logged return spread
```Python
Factor2 = np.log(np.array(data['High'][5:])) - np.log(np.array(data['High'][5:]))
```
3. Computing each 5 days logged volume spread
```Python
Factor3 = np.log(np.array(data['Volume'][5:])) - np.log(np.array(data['Volume'][5:]))
```

After that, we preset six potential states of *CSI300* and begin our assessment in `HMM_arbitrage.py`

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Model/HMM/HMM_Status.png" height="330" align=center>
<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Model/HMM/Status_Judgement.png" height="330" align=center>


Finally, we demonstrate our trading return based on previous HMM prediction

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Model/HMM/Return.png" height="330" align=center>

---
+ **Cross-star Arbitrage** on dominant futures *Pb*

1. Pb Dominant Futures Duration

|start |end |symbol|
|--------|--------|--------|
|2017/10/19 |2017/10/23 |PB1711
|2017/10/24 |2017/11/16 |PB1712
|2017/11/17 |2017/12/19 |PB1801
|2017/12/20 |2018/1/17 |PB1802
|2018/1/18 |2018/2/14| PB1803
|2018/2/22 |2018/3/14| PB1804
|2018/3/15 |2018/4/17 |PB1805
|2018/4/18 |2018/5/23| PB1806
|2018/5/24 |2018/6/26| PB1807
|2018/6/27 |2018/7/23| PB1808
|2018/7/24 |2018/8/20 |PB1809
|2018/8/21 |2018/9/19 |PB1810
|2018/9/20 |2018/10/19| PB1811

2. Pb Dominant Contract Backtesting Return(ignore trading fees)

we run our Cross-Star strategy on *Pb* Dominant contract from 2018/05/05 to 2018/11/10. For more details in `Integrate_Pb.ipynb`

<img src="https://github.com/Gaochenyin/Quantative-Trading-Models/blob/master/Model/Cross_Star/Pb/TradingResults/Pb_Return.png" height="330">

## Set up
+ [***vnpy***](https://github.com/vnpy/vnpy)(vnpy-1.8)
+ ***hmmlearn***
+ ***numpy*** 
+ ***pandas*** 
+ ***matplotlib***

## Contact
+ gaochy5@mail2.sysu.edu.cn

![license](https://img.shields.io/packagist/l/doctrine/orm.svg)
