import json
import os
from flask import Flask
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy
import http.client

from flask import request, jsonify, abort, make_response



app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


from models import *

#####################################################################
# WEBHOOK ENTRY #
#####################################################################
@app.route('/resourcedetails/', methods=['POST'])
def resourcelists():
		req = request.get_json(silent=True, force=True)
		result = req.get("result")
		parameters = result.get("parameters")
		#print("Request:", json.dumps(req, indent=4))
		#print("Params : ", req.get("result").get("parameters"))
		
		## Get the parameters
		skillset = parameters.get("skillset")
		location = parameters.get("location")
		bench = parameters.get("bench")
		username = parameters.get("username")
		years = parameters.get("years")
		yearfilter = parameters.get("yearfilter")
		expfilter = parameters.get("expfilter")
		projectname = parameters.get("projectname")
		reportingmanager = parameters.get("reportingmanager")
		practices = parameters.get("practices")
		practicename = parameters.get("practicename")

		displayText = ""
		if username is not None :
			if expfilter is not None:
				displayText = get_experience(expfilter, username)
			else:
				displayText = get_user_email(username)
		elif practices is not None :
			displayText = get_practices()
		elif practicename is not None :
			displayText = get_practice_headcount(practicename)
		elif reportingmanager is not None:
			displayText = get_user_by_manager(reportingmanager)
		elif projectname is not None:
			displayText = get_user_based_on_project(projectname)
		else : 
			if years is None:
				displayText = get_resources(skillset, location, bench)
			else:
				displayText = get_resources_with_years(yearfilter, skillset, location, bench, years)


		return {
			"speech": displayText,
			"displayText": displayText,
            "source": "tekresourcebotheroku"
        }

#####################################################################
# Get user email #
#####################################################################
def get_user_email(username) :
	displayText = ""
	contactinfo = Resourcelist.get_contact(username.lower())
	print("CONTACT INFO : ", contactinfo)
	if contactinfo is None :
		displayText = "Sorry, I could not find that info"
	else :
		displayText = "The email address of " + username + " is " + contactinfo.email
	return displayText

#####################################################################
# Get resource details #
#####################################################################
def get_resources(skillset, location, bench) :
	displayText = ""
	bucketlists = Resourcelist.get_all(skillset, location, bench)
	results = []
	names = ""
	for bucketlist in bucketlists:
		names += bucketlist.name+ " (" + bucketlist.designation + ")" +", "

	names = names.rstrip(", ")
	print ("NAMES. : ", names)

	if names == "":
		displayText="No resources found"
	else:
		displayText = "The number of resources are " + str(bucketlists.count()) + " and their names are " + names
		return displayText

#####################################################################
# Get resource details with year filter #
#####################################################################
def get_resources_with_years(yearfilter, skillset, location, bench, years) : 
	yearfiltertext=""
	displayText = ""
	if yearfilter=="greater":
		yearfiltertext="greater than"
		reslists = Resourcelist.get_exp_greaterthan(skillset, location, bench, years)
		names = ""
		for reslist in reslists:
			names += reslist.name+" - " + str(round(reslist.tek_experience,2)) +" years, "

		names = names.rstrip(", ")
		print ("NAMES. : ", names)

	elif yearfilter=="less":
		yearfiltertext="less than"
		reslists = Resourcelist.get_exp_lessthan(skillset, location, bench, years)
		names = ""
		for reslist in reslists:
			names += reslist.name+" - " + str(round(reslist.tek_experience,2)) +" years, "

		names = names.rstrip(", ")
		print ("NAMES. : ", names)

	if names == "":
		displayText="No resources found"
	else:
		displayText = "The number of resources who have " + yearfiltertext + " " + str(years) + " years of tek experience are " + str(len(reslists)) + " and their names are " + names
	return displayText

#####################################################################
# Get experience #
#####################################################################
def get_experience(expfilter, username) :
	displayText = ""
	user = Resourcelist.get_user(username.lower())
	names = ""
	if(expfilter=="tek") :
		names += user.name+ " - " + str(round(user.tek_experience,2)) + " years of TEK experience"
	else :
		names += user.name+ " - " + str(round(user.total_experience,2)) + " years of total experience"

	if user is None:
		displayText="No resources found"
	else:
		displayText = names
		return displayText

