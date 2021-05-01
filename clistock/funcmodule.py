import requests
import pandas as pd
import json
import sys
import datetime
import time
from datetime import datetime
from datetime import timedelta
import math
import plotille
import numpy as np

symbols = ['AAPL','GOOGL','TSLA']#,'ARAO','HALFF','LNC','SFTBY','HITD','AVD','LGAH','PCDAF','JNSTF','CRUUF','CKGDF','FCRD','PBSV','EEH','SEOTF','SWMD','SBBP',
				#'XXFPL','GBLHF','BBRYF','TRIT','LSTYF','ERGN','UCBJF','STLM','DRNA','CNWT','REGI','XRAY','BAJFF','LRSNF','SBCF','HPCRF','ITMSF','SMTOY','CIXPF','LTMAQ','FLIA','RYTTF',
				#'ULUR','CODX','FLY','NCB','SFBS','CBSU','BLPFF','SVLPF','WTBDY','CRZBF','DBV','BYLTF','BIEL','SWDHY','SOSSF','NSRCF','FBZ','FIRRY','NNMIF','VPTV','WOW','OPT','COBAF',
				#'SRRK','AGXKF','CRFQF','SMMD','RDDTF','CIB','CPS','NXTH','VDOMF','PSTV','EVSV','HGRVF','FPAFY','KEWL','OBTEF','CGUD','SVNNF','TXCCQ','HENOY','FINV','ERILF','XMVM','FMAT',
				#'EHITF','BCBHF','KBH','FNB','GYNAF','EMSWF','SMGBF','GYYMF','UNPA','ECUI','MLVF']
	

def my_function(args):
	stock_data = pd.DataFrame()
	fx_data = pd.DataFrame()
	anagraphic_data  = get_anagraphic_data(symbols)
	historical_data = get_historical_data(anagraphic_data)
	anagraphic_data_fx = get_anagraphic_exch()
	historical_data_fx = get_historical_data_fx(anagraphic_data_fx)
	
	if(args[0]=="crypto_symbols"):
		crypto_symbols()
	
	if(args[0]=="crypto"):
		crypto(args)
	
	if(args[0]=="weather"):
		weather()
	
	
	
	if(args[0] == "time_stock_graph"):
		if(len(args)<3):
			print("Not enough arguments inserted! Pleaes insert stock symbol and start date.", file = sys.stderr)
		elif(len(args) == 3):
			first = datetime.strptime(args[2], '%Y-%m-%d').timestamp()
			time_stock_graph(args[1],math.floor(first))
		elif(len(args) == 4):
			first = datetime.strptime(args[2], '%Y-%m-%d').timestamp()
			second = datetime.strptime(args[3], '%Y-%m-%d').timestamp()
			time_stock_graph(args[1],math.floor(first),math.floor(second))
	
	if(args[0] == "graph_hist_fx"):
		if(len(args)<2):
			print("Not enough arguments inserted!", file = sys.stderr)
		elif(len(args) == 2):
			for i in historical_data_fx:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			print_graph(stock_data)
	
	if(args[0] == "graph_hist_stock"):
		if(len(args)<2):
			print("Not enough arguments inserted!", file = sys.stderr)
		elif(len(args) == 2):			
			for i in historical_data:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			print_graph(stock_data)
		elif(len(args) == 3):			
			for i in historical_data:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			for i in historical_data_fx:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[2]):
					fx_data = i	
			print_graph(stock_data,fx_data)
	
	if(args[0] == "print_graph"):
		if(len(args)<2):
			print("Not enough arguments inserted!", file = sys.stderr)
		elif(len(args) == 2):			
			for i in historical_data:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			print_graph(stock_data)
		elif(len(args) == 3):			
			for i in historical_data:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			for i in historical_data_fx:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[2]):
					fx_data = i	
			print_graph(stock_data,fx_data)
	
	if(args[0] == "print_historical"):
		if(len(args)<2):
			print("Not enough arguments inserted!", file = sys.stderr)
		elif(len(args) == 2):			
			for i in historical_data:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			print_historical(stock_data)
		elif(len(args) == 3):			
			for i in historical_data:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[1]):
					stock_data = i
			for i in historical_data_fx:
				a=i.loc[0,['symbol']].to_list()
				if(a[0]==args[2]):
					fx_data = i	
			print_historical(stock_data,fx_data)

