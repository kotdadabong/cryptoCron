import robin_stocks as r
import sys

from decimal import *

#tradingcrypto=str(sys.argv[1])

cryptoSymbols=['BTC','DOGE','ETC','LTC']
spendLimit=1


login=r.login('your@email.com','password')


def buyCryptoQuantity(tradingcrypto,quantity,pricetype):
	reciept=r.orders.order_buy_crypto_by_quantity(tradingcrypto,quantity,pricetype,'gtc')
	return(reciept)
def buyCryptoPrice(tradingcrypto,spendinglimit,pricetype):
	reciept=r.orders.order_buy_crypto_by_price(tradingcrypto,spendinglimit,pricetype,'gtc')
	return(reciept)
def buyCryptoLimit(tradingcrypto,quantity,limitprice):
	reciept=r.orders.order_buy_crypto_limit(tradingcrypto,quantity,limitprice,'gtc')
	return(reciept)
	
def sellCryptoQuantity(tradingcrypto,quantity,pricetype):
	reciept=r.orders.order_sell_crypto_by_quantity(tradingcrypto,quantity,pricetype,'gtc')
	return(reciept)
def sellCryptoPrice(tradingcrypto,spendinglimit,pricetype):
	reciept=r.orders.order_sell_crypto_by_price(tradingcrypto,spendinglimit,pricetype,'gtc')
	return(reciept)
def sellCryptoLimit(tradingcrypto,quantity,limitprice):
	reciept=r.orders.order_sell_crypto_limit(tradingcrypto,quantity,limitprice,'gtc')
	return(reciept)
	
def checkOrderStatus( order_id):
	reciept=r.orders.get_crypto_order_info(order_id)
	#print(reciept)
	
	return(reciept)
def cancelCryptoOrder(order_id):
	reciept=r.orders.cancel_crypto_order(order_id)
	return(reciept)

def readAnalyzerFile(fileName):
	with open(fileName, encoding="utf-8") as readPrices:
		intake=readPrices.read()
		fileString=""
		for x in intake:
			fileString=fileString+x
		
		fileList=fileString.split('<$?>')
		#EZ Read list for indexed data
		#print(priceFile,' high',fileList[0])
		#print(priceFile,' low',fileList[1])
		#print(priceFile,' true',fileList[2])
		#print(priceFile,' highs',fileList[3])
		#print(priceFile,' lows',fileList[4])
		#print(priceFile,' opens',fileList[5])
		#print(priceFile,' closes',fileList[6])
		#print('priceFile,' times',fileList[7])
		#print(priceFile,' candlesticks',fileList[8])
		del fileList[-1]
		return(fileList)
def splitStringToList(stringAtHand):
	x=stringAtHand[1:]	
	x=x[:-1]
	newlist=x.split(', ')
	return(newlist)	
def processPositionsInfo(profileAnalysis):
	cryptoPositions=[]
	positionString=profileAnalysis[1]                  #PROCESSING ALL POSITIONS
	positionString=positionString[2:]                  #
	positionString=positionString[:-2]                 #
	positionsList=positionString.split("], [")         #
													   #
	for x in positionsList:                            #
		x=x[1:]                                        #work it
		x=x[:-1]                                       #
		cryptoPosition=x.split("', '")                 #split it
		#print(cryptoPosition)                          #
		cryptoPositions.append(cryptoPosition)         #filled cryptoPositions with the positions
	return(cryptoPositions)
def processProfileInfo(profileAnalysis):
	sufficientbuyingpower=False
	if float(profileAnalysis[0])>=3.00: 
		print(profileAnalysis[0])               #IF THERES MONEY TO TRADE
		sufficientbuyingpower=True
	return(sufficientbuyingpower)

def analyzeRSI(rawRSI,timeframe):
	rsi=float(rawRSI)

	print(timeframe,'RSI ANALYSIS:')
	if rsi<30:
		print('great time to buy')
	elif rsi>30 and rsi<50:
		print('theres probably some decent room for profit')
	elif rsi>50 and rsi<70:
		print('should probably sell soon')
	elif rsi>70:
		print('DONT BUY, DONT WAIT. SELL NOW')
def analyzeSpansOverallChanges(changelist):
	spanlabels=['5min','30min','hour','day','week','month']

	for x in range (0,len(changelist)):
		change=changelist[x]
		changeint=int(change)
		if changeint>0:
			print('the last',spanlabels[x],'has been gaining by:',abs(changeint))
		elif changeint<0:
			print('the last',spanlabels[x],'has been losing by:',abs(changeint))
		else:
			print(changeint) 
