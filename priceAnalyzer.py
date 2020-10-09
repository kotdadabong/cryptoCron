import robin_stocks as r
import sys
from decimal import *
import time


login=r.login('your@email.com','password')

#tradingcrypto='DOGE'
#tradingcrypto=str(sys.argv[1])
cryptoSymbols=['BTC','DOGE','ETC','LTC']


engulfingNow=False
askavg=[]
markavg=[]
bidavg=[]

def averageHistoricalQuotes(tradingcrypto,interval,span):
	lowprices=[]
	highprices=[]



	history=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7')
	#format the product
	for x in range (0,len(history)):
		dataset=history[x]
		#print('begins_at',dataset['begins_at'])
		#print('low price ',dataset['low_price'])
		#print('high price ',dataset['high_price'])	
		#print('##########################################################')
		
		lowprices.append(dataset['low_price'])
		highprices.append(dataset['high_price'])
		
	#####Average out the low prices#######################
	lowtotal=0
	hightotal=0
	for x in range(0,len(lowprices)):
		adder=float(lowprices[x])
		lowtotal+=adder
	for x in range(0,len(highprices)):
		adder=float(highprices[x])
		hightotal+=adder
	lowavg=lowtotal/len(lowprices)
	highavg=hightotal/len(highprices)

	print('datapoints: ',len(lowprices))
	print('low average: ', round(lowavg,6))
	print('high average: ',round(highavg,6))
	return(round(lowavg,6),round(highavg,6)) ####RETURNS TUPLE [LOWPRICE,HIGHPRICE]
def getAveragePrices():
	ask=[strtPrice]
	mark=[strtPrice]
	bid=[strtPrice]
	askAvg=0.00
	markAvg=0.00
	bidAvg=0.00
	for x in range (0,5):
		ping=getcryptoquotes(tradingcrypto)
		print(tradingcrypto+' current prices:')
		print(ping)
		ask.append(ping['Ask'])
		mark.append(ping['Mark'])
		bid.append(ping['Bid'])
		#time.sleep(10)
	for y in range (0,5):
		
		askAvg=(askAvg+float(ask[y+1]))
		markAvg=(markAvg+float(mark[y+1]))
		bidAvg=(bidAvg+float(bid[y+1]))
		
	askAvg=(askAvg/5)
	markAvg=(markAvg/5)
	bidAvg=(bidAvg/5)
	print('final avg:')
	print ('Ask: ',askAvg)
	print ('Mark: ',markAvg)
	print ('Bid: ',bidAvg)
	
def calculateBuyPrice():
	print('Calculating the buy price')
	hourlyAverages=averageHistoricalQuotes(tradingcrypto,'15second','hour')    #update hourly avg
	dailyAverages=averageHistoricalQuotes(tradingcrypto,'10minute','day')      #update daily avg
	weeklyAverages=averageHistoricalQuotes(tradingcrypto,'hour','week')        #update weekly avg
	print ('hourly averages',str(hourlyAverages),'daily averages:',str(dailyAverages),'weekly average:',str(weeklyAverages))
	getcryptoquotes(tradingcrypto)                                             #update the current prices
	print(lastmarkprice)
		#if currentprice is lower than averages _______________________________                              
	if lastmarkprice <= hourlyAverages[0]:                                    #
		print('using last mark price of' + str(lastmarkprice))                #
		return(lastmarkprice)                                                 #
	elif hourlyAverages[0] <= dailyAverages[0]:                               # choosing the lowest
		print('using hourly average of' + str(hourlyAverages[0]))             # between the last mark or
		return(hourlyAverages[0])                                             # the lowest local average
	else:                                                                     #
		#print('using daily average of' + str(dailyAverages[0]))               #
		#return(dailyAverages[0])#_______________________________________________
		
		hourlyAveragesum=hourlyAverages[0]+hourlyAverages[1] 
		hourlyAverage=round(hourlyAveragesum/2,6)
		print('using hourly average of ' + str(hourlyAverage))
		return(hourlyAverage)                                       
	'''
	These are a couple small comparators to get started. Uncomment to pick
	and use each one or just c+p into wherever it needs to be.
	
	#if local lowprice is higher than the broader highprice dont buy
	if hourlyAverages[0] > dailyAverages[1]:
		return(0)
	if dailyAverages[0] > weeklyAverages[1]:
		return(0)
	
	#if local highPrice is less than broader lowprice consider for buy	
	if hourlyAverages[1] < dailyAverages[0]:
		return(0)
	if dailyAverages[1] < weeklyAverages[0]:
		return(0)
	'''	
