
# Copyright (c) 2014 Zirui Wang @elexonics

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



# This is a simple ATT Mobile Share Value Plan 10GB phone bill spliter.
# The basic pricing is as follows,
# 	Group owner basic is 104.54, including member basic and group addition
# 	Group member basic is 19.39
# So the average basic for each is 27.905, the average group addition per person is 8.515
# If there exists any over usage, will lead to extra fees, works as follows,
# 	Data over usage: fees applied to the owners, need to split with actual over-user
#   Other over usage & extra service: 
# 	  1) if applied to individual, counts towards him/herself's total
# -->>2) if applied to owner, need calc manually


#! python3
import os.path
import re

class BillDetailer:
	def __init__(self, path=os.getcwd()):
		self.dataBase={} #{number:[expense, data, dataExtraExpense]}
		self.phoneBook={'5124685514':'5514',
						'5124686959':'6959',
						'5124963468':'3468',
						'5126947091':'7091',
						'5128266324':'6324',
						'5128658134':'8134',
						'5129132195':'2195',
						'5129232219':'Owner',
						'5129547686':'7686',
						'5129547693':'7693'}
		self.ownerNumber='5129232219'
		self.totalMember=len(self.phoneBook)-1
		self.extraDataTotal=0
		self.dataUsage=""
		self.billContent=""

	def setDataUsage(self, dataUsage):
		self.dataUsage=re.sub('[-() ,]', '', dataUsage)

	def setBillContent(self, billContent):
		self.billContent=re.sub('[-() ,]', '', billContent)

	def setBalanceStoreLocation(self, storeLocation):
		self.storeLocation=storeLocation

	def checkAllDetailsSet(self):
		if self.dataUsage and self.billContent:
			return True
		else:
			return False

	def findBillAndUsageForEach(self):
		#find bill detail for each
		for number in self.phoneBook:
			numberStartPos=0
			numberStartPos=self.billContent.find(number, numberStartPos)
			expenseStartPos=self.billContent.find("$", numberStartPos)
			endPos=self.billContent.find(".", expenseStartPos)+2
			expense=float(self.billContent[expenseStartPos+1:endPos+1])
			self.dataBase[number]=[expense]
		#find usage detail for each
		self.extraDataTotal=0
		for number in self.dataBase:
			startPos=0
			startPos=self.dataUsage.find(number, startPos)
			endPos=self.dataUsage.find("\n", startPos)
			data=int(self.dataUsage[startPos+10:endPos+1])
			if data>1024:
				self.extraDataTotal+=data
			self.dataBase[number].append(data)

	def splitBill(self):
		dataExtraExpenseTotal=self.dataBase[self.ownerNumber][0]-104.54
		for number in self.dataBase:
			if self.extraDataTotal > 0:
				extraData=self.dataBase[number][1]-1024
				if extraData<0: extraData=0
				self.dataBase[number].append(dataExtraExpenseTotal*extraData/float(self.extraDataTotal))
			else:
				self.dataBase[number].append(0)
			if number == self.ownerNumber:
				self.dataBase[number].append(self.dataBase[number][2]+27.905)
			else:
				self.dataBase[number].append(self.dataBase[number][0]+self.dataBase[number][2]+8.515)

	def printMessage(self, display=print, index=3):
		#print("index=",index)
		for number in self.dataBase:
			display(self.phoneBook[number],"'s balance:",round(self.dataBase[number][index],3))


