.PHONY: all, clean

all: probgen-2018-poster.pdf

probgen-2018-poster.pdf : refs.bib stats_1.pdf stats_2.pdf stats_3.pdf

stats_%.pdf : stats.ink.svg
	../export-layers-svg.sh $< tree_$* numbers_$* > $@

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

%.png : %.pdf
	convert -density 300 $< -flatten $@

%.pdf : %.svg
	inkscape $< --export-pdf=$@

%.pdf : %.ink.svg
	inkscape $< --export-pdf=$@

%.pdf: %.asy
	asy -f pdf $<