def calculateSellPrice():
	print('Calculating the sell price')
	hourlyAverages=averageHistoricalQuotes(tradingcrypto,'15second','hour')    #update hourly avg
	dailyAverages=averageHistoricalQuotes(tradingcrypto,'10minute','day')      #update daily avg
	weeklyAverages=averageHistoricalQuotes(tradingcrypto,'hour','week')        #update weekly avg
	getcryptoquotes(tradingcrypto)                                             #update the current prices
	buyometer=0 
	'''		#if currentprice is lower than averages
	if lastmarkprice <= hourlyAverages[0]:
		print('using last mark price')
		return(lastmarkprice)
	elif hourlyAverages[0] <= dailyAverages[0]:
		print('using hourly average')
		return(hourlyAverages[0])
	else:
		print('using daily average')
		return(dailyAverages[0])
	'''
	print('using daily high average of' + str(dailyAverages[1]))
	if actualbuyprice > round(float(dailyAverages[1])):
		return(actualbuyprice+minProfit)
	else:
		pricesum=actualbuyprice+float(dailyAverages[1])
		sellprice=pricesum/2
		return(round(sellprice,6))
def pennyProfit(pricePaid):
	sellPrice=pricePaid+ minProfit
	return(round(sellPrice,6))
def calculateMovingAvg(avg):
	adder=0.000000
	currentavg=0.000000
	#floater=1.000000
	#print(avg)
	print('total numbers being averaged together:'+ str(len(avg)))
	for item in range(0, len(avg)):
		#print(avg[item])
		adder=adder+float(avg[item])
	currentavg=adder/len(avg)
	return(round(currentavg,6))
		

def dailyHighLowsForMonth(cryptoSymbol,peak):
	interval='day'
	span='month'
	localHighs=[]
	localLows=[]
	
	history=r.get_crypto_historicals(cryptoSymbol,interval,span,'24_7')
	#format the product
	for x in range (0,len(history)):
		dataset=history[x]
		#printCryptoQuoteDataset(dataset)
		localLows.append(dataset['low_price'])
		localHighs.append(dataset['high_price'])
	if peak=='lows':
		return(localLows)
	elif peak =='highs':
		return(localHighs)
	else:
		print('peak not specified')

########tried and true fxns
######################MOVING AVERAGE AND HIGH/LOWS FOR SPANS
def yesterdaysHighLows(tradingcrypto): #index0 for high, index1 for low
	lastMonth=monthlyAvgs(tradingcrypto)
	lastMonthHighs=lastMonth[3]
	lastMonthLows=lastMonth[4]
	yesterdayHighLow=[]
	yesterdayIndexPosition=len(lastMonthHighs)-2
	#print(yesterdayIndexPosition)
	yesterdayHighLow.append(lastMonthHighs[yesterdayIndexPosition])
	yesterdayHighLow.append(lastMonthLows[yesterdayIndexPosition])
	return(yesterdayHighLow)
def halfhourcandlegenerator(dayCandlesList,daytimesStringList):
	halfhourcandles=[]
	for x in range(0,len(dayCandlesList)):
		testTimeoriginal=daytimesStringList[x]
		testTime=testTimeoriginal[14:]
		testTime=testTime[:-4]

		if testTime=='00' or testTime=='30':
			if x<=(len(dayCandlesList)-3):
				halfhouropen=dayCandlesList[x][1]
				halfhourclose=dayCandlesList[x+2][2]
				maxes=[dayCandlesList[x][0],dayCandlesList[x+1][0],dayCandlesList[x+2][0]]
				mins=[dayCandlesList[x][3],dayCandlesList[x+1][3],dayCandlesList[x+2][3]]
				halfhourcandle=[max(maxes),halfhouropen,halfhourclose,min(mins),testTimeoriginal]
				halfhourcandles.append(halfhourcandle)
	return(halfhourcandles)
