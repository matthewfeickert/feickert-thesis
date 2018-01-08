file = feickert_thesis
driver = $(file).tex
date=$(shell date +%Y-%m-%d)
output_file = draft_$(date).pdf
tex_source = $(wildcard *.tex) $(wildcard src/*.tex) $(wildcard src/backup/*.tex)
image_source = $(wildcard images/figures/*.pdf) $(wildcard images/figures/*.jpg) $(wildcard images/figures/*.png)
#bib_source = SMU_ATLAS.bib
bib_source = $(wildcard *.bib) $(wildcard bib/*.bib)
REFERENCES = true
#REFERENCES = false
TEX=xelatex

all: document

text: $(driver) $(tex_source) $(image_source)
	$(TEX) $(driver)
	$(TEX) $(driver)

document: $(driver) $(tex_source) $(image_source) $(bib_source)
	make text 
	if [ "$(REFERENCES)" = true ]; then bibtex $(basename $(driver)); $(TEX) $(driver); $(TEX) $(driver); fi
	cp $(basename $(driver)).pdf $(output_file)

upload:
	scp draft_$(date).pdf feickert@lxplus.cern.ch:/eos/user/f/feickert/www/thesis/draft.pdf
	@echo "### File viewable at: https://cern.ch/feickert/thesis/draft.pdf"

clean:
	\rm -f *.aux *.bbl *.blg *.dvi *.idx *.lof *.log *.lot *.toc *.glg *.gls *.glo *.xdy *.nav *.out *.snm *.vrb *.mp *.synctex.gz

realclean: clean
	\rm -f *.pdf

final:
	if [ -f *.aux ]; then make clean; fi
	make document
	make clean
