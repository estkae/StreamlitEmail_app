# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc

# EDA Pkgs
import pandas as pd
import neattext.functions as nfx

# Utils
import base64
import time
# -*- coding: utf-8 -*-
import scrapy
import re
from tld import get_tld
from scrapy.crawler import CrawlerProcess

import os
timestr = time.strftime("%Y%m%d-%H%M%S")
import requests
from Linkedin_project_Part_5 import scrape
# from gather_details import startparse
# from contact_details/contact_details/spiders/gather_details import GatherDetailsSpider

# Fxn to Download
def make_downloadable(data,task_type):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download Results File ** ")
    new_filename = "extracted_{}_result_{}.csv".format(task_type,timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)

# Fxn to Download
def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download CSV File ** ")
    new_filename = "extracted_data_result_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Fxn to Fetch Result
@st.cache
def fetch_query(query):
	base_url = "https://www.google.com/search?q={}".format(query)
	r = requests.get(base_url)
	return r.text


# Beautification

custom_title = """
<div style="font-size:60px;font-weight:bolder;background-color:#fff;padding:10px;
border-radius:10px;border:5px solid #464e5f;text-align:center;">
		<span style='color:blue'>E</span>
		<span style='color:black'>m</span>
		<span style='color:red'>a</span>
		<span style='color:green'>i</span>
		<span style='color:purple'>l</span>

		<span style='color:blue'>E</span>
		<span style='color:red'>x</span>
		<span style='color:yellow'>t</span>
		<span style='color:#464e5f'>r</span>
		<span style='color:red'>a</span>
		<span style='color:green'>c</span>
		<span style='color:yellow'>t</span>
		<span style='color:black'>o</span>
		<span style='color:blue'>r</span>

</div>
"""

# DB Management
import sqlite3
conn = sqlite3.connect('emails_data.db')