def timeListGenerator(timeList):
	timeListstring=timeList[7]                          #timestamps pulled into string
	timeListstring=timeListstring[2:]                   #timestamps being edited
	timeListstring=timeListstring[:-2]                  #timestamps being edited
	timeListStringList=timeListstring.split("', '")     #splitting it into a list of string times
	return(timeListStringList)                                    #tada
def candleListGenerator(candleList):
	candlesString=candleList[8]                       #days candles into string
	candlesStringList=candlesString.split("<**>")    #split to individual string candles
	candlesList=[]                                   #empty list of final candles
	for x in range(0,len(candlesStringList)):        #turning string candles into list candles
		stringAtHand=candlesStringList[x]            #item up
		stringAtHand=stringAtHand[2:]                #edit item
		stringAtHand=stringAtHand[:-2]               #edit item
		candleprices=stringAtHand.split("', '")      #split candle to list of string prices
		candlesList.append(candleprices)             #add to list of final candles
	del candlesList[-1]                              #take off weird empty spot on end
	return(candlesList)


def average(list):
	total=0
	for x in range (0,len(list)):
		adder=float(list[x])
		total+=adder
	return(total/len(list))
def lastHourByMinute(cryptoSymbol,span,peak):
	history=r.get_crypto_historicals(cryptoSymbol,'15second',span,'24_7')
	#format the product
	localLows=[]
	localHighs=[]
	for x in range (0,len(history)):
		if x%4==0:
			dataset=history[x]
			#print(dataset['begins_at'])
			localLows.append(dataset['low_price'])
			localHighs.append(dataset['high_price'])
	
	if peak=='highs':
		return(localHighs)
	elif peak== 'lows':
		return(localLows)
	else:
		print('needs a peak specified')
def getHistoricalQuotes(cryptoSymbol,interval,span,peak): #gets quotes at specific interval per span and stores
	history=r.get_crypto_historicals(cryptoSymbol,interval,span,'24_7')
	#format the product
	localHighs=[]
	localLows=[]
	for x in range (0,len(history)):
		dataset=history[x]
		#printCryptoQuoteDataset(dataset)
		localLows.append(dataset['low_price'])
		localHighs.append(dataset['high_price'])
	if peak=='lows':
		return(localLows)
	elif peak =='highs':
		return(localHighs)
	else:
		print('peak not specified')	
	'''
	symbol (str) – The crypto ticker.
	interval (str) – The time between data points. Can be ’15second’, ‘5minute’, ‘10minute’, ‘hour’, ‘day’, or ‘week’. Default is ‘hour’.
	span (str) – The entire time frame to collect data points. Can be ‘hour’, ‘day’, ‘week’, ‘month’, ‘3month’, ‘year’, or ‘5year’. Default is ‘week’
	bound (str) – The times of day to collect data points. ‘Regular’ is 6 hours a day, ‘trading’ is 9 hours a day, ‘extended’ is 16 hours a day, ‘24_7’ is 24 hours a day. Default is ‘24_7’
	info (Optional[str]) – Will filter the results to have a list of the values that correspond to key that matches info.
	Returns:	
	[list] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

	Dictionary Keys:
	
	begins_at
	open_price
	close_price
	high_price
	low_price
	volume
	session
	interpolated
	symbol
	'''
	
	'''
	#all keys per datapoint per span
	print('Begins At: '+str(dataset['begins_at']))
	print('Open Price: '+str(dataset['open_price']))
	print('Close Price: '+str(dataset['close_price'])) 
	print('High Price: '+str(dataset['high_price']))
	print('Low Price: '+str(dataset['low_price']))
	print('Volume: '+str(dataset['volume']))
	print('Session: '+str(dataset['session']))
	print('Interpolated: '+str(dataset['interpolated']))
	print('Symbol: '+str(dataset['symbol']))
	print('')
	'''
def getcryptoquotes(tradingcrypto):            #gets current quotes and stores into 100 most recent value list
	mp=r.get_crypto_quote(tradingcrypto,'mark_price')
	ap=r.get_crypto_quote(tradingcrypto,'ask_price')
	bp=r.get_crypto_quote(tradingcrypto,'bid_price')
	prices = {'Ask':ap,'Mark':mp,'Bid':bp}
	return(prices)

