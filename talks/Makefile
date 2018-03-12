SHELL := /bin/bash
# use bash for <( ) syntax

.PHONY : sim_ts_gifs ne_walkthrough sm_walkthrough simp_walkthrough

broad_12_mar_2018.slides.html : file_size.png example_tree_sequence.png sim_ts.anim.gif sim_wf.anim.gif sim_wf_unlabeled.anim.gif sim_wf_simplified.anim.gif ne_walkthrough sm_walkthrough simp_walkthrough

sim_ts/done sim_wf/done sim_wf_unlabeled/done sim_wf_simplified/done : make_figs.py
	python3 make_figs.py

run_sim : sim_ts/done sim_wf/done sim_wf_unlabeled/done sim_wf_simplified/done

sim_ts_gifs = $(wildcard sim_ts/*.svg)
sim_ts_svgs = $(patsubst %.svg,%.gif,$(sim_ts_gifs))
sim_wf_gifs = $(wildcard sim_wf/*.svg)
sim_wf_svgs = $(patsubst %.svg,%.gif,$(sim_wf_gifs))
sim_wf_ul_gifs = $(wildcard sim_wf_unlabeled/*.svg)
sim_wf_ul_svgs = $(patsubst %.svg,%.gif,$(sim_wf_ul_gifs))
sim_wf_simp_gifs = $(wildcard sim_wf_simplified/*.svg)
sim_wf_simp_svgs = $(patsubst %.svg,%.gif,$(sim_wf_simp_gifs))

$(sim_ts_svg) s $(sim_wf_svg) s $(sim_wf_ul_svg) s $(sim_wf_simp_svgs) : run_sim

sim_ts.anim.gif : $(sim_ts_gifs)

sim_wf.anim.gif : $(sim_wf_gifs)

sim_wf_unlabeled.anim.gif : $(sim_wf_unl_gifs)

sim_wf_simplified.anim.gif : $(sim_wf_simp_gifs)

ne_walkthrough : nodes_edges_walkthrough/nodes_edges_walkthrough.0.png nodes_edges_walkthrough/nodes_edges_walkthrough.1.png nodes_edges_walkthrough/nodes_edges_walkthrough.2.png nodes_edges_walkthrough/nodes_edges_walkthrough.3.png nodes_edges_walkthrough/nodes_edges_walkthrough.4.png nodes_edges_walkthrough/nodes_edges_walkthrough.5.png nodes_edges_walkthrough/nodes_edges_walkthrough.6.png

sm_walkthrough : sites_muts_walkthrough/sites_muts_walkthrough.0.png sites_muts_walkthrough/sites_muts_walkthrough.1.png sites_muts_walkthrough/sites_muts_walkthrough.2.png sites_muts_walkthrough/sites_muts_walkthrough.3.png sites_muts_walkthrough/sites_muts_walkthrough.4.png

simp_walkthrough : simplify_walkthrough.png simplify_walkthrough/simplify_walkthrough.0.png simplify_walkthrough/simplify_walkthrough.1.png simplify_walkthrough/simplify_walkthrough.2.png simplify_walkthrough/simplify_walkthrough.3.png simplify_walkthrough/simplify_walkthrough.4.png simplify_walkthrough/simplify_walkthrough.5.png simplify_walkthrough/simplify_walkthrough.6.png simplify_walkthrough/simplify_walkthrough.7.png simplify_walkthrough/simplify_walkthrough.8.png simplify_walkthrough/simplify_walkthrough.9.png simplify_walkthrough/simplify_walkthrough.10.png simplify_walkthrough/simplify_walkthrough.11.png simplify_walkthrough/simplify_walkthrough.12.png simplify_walkthrough/simplify_walkthrough.13.png simplify_walkthrough/simplify_walkthrough.14.png simplify_walkthrough/simplify_walkthrough.15.png 

####### ink.svg figures

# walkthrough of node, edge tables
nodes_edges_walkthrough/nodes_edges_walkthrough.%.pdf : tables_walkthrough.ink.svg
	(mkdir -p nodes_edges_walkthrough; \
	 ADDLAYERS="borders scale_axes nodes_table edge_0";\
	 for k in $$(seq $*); do \
		ADDLAYERS="$$ADDLAYERS edge_$${k}"; \
	 done; \
	 ./export-layers-svg.sh $< $$ADDLAYERS > $@)


# walkthrough of mut, site tables
sites_muts_walkthrough/sites_muts_walkthrough.%.pdf : tables_walkthrough.ink.svg
	(mkdir -p sites_muts_walkthrough; \
	 ADDLAYERS="borders scale_axes sites_table muts_0";\
	 for k in $$(seq $*); do \
		ADDLAYERS="$$ADDLAYERS muts_$${k}"; \
	 done; \
	 ./export-layers-svg.sh $< $$ADDLAYERS > $@)

# set-up
simplify_walkthrough.pdf : simplify_walkthrough.ink.svg
	 ./export-layers-svg.sh $< orig_tables pedigree labels crossing-overs > $@


# walkthrough of simplify: sequential layers, not cumulative
simplify_walkthrough/simplify_walkthrough.%.pdf : simplify_walkthrough.ink.svg
	(mkdir -p simplify_walkthrough; \
	 ./export-layers-svg.sh $< table_background pedigree labels crossing-overs step_$* > $@)



######## general-purpose

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

# %.svg : %.pdf
# 	inkscape $< --export-plain-svg=$@

%.png : %.pdf
	convert -density 300 $< -flatten $@

%.gif : %.pdf
	convert -density 300 $< -flatten $@

%.png : %.svg
	convert -density 300 $< -flatten $@

%.gif : %.svg
	convert -density 300 $< -flatten $@

%.pdf : %.ink.svg
	inkscape $< --export-pdf=$@

# animated gif
%.anim.gif : $(wildcard %/*.gif)
	convert -loop 0 -delay 10 -coalesce -fuzz 2% -layers optimize $$(ls $*/*.gif) $@
