from subprocess import call

def xelatex():
	call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "resume_cv.tex"])
	print "done"