def rsi(tradingcrypto,interval,span):
	#measure period of closes
	history=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7')
	closeprices=[]

	for x in range (0, len(history)):
		dataset=history[x]
		closeprices.append(dataset['close_price'])
	#measure differences between closes and globulate gains and losses
	gains=[]
	losses=[]
	nochange=[]
	for x in range(0,len(closeprices)-1):
		preresult=Decimal(float(closeprices[x]))-Decimal(float(closeprices[x+1]))
		result=round(preresult,6)
		if result<0:
			losses.append(result)
		elif result>0:
			gains.append(result)
		else:
			nochange.append(result)
	
	gaintotal=0
	losstotal=0
	#print('gains/losses amounts')
	#print(len(gains))
	#print(len(losses))
	for x in range(0,len(gains)-1):
		gaintotal=Decimal(float(gaintotal))+Decimal(float(gains[x]))
		
	for x in range(0,len(losses)-1):
		losstotal=Decimal(float(losstotal))+Decimal(float(losses[x]))
	#print('gain/loss totals')
	#print(round(gaintotal,6))
	#print(round(losstotal,6))
	#divide gains by periods and divide losses by periods
	gainstrength=Decimal(gaintotal)/len(closeprices)
	lossstrength=Decimal(abs(losstotal))/len(closeprices)
	#print('gain/loss strength')
	#print(round(gainstrength,6))
	#print(round(lossstrength,6))
	#divide gain/periods by loss/periods. this is the relative strength
	relativestrength=Decimal(gainstrength)/Decimal(lossstrength)
	#print('relative strength')
	#print(round(relativestrength,6))
	#RSI= 100-(100/(1+RS))
	rsi=100-(100/(1+Decimal(relativestrength)))
	return(rsi)
def standard14DayRSI(tradingcrypto):
	#measure period of closes
	history=r.get_crypto_historicals(tradingcrypto,'day','month','24_7')
	closeprices=[]

	for x in range (0, len(history)-16):
		dataset=history[x+15]
		closeprices.append(dataset['close_price'])
	#measure differences between closes and globulate gains and losses
	gains=[]
	losses=[]
	nochange=[]
	for x in range(0,len(closeprices)-1):
		preresult=Decimal(float(closeprices[x]))-Decimal(float(closeprices[x+1]))
		result=round(preresult,6)
		if result<0:
			losses.append(result)
		elif result>0:
			gains.append(result)
		else:
			nochange.append(result)
	
	gaintotal=0
	losstotal=0
	#print('gains/losses amounts')
	#print(len(gains))
	#print(len(losses))
	for x in range(0,len(gains)-1):
		gaintotal=Decimal(float(gaintotal))+Decimal(float(gains[x]))
		
	for x in range(0,len(losses)-1):
		losstotal=Decimal(float(losstotal))+Decimal(float(losses[x]))
	#print('gain/loss totals')
	#print(round(gaintotal,6))
	#print(round(losstotal,6))
	#divide gains by periods and divide losses by periods
	gainstrength=Decimal(gaintotal)/len(closeprices)
	lossstrength=Decimal(abs(losstotal))/len(closeprices)
	#print('gain/loss strength')
	#print(round(gainstrength,6))
	#print(round(lossstrength,6))
	#divide gain/periods by loss/periods. this is the relative strength
	relativestrength=Decimal(gainstrength)/Decimal(lossstrength)
	#print('relative strength')
	#print(round(relativestrength,6))
	#RSI= 100-(100/(1+RS))
	rsi=100-(100/(1+Decimal(relativestrength)))
	return(rsi)

def detectTrend():   ####needs verification
	print(hourlyAvgs[3])
	print(hourlyAvgs[4])
	markAvgs=[]
	hourlyhighs=hourlyAvgs[3]
	hourlylows=hourlyAvgs[4]
	for x in range(0,len(hourlyAvgs[3])):
		
		sum=Decimal(float(hourlyhighs[x]))+Decimal(float(hourlylows[x]))
		markavg=sum/2
		markAvgs.append(round(float(markavg),6))
	print(markAvgs)
	for x in range(0,len(markAvgs)-1):
		if float(markAvgs[x])>float(markAvgs[x+1]):
			print('falling')
		elif float(markAvgs[x])<float(markAvgs[x+1]):
			print('rising#################')
		else:
			print('nochange')
	hourlyChange=Decimal(float(markAvgs[0]))-Decimal(float(markAvgs[len(markAvgs)-1]))
	print(round(hourlyChange,6)*-1)
