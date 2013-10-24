# Confluence Downloader (modified)
#
# Original file found at: https://answers.atlassian.com/questions/114490/how-to-get-all-attachments-under-a-space-via-rest-api
# Original autor: Adam Laskowski
# 24th October 2013

#!/usr/bin/python

import sys, string, xmlrpclib, re, getpass, os

serverurl = 'http://confluence.company.com/rpc/xmlrpc'
server = xmlrpclib.ServerProxy(serverurl) # XML-RPC of Atlassian Confluence
user = raw_input("User: ") # Username
pswd = getpass.getpass() # Password
token = server.confluence2.login(user, pswd) # Login method (latest version uses confluence2 object)
space = raw_input("Space: ") # Space of the attachments
pagetree = server.confluence2.getPages(token, space) # Creates a list of dicts
filetypes = ['application/x-font-ttf', 'application/vnd.oasis.opendocument.formula-template'] # Filetypes to be downloaded
allattachments = [] # Array of all the attachments available (initially empty)

for pagedict in pagetree:
	pageid = pagedict['id'] # Pulls the ID from each page from the pagetree list
	pagetitle = pagedict['title']
	attachments = server.confluence2.getAttachments(token, pageid) # Creates another list of dicts
	auxDict = {'id': pageid, 'title': pagetitle, 'attachments': attachments} # Adds attachment list to a temp dict
	allattachments.append(auxDict) # Appends each new dict to the allattachments list 

# Print the page title and all attachments and their file types from the first dict in the allattachments list
for each in allattachments:
	for attachment in each['attachments']:
		if (attachment['contentType'] in filetypes):
			print attachment['title']
			## Block to download the files with its name
			try:
				filed = open("downloads/"+attachment['title'], 'wb') # Important to open the file in binary mode! 'b'
				filed.write(str(server.confluence2.getAttachmentData(token, each['id'], attachment['title'], "0"))) # 0 for the latest version
				filed.close() # Close the file
				break
			except Exception, ex:
				print "Couldnt download the file. Error: "+ex
exit('Done!')