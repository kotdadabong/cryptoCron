import robin_stocks as r
import sys
from decimal import *

#tradingcrypto=str(sys.argv[1])


login=r.login('your@email.com','password')

currentOrders=[]

'''
def getTradingCryptoPosition(tradingcrypto):
	position=r.get_crypto_positions()
	tradingposition=[]
	for x in range (0,len(position)):
		details=position[x]
		costbasislist=details['cost_bases']
		costbasis=costbasislist[0]
		currency=details['currency']
		if currency['code']==tradingcrypto:
			tradingposition.append(currency['code'])
			tradingposition.append(details['quantity_available'])
			tradingposition.append(details['quantity_held_for_sell'])
			if float(details['quantity_available'])>0 or float(details['quantity_held_for_sell'])>0:
				preavgprice=Decimal(float(costbasis['direct_cost_basis']))/Decimal(float(costbasis['direct_quantity']))
				avgprice=round(float(preavgprice),6)
				tradingposition.append(avgprice)
			else:
				tradingposition.append(0.00)
			
		
	return(tradingposition)		
'''
def getAllCryptoPositions():
	positions=r.get_crypto_positions()
	cryptopositions=[]
	for x in range (0,len(positions)):
		details=positions[x]
		costbasislist=details['cost_bases']
		costbasis=costbasislist[0]
		currency=details['currency']
		cryptoposition=[]
		cryptoposition.append(currency['code'])
		cryptoposition.append(details['quantity_available'])
		cryptoposition.append(details['quantity_held_for_sell'])
		cryptoposition.append(details['quantity_held_for_buy'])
		if float(details['quantity_available'])>0 or float(details['quantity_held_for_sell'])>0:
			preavgprice=Decimal(float(costbasis['direct_cost_basis']))/Decimal(float(costbasis['direct_quantity']))
			avgprice=round(float(preavgprice),6)
			cryptoposition.append(str(avgprice))
		else:
			cryptoposition.append(str(0.00))
		
		cryptopositions.append(cryptoposition)
		
	return(cryptopositions)		
def getBuyingPower():
	return(float(r.load_account_profile('buying_power')))
def getCryptoOrder():
	orders=r.orders.get_all_open_crypto_orders()
	if len(orders)>1:
		for x in orders:
			y=[]
			y.append(x)
		#print(orders)
		return(y)
	elif len(orders)>0 and len(orders)<2:
		return(orders[0])
	else:
		return('no open orders')
def writeToAnalysisFile(analysisList):
	with open("profile.analysis", mode="w", encoding="utf-8") as analysis:
		for x in range (0, len(analysisList)):
			datapoint="".join([str(analysisList[x]),"<$?>"])
			analysis.write(datapoint)

buyingpower=getBuyingPower()
#tradingCryptoPosition=getTradingCryptoPosition(tradingcrypto)
allCryptoPositions=getAllCryptoPositions()
openOrders=getCryptoOrder()

profileAnalysis=[]
profileAnalysis.append(buyingpower)
profileAnalysis.append(allCryptoPositions)
profileAnalysis.append(openOrders)

writeToAnalysisFile(profileAnalysis)

print('profile.analysis file updated')
