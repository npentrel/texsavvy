from subprocess import call
from iso3166 import countries

def personalinfoFile(data):
    target = open('personalinfo.tex', 'w')
    dict = {}
    dict['DfullName'] = data['formattedName']
    dict['Dtagline'] = data['headline']
    dict['Dmail'] = data['emailAddress']
    dict['DpictureUrl'] = data['pictureUrls']['values'][0]
    dict['Dlinkedin'] = data['publicProfileUrl']
    dict['DpositionOnetitle'] = data['positions']['values'][0]['title']
    dict['DpositionOneSummary'] = data['positions']['values'][0]['summary']
    dict['DpositionOneStartMonth'] = data['positions']['values'][0]['startDate']['month']
    dict['DpositionOneStartYear'] = data['positions']['values'][0]['startDate']['year']
    dict['DpositionOneCompany'] = data['positions']['values'][0]['company']['name']
    dict['DfirstName'] = data['firstName'] 
    dict['DlastName'] = data['lastName']
    dict['Dcity'] = data['location']['name']
    dict['Dcountry'] = countries.get(data['location']['country']['code'])[0]
    pos = ""
    for v in data['positions']['values']:
    	pos += v['title'] + "/" + v['summary'] + "/" + v['company']['name'] + "/" + str(v['startDate']['month']) + "/" + str(v['startDate']['year']) + ","
	dict['Dpositions'] = pos[:(len(pos)-1)]

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

    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_2.tex"])
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_2.tex"])

    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "resume_cv.tex"])
    # call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "resume_cv.tex"])

    call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU.tex"])
    call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "texsavvy_EU.tex"])
    print "done"
    return 'OK'
