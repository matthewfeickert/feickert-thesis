file = feickert_thesis
driver = $(file).tex

tex_source = $(wildcard *.tex) $(wildcard src/*.tex) $(wildcard src/backup/*.tex)
image_source = $(wildcard images/figures/*.pdf) $(wildcard images/figures/*.jpg) $(wildcard images/figures/*.png)
bib_source = $(wildcard *.bib) $(wildcard bib/*.bib)

LATEX = xelatex
BIBTEX = bibtex
# BIBTEX = biber

# The main document filename
BASENAME = feickert_thesis

date=$(shell date +%Y-%m-%d)
output_file = draft_$(date).pdf

default: run_latexmk
	make copy_draft

all: document

run_latexmk:
	latexmk -pdf $(BASENAME)

%.pdf: %.tex *.tex *.bib
	$(LATEX) $<
	-$(BIBTEX)  $(basename $<)
	$(LATEX) $<
	$(LATEX) $<

copy_draft:
	rsync $(BASENAME).pdf $(output_file)

text: $(driver) $(tex_source) $(image_source)
	$(LATEX) $(driver)
	$(LATEX) $(driver)

document: $(driver) $(tex_source) $(image_source) $(bib_source)
	make text
	bibtex $(basename $(driver)); $(LATEX) $(driver); $(LATEX) $(driver);
	cp $(basename $(driver)).pdf $(output_file)

upload:
	scp draft_$(date).pdf feickert@lxplus.cern.ch:/eos/user/f/feickert/www/thesis/draft.pdf
	@echo "### File viewable at: https://cern.ch/feickert/thesis/draft.pdf"

clean:
	\rm -f *.aux *.bbl *.blg *.dvi *.idx *.lof *.log *.lot *.toc *.glg *.gls *.glo *.xdy *.nav *.out *.snm *.vrb *.mp *.synctex.gz *.brf

realclean: clean
	\rm -f *.pdf

final:
	if [ -f *.aux ]; then make clean; fi
	make document
	make clean
