from subprocess import call
from iso3166 import countries
import urllib
import os
import shutil
import string

def personalinfoFile(data):
    target = open('personalinfo.tex', 'w')
    dict = {}
    dict['DfullName'] = data['formattedName']
    dict['Dtagline'] = data['headline']
    dict['Dmail'] = data['emailAddress']
    dict['DpictureUrl'] = data['pictureUrls']['values'][0]
    urllib.urlretrieve(dict['DpictureUrl'], "image.jpg")
    
    dict['Dlinkedin'] = data['publicProfileUrl']
    # dict['DpositionOnetitle'] = data['positions']['values'][0]['title']
    # dict['DpositionOneSummary'] = data['positions']['values'][0]['summary']
    # dict['DpositionOneStartMonth'] = data['positions']['values'][0]['startDate']['month']
    # dict['DpositionOneStartYear'] = data['positions']['values'][0]['startDate']['year']
    # dict['DpositionOneCompany'] = data['positions']['values'][0]['company']['name']
    dict['DfirstName'] = data['formattedName'].split()[0] 
    dict['DlastName'] = " ".join(data['formattedName'].split()[1:])
    # dict['Dcity'] = data['location']['name']
    # dict['Dcountry'] = countries.get(data['location']['country']['code'])[0]
    dict['DpositionOnetitle'] = ""
    dict['DpositionOneSummary'] = ""
    dict['DpositionOneStartMonth'] = ""
    dict['DpositionOneStartYear'] = ""
    dict['DpositionOneCompany'] = ""
    dict['Dcity'] = "London"
    dict['Dcountry'] = "UK"
    dict['Dpositions'] = {}
    experiences = ""
    for i in range(1, data['experienceFound']):
        experiences += string.replace(data['experience' + str(i)]['title'].split("at")[0], ",", ";") + "/" + string.replace(data['experience' + str(i)]['body'], ",", ";")[:(len(string.replace(data['experience' + str(i)]['body'], ",", ";"))-1)] + "/" + string.replace(data['experience' + str(i)]['title'].split("at")[1], ",", ";") + "/" + str(5) + "/" + str(2013) + ","
    dict['Dpositions'] = experiences[:(len(experiences)-1)]

    # for v in data['positions']['values']:
    # 	pos += v['title'] + "/" + v['summary'] + "/" + v['company']['name'] + "/" + str(v['startDate']['month']) + "/" + str(v['startDate']['year']) + ","
    # dict['Dpositions'] = pos[:(len(pos)-1)]

    for d in dict:
        target.write("\\newcommand{\\")
        target.write(d)
        target.write("}{")
        if (isinstance(dict[d], unicode)):
	        target.write((dict[d]).encode('utf-8'))
        else:
        	target.write(str(dict[d]))
        target.write("}\n")	
    target.close()

def xelatex(data):
    personalinfoFile(data)
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "benicv.tex"])
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "benicv.tex"])
    # shutil.copy("benicv.pdf", "static/resume.pdf")

    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_2.tex"])
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_2.tex"])
    # shutil.copy("texsavvy_2.pdf", "static/resume.pdf")

    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "resume_cv.tex"])
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "resume_cv.tex"])
    # shutil.copy("resume_cv.pdf", "static/resume.pdf")

    call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU.tex"])
    call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU.tex"])    
    shutil.copy("texsavvy_EU.pdf", "static/resume.pdf")
    print "done"
    return 'OK'
