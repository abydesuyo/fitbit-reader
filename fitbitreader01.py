
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import kivy
# import wx
import dfgui

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.popup import Popup
# from kivy.uix.label import Label



class mainFrame(App):

	def build(self):
		layout = BoxLayout(orientation='vertical', padding=30)
		# fbobj = fitbitData()
		btnConnect = Button(text='Connect to Fitbit')
		btnConnect.bind(on_press=self.authFitBitConnection)
		# btn1.bind(on_press=self.testFunction)
		btnGetSleep = Button(text='Show Sleep Data')
		btnGetSleep.bind(on_press=self.getSleepData)
		btnGetHR = Button(text='Show HR Data')
		btnGetHR.bind(on_press=self.getHRData)
		# btn2.bind(on_press=fbobj.getSleepData)
		layout.add_widget(btnConnect)
		layout.add_widget(btnGetSleep)
		layout.add_widget(btnGetHR)
		return layout


	def authFitBitConnection(self, instance):
		# print('The button <%s> is being pressed' % instance.text)
		CLIENT_ID = '22BMFK'
		CLIENT_SECRET = '8750dfbe95041b1c60f2584fe975c2b2'	
		server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
		server.browser_authorize()
		ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
		REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
		self.auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
		self.yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
		self.yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
		self.today = str(datetime.datetime.now().strftime("%Y%m%d"))


	def getSleepData(self, instance):
		fit_statsSl = self.auth2_client.sleep(date='today')
		stime_list = []
		sval_list = []
		for i in fit_statsSl['sleep'][0]['minuteData']:
		    stime_list.append(i['dateTime'])
		    sval_list.append(i['value'])
		sleepdf = pd.DataFrame({'State':sval_list, 'Time':stime_list})
		sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
		dfgui.show(sleepdf)
		# for index, row in sleepdf.iterrows():
		# 	print(index, row)
		# print (sleepdf['Interpreted'])


	def getHRData(self, instance):

		fit_statsHR = self.auth2_client.intraday_time_series('activities/heart', base_date='today', detail_level='1sec')
		time_list = []
		val_list = []
		# for x in fit_statsHR.keys():
		# 	for y in fit_statsHR[x]:
		# 		print(y.keys())
		# print(fit_statsHR.keys())
		# print(fit_statsHR['activities-heart-intraday'])
		for item in fit_statsHR['activities-heart-intraday']['dataset']:
		    val_list.append(item['value'])
		    time_list.append(item['time'])
		    # print (val_list)
		    # print(time_list)
		    # print(item)
		heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})
		dfgui.show(heartdf)

	# def popupBox(self, instance):
	# 	popup = Popup(title='Test popup', content=Label(text='Hello world'), size_hint=(None, None), size=(400, 400))
	# 	popup = Popup(title='Test popup', content=Label(text='Hello world'), auto_dismiss=False)
	# 	popup.open()

	def testFunction(self,instance):
		print ("Helooo Button")


if __name__ == "__main__":
    app = mainFrame()
    app.run()




# yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
# print(sleepdf)