def main():
	"""Email Extraction Streamlit App"""
	# class GatherDetailsSpider (scrapy.Spider):
	# 	name = 'gather_details'
	# 	greedy = True
	# 	domain = ''
	# 	# custom_settings = {'DOWNLOD_DELAY': 1}
	# 	email_regex = re.compile (r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
	# 	forbidden_keys = ['tel:' , 'mailto:' , '.jpg' , '.pdf' , '.png']
	# 	allowed_domains = [f'{domain}']
	# 	start_urls = [f'https://{domain}']
	#
	# 	# def __init__(self , domain):
	# 	#     print ("init")
	# 	#     self.allowed_domains = [f'{domain}']
	# 	#     self.start_urls = [f'https://{domain}']
	# 	#     super ().__init__
	#
	# 	def parse(self , response):
	# 		try:
	# 			html = response.body.decode ('utf-8')
	# 		except UnicodeDecodeError:
	# 			return
	# 		emails = []
	# 		phones = []
	# 		print ("parse")
	# 		# Find mailto's
	# 		mailtos = response.xpath ("//a[starts-with(@href, 'mailto')]/@href").getall ()
	# 		tels = response.xpath ("//a[starts-with(@href, 'tel:')]/@href").getall ()
	# 		phones += [tel.replace ("tel:" , "") for tel in tels]
	# 		emails = [mail.replace ('mailto:' , '') for mail in mailtos]
	# 		body_emails = self.email_regex.findall (html)
	# 		emails += [email for email in body_emails if \
	# 				   get_tld ('https://' + email.split ('@')[-1] , fail_silently=True)]
	# 		yield {
	# 			'emails': list (set (emails)) ,
	# 			'phones': list (set (phones)) ,
	# 			'page': response.request.url
	# 		}
	# 		if self.greedy:
	# 			links = response.xpath ("//a/@href").getall ()
	# 			# If there are external links, scrapy will block them
	# 			# because of the allowed_domains setting
	# 			for link in links:
	# 				skip = False
	# 				for key in self.forbidden_keys:
	# 					if key in link:
	# 						skip = True
	# 						break
	# 				if skip:
	# 					continue
	# 				try:
	# 					yield scrapy.Request (link , callback=self.parse)
	# 				except ValueError:
	# 					try:
	# 						yield response.follow (link , callback=self.parse)
	# 					except:
	# 						pass

	st.title("Email Extractor App")
	# custom_banner  = """<div>
	# <span style="color:red;font-size:30px">E</span>
	# <span style="color:blue;font-size:30px">M</span>
	# """
	stc.html(custom_title)

	menu = ["Home","Contact Detail","Linkedin Extractor","Single Extractor","Bulk Extractor","DataStorage","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Search & Extract")
		countries_list = ["Afghanistan","Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Austrian Empire", "Azerbaijan", "Baden*", "Bahamas, The", "Bahrain", "Bangladesh", "Barbados", "Bavaria*", "Belarus", "Belgium", "Belize", "Benin (Dahomey)", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Brunswick and Lüneburg", "Bulgaria", "Burkina Faso (Upper Volta)", "Burma", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Cayman Islands, The", "Central African Republic", "Central American Federation*", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo Free State, The", "Costa Rica", "Cote d’Ivoire (Ivory Coast)", "Croatia", "Cuba", "Cyprus", "Czechia", "Czechoslovakia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Duchy of Parma, The*", "East Germany (German Democratic Republic)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Federal Government of Germany (1848-49)*", "Fiji", "Finland", "France", "Gabon", "Gambia, The", "Georgia", "Germany", "Ghana", "Grand Duchy of Tuscany, The*", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Hanover*", "Hanseatic Republics*", "Hawaii*", "Hesse*", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kingdom of Serbia/Yugoslavia*", "Kiribati", "Korea", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Lew Chew (Loochoo)*", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mecklenburg-Schwerin*", "Mecklenburg-Strelitz*", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Namibia", "Nassau*", "Nauru", "Nepal", "Netherlands, The", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North German Confederation*", "North German Union*", "North Macedonia", "Norway", "Oldenburg*", "Oman", "Orange Free State*", "Pakistan", "Palau", "Panama", "Papal States*", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Piedmont-Sardinia*", "Poland", "Portugal", "Qatar", "Republic of Genoa*", "Republic of Korea (South Korea)", "Republic of the Congo", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Schaumburg-Lippe*", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands, The", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Texas*", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Two Sicilies*", "Uganda", "Ukraine", "Union of Soviet Socialist Republics*", "United Arab Emirates, The", "United Kingdom, The", "Uruguay", "Uzbekistan", "USA","UK", "Vanuatu", "Venezuela", "Vietnam", "Württemberg*", "Yemen", "Zambia", "Zimbabwe"]
		email_extensions_list = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "hotmail.co.uk", "hotmail.fr", "msn.com", "yahoo.fr", "wanadoo.fr", "orange.fr", "comcast.net", "yahoo.co.uk", "yahoo.com.br", "yahoo.co.in", "live.com", "rediffmail.com", "free.fr", "gmx.de", "web.de", "yandex.ru", "ymail.com", "libero.it", "outlook.com", "uol.com.br", "bol.com.br", "mail.ru", "cox.net", "hotmail.it", "sbcglobal.net", "sfr.fr", "live.fr", "verizon.net", "live.co.uk", "googlemail.com", "yahoo.es", "ig.com.br", "live.nl", "bigpond.com", "terra.com.br", "yahoo.it", "neuf.fr", "yahoo.de", "alice.it", "rocketmail.com", "att.net", "laposte.net", "facebook.com", "bellsouth.net", "yahoo.in", "hotmail.es", "charter.net", "yahoo.ca", "yahoo.com.au", "rambler.ru", "hotmail.de", "tiscali.it", "shaw.ca", "yahoo.co.jp", "sky.com", "earthlink.net", "optonline.net", "freenet.de", "t-online.de", "aliceadsl.fr", "virgilio.it", "home.nl", "qq.com", "telenet.be", "me.com", "yahoo.com.ar", "tiscali.co.uk", "yahoo.com.mx", "voila.fr", "gmx.net", "mail.com", "planet.nl", "tin.it", "live.it", "ntlworld.com", "arcor.de", "yahoo.co.id", "frontiernet.net", "hetnet.nl", "live.com.au", "yahoo.com.sg", "zonnet.nl", "club-internet.fr", "juno.com", "optusnet.com.au", "blueyonder.co.uk", "bluewin.ch", "skynet.be", "sympatico.ca", "windstream.net", "mac.com", "centurytel.net", "chello.nl", "live.ca", "aim.com", "bigpond.net.au"]
		country_name = st.sidebar.selectbox("Country",countries_list)
		email_type = st.sidebar.selectbox("Email Type",email_extensions_list)
		num_per_page = st.sidebar.number_input("Number of Results Per Page",10,100,step=10)

		tasks_list = ["Emails","URLS","Phonenumbers"]
		task_option = st.sidebar.multiselect("Task",tasks_list,default="Emails")
		search_text = st.text_input("Paste Term Here")
			# devops + USA + email@gmail.com
		generated_query = f"{search_text} + {country_name} + email@{email_type}&num={num_per_page}"
		print(search_text)
		st.info("Generated Query: {}".format(generated_query))

		if st.button("Search & Extract"):
			if generated_query is not None:
				text = fetch_query(generated_query)
				# st.write(text)

				task_mapper = {"Emails":nfx.extract_emails(text),"URLS":nfx.extract_urls(text)
				,"Phonenumbers":nfx.extract_phone_numbers(text)}

				all_results = []
				for task in task_option:
					result = task_mapper[task]
					# st.write(result)
					all_results.append(result)
				st.write(all_results)

				with st.beta_expander("Results As DataFrame"):
					result_df = pd.DataFrame(all_results).T
					result_df.columns = task_option

					# Save TO Database as SQL
					result_df['Emails'].to_sql(name='EmailsTable',con=conn,if_exists='append')
					st.dataframe(result_df)
					make_downloadable_df(result_df)


	elif choice == "Linkedin Extractor":
