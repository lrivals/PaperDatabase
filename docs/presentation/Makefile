# Compile la présentation : make ; nettoyage : make clean
DOC = paperdatabase-slides

all: $(DOC).pdf

$(DOC).pdf: $(DOC).tex
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex >/dev/null
	@grep -E "undefined|Overfull" $(DOC).log || echo "OK : $(DOC).pdf"

clean:
	rm -f $(DOC).aux $(DOC).log $(DOC).nav $(DOC).out $(DOC).snm $(DOC).toc $(DOC).vrb

.PHONY: all clean
