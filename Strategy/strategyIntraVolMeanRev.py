# encoding: UTF-8

"""
这里的Demo是一个最简单的双均线策略实现
"""

from __future__ import division

from vnpy.trader.vtConstant import *
from vnpy.trader.app.ctaStrategy.ctaBase import *
from vnpy.trader.app.ctaStrategy.ctaTemplate import (CtaTemplate, 
                                                     BarGenerator,
                                                     ArrayManager)
import numpy as np
import datetime
MINWAITINGTIME=datetime.timedelta(seconds=0.1) #只对间隔100ms以上的tick做出交易操作
########################################################################
class LimitOrder2TradeStrategy(CtaTemplate):
    """双指数均线策略Demo"""
    className = 'LimitOrder2TradeStrategy'
    author = u'Hunggin'
    
    # 策略参数
    initDays = 1            # 初始化数据所用的天数
    multiplier = 1          # 手数    
    bufferSize = 40         # 缓存的tick数据长度
    difference = 6          # 钓鱼单离盘口的距离，后续的改进重点
    maxWaitingTime = 120    # 强制退场最大等待时间    
    priceTick = 1           # 最小价格变动
    
    # 策略变量    
    posTimer = 0                  # 进场计时器，用来触发强制退场条件
    timer = datetime.datetime(1,1,1,0) # 时间计时器

    buyPrice = EMPTY_FLOAT        # 钓鱼买单价
    shortPrice = EMPTY_FLOAT      # 钓鱼卖单价

    buyOrderList = []             # 钓鱼买单订单列表
    shortOrderList = []           # 钓鱼卖单订单列表
    exitOrderList = []            # 离场单列表

    askPriceArray = np.zeros(bufferSize)        # 卖一价序列
    bidPriceArray = np.zeros(bufferSize)        # 买一价序列
    askVolumeArray = np.zeros(bufferSize)       # 卖一量
    bidVolumeArray = np.zeros(bufferSize)       # 买一两
    volumeArray = np.zeros(bufferSize)          # 总成交量序列
    currentVolumeArray = np.zeros(bufferSize)   # 现成交量序列

    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'multiplier',
                 'bufferSize',
                 'difference',
                 'maxWaitingTime',
                 'priceTick']    
    
    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos',
               'buyPrice',
               'shortPrice',
               'posTimer']  
    
    # 同步列表，保存了需要保存到数据库的变量名称
    syncList = ['pos']

    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(LimitOrder2TradeStrategy, self).__init__(ctaEngine, setting)

        self.lastPriceArray = np.zeros(self.bufferSize)
        self.askPriceArray = np.zeros(self.bufferSize)
        self.bidPriceArray = np.zeros(self.bufferSize)
        self.askVolumeArray = np.zeros(self.bufferSize)
        self.bidVolumeArray = np.zeros(self.bufferSize)
        self.volumeArray = np.zeros(self.bufferSize)
        self.currentVolumeArray = np.zeros(self.bufferSize)
        self.buyOrderList = []
        self.shortOrderList = []
        self.exitOrderList = []

        
        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）
        
    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'钓鱼策略初始化')
        
        initData = self.loadTick(self.initDays)
        for tick in initData:
            self.onTick(tick)
        
        self.timer = datetime.datetime.now()
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'钓鱼策略启动')
        self.putEvent()
    
    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'钓鱼策略停止')
        self.putEvent()
        
    #----------------------------------------------------------------------
    def setBuyPrice(self, price):
        self.buyPrice = price

    #----------------------------------------------------------------------
    def setShortPrice(self, price):
        self.shortPrice = price

    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""

        # 数据更新
        timer = datetime.datetime.now()
        self.lastPriceArray[0:self.bufferSize-1] = self.lastPriceArray[1:self.bufferSize]

        self.askPriceArray[0:self.bufferSize-1] = self.askPriceArray[1:self.bufferSize]
        self.bidPriceArray[0:self.bufferSize-1] = self.bidPriceArray[1:self.bufferSize]
        self.askVolumeArray[0:self.bufferSize-1] = self.askVolumeArray[1:self.bufferSize]
        self.bidVolumeArray[0:self.bufferSize-1] = self.bidVolumeArray[1:self.bufferSize]
        self.volumeArray[0:self.bufferSize-1] = self.volumeArray[1:self.bufferSize]
        self.currentVolumeArray[0:self.bufferSize-1] = self.currentVolumeArray[1:self.bufferSize]       
        
        self.lastPriceArray[-1] = tick.lastPrice
        self.askPriceArray[-1] = tick.askPrice1
        self.bidPriceArray[-1] = tick.bidPrice1        
        self.askVolumeArray[-1] = tick.askVolume1
        self.bidVolumeArray[-1] = tick.bidVolume1
        self.volumeArray[-1] = tick.volume

        currentVolume = self.volumeArray[-1] - self.volumeArray[-2]                                 # 正常计算现手
        self.currentVolumeArray[-1] = self.volumeArray[-1] if currentVolume < 0 else currentVolume  # 但如果遇到新的交易日，会出现现手为负的情况，此时以总成交量作为现手

        shortPrice = tick.askPrice1 + self.difference if tick.askPrice1 > 0 else 0                  # 计算钓鱼卖单价
        buyPrice = tick.bidPrice1 - self. difference if tick.bidPrice1 > 0 else 0                   # 计算钓鱼买单价

        if shortPrice >= tick.upperLimit and tick.upperLimit != 0:      # 检验是否超过涨停价,从TB导出的数据没有upperLimit,即为0,但实盘有
            shortPrice = 0.0
        if buyPrice <= tick.lowerLimit and tick.lowerLimit != 0:        # 检验是否超过跌停价,从TB导出的数据没有lowerLimit,即为0,但实盘有
            buyPrice = 0.0

              
        #print timer, self.timer, buyPrice, self.buyPrice
        #print timer, self.timer, shortPrice, self.shortPrice                             
        if timer - self.timer > MINWAITINGTIME or self.getEngineType() == ENGINETYPE_BACKTESTING: #实盘的有效数据 or 回测,即过滤实盘延迟tick,才进行撤单操作
            if buyPrice != self.buyPrice:                                   # 如果钓鱼买入价格发生变动
                for buyOrderID in self.buyOrderList:
                    if buyOrderID in self.buyOrderList:
                        #print timer, self.timer, buyPrice, self.buyPrice                                 
                        self.cancelOrder(buyOrderID)                            # 则撤单
                        self.buyOrderList.remove(buyOrderID)
            if shortPrice != self.shortPrice:                               # 如果钓鱼卖出价格发生变动
                for sellOrderID in self.shortOrderList:
                    if sellOrderID in self.shortOrderList:                    
                        #print datetime.datetime.now(), tick.time, shortPrice, self.shortPrice     
                        self.cancelOrder(sellOrderID)
                        self.shortOrderList.remove(sellOrderID)                 # 则撤单      
            self.setShortPrice(shortPrice)                              # 并甚至新的钓鱼卖出价格
            self.setBuyPrice(buyPrice)                                  # 并设置新的钓鱼买入价

        if "09:00:30.0" <= tick.time <= "14:56:59.5" or "21:00:30.0" <= tick.time <= "22:59:50.5":  # 钓鱼时间过滤
            if self.pos == 0:                                                       # 如果没有仓位，则执行钓鱼
                for exitOrder in self.exitOrderList:
                    if exitOrder in self.exitOrderList:
                        self.exitOrderList.remove(exitOrder)                        # 首先，把离场单清空
                self.posTimer = 0                                                   # 初始化离场计时器
                if len(self.buyOrderList) == 0:                                     # 保持买入钓鱼
                    if self.buyPrice > 0:   
                        l1 = self.buy(self.buyPrice, self.multiplier)
                        self.buyOrderList.extend(l1)
                if len(self.shortOrderList) == 0:                                   # 保持卖出钓鱼
                    if self.shortPrice > 0:
                        l2 = self.short(self.shortPrice, self.multiplier)
                        self.shortOrderList.extend(l2)
        else:                                                                       # 非钓鱼时间
            for buyOrderID in self.buyOrderList:                                  
                self.cancelOrder(buyOrderID)                                        # 撤买入钓鱼单
                self.buyOrderList.remove(buyOrderID)
            for sellOrderID in self.shortOrderList:
                self.cancelOrder(sellOrderID)                                       # 撤卖出钓鱼单
                self.shortOrderList.remove(sellOrderID)             
        if self.pos < 0:                                                            # 空头平仓设置
            self.posTimer += 1
            if len(self.exitOrderList) == 0:
                l3 = self.cover(self.bidPriceArray.mean() + self.priceTick, abs(self.pos))  # 这里采用的是买一盘口均价多一跳
                self.exitOrderList.extend(l3)
        if self.pos > 0:                                                            # 多头平仓设置
            self.posTimer +=1
            if len(self.exitOrderList) == 0:
                l4 = self.sell(self.askPriceArray.max() - self.priceTick, abs(self.pos))    # 这里采用的是卖一均价多一跳
                self.exitOrderList.extend(l4)                               

        if self.posTimer >= self.maxWaitingTime:                                    # 最大等待时间已够，触发强制离场
            self.cancelAll()                                                        # 强平前，全部撤单（其实只需要撤exitOrderList里面的单即可）
            if self.pos < 0:                                                        # 如果空头
                l1 = self.cover(self.askPriceArray[-1] + self.priceTick, abs(self.pos)) # 对手价+1跳，多头离场
            elif self.pos > 0:
                l2 = self.sell(self.bidPriceArray[-1] - self.priceTick, abs(self.pos))  # 对手价-1跳，空头离场
        #print timer, self.timer, tick.time
        self.timer = timer
        self.putEvent()
    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        pass
    
    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onTrade
        pass
    
    #----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass    