def get_anagraphic_data(symb = ['AAPL']):
	url = 'https://finnhub.io/api/v1/stock/symbol?exchange=US&token=c0dff3n48v6sgrj2il4g'
	anagraphic_data_all = requests.get(url)
	anagraphic_data = pd.DataFrame(anagraphic_data_all.json())
	anagraphic_data = anagraphic_data[anagraphic_data['symbol'].isin(symb)]
	return anagraphic_data
	
def get_historical_data(anag):
	symbs=anag.loc[:]['symbol'].to_list()
	historical_data = []
	time_now = round(time.time() * 1000)
	for i in range(len(symbs)):
		hist_temp = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol={s}&resolution=D&from=1572651390&to={t}&token=c0dff3n48v6sgrj2il4g'.format(s=symbs[i],t=time_now)).json())
		hist_temp["symbol"]=symbs[i]
		hist_temp['t'] = hist_temp['t'].map(lambda y: datetime.fromtimestamp(y).date())
		historical_data.append(hist_temp.loc[:,['symbol','c','t']])
	return historical_data
	
def get_anagraphic_exch():
	fx_rates = ['OANDA:AUD_USD','OANDA:EUR_USD','OANDA:GBP_USD']
	fx_anagraphic_all = requests.get('https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=c0dff3n48v6sgrj2il4g').json()
	fx_anagraphic_all = pd.DataFrame(fx_anagraphic_all)
	fx_anagraphic_data = fx_anagraphic_all.loc[fx_anagraphic_all['symbol'].isin(fx_rates)]
	return fx_anagraphic_data	

def get_historical_data_fx(anag):
	symbs=anag.loc[:]['symbol'].to_list()
	fx_historical_data =[]
	time_now = round(time.time() * 1000)	
	for i in range(len(symbs)):
		hist_temp = pd.DataFrame(requests.get('https://finnhub.io/api/v1/forex/candle?symbol={s}&resolution=D&from=1572651390&to={t}&token=c0dff3n48v6sgrj2il4g'.format(s=symbs[i],t=time_now)).json())
		hist_temp["symbol"]=symbs[i]
		hist_temp['t'] = hist_temp['t'].map(lambda y: datetime.fromtimestamp(y).date())
		fx_historical_data.append(hist_temp.loc[:,['symbol','c','t']])
	return fx_historical_data
	
def print_historical(hist_data,hist_data_fx):
	if(hist_data_fx.empty):
		sys.stdout.write(hist_data)
	else:
		stock_data = hist_data[hist_data['t'].isin(hist_data_fx.loc[:]['t'].to_list())]
		stock_data['c'] = stock_data['c']*hist_data_fx['c']
		sys.stdout.write(stock_data.to_string())

def print_graph(stock_data, fx_data= pd.DataFrame()):
	if(stock_data.empty):
		print("No data found for this stock. Please try with correct symbol", file = sys.stderr)
	else:	
		fig = plotille.Figure()
		fig.width = 60
		fig.height = 30
		fig.color_mode = 'byte'
		x = stock_data['c']
		y = stock_data['t']
		fig.plot(y,x,lc=200,label='plot')
		print(fig.show(legend=True))