#		st.subheader("Linkedin Extractor")
		st.subheader("Search Data")
#		site:linkedin.com/in/ AND "python developer" AND "Zürich"
		search_text = st.text_input("Paste Link Here", value='site:linkedin.com/in/ AND "python developer" AND "Zürich"')
		username = st.text_input ("Paste Mail Here")
		password = st.text_input ("Paste Password Here", type="password")
		text = st.text_area("Paste Text Here")

		# print (name)
		# print (job_title)
		# print (schools)
		# print (location)
		# print (ln_url)


		if st.button("Search Data"):
		   result_df = scrape(search_text, password, username)
		   st.dataframe (result_df)
		   make_downloadable_df (result_df)
		else:
			tasks_list = ["Name", "phone","Job-Titel","schools","Location","Emails","URLS","Phonenumbers"]
			task_option = st.sidebar.multiselect("Task",tasks_list,default="Emails")
			task_mapper = {"Emails":nfx.extract_emails(text),"URLS":nfx.extract_urls(text),
			"Phonenumbers":nfx.extract_phone_numbers(text),
			 "Name":"name",
			 "Phone":"phone",
			 "Job-Titel":"Job-Titel",
			 "schools":"schools",
			 "Location":"location"}
			all_results = []
			for task in task_option:
				result = task_mapper[task]
				# st.write(result)
				all_results.append(result)
			st.write(all_results)

			with st.beta_expander("Results As DataFrame"):
				result_df = pd.DataFrame(all_results).T
				result_df.columns = task_option
				st.dataframe(result_df)
				make_downloadable_df(result_df)

	elif choice == "Contact Detail":
		#		st.subheader("Linkedin Extractor")
		st.subheader ("Search Data")
		#		site:linkedin.com/in/ AND "python developer" AND "Zürich"
		search_text = st.text_input ("Paste URL Here" , value='inspirant.ch')
		# username = st.text_input ("Paste Mail Here")
		# password = st.text_input ("Paste Password Here" , type="password")
		text = st.text_area ("Paste Text Here")

		# print (name)
		# print (job_title)
		# print (schools)
		# print (location)
		# print (ln_url)


		if st.button ("Search Data"):
			# result_df = scrape (search_text , password , username)
			# Check if New path exists
			# from scrapy.crawler import CrawlerProcess
			#
			# c = CrawlerProcess ({
			# 	'USER_AGENT': 'Mozilla/5.0' ,
			# 	'FEED_FORMAT': 'json' ,
			# 	'FEED_URI': 'emails.json' ,
			# })
			# c.crawl (gather_details)
			# c.start ()
			# if os.path.exists ("contact_details"):
			# 	# Change the current working Directory
			# 	# st.text(os.uname())
			# 	# st.text(os.getcwd())
			import subprocess
			variable = 'gather_details.py'
			# 	# subprocess.call("cd " + variable + "| pwd", shell=True)
			# 	# variable = 'contact_details/emails.json'
			subprocess.call("rm " + "emails.json", shell=True)
			subprocess.call("python " + variable + " " + search_text, shell=True)

			# 	# os.chdir("contact_details")
			# 	# cp = subprocess.call(["scrapy crawl gather_details -a domain="+ search_text +" -o emails.json"], shell=True)
			# 	# st.text (cp)
			# 	# os.chdir("..")
			#     #
			# 	#cmd ="scrapy crawl gather_details -a domain="+ search_text + " -o emails.json"
			# 	#subprocess.call("scrapy crawl gather_details", shell=True)
			# 	# os.chdir("..")
			# 	startparse(search_text)
			# else:
			# 	st.text ("Can't change the Current Working Directory")
			# print ("initparse")
			# process = CrawlerProcess (settings={
			# 	"FEEDS": {
			# 		"emails.json": {"format": "json"} ,
			# 	} ,
			# 	'USER_AGENT': 'Mozilla/5.0' ,
			# })
			# GatherDetailsSpider.domain = search_text
			# print (search_text)
			# process.crawl (GatherDetailsSpider)
			# process.start ()
			st.text('Contact Details finished !')
			# st.dataframe (result_df)
			# make_downloadable_df (result_df)
			#
			with st.beta_expander ("Results As DataFrame"):
				if os.stat("emails.json").st_size == 0:
					st.text ('No entry !')
				else:
					result_df = pd.read_json('emails.json')
					result_df.columns = ['emails','phones','page']
					st.dataframe (result_df)
					make_downloadable_df (result_df)

	elif choice == "Single Extractor":
		st.subheader("Extract A Single Term")
		text = st.text_area("Paste Text Here")
		task_option = st.sidebar.selectbox("Task",["Name","Job-Titel","schools","Location","Emails","URLS","Phonenumbers"])
		if st.button("Extract"):

			if task_option == "URLS":
				results = nfx.extract_urls(text)
			elif task_option == "Phonenumbers":
				results = nfx.extract_phone_numbers(text)
			elif task_option == "Emails":
				results = nfx.extract_emails (text)
			elif task_option == "Name":
				results = "name"
			elif task_option == "Phone":
				results = "phone"
			elif task_option == "Job-Titel":
				results = "Job-Titel"
			elif task_option == "schools":
				results = "schools"
			else:
				result = "Location"


			st.write(results)

			with st.beta_expander("Results As DataFrame"):
				result_df = pd.DataFrame({'Results':results})
				st.dataframe(result_df)
				make_downloadable(result_df,task_option)




	elif choice == "Bulk Extractor":
		st.subheader("Bulk Extractor")
		text = st.text_area("Paste Text Here")
		tasks_list = ["Emails","URLS","Phonenumbers"]
		task_option = st.sidebar.multiselect("Task",tasks_list,default="Emails")
		task_mapper = {"Emails":nfx.extract_emails(text),"URLS":nfx.extract_urls(text)
		,"Phonenumbers":nfx.extract_phone_numbers(text)}

		all_results = []
		for task in task_option:
			result = task_mapper[task]
			# st.write(result)
			all_results.append(result)
		st.write(all_results)

		with st.beta_expander("Results As DataFrame"):
			result_df = pd.DataFrame(all_results).T
			result_df.columns = task_option
			st.dataframe(result_df)
			make_downloadable_df(result_df)

	elif choice == "DataStorage":
		st.subheader("Data Storage of Emails")
		new_df = pd.read_sql('SELECT * FROM EmailsTable',con=conn)

		with st.beta_expander("View All Emails"):
			st.dataframe(new_df)


	else:
		st.subheader("About")


if __name__ == '__main__':
	main()
