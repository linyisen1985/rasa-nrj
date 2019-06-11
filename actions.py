# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []
import requests
import json
import os
import re
import datetime
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from pymongo import MongoClient
		
#WITHOUTEID = "sorry, we can't provide you service without valid eid"

#class ActionVM(Action):
#	def name(self):
#		return "action_vm"
#
#	def run(self, dispatcher, tracker, domain):
#		if tracker.get_slot('eid') is None:
#			return [dispatcher.utter_template("utter_ask_eid", tracker)]
#		vmaction = ['os','vcpu','mem','disk','other','confirm']
#		cur = 0
#		for vma in vmaction:
#			if not tracker.get_slot('vm_asked_'+vma):
#				res = tracker.latest_message['text']
#				tmpslot = getSlot(vma,res)
#				#dispatcher.utter_message(tmpslot)
#				#dispatcher.utter_message(domain['slots']['vm_'+vma]['values'])
#				if tmpslot != 'none':
#					if ((vma == 'vcpu' or vma == 'disk') and (tmpslot not in domain['slots']['vm_'+vma]['values'])):
#						tmpslot == 'none'
#					if ((vma == 'mem' or vma == 'disk') and (tmpslot < domain['slots']['vm_'+vma]['min_value'] or tmpslot > domain['slots']['vm_'+vma]['max_value'])):
#						tmpslot == 'none'
#				if tmpslot == 'none':
#					dispatcher.utter_message("please type valid word:\nos in 'CentOSX,UbuntuX and WindowsX'\nvcpu in '1,2,4,8,16'\nmemory between 1 and 40\ndisk between 50 and 40960\nconfirm is 'yes' or 'no'")
#					return [dispatcher.utter_template("utter_ask_vm_"+vma, tracker)]
#				
#				#dispatcher.utter_message(cur)
#				#dispatcher.utter_message(len(vmaction))
#				if cur+1>=len(vmaction):
#					if tracker.get_slot('vm_confirm') == 'yes':
#						ActionEmail.run(self, dispatcher, tracker, domain)
#					else:
#						return [SlotSet("vm_os", None),
#						SlotSet("vm_confirm", None),
#						SlotSet("vm_disk", None),
#						SlotSet("vm_mem", None),
#						SlotSet("vm_other", None),
#						SlotSet("vm_vcpu", None),
#						SlotSet("vm_asked_os", None),
#						SlotSet("vm_asked_vcpu", None),
#						SlotSet("vm_asked_disk", None),
#						SlotSet("vm_asked_other", None),
#						dispatcher.utter_template("utter_ask_os", tracker)]
#				else:
#					cur+=1
#					nextvma = vmaction[cur]
#					dispatcher.utter_message(nextvma)
#					dispatcher.utter_template("utter_ask_vm_"+nextvma, tracker)
#					return [SlotSet('vm_asked_'+vma,True),SlotSet('vm_'+vma,tmpslot)]
#		return []

#class ActionVMother(Action):
#	def name(self):
#		return "action_vm_other"
#
#	def run(self, dispatcher, tracker, domain):
#		msg = tracker.latest_message['text']
#		#tracker.slots['name'] = dis
#		#dispatcher.utter_message(dis)  # send the message back to the user
#		#dispatcher.utter_template("utter_ask_vm_confirm", tracker)
#		return [SlotSet("vm_other", msg if msg is not None else [])]
#class ActionEid(Action):
#	def name(self):
#		return "action_eid"
#
#	def run(self, dispatcher, tracker, domain):
#		eid = tracker.get_slot('eid')
#		request = requests.get('http://tools.ao.ericsson.se/ptm/rnea/getECDData?corpId='+eid).json()  # make an api call
#		dis = request['displayName']  # extract a display from returned json response
#		#dispatcher.utter_template("utter_greet", tracker)
#		return [SlotSet("name", dis if dis is not None else [])]
#WITHOUTEID = "sorry, we can't provide you service without valid eid"
class ActionEid(Action):
	def name(self):
		return "action_eid"

	def run(self, dispatcher, tracker, domain):
		
		if tracker.get_slot('eid'):
			eid = tracker.get_slot('eid')
		else:
			eid = tracker.latest_message['text']
			eid = eidFilter(eid)
		if eid != 'none':
			request = requests.get('http://tools.ao.ericsson.se/ptm/rnea/getECDData?corpId='+eid).json()  # make an api call
			dis = request['displayName']  # extract a display from returned json response
			#dispatcher.utter_message(dis)
			#dispatcher.utter_template("utter_greet", tracker)
			
			return [SlotSet("name", dis if dis is not None else []),dispatcher.utter_template("utter_greet", tracker,name=dis)]
		else:
			dispatcher.utter_message("sorry, we can't provide you service without valid eid")
			return [dispatcher.utter_template("utter_ask_eid", tracker)]

		
#class ActionEmail(Action):
#	def name(self):
#		return "action_email"
#
#	def run(self, dispatcher, tracker, domain):
#		content = "Request from "+tracker.get_slot('name')+"("+tracker.get_slot('eid')+"):\n"
#		content += "CentOS: "+tracker.get_slot('vm_os')+"\n"
#		content += "vCPU: "+tracker.get_slot('vm_vcpu')+"\n"
#		content += "Memory: "+tracker.get_slot('vm_memory')+" M\n"
#		content += "Disk: "+tracker.get_slot('vm_disk')+" G\n"
#		content += "Other: "+tracker.get_slot('vm_other')+" G\n"
#        #content = 'test'
#		conn = MongoClient('146.11.85.168', 20000)
#		db = conn.rasa
#		request = db.request
#		dateStr = datetime.datetime.now()
#		request.insert({
#			"resid":tracker.sender_id,
#			"requestor":tracker.get_slot('eid'),
#			"status":"open",
#			"res":content,
#			"resdate":dateStr,
#			"lastupdate":dateStr
#			})
#		conn.close()
#	
#		dispatcher.utter_template("utter_email_confirm", tracker)  # send the message back to the user
#		return [dispatcher.utter_message('your request id is '+tracker.sender_id)]

#if __name__ == '__main__':
#    Action.run();

def eidFilter(msg):
	rlt = 'none'
	searchObj = re.search(r'[a-zA-Z]{7}',msg,re.M|re.I)
	if searchObj:
		rlt = searchObj.group()
	return rlt

#def getSlot(vma,res):
#	rlt = "none"
#	if vma == 'os':
#		searchObj = re.search(r'(centos\s?\d)|(ubuntu\s?\d{2})|(windows\s?\w{1,6})',res,re.M|re.I)
#		if searchObj:
#			rlt = searchObj.group()
#	elif vma == 'vcpu':
#		searchObj = re.search(r'\d{1,2}',res,re.M|re.I)
#		if searchObj:
#			rlt = searchObj.group()
#	elif vma == 'mem':
#		searchObj = re.search(r'\d{1,2}',res,re.M|re.I)
#		if searchObj:
#			rlt = searchObj.group()
#	elif vma == 'mem':
#		searchObj = re.search(r'\d{2,5}',res,re.M|re.I)
#		if searchObj:
#			rlt = searchObj.group()
#	elif vma == 'other':
#		rlt = res
#	elif vma == 'confirm': 
#		searchObj = re.search(r'yes|no.',res,re.M|re.I)
#		if searchObj:
#			rlt = searchObj.group()
#	return rlt