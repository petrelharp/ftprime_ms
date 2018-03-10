SHELL := /bin/bash
# use bash for <( ) syntax

.PHONY : 

broad_12_mar_2018.slides.html : file_size.png

# change this to the location of your local MathJax.js library
LOCAL_MATHJAX = /usr/share/javascript/mathjax/MathJax.js
ifeq ($(wildcard $(LOCAL_MATHJAX)),)
	MATHJAX = https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js
else
	MATHJAX = $(LOCAL_MATHJAX)
endif

# may want to add "--self-contained" to the following
PANDOC_OPTS = --mathjax=$(MATHJAX)?config=TeX-AMS-MML_HTMLorMML --standalone
# optionally add in a latex file with macros
LATEX_MACROS = macros.tex
ifeq ($(wildcard $(LATEX_MACROS)),)
	# macros file isn't there
else
	PANDOC_OPTS += -H .pandoc.$(LATEX_MACROS)
endif

.pandoc.$(LATEX_MACROS) : $(LATEX_MACROS)
	if [ -e $(LATEX_MACROS) ]; then (echo '\['; cat $(LATEX_MACROS); echo '\]') > $@; fi

setup : .pandoc.$(LATEX_MACROS)
	@:

%.html : %.md setup
	pandoc -o $@ $(PANDOC_OPTS) $<

%.md : %.Rmd
	Rscript -e 'templater::render_template("$<", output="$@", change.rootdir=TRUE)'


## VARIOUS SLIDE METHODS
REVEALJS_OPTS = -t revealjs -V theme=simple -V slideNumber=true -V transition=none -H resources/adjust-revealjs.style --slide-level 2
SLIDES_OPTS = $(REVEALJS_OPTS)

%.slides.html : %.md setup
	pandoc -o $@ $(SLIDES_OPTS) $(PANDOC_OPTS) $<


## image conversion

%.pdf : %.svg
	inkscape $< --export-pdf=$@

%.svg : %.pdf
	inkscape $< --export-plain-svg=$@

%.png : %.pdf
	convert -density 300 $< -flatten $@

%.gif : %.pdf
	convert -density 300 $< -flatten $@

%.pdf : %.ink.svg
	inkscape $< --export-pdf=$@

# animated gif
.SECONDEXPANSION :
%.anim.gif : $$(wildcard %/*.gif)
	convert -loop 1 -delay 10 -coalesce -fuzz 2% -layers optimize $^ $@