#####################################################################
# Get user based on given project #
#####################################################################
def get_user_based_on_project(projectname):
	displayText = ""
	reslists = Resourcelist.get_user_based_on_project(projectname.lower())
	names = ""
	for reslist in reslists:
		names += reslist.name+", "

	names = names.rstrip(", ")
	print ("NAMES. : ", names)
	displayText = 'The resources working on ' + '"'+ projectname + '" project are ' + names
	return displayText

#####################################################################
# Get user by manager #
#####################################################################
def get_user_by_manager(reportingmanager):
	displayText = ""
	reslists = Resourcelist.get_user_by_manager(reportingmanager)
	names = ""
	for reslist in reslists:
		names += reslist.name+", "

	names = names.rstrip(", ")
	print ("NAMES. : ", names)
	displayText = 'The resources under ' + '"'+ reportingmanager + '" are ' + names
	return displayText

#####################################################################
# Get list of practices #
#####################################################################
def get_practices():
	displayText = ""
	reslists = Resourcelist.get_practices()
	
	names = ""
	for reslist in reslists:
		names += reslist['organization']+", "

	names = names.rstrip(", ")
	print ("NAMES. : ", names)
	displayText = 'Total number of practices are ' +  str(len(reslists)) +' and their names are ' + names
	return displayText

#####################################################################
# Get headcount of practice #
#####################################################################
def get_practice_headcount(practicename):
	displayText = ""
	headcount = Resourcelist.get_practice_headcount(practicename)
	print ("The headcount is ", headcount)
	
	displayText = 'Total headcount of ' + '"'+ practicename + '" is ' + headcount
	return displayText

#####################################################################
# DEFAULT API #
#####################################################################
@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

#####################################################################
# SFDC Bot API Middleware #
#####################################################################
@app.route('/sfdcwebhook/', methods=['POST'])
def sfdcwebhook():
	req = request.get_json(silent=True, force=True)
	result = req.get("result")
	parameters = result.get("parameters")
	print("Request:", json.dumps(req, indent=4))
	statusmsg=""
	#print("Params : ", req.get("result").get("parameters"))

	# Make a call to fetch access_token from SFDC
	conn = http.client.HTTPSConnection("tek-global-services-dev-ed.my.salesforce.com")
	headers = {
	    'content-type': "application/json",
	    'authorization': "Basic M01WRzlkOC4uei5oRGNQSlZvcWVKLlhvLjZlUS56RVpGaWNrR2t0eUh0Yi5SejNydnRPRlhBRGZzS3dmN0ZwMW5ITmR5UnhMMWhfc01kNmJ5Rjc2QzoxNjAzNzg0MDE4NzI0MzA4OTcx",
	    'cache-control': "no-cache",
	    }

	conn.request("POST", "/services/oauth2/token?grant_type=password&client_id=3MVG9d8..z.hDcPJVoqeJ.Xo.6eQ.zEZFickGktyHtb.Rz3rvtOFXADfsKwf7Fp1nHNdyRxL1h_sMd6byF76C&client_secret=1603784018724308971&username=nisha%40teksystems.com&password=Bot!2017YTNZ3eZafmtIIyY0JCS38HIoO", headers=headers)
	res = conn.getresponse()
	data = res.read()
	res_data = json.loads(data.decode("utf-8"))

	# Use the access token and post the original request to SFDC
	access_token = res_data.get("access_token")
	payload = req

	headers = {
	    'content-type': "application/json",
	    'authorization': "Bearer " + access_token,
	    'cache-control': "no-cache"
	    }

	conn.request("POST", "/services/apexrest/EnquiryFormcreateAPI/v1/register?access_token=", payload, headers)
	res = conn.getresponse()
	data = res.read()

	res_data = json.loads(data.decode("utf-8"))
	print(res_data)

	statusmsg = "An enquiry has been created on Salesforce.com and a Sales representative has been assigned to you! We will reach out to you shortly. Thanks for your time. Have a great day!",
	
	return {
		"speech": statusmsg,
		"displayText": statusmsg,
        "source": "sfdcbotheroku"
    }


if __name__ == '__main__':
    app.run()
