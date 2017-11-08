.PHONY: all, clean

all: forwards_paper.pdf

forwards_paper.pdf : method_diagram.pdf references.bib example_tree_sequence.pdf sims/wf-after.pdf sims/wf-before.pdf

clean: 
	-rm *.aux *.log *.bbl *.blg

sims/wf-after.svg sims/wf-before.svg : sims/wf-figures.py
	python3 $<

%.pdf : %.tex %.bbl
	while ( pdflatex $<;  grep -q "Rerun to get" $*.log ) do true ; done

%.aux : %.tex
	-pdflatex $<

%.bbl : %.aux
	bibtex $<

%.html : %.md
	Rscript -e "templater::render_template(md.file='$<', output='$@')"

%.svg : %.pdf
	inkscape $< --export-plain-svg=$@

%.png : %.pdf
	convert -density 300 $< -flatten $@

%.pdf : %.svg
	inkscape $< --export-pdf=$@

%.pdf : %.ink.svg
	inkscape $< --export-pdf=$@

example_tree_sequence.pdf: example_tree_sequence.asy
	asy -f pdf example_tree_sequence.asy
