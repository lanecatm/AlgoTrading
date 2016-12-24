class clientOrder(object):
    # def __init__(self, orderId, stockId, startTime, endTime, stockAmount, buysell, algChoice, timeInterval, completed, status):
    # buy 0 sell 1
    # 0 TWAP 1 VWAP
    UNINIT = 0
    INIT = 1
    COMPLETED = 2

    def create_order(self, stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType):
        self.orderId = None
        self.stockId = stockId
        self.startTime = startTime
        self.endTime = endTime
        self.stockAmount = stockAmount
        self.buySell = buysell
        self.algChoice = algChoice
        self.processId = processId
        self.tradingType = tradingType

        # 目前完成的数量 int
        self.completedAmount = 0
        # order 状态 0 未初始化 1 初始化 2 完成
        self.status = UNINIT
        # 量化分析dict
        self.quantAnalysisDict = None
        # 上一次更新时间 datetime
        self.updateTime = None
        # 下一次更新时间 datetime
        self.nextUpdateTime = None
        # 更新时间间隔
        self.updateTimeInterval = 1
        # 交易时间
        self.tradeTime = None

        # 当全部订单完成后更新
        # 总共交易金额
        self.trunOver = 0
        # 总共交易价格
        self.avgPrice = 0

    def init_order(self, quantAnalysisDict, timeInterval = 1):
        self.status = INIT
        self.quantAnalysisDict = quantAnalysisDict
        self.updateTime = self.startTime
        self.nextUpdateTime = self.startTime
        self.timeInterval = timeInterval


    def create_order_by_sql_list(self, sqlList):
        # 一开始赋值并且不改变的字段
        # client order id int
        self.orderId = sqlList[0]
        # stock id int
        self.stockId = sqlList[1]
        # 开始时间 datetime
        self.startTime = sqlList[2]
        # 结束时间 datetime
        self.endTime = sqlList[3]
        # 期望交易的股票数量 int
        self.stockAmount = sqlList[4]
        # BUY or SELL
        self.buySell = sqlList[5]
        # TWAP / VWAP
        self.algoChoice = sqlList[6]
        # 进程id 1
        self.processId = sqlList[10]
        # 交易类型 pool中的
        self.tradingType = sqlList[15]

        # 在运行过程中更新的字段
        # 目前完成的数量 int
        self.completedAmount = sqlList[7]
        # order 状态 0 未初始化 1 初始化 2 完成
        self.status = sqlList[8]
        # 量化分析dict
        self.quantAnalysisDict = eval(sqlList[9])
        # 上一次更新时间 datetime
        self.updateTime = sqlList[11]
        # 下一次更新时间 datetime
        self.nextUpdateTime = sqlList[12]
        # 更新时间间隔
        self.updateTimeInterval = sqlList[13]
        # 交易时间
        self.tradeTime = sqlList[14]

        # 当全部订单完成后更新
        # 总共交易金额
        self.trunOver = sqlList[16]
        # 总共交易价格
        self.avgPrice = sqlList[17]

