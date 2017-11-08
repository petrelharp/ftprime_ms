.PHONY: all, clean

all: forwards_paper.pdf

forwards_paper.pdf : method_diagram.pdf references.bib example_tree_sequence.pdf wf-before-after.pdf simplify-state-diagram.pdf

clean: 
	-rm *.aux *.log *.bbl *.blg

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

%.pdf : %.ink.svg
	inkscape $< --export-pdf=$@

example_tree_sequence.pdf: example_tree_sequence.asy
	asy -f pdf example_tree_sequence.asy
