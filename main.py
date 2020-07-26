from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout 

import hltv_api as hltv 
import math

def calc_cof(team1, team2):
	#team1 = input("Введите команду №1\n")
	#team2 = input("Введите команду №2\n")
	team_dict = hltv.get_teams()
	team1_id = team_dict[team1]
	team2_id = team_dict[team2]
	cof_team1 = 0 
	cof_team2 = 0
	rank_team1 = 0
	rank_team2 = 0
	history_team1 = hltv.get_results(team1_id)
	history_team2 = hltv.get_results(team2_id)
	top30teams = hltv.top30teams()

	for i in range(len(top30teams)):
		if team1 in top30teams[i]["name"]:
		    rank_team1 = top30teams[i]["rank-points"]
		if team2 in top30teams[i]["name"]:
		    rank_team2 = top30teams[i]["rank-points"]
	if (rank_team1 == 0): rank_team1 = 100
	if (rank_team2 == 0): rank_team2 = 100 

	for i in range(len(history_team1)):
	    if (history_team1[i]["team1score"] > history_team1[i]["team2score"] and history_team1[i]["team1"] == team1) or (history_team1[i]["team1score"] < history_team1[i]["team2score"] and history_team1[i]["team2"] == team1):
	        cof_team1 += 1000 - i 
	    else:
	        cof_team1 -= 500 - i 
	    if (history_team1[i]["team1"] == team1 and history_team1[i]["team2"] == team2 ):
	    	if (history_team1[i]["team1score"] > history_team1[i]["team2score"]):
	    		cof_team1 += 1000
	    	else:
	    		cof_team2 += 1000
	        
	for i in range(len(history_team2)):
	    if (history_team2[i]["team1score"] > history_team2[i]["team2score"] and history_team2[i]["team1"] == team2) or (history_team2[i]["team1score"] < history_team2[i]["team2score"] and history_team2[i]["team2"] == team2):
	        cof_team2 += 1000 - i 
	    else:
	        cof_team2 -= 500 - i 
	    if (history_team2[i]["team1"] == team1 and history_team2[i]["team2"] == team2 ):
	    	if (history_team2[i]["team1score"] > history_team2[i]["team2score"]):
	    		cof_team1 += 1000
	    	else:
	    		cof_team2 += 1000
	#result = (1/cof_team1) * 1000
	result = cof_team1 / (cof_team1 + cof_team2) * 100
	#print("Процент победы первой команды - " + str(result) + " %")
	message = "\n Процент победы первой команды - " + str(result) + " %"
	if result > 50:
		message +="\n Если коэффициент на команду №1 больше "+ str(round(100/result,2)) + " можно ставить бабкину пенсию"
	return (message)

class BetsApp(App):

	def add_team(self,instance):
		if ("№2" in self.lbl.text) or (self.lbl.text == ""):
			self.lbl.text = " Команда №1 - " + instance.text
			self.t1 = instance.text
		elif "№1" in self.lbl.text:
			self.lbl.text += "\n Команда №2 - " + instance.text
			self.t2 = instance.text
			self.lbl.text += calc_cof(self.t1, self.t2)
		else: 
			self.lbl.text = ""

	def build(self):

		self.t1 = ""
		self.t2 = ""
		team_dict = hltv.get_teams()
		sorted_teams = []

		for i in team_dict.keys():
			sorted_teams.append(i)
		sorted_teams.sort()

		boxl = BoxLayout(orientation = "vertical")
		self.lbl = Label(size_hint = (1 , .20))
		boxl.add_widget(self.lbl)

		grydl = GridLayout(cols = 18)
		for i in sorted_teams:
			grydl.add_widget(Button(text = i, font_size = 12, on_press = self.add_team))

		boxl.add_widget(grydl)

		return boxl 


if __name__ == "__main__":
	BetsApp().run()