def detectConsecutiveChanges(integerPriceList):
	del integerPriceList[0]
	changelist=[]
	for x in range(0,len(integerPriceList)-1):
		
		change=int(integerPriceList[x])-int(integerPriceList[x+1])
		truechange=change*-1
		changelist.append(truechange)
	return(changelist)
def detectOverallChange(integerPriceList):
	del integerPriceList[0]
	changelist=[]
	for x in range(0,len(integerPriceList)-1):
		
		change=int(integerPriceList[0])-int(integerPriceList[x+1])
		truechange=change*-1
		changelist.append(truechange)
	return(changelist)
def detectBullishEngulfing(candleList,span,timeList):
	###VARIANT 1##############################################################################
	be=0
	for x in range(0,(len(candleList)-2)):
		candleA=candleList[x]
		candleB=candleList[x+1]
		candleADirection=''
		candleBDirection=''
		if float(candleA[1])>=float(candleA[2]):
			#candleA is bearish	
			if float(candleB[1])<=float(candleA[2]):
				#candleB opened equal or lower than candleA closed
				if float(candleB[2])>float(candleA[1]):
					#candleB closed higher than candleA opened
					be+=1
					#print('Historically, candle ',x+1,' presents bullish engulfing at ',timeList[x+1],' minus 3 hours')
	if candleList[-3][1]>candleList[-3][2]:         #if 3rd from last candles open is higher than its close	
		if candleList[-2][1]<=candleList[-3][2]:    #if 2nd from last candles open is less or equal to 3rd from lasts close		
			if candleList[-2][2]>candleList[-3][1]: #if 2nd from last candles close is higher than     3rd from lasts open
				#print('currently on a bullish trend. recommend a buy in at',time.localtime())
				engulfingNow=True
				print(engulfingNow,'at',span)
				return('NOW')
								
	if be>0:
		#print('bullish engulfing candles',span,':', be)
		return(True)
	else:
		#print('no cases of bullish engulfing located in this span:',span)
		return(False)
			
'''	
###VARIANT 2-FULL ENGULFING#########################################################
	null=False
	for x in range(0,(len(candleList)-2)):
		candleA=candleList[x]
		candleB=candleList[x+1]
		candleADirection=''
		candleBDirection=''
		if float(candleA[1])>=float(candleA[2]):
			#candleA is bearish	
			if float(candleB[1])<float(candleA[3]):
				#candleB opened lower than candleA min
				if float(candleB[2])>float(candleA[0]):
					#candleB closed higher than candleA max
					#print('Historically, candle ',x+1,' presents bullish engulfing at ',timeList[x+1],' minus 3 hours')
					null=True

		if candleList[-2][1]>candleList[-2][2]:         #if 3rd from last candles open is higher than its close	
			if candleList[-1][1]<candleList[-2][3]:     #if 2nd from last candles open is less than    3rd from lasts low		
				if candleList[-1][2]>candleList[-2][0]: #if 2nd from last candles close is higher than 3rd from lasts high
					#print('currently on a bullish trend. recommend a buy in at',time.localtime())
					if span=='hour':
						engulfingNow=True
	if null==True:
		return(True)
	#print('no cases of bullish engulfing located in this span:',span)
	return(False)
'''

def formatPriceList(cryptosymbol,pricelist):
	if cryptosymbol == 'DOGE':
		priceliststring=pricelist
		pricelistunpacker=priceliststring.split(',0.00')
		actualpriceList=pricelistunpacker[0]

		nofirst=actualpriceList[6:]
		nolast=nofirst[:-2]
		priceList=nolast.split("', '0.00")
		intPriceList=[]
		for x in range(0,len(priceList)):
			intPriceList.append(int(priceList[x]))

		return(intPriceList)
	else:
		priceliststring=pricelist
		priceliststring=priceliststring[2:]
		priceliststring=priceliststring[:-2]
		actualpriceList=priceliststring.split("', '")
		intpricelist=[]
		for x in actualpriceList:
			x=float(x)
			x="%.2f" % x
			x=str(x)
			x=x.replace('.','')
			x=int(x)
			intpricelist.append(x)
		return(intpricelist)
