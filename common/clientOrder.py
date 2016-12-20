class clientOrder(object):
	# def __init__(self, orderId, stockId, startTime, endTime, stockAmount, buysell, algChoice, timeInterval, completed, status):
	def __init__(self, orderId, stockId, startTime, endTime, stockAmount, buysell, algChoice, completed, status):
		#super(clientOrder, self).__init__()
		#super(clientOrder, self).__init__()
		self.orderId = orderId
		self.stockId = stockId
		self.startTime = startTime
		self.endTime = endTime
		self.stockAmount = stockAmount
		self.buysell = buysell
		self.algChoice = algChoice
		# self.timeInterval = timeInterval
		self.completed = completed # number of shares that have been completed.
		self.status = status # 0 places, 1 sent, 2 completed