def time_stock_graph(symb, first ,second = round(time.time() * 1000) ):
	stock_data = pd.DataFrame(requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={symb}&resolution=D&from={first}&to={second}&token=c0dff3n48v6sgrj2il4g').json())
	stock_data["symbol"]=symb
	stock_data['t'] = stock_data['t'].map(lambda y: datetime.fromtimestamp(y).date())
	stock_data = stock_data.loc[:,['symbol','c','t']]
	print_graph(stock_data)

def test():
	base_url = 'https://finnhub.io/api/v1/company-news?'
	r = requests.get(base_url, params = {'symbol': 'AAPL','token':'c0dff3n48v6sgrj2il4g', 'from':'2020-06-21', 'to':'2020-06-25'})
	text = r.text
	company_news = json.loads(text)
	print(company_news[0])

def crypto_symbols():
	url = 'https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=c0dff3n48v6sgrj2il4g'
	crypto_sym_all = requests.get(url)
	crypto_sym = pd.DataFrame(crypto_sym_all.json())
	print("befor writing to excel file")
	crypto_sym.to_excel("output.xlsx")
	print(datetime.fromtimestamp(1583098857).date())
	print(datetime.fromtimestamp(1584308457).date())
	

def crypto(args):
	symb=args[1]
	res=int(args[2])
	
	time_cont = 1
	if(res == 60):
		time_cont = 24
	elif(res == 30 ):
		time_cont = 48
	elif(res == 15):
		time_cont = 96
	elif(res == 5):
		time_cont = 192
	elif(res == 1):
		time_cont = 384
	else:
		time_cont =1
	
	beg_period = datetime.strptime(args[3], '%Y-%m-%d')
	ending = datetime.strptime(args[4], '%Y-%m-%d')
	indicator="&"
	count = 5
	while(count < len(args)):
		indicator = indicator + args[count] + "&"
		count= count+1
	print(indicator)
	print("below")
	days_diff = (ending-beg_period).days
	rec_count = days_diff * time_cont
	req_count = math.floor(rec_count / 500) +1
	
	crypto_all = pd.DataFrame()
	for i in range(req_count):
		end_period  = beg_period + timedelta(minutes = res*499)
		if(i == req_count -1 ):
			end_period  = ending
		start = math.floor(beg_period.timestamp())
		end = math.floor(end_period.timestamp())
		print(start)
		print(end)
		crypto_period = pd.DataFrame(requests.get('https://finnhub.io/api/v1/crypto/candle?symbol={s}&resolution={r}&from={f}{indic}&to={t}&token=c0dff3n48v6sgrj2il4g'.format(s=symb,r=res,f=start,t=end,indic = indicator)).json())
		crypto_period['t'] = crypto_period['t'].map(lambda y: datetime.fromtimestamp(y))
		crypto_all = pd.concat([crypto_all, crypto_period], ignore_index=True, sort=True)
		beg_period = end_period + timedelta(minutes = res)
	
	crypto_all.to_excel(str(str(symb) + ".xlsx").replace(":","_"))
	

def weather():
	#sdates = ['2015-01-01','2015-02-01','2015-03-01','2015-04-01','2015-05-01','2015-06-01','2015-07-01','2015-08-01','2015-09-01','2015-10-01','2015-11-01','2015-12-01','2016-01-01','2016-02-01','2016-03-01','2016-04-01','2016-05-01','2016-06-01','2016-07-01','2016-08-01','2016-09-01','2016-10-01','2016-11-01','2016-12-01']
	sdates = ['2017-01-01','2017-02-01','2017-03-01','2017-04-01','2017-05-01','2017-06-01','2017-07-01','2017-08-01','2017-09-01','2017-10-01','2017-11-01','2017-12-01','2018-01-01','2018-02-01','2018-03-01','2018-04-01','2018-05-01','2018-06-01','2018-07-01','2018-08-01','2018-09-01','2018-10-01','2018-11-01','2018-12-01']
	#edates = ['2015-01-31','2015-02-31','2015-03-31','2015-04-31','2015-05-31','2015-06-31','2015-07-31','2015-08-31','2015-09-31','2015-10-31','2015-11-31','2015-12-31','2016-01-31','2016-02-31','2016-03-31','2016-04-31','2016-05-31','2016-06-31','2016-07-31','2016-08-31','2016-09-31','2016-10-31','2016-11-31','2016-12-31']
	edates = ['2017-01-31','2017-02-31','2017-03-31','2017-04-31','2017-05-31','2017-06-31','2017-07-31','2017-08-31','2017-09-31','2017-10-31','2017-11-31','2017-12-31','2018-01-31','2018-02-31','2018-03-31','2018-04-31','2018-05-31','2018-06-31','2018-07-31','2018-08-31','2018-09-31','2018-10-31','2018-11-31','2018-12-31']
	weat_all = pd.DataFrame()
	print(len(sdates))
	#for i in range(len)
	for i in range(len(sdates)):
		weat = pd.DataFrame(requests.get('http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=870c3fd02c8848aeaf7213957212704&q=Bilbao&format=json&date={s}&enddate={e}&tp=1'.format(s=sdates[i],e=edates[i])).json())
		weat = weat.transpose()
		weat = pd.DataFrame(weat['weather'])
		weat = pd.DataFrame(weat.iloc[0]['weather'])
		weat =weat.loc[:,['date','hourly']]
		weat_all =pd.concat([weat_all, weat], ignore_index=True, sort=True)
		
	#weat = filter(lambda k: 'hourly' in k, weat)	
	weat_all.to_excel("weather.xlsx")
