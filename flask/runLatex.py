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
    dict['DfirstName'] = data['formattedName'].split()[0] 
    dict['DlastName'] = " ".join(data['formattedName'].split()[1:])
    dict['Dcity'] = "London"
    dict['Dcountry'] = "UK"
    dict['Dpositions'] = {}
    experiences = ""
    for i in range(1, data['experienceFound']+1):
        experiences += string.replace(data['experience' + str(i)]['title'].split("at")[0], ",", ";") + "/" + string.replace(data['experience' + str(i)]['body'], ",", ";")[:(len(string.replace(data['experience' + str(i)]['body'], ",", ";"))-1)] + "/" + string.replace(data['experience' + str(i)]['title'].split("at")[1], ",", ";") + "/" + data['experience' + str(i)]['time1'] + "/" + "" + ","
    dict['Dpositions'] = experiences[:(len(experiences)-1)]
    dict['Deducation'] = {}

    education = ""
    for i in range(1, data['educationFound']+1):
        education += data['education' + str(i)]['title'] + "/" + string.replace(data['education' + str(i)]['body'], ",", ";") + "/" + data['education' + str(i)]['time1'] + "/" + data['education' + str(i)]['time2'] + ","
    dict['Deducation'] = education[:(len(education)-1)]
    print "!!!"
    print education

    # for v in data['positions']['values']:
    # 	pos += v['title'] + "/" + v['summary'] + "/" + v['company']['name'] + "/" + str(v['startDate']['month']) + "/" + str(v['startDate']['year']) + ","
    # dict['Dpositions'] = pos[:(len(pos)-1)]

    target.write("\\providetoggle{lang}\n")
    if (data['lang']):
        target.write("\\settoggle{lang}{true}")
        languages = ""
        for i in range(1, data['languagesFound']+1):
            languages += data['languages' + str(i)]['title'] + "/" + string.replace(data['languages' + str(i)]['body'], ",", ";") + ","
        dict['Dlanguages'] = languages[:(len(languages)-1)]
        print "!!!"
        print languages

    else : 
        target.write("\\settoggle{lang}{false}")


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


    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU_no_photo.tex"])
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU_no_photo.tex"])    
    # shutil.copy("texsavvy_EU_no_photo.pdf", "static/resume.pdf")


    call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU.tex"])
    call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU.tex"])    
    shutil.copy("texsavvy_EU.pdf", "static/resume.pdf")
    print "done"
    return 'OK'
