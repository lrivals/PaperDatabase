# Compile l'article (français et anglais) : make ; nettoyage : make clean
DOCS = paperdatabase paperdatabase-en

all: $(addsuffix .pdf,$(DOCS))

%.pdf: %.tex refs.bib
	pdflatex -interaction=nonstopmode -halt-on-error $*.tex >/dev/null
	bibtex $* >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $*.tex >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $*.tex >/dev/null
	@grep -E "undefined|Warning: Citation" $*.log || echo "OK : $*.pdf"

clean:
	rm -f $(foreach d,$(DOCS),$(d).aux $(d).bbl $(d).blg $(d).log $(d).out $(d).toc)

.PHONY: all clean
