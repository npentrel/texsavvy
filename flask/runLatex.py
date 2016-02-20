from subprocess import call

def xelatex():
	call(["/usr/local/texlive/2015/bin/universal-darwin/xelatex", "/Users/Naomi/coding/texsavvy/flask/templates/resume_cv.tex"])

