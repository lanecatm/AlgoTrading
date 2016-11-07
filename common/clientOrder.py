class clientOrder(object):
	"""docstring for clientOrder"""
	def __init__(self, orderId, stockId, startTime, endTime, stockAmount, buysell, algChoice, timeInterval, status):
		#super(clientOrder, self).__init__()
		#self.arg = arg
		self.orderId = orderId
		self.stockId = stockId
		self.startTime = startTime
		self.endTime = endTime
		self.stockAmount = stockAmount
		self.algChoice = algChoice
		self.buysell = buysell
		self.timeInterval = timeInterval
                self.status = status # 0 places, 1 sent, 2 completed
