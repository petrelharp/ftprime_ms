.PHONY: all clean phony

all: forwards_paper.pdf cover_letter.pdf review_responses.pdf forwards_paper_line_nums.pdf

diffs: forwards_paper-diffa30eb785835ce2d82c7643e316e2b0a7f7e206d4.pdf

forwards_paper.pdf : method_diagram.pdf references.bib example_tree_sequence.pdf wf-before-after.pdf simplify-state-diagram.pdf review-responses.tex review-response-commands.tex

cover_letter.pdf : forwards_paper.pdf
	pdfjam --outfile $@ $< 34

review_responses.pdf : forwards_paper.pdf
	pdfjam --outfile $@ $< 35-

forwards_paper_line_nums.pdf : forwards_paper.pdf
	pdfjam --outfile $@ $< 1-33

clean: 
	-rm -f *.aux *.log *.bbl *.blg

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

%.pdf: %.asy
	asy -f pdf $<

forwards_paper-diff%.tex : forwards_paper.tex
	latexdiff-git -r $* forwards_paper.tex