def unpackEngulfments(engulfmentString):
	engulfmentLabels=['15Second Engulfing in the last hour','10Minute Engulfing in the last Day','Hourly Engulfing in the last Week','Daily Engulfing in the last Month','Engulfing Now']
	e=engulfmentString[2:]
	e=e[:-2]
	elist=e.split("', '")
	return(elist)
#read from analyzer file

#PROFILE ANALYSIS
profileAnalysis=readAnalyzerFile('profile.analysis')   #strings of buyingpower and allcryptopositions


hasInvestableFunds=processProfileInfo(profileAnalysis)  #If theres Funds to trade with
print('Has investable funds: ',hasInvestableFunds)
print('')
currentPositions=processPositionsInfo(profileAnalysis)  #Statusappending to positions
print('Current Crypto Positions:')
for x in currentPositions:
	#print(x)
	if float(x[1])>0 and float(x[2])==0:
		print(x[0], 'has quantity to sell: ',x[1])
		x.append('sellable')
	elif float(x[1])==0:
		print(x[0], 'is ready to begin a new trade')
		x.append('buyable')
	elif float(x[2])>0:
		print(x[0], 'has sell waiting to complete: ',x[2])
		x.append('awaiting sell')
	else:
		print(';no telling what happened')
print('')

for x in cryptoSymbols:
	pricefile=x+'situation.analysis'
	print(x+'###################################################################')
	#PRICE ANALYSIS
	priceanalysis=readAnalyzerFile(pricefile)
	#print(priceanalysis)
	priceanalysiskey=['Current Ask','Current Mark','Current Bid','RSI-24hr,14day,30day','Engulfments-hour,day,week,month,now','Moving Avgs-5min,hr,day,week,month','Span Changes-5min,30min,hour,day,week,month']
	currentAsk=priceanalysis[0]
	currentMarkd=priceanalysis[1]
	currentBid=priceanalysis[2]
	rsiList=splitStringToList(priceanalysis[3])
	engulfments=splitStringToList(priceanalysis[4])
	averages=splitStringToList(priceanalysis[5])
	spanChangesString=priceanalysis[6] #last 5min,30min,hour,day,week,months changes
	daysRSI=rsiList[0]
	standardRSI=rsiList[1]
	monthlyRSI=rsiList[2]
	hourlyEngulfing=engulfments[0]
	dayEngulfing=engulfments[1]
	weekEngulfing=engulfments[2]
	monthEngulfing=engulfments[3]
	engulfingNow=engulfments[4]
	last5avg=averages[0]
	houravg=averages[1]
	dayavg=averages[2]
	weekavg=averages[3]
	monthavg=averages[4]
	spanChangeList=splitStringToList(spanChangesString)
	#READABLE ANALYSIS
	for y in range (0,len(priceanalysis)):
		print(priceanalysiskey[y],': ',priceanalysis[y])
	###############################################TRADING LOGIC
	currentPosition=[]
	for symbol in range(0,len(currentPositions)):
		if currentPositions[symbol][0]==x:
			currentPosition=currentPositions[symbol]
	testables=[currentPosition[5],hasInvestableFunds]
	print('currentAsk',currentAsk)
	quantity=spendLimit/Decimal(float(currentAsk))
	if testables==['buyable',True]:
		if float(daysRSI)<50:
			
			print(buyCryptoLimit(x,round(float(quantity),8),round(float(currentAsk),2)))
			print('put in order to buy')
	elif currentPosition[5]==('sellable'):
		currentCryptocostBasis=0
		for symbol in currentPositions:
			if symbol[0]==x:
				currentCryptocostBasis=currentPosition[4]
		if float(currentBid)>float(currentCryptocostBasis):
			if daysRSI>55:
				print(sellCryptoQuantity(x,x[1],'bid_price'))
				print('put in sell order')
			else:
				print('rsi still too low to sell')
		else:
			print('price isnt right')
			print(currentPosition)
	elif currentPosition[5]==('awaiting sell'):
		##wait
		orders=r.orders.get_all_open_crypto_orders()
		print(orders)
		print(currentPosition[5])
	else:
		print('not buyable or insufficient funds')

	#print('')
	#analyzeRSI(daysRSI, '24HR')
	#analyzeRSI(standardRSI, '14 Day')
	#analyzeRSI(monthlyRSI, '30 Day')
	#print('')
	#analyzeSpansOverallChanges(spanChangeList)
