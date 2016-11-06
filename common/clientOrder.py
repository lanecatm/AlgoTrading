class clientOrder(object):
	"""docstring for clientOrder"""
	def __init__(self, action, stockId, startTime, endTime, stockAmount, algChoice):
		#super(clientOrder, self).__init__()
		#self.arg = arg
		self.action = action
		self.stockId = stockId
		self.startTime = startTime
		self.endTime = endTime
		self.stockAmount = stockAmount
		self.algChoice = algChoice

		