#Andrew Sager
#8/10/2017
#TODO: Make command line interface so user doesn't need to edit anything in the file

import requests
from requests.auth import HTTPBasicAuth
import json
import csv

def open_and_parse_url(url): 
	headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'} #most recent headers Maropost requires for GET request
	sesh = requests.get(url, headers = headers)
	raw_json = sesh.text
	parsed_json = json.loads(raw_json)
	return parsed_json	

def write_csv(data, output_file):
	try:
		with open(output_file, 'w', newline = '', encoding = 'utf-8') as output:
			csv_writer = csv.writer(output, dialect = 'excel', quoting = csv.QUOTE_NONNUMERIC)
			for row in data:
				csv_writer.writerow(row)
	except IOError:
		print("IO Error") #if experiencing this throw, close Excel!
	return

def write_report(text, report_name): #mostly redundant to write_csv, used for debugging that process
	try:
		with open(report_name, 'w') as output:
			output.write(text)
	except IOError:
		print("IO Error")
	return


def get_campaign_ids(api_key, include_in_name = ""): #searches through all campaigns in Maropost
	#keys = ['account_id', 'contacts_count', 'sent_at', 'id'] #legacy from when writing an 'All Campaigns.csv file'
	campaign_key = 'id' #this is what we're really looking for
	campaign_ids = [] #we return this
	term = False #set to True if we reach the final page of campaigns
	page_number = 1
	while (not term):
		request = 'http://api.maropost.com/accounts/346/campaigns?auth_token={0}&page={1}'.format(api_key, page_number)
		parsed_json = open_and_parse_url(request) #load the page of campaigns
		if (len(parsed_json) == 0): #didn't get any data back, we found the final page
			term = True
		else:
			for item in parsed_json:
				if (include_in_name == "" or include_in_name in item['name']): #if passed "", signifies we want all campaigns
					campaign_ids.append(item[campaign_key]) 				   #otherwise, only grabs campaigns with certain string
					print(item['name']) #print the names of campaigns we're getting
			page_number += 1
	print(campaign_ids)
	return campaign_ids

def get_emails_sent(api_key, campaign_ids):
	debug_report = ""
	keys = ['contact_id','email','created_at']
	request = 'https://api.maropost.com/accounts/346/campaigns/{0}/delivered_report.json?auth_token={1}'
	sent_csv = []
	sent_csv.append(keys)
	for campaign_id in campaign_ids:
		debug_report += "Campaign _id: " + str(campaign_id)
		parsed_json = open_and_parse_url(request.format(campaign_id, api_key))
		for item in parsed_json:
			debug_report += str(item)
			sent_csv.append([item[keys[0]],item[keys[1]],item[keys[2]]])
		debug_report += "\n\n"
	write_csv(sent_csv, 'All Emails Sent.csv')
	write_report(debug_report, 'emails_sent_debugging_report.txt') #not very important, might be useful if issues arise with the JSON


def get_clicks(api_key, campaign_ids):
	debug_report = ""
	keys = ['contact_id','email','recorded_at']
	request = 'https://api.maropost.com/accounts/346/campaigns/{0}/click_report.json?auth_token={1}'
	clicks_csv = []
	clicks_csv.append(keys)
	for campaign_id in campaign_ids:
		debug_report += "Campaign _id: " + str(campaign_id)
		parsed_json = open_and_parse_url(request.format(campaign_id, api_key))
		for item in parsed_json:
			debug_report += str(item)
			clicks_csv.append([item[keys[0]],item[keys[1]],item[keys[2]]])
		debug_report += "\n\n"
	write_csv(clicks_csv, 'All Clicks.csv')
	write_report(debug_report, 'clicks_debugging_report.txt') #not very important, might be useful if issues arise with the JSON

def get_opens(api_key, campaign_ids):
	debug_report = ""
	keys = ['contact_id','email','recorded_at']
	request = 'https://api.maropost.com/accounts/346/campaigns/{0}/click_report.json?auth_token={1}'
	opens_csv = []
	opens_csv.append(keys)
	for campaign_id in campaign_ids:
		debug_report += "Campaign _id: " + str(campaign_id)
		parsed_json = open_and_parse_url(request.format(campaign_id, api_key))
		for item in parsed_json:
			debug_report += str(item)
			opens_csv.append([item[keys[0]],item[keys[1]],item[keys[2]]])
		debug_report += "\n\n"
	write_csv(opens_csv, 'All Opens.csv')
	write_report(debug_report, 'opens_debugging_report.txt') #not very important, might be useful if issues arise with the JSON

def get_bouncebacks(api_key, campaign_ids):
	debug_report = ""
	keys = ['contact_id','email','recorded_on']
	request = 'https://api.maropost.com/accounts/346/campaigns/{0}/bounce_report.json?auth_token={1}'
	bouncebacks_csv = []
	bouncebacks_csv.append(keys)
	for campaign_id in campaign_ids:
		debug_report += "Campaign _id: " + str(campaign_id)
		parsed_json = open_and_parse_url(request.format(campaign_id, api_key))
		for item in parsed_json:
			debug_report += str(item)
			bouncebacks_csv.append([item[keys[0]],item[keys[1]],item[keys[2]]])
		debug_report += "\n\n"
	write_csv(bouncebacks_csv, 'All Bouncebacks.csv')
	write_report(debug_report, 'bouncebacks_debugging_report.txt') #not very important, might be useful if issues arise with the JSON


def get_unsubscribes(api_key, campaign_ids):
	debug_report = ""
	keys = ['contact_id','email','recorded_on']
	request = 'https://api.maropost.com/accounts/346/campaigns/{0}/unsubscribe_report.json?auth_token={1}'
	unsubscribes_csv = []
	unsubscribes_csv.append(keys)
	for campaign_id in campaign_ids:
		debug_report += "Campaign id: " + str(campaign_id)
		parsed_json = open_and_parse_url(request.format(campaign_id, api_key))
		for item in parsed_json:
			debug_report += str(item)
			unsubscribes_csv.append([item[keys[0]], item[keys[1]], item[keys[2]]])
		debug_report += "\n\n"
	write_csv(unsubscribes_csv, 'All Unsubscribes.csv')
	write_report(debug_report, "unsubscribes_debugging_report.txt") #not very important, might be useful if issues arise with the JSON


api_key = 'INVALID,REPLACE'
include_in_campaign_name = "" #default is "", which finds all campaigns, otherwise string must be in campaign name
campaign_ids = get_campaign_ids(api_key, include_in_campaign_name) #search for all campaigns with a certain tag, dea

get_emails_sent(api_key, campaign_ids)
get_clicks(api_key, campaign_ids)
get_opens(api_key, campaign_ids)
get_bouncebacks(api_key, campaign_ids)
get_unsubscribes(api_key, campaign_ids)
print("All reports and debugging files have been written.")
