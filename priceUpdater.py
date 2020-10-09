import robin_stocks as r
import sys
import time

from decimal import*

login=r.login('your@email.com','password')


#tradingcrypto=str(sys.argv[1])
cryptoSymbols=['BTC','DOGE','ETC','LTC']

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
def spanAvgs(tradingcrypto,interval,span):
	intervalhigh=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7','high_price')
	intervallow=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7','low_price')   
	intervalopen=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7','open_price')
	intervalclose=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7','close_price')
	intervaltimes=r.get_crypto_historicals(tradingcrypto,interval,span,'24_7','begins_at')
	intervallowAverage=round(average(intervallow),6)                                           
	intervalhighAverage=round(average(intervalhigh),6)                                         
	intervalAvgs=[intervalhighAverage,intervallowAverage]                                            
	intervalAverage=round(average(intervalAvgs),6)                                                
	
	intervalLists=[]
	intervalLists.append(intervalhighAverage)                                        
	intervalLists.append(intervallowAverage)
	intervalLists.append(intervalAverage)
	intervalLists.append(intervalhigh)
	intervalLists.append(intervallow)
	intervalLists.append(intervalopen)
	intervalLists.append(intervalclose)
	intervalLists.append(intervaltimes)
	labels=['high','low','true','highs','lows','opens','closes','times']
	return(intervalLists)

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
	
	
	askavg.append(prices['Ask'])
	if len(askavg) >= 100:
		for x in range (0,(len(askavg)-100)):
			del askavg[0]
	
	markavg.append(prices['Mark'])
	if len(markavg) >= 100:
		for x in range (0,(len(markavg)-100)):
			del markavg[0]
	
	bidavg.append(prices['Bid'])
	if len(bidavg) >= 100:
		for x in range (0,(len(bidavg)-100)):
			del bidavg[0]
	
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

	for x in range (0, len(history)-15):
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
def makeCandleListString(spanPrices):
	candles=[]
	candleStringMaker=''
	divider=0
	for x in range (0,len(spanPrices[3])):             #high, low, open, or close
		divider+=1
		candle=[]
		candle.append(spanPrices[3][x]) #High
		candle.append(spanPrices[5][x]) #Open
		candle.append(spanPrices[6][x]) #Close
		candle.append(spanPrices[4][x]) #Low
		candles.append(candle)
		#if x%3==0:
		candleStringMaker+=(str(candle)+"<**>")
	return(candleStringMaker)

def updatePrices(cryptosymbol):
	with open(cryptosymbol+"hourly.prices", mode="w", encoding="utf-8") as hourlyPrices:
		for x in range (0, len(hourAvgs)):
			datapoint="".join([str(hourAvgs[x]),"<#>"])
			hourlyPrices.write(datapoint)
	with open(cryptosymbol+"daily.prices", mode="w", encoding="utf-8") as dailyPrices:
	
		for x in range (0, len(dayAvgs)):
			datapoint="".join([str(dayAvgs[x]),"<#>"])
			dailyPrices.write(datapoint)
	with open(cryptosymbol+"weekly.prices", mode="w", encoding="utf-8") as weeklyPrices:
		
		for x in range (0, len(weekAvgs)):
			datapoint="".join([str(weekAvgs[x]),"<#>"])
			weeklyPrices.write(datapoint)
	with open(cryptosymbol+"monthly.prices", mode="w", encoding="utf-8") as monthlyPrices:
		
		for x in range (0, len(monthAvgs)):
			datapoint="".join([str(monthAvgs[x]),"<#>"])
			monthlyPrices.write(datapoint)

'''
###########PRINTING PRICE AVERAGES
print('hourly high/low/true avgs')
hourAvgs=calculate60MinuteAvgs(tradingcrypto)
for x in range (0,3):
	print(hourAvgs[x])

print('daily high/low/true avgs')
dayAvgs=dailyAvgs(tradingcrypto)
for x in range (0,3):
	print(dayAvgs[x])

print('weekly high/low/true avgs')
weekAvgs=weeklyAvgs(tradingcrypto)
for x in range (0,3):
	print(weekAvgs[x])
print('monthly high/low/true avgs')
monthAvgs=monthlyAvgs(tradingcrypto)
for x in range (0,3):
	print(monthAvgs[x])
print('30 day RSI')
print(rsi(tradingcrypto,'day','month'))
print('14 day RSI')
print(standard14DayRSI(tradingcrypto))
print('current prices')
#print(getcryptoquotes(tradingcrypto))
'''

for x in cryptoSymbols:
	pricefile=x+'situation.analysis'
	hourAvgs=spanAvgs(x,'15second','hour')
	hourCandles=makeCandleListString(hourAvgs)
	hourAvgs.append(hourCandles)

	dayAvgs=spanAvgs(x,'10minute','day')
	dayCandles=makeCandleListString(dayAvgs)
	dayAvgs.append(dayCandles)

	weekAvgs=spanAvgs(x,'hour','week')
	weekCandles=makeCandleListString(weekAvgs)
	weekAvgs.append(weekCandles)

	monthAvgs=spanAvgs(x,'day','month')
	monthCandles=makeCandleListString(monthAvgs)
	monthAvgs.append(monthCandles)

	rsi30Day=rsi(x,'day','month')
	rsi14Day=standard14DayRSI(x)

	#currentprices=getcryptoquotes(x)

	updatePrices(x)
	print(x,'price files updated')

