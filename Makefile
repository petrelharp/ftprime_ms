.PHONY: all clean phony

SUBMITFIGS= submit/Fig1.eps submit/Fig2.eps submit/Fig3.eps submit/Fig4.eps submit/Fig5.eps submit/Fig6.eps submit/Fig7.eps

all: forwards_paper.pdf final_format_forwards_paper.pdf appendix.pdf $(SUBMITFIGS)

diffs: forwards_paper-diffa30eb785835ce2d82c7643e316e2b0a7f7e206d4.pdf

forwards_paper.pdf : method_diagram.pdf references.bib example_tree_sequence.pdf wf-before-after.pdf simplify-state-diagram.pdf review-responses.tex review-response-commands.tex

appendix.pdf : forwards_paper.pdf
	# do this with nice version
	pdfjam --outfile $@ $< 22-

cover_letter.pdf : forwards_paper.pdf
	pdfjam --outfile $@ $< 34

review_responses.pdf : forwards_paper.pdf
	pdfjam --outfile $@ $< 35-

forwards_paper_line_nums.pdf : forwards_paper.pdf
	pdfjam --outfile $@ $< 1-33

clean: 
	-rm -f *.aux *.log *.bbl *.blg

submit/Fig1.eps : sims/rawspeed_logy.eps

submit/Fig2.eps : sims/speedup.eps

submit/Fig3.eps : example_tree_sequence.eps

submit/Fig4.eps : wf-before-after.eps

submit/Fig5.eps : method_diagram.eps

submit/Fig6.eps : simplify-state-diagram.eps

submit/Fig7.eps : sims/simplify-results.eps

$(SUBMITFIGS) :
	ln -s ../$< $@

# doesn't need bbl since refs go in the latex FOR SOME REASON
final_format_forwards_paper.pdf : final_format_forwards_paper.tex
	while ( pdflatex $<;  grep -q "Rerun to get" final_format_forwards_paper.log ) do true ; done

%.pdf : %.tex %.bbl
	while ( pdflatex $<;  grep -q "Rerun to get" $*.log ) do true ; done

%.aux : %.tex
	-pdflatex $<

%.bbl : %.aux references.bib
	bibtex $<

%.html : %.md
	Rscript -e "templater::render_template(md.file='$<', output='$@')"

%.eps : %.pdf
	inkscape $< --export-eps=$@

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
