#!/usr/bin/env python

# Adapted ffrom https://pypi.python.org/pypi/pdfminer/

import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
from cStringIO import StringIO
import string
import re

def processing(txt):
    txtraw = txt.splitlines()
    txt = {}
    i = 0
    skip = False
    for line in txtraw:
        if not skip:            
            if "Page" not in line:
                line = string.replace(line, "\x0c", "")
                line = string.replace(line, "&", "\&")
                txt[i] = string.replace(line, "\xe2\x82\xac", " Euro")
                i += 1
            else:
                skip = True
        else:
            skip = False

    # print txt
    fields = {}
    fields['formattedName'] = txt[0]
    fields['headline'] = txt[1]
    fields['emailAddress'] = txt[2]
    fields['experience1'] = {}
    fields['experience2'] = {}
    fields['experience3'] = {}
    fields['experience4'] = {}
    fields['experience5'] = {}
    fields['experience6'] = {}
    fields['experience7'] = {}
    fields['experience8'] = {}
    fields['experience9'] = {}
    fields['experience10'] = {}
    fields['education1'] = {}
    fields['education2'] = {}

    experience = False
    experienceFound = 0
    education = False
    educationFound = 0
    i = 0
    while i < len(txt):
        if txt[i] == 'Experience':
            experience = True
            i += 1
        if experienceFound == 3:
            experience = False
        if txt[i] == 'Volunteer Experience' or txt[i] == 'Education':
            experience = False
        if experience:
            fields['experience' + str(experienceFound + 1)]['title'] = txt[i]
            i += 1
            m = re.search('[^(]*', txt[i])
            fields['experience' + str(experienceFound + 1)]['time1'] = m.group(0) 
            fields['experience' + str(experienceFound + 1)]['time2'] = re.search('-.*', m.group(0)).group(0)[1:]  
            i += 2
            fields['experience' + str(experienceFound + 1)]['body'] = ''
            while txt[i] != '':                    
                fields['experience' + str(experienceFound + 1)]['body'] = fields['experience' + str(experienceFound + 1)]['body'] + ' ' + txt[i]
                i += 1
            experienceFound += 1
            i += 1
        else :
            i += 1

    fields['experienceFound'] = experienceFound
    i = 0
    while i < len(txt):
        if txt[i] == 'Education':
            education = True
            i += 1
        if educationFound == 2:
            education = False
        if txt[i] == 'Interests' or txt[i] == 'Education':
            education = False
        if education:
            fields['education' + str(educationFound + 1)]['title'] = txt[i]
            i += 1
            fields['education' + str(educationFound + 1)]['body'] = ''
            # while txt[i] != '':                    
            fields['education' + str(educationFound + 1)]['body'] = fields['education' + str(educationFound + 1)]['body'] + ' ' + re.search('[^\d]+', txt[i]).group(0)[:-2]
            m = re.search('(\\d)+', txt[i])
            fields['education' + str(educationFound + 1)]['time1'] = m.group(0) 
            fields['education' + str(educationFound + 1)]['time2'] = re.search('-.*', txt[i]).group(0)[1:]  
            i += 1
            educationFound += 1
            # i += 1
        else :
            i += 1

    fields['educationFound'] = educationFound
    # print fields
    return fields

# main
def pdfytxt(argv):
    import getopt
    def usage():
        print ('usage: %s [-d] [-p pagenos] [-m maxpages] [-P password] [-o output]'
               ' [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin] [-W word_margin]'
               ' [-F boxes_flow] [-Y layout_mode] [-O output_dir] [-R rotation]'
               ' [-t text|html|xml|tag] [-c codec] [-s scale]'
               ' file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:t:c:s:')
    except getopt.GetoptError:
        return usage()
    if not args: return usage()
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-C': caching = False
        elif k == '-n': laparams = None
        elif k == '-A': laparams.all_texts = True
        elif k == '-V': laparams.detect_vertical = True
        elif k == '-M': laparams.char_margin = float(v)
        elif k == '-L': laparams.line_margin = float(v)
        elif k == '-W': laparams.word_margin = float(v)
        elif k == '-F': laparams.boxes_flow = float(v)
        elif k == '-Y': layoutmode = v
        elif k == '-O': imagewriter = ImageWriter(v)
        elif k == '-R': rotation = int(v)
        elif k == '-t': outtype = v
        elif k == '-c': codec = v
        elif k == '-s': scale = float(v)
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = StringIO()
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                              imagewriter=imagewriter)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    else:
        return usage()
    for fname in args:
        fp = file(fname, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)            
        fp.close()
    device.close()

    text = outfp.getvalue()
    data = processing(text)
    return data

if __name__ == '__main__': sys.exit(main(sys.argv))
