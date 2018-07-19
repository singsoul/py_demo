import requests
import json
import pandas as pd
import datetime
import time
burp0_cookies = {"_abtest_userid": "e1a3dd65-a0b2-47ef-836c-a4abe7acaa32", 
"_bfa": "1.1523348937463.3q1ygg.1.1523692918963.1523851107974.6.10", 
"_RF1": "36.27.55.194", "_RSG": "1Z4gRojpAIEw15JltYtbY8", "_RDG": "288bca7b096f6d22e418d93e9af6ab9e5d",
 "_RGUID": "e48acedc-9ba8-48c1-88a5-de2def4c507a", "__zpspc": "9.6.1523851129.1523851274.2%234%7C%7C%7C%7C%7C%23",
  "_jzqco": "%7C%7C%7C%7C1523851129902%7C1.2036090304.1523348943464.1523851129743.1523851274792.1523851129743.1523851274792.undefined.0.0.9.9", "_ga": "GA1.2.469993046.1523348945"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
 "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
  "Accept-Encoding": "gzip, deflate", 
  "Referer": "http://flights.ctrip.com/domestic/Search/FirstRoute/?dcity1=BJS&acity1=SHA&ddate1=2018-07-20&searchtype=S", "Connection": "close"}

class xiecheng():
	def __init__(self):
		self.main_url = "http://flights.ctrip.com:80/domesticsearch/search/SearchFirstRouteFlights?DCity1=BJS&ACity1=SHA&SearchType=S&DDate1={}&LogToken=93e9b40cf9654c49a217a8eb5d659750&CK=61C3A1C025F83C9D68F5D5EF814F3C3A"
		self.mylist = []


	def start(self):
		now = datetime.datetime.now()
		for i in range(0,3):
			delta = datetime.timedelta(days=i)
			n_days = now + delta
			self.getContent(self.main_url.format(n_days.strftime('%Y-%m-%d')))
			time.sleep(4)
		df = pd.DataFrame(self.mylist)
		# df.rename(columns=datacol,inplace=True)
		df.to_csv('demo.csv')


	def getContent(self,urls):
		print(urls)
		resp = requests.get(urls, headers=burp0_headers, cookies=burp0_cookies)
		print(resp.text)
		if resp:
			myjson = json.loads(resp.text)
			fis = myjson['fis']
			for fj in fis:
				hb = fj['fn']
				splace = fj['dpbn']
				eplace = fj['apbn']
				stime = fj['dt']
				etime = fj['at']
				iszf = fj['sts']
				list1= [hb,splace,eplace,stime,etime]
				print(list1)
				if iszf:
					list1.append('不是直飞')
				else:
					list1.append('直飞')
				for place in fj['scs']:
					# zk = place['rt']
					# if place['c'] == 'Y': #Y:经济舱 C:公务舱 F:头等舱
					# 	list1.append(f'经济舱{zk}')
					# elif place['c'] == 'C':
					# 	list1.append(f'公务舱{zk}')
					# elif place['c'] == 'F':
					# 	list1.append(f'头等舱{zk}')
					types = {'Y':'经济舱','C':'公务舱','F':'头等舱'}
					salep = place['salep']
					tp = place['tgq']['rfn']
					gq = place['tgq']['rrn']
					fj_str = str(types[place['c']]) + str(place['rt']) + " " + str(salep) + '\n' + str(tp) + '\n' + str(gq)
					list1.append(fj_str)

				self.mylist.append(list1)



if __name__ == '__main__':
	xiecheng().start()

# with open('a.txt','r',encoding='utf-8') as f:
# 	aaa = f.read()

# myjson = json.loads(aaa)
# mylist = []
# fis = myjson['fis']
# for fj in fis:
# 	hb = fj['fn']
# 	splace = fj['dpbn']
# 	eplace = fj['apbn']
# 	stime = fj['dt']
# 	etime = fj['at']
# 	iszf = fj['sts']
# 	list1= [hb,splace,eplace,stime,etime]
# 	if iszf:
# 		list1.append('不是直飞')
# 	else:
# 		list1.append('直飞')
# 	for place in fj['scs']:
# 		# zk = place['rt']
# 		# if place['c'] == 'Y': #Y:经济舱 C:公务舱 F:头等舱
# 		# 	list1.append(f'经济舱{zk}')
# 		# elif place['c'] == 'C':
# 		# 	list1.append(f'公务舱{zk}')
# 		# elif place['c'] == 'F':
# 		# 	list1.append(f'头等舱{zk}')
# 		types = {'Y':'经济舱','C':'公务舱','F':'头等舱'}
# 		salep = place['salep']
# 		tp = place['tgq']['rfn']
# 		gq = place['tgq']['rrn']
# 		fj_str = types[place['c']] + place['rt'] + " " + str(salep) + '\n' + tp + '\n' + gq
# 		list1.append(fj_str)

# 	mylist.append(list1)
# df = pd.DataFrame(mylist)
# # df.rename(columns=datacol,inplace=True)
# df.to_csv('demo.csv')