def formatSinglePrice(cryptosymbol,price):
	if cryptosymbol=='DOGE':
		price=int(price[4:])
		return(price)
	else:
		price=float(price)
		price="%.2f" %price
		price=int(price.replace('.',''))
		return(price)
		

def checkPriceFile(cryptosymbol,priceFile):
	pf=cryptosymbol+priceFile
	with open(pf, encoding="utf-8") as readPrices:
		intake=readPrices.read()
		fileString=""
		for x in intake:
			fileString=fileString+x
		
		fileList=fileString.split('<#>')
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
		return(fileList)
def writeToAnalysisFile(cryptosymbol,analysisList):
	with open(cryptosymbol+"situation.analysis", mode="w", encoding="utf-8") as analysis:
		for x in range (0, len(analysisList)):
			datapoint="".join([str(analysisList[x]),"<$?>"])
			analysis.write(datapoint)

for symbol in cryptoSymbols:
	pricefile=symbol+'situation.analysis'

	currentPrices=getcryptoquotes(symbol)
	currentAsk=currentPrices['Ask']
	currentMark=currentPrices['Mark']
	currentBid=currentPrices['Bid']
	#print(currentPrices)
	##############################################################################################################################
	hourPrices=checkPriceFile(symbol,'hourly.prices')
	hourPricesIntList=formatPriceList(symbol,hourPrices[3])
	hourPricesIntListLows=formatPriceList(symbol,hourPrices[4])
	hourConsecutiveChanges=detectConsecutiveChanges(hourPricesIntList)
	hourOverallChange=detectOverallChange(hourPricesIntList)
	houravg=hourPrices[2]                              #pulled true hour average
	houravgInt=formatSinglePrice(symbol,houravg)            #converted stringprice to int price
	hourdifference=(houravgInt-hourPricesIntList[0])*-1    #difference between start of set vs span avg
	hourldiff=(houravgInt-hourPricesIntList[-1])*-1        #difference between end   of set vs span avg
	hourTimeIntervalLabels=timeListGenerator(hourPrices) #list of time labels for hourprices
	hourCandles=candleListGenerator(hourPrices)          #list of candles for hourprices
	hourEngulfing=detectBullishEngulfing(hourCandles,'hour',hourTimeIntervalLabels)                 #detect bullish engulfing per interval/span
	avghourpricesInts=[]
	for x in range(0,len(hourPricesIntListLows)-2):
		hourpricesum=hourPricesIntList[x]+hourPricesIntListLows[x]
		hourpriceavg=hourpricesum/2
		avghourpricesInts.append(int(hourpriceavg))
	halfHourIndex=round(len(hourOverallChange)/2)
	fiveMinIndex=round(len(hourOverallChange)-(len(hourOverallChange)/12))
	currentMarkInt=formatSinglePrice(symbol,currentMark)
	halfhourChange=round(currentMarkInt-avghourpricesInts[halfHourIndex])
	fiveMinChange=round(currentMarkInt-avghourpricesInts[fiveMinIndex])
	#print(avghourpricesInts[fiveMinIndex])
	
	last5minIndex=len(hourCandles)-20
	totaler=0
	for x in range(last5minIndex-1,len(hourCandles)-1):
		candlesum=Decimal(hourCandles[x][1])+Decimal(hourCandles[x][2])
		candleavg=Decimal(candlesum)/Decimal(2)
		totaler=Decimal(totaler)+Decimal(candleavg)
		
	last5avg=str(Decimal(totaler)/Decimal(20))
	
	

	############################################################################################################################
	dayPrices=checkPriceFile(symbol,'daily.prices')
	dayPricesIntList=formatPriceList(symbol,dayPrices[3])
	dayConsecutiveChanges=detectConsecutiveChanges(dayPricesIntList)
	dayOverallChange=detectOverallChange(dayPricesIntList)
	dayavg=dayPrices[2]                              #pulled true day average
	dayavgInt=formatSinglePrice(symbol,dayavg)            #converted stringprice to int price
	daydifference=(dayavgInt-dayPricesIntList[0])*-1    #difference between start of set vs span avg
	dayldiff=(dayavgInt-dayPricesIntList[-1])*-1        #difference between end   of set vs span avg
	dayTimeIntervalLabels=timeListGenerator(dayPrices) #list of time labels for dayprices
	dayCandles=candleListGenerator(dayPrices)          #list of candles for dayprices
	dayEngulfing=detectBullishEngulfing(dayCandles,'10 minute day increments',dayTimeIntervalLabels)                 #detect bullish engulfing per interval/span
	##
	halfhourcandles=halfhourcandlegenerator(dayCandles,dayTimeIntervalLabels)#special list to fit robinhood graphs for debugging
	halfhourEngulfing=detectBullishEngulfing(halfhourcandles,'30 mins increments',dayTimeIntervalLabels)            #detect bullish engulfing per half hour to match with robinhood graph
	##
	###############################################################################################################################
	weekPrices=checkPriceFile(symbol,'weekly.prices')
	weekPricesIntList=formatPriceList(symbol,weekPrices[3])
	weekConsecutiveChanges=detectConsecutiveChanges(weekPricesIntList)
	weekOverallChange=detectOverallChange(weekPricesIntList)
	weekavg=weekPrices[2]                              #pulled true week average
	weekavgInt=formatSinglePrice(symbol,weekavg)            #converted stringprice to int price
	weekdifference=(weekavgInt-weekPricesIntList[0])*-1    #difference between start of set vs span avg
	weekldiff=(weekavgInt-weekPricesIntList[-1])*-1        #difference between end   of set vs span avg
	weekTimeIntervalLabels=timeListGenerator(weekPrices) #list of time labels for weekprices
	weekCandles=candleListGenerator(weekPrices)          #list of candles for weekprices
	weekEngulfing=detectBullishEngulfing(weekCandles,'week',weekTimeIntervalLabels)                 #detect bullish engulfing per interval/span

	################################################################################################################################

	monthPrices=checkPriceFile(symbol,'monthly.prices')
	monthPricesIntList=formatPriceList(symbol,monthPrices[3])
	monthConsecutiveChanges=detectConsecutiveChanges(monthPricesIntList)
	monthOverallChange=detectOverallChange(monthPricesIntList)
	monthavg=monthPrices[2]                              #pulled true month average
	monthavgInt=formatSinglePrice(symbol,monthavg)            #converted stringprice to int price
	monthdifference=(monthavgInt-monthPricesIntList[0])*-1    #difference between start of set vs span avg
	monthldiff=(monthavgInt-monthPricesIntList[-1])*-1        #difference between end   of set vs span avg
	monthTimeIntervalLabels=timeListGenerator(monthPrices) #list of time labels for monthprices
	monthCandles=candleListGenerator(monthPrices)          #list of candles for monthprices
	monthEngulfing=detectBullishEngulfing(monthCandles,'month',monthTimeIntervalLabels)                 #detect bullish engulfing per interval/span

	###########################################################################################################################
	print(engulfingNow)

	standardRSI=standard14DayRSI(symbol)
	standardRSI=round(float(standardRSI),2)
	#print('14 Day RSI', standardRSI)

	monthlyRSI=rsi(symbol,'day','month')
	monthlyRSI=round(float(monthlyRSI),2)
	#print('30 Day RSI', monthlyRSI)

	daysRSI=rsi(symbol,'5minute','day')
	daysRSI=round(float(daysRSI),2)
	#print('Last 24 RSI', daysRSI)
	#print('')
	overallChanges=[fiveMinChange,halfhourChange,hourOverallChange[-1],dayOverallChange[-1],weekOverallChange[-1],monthOverallChange[-1]]
	engulfments=[hourEngulfing,dayEngulfing,weekEngulfing,monthEngulfing,engulfingNow]
	rsiList=[daysRSI,standardRSI,monthlyRSI]
	averages=[last5avg,houravg,dayavg,weekavg,monthavg]
	
	print(engulfments[4])
	

	finalAnalysis=[]
	finalAnalysis.append(currentAsk)
	finalAnalysis.append(currentMark)
	finalAnalysis.append(currentBid)
	finalAnalysis.append(rsiList)
	finalAnalysis.append(engulfments)
	finalAnalysis.append(averages)
	finalAnalysis.append(overallChanges)
	print(finalAnalysis[3])

	writeToAnalysisFile(symbol,finalAnalysis)
	print(symbol+'price.analysis file updated')
