# Compile l'article : make ; nettoyage : make clean
DOC = paperdatabase

$(DOC).pdf: $(DOC).tex refs.bib
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex >/dev/null
	bibtex $(DOC) >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex >/dev/null
	@grep -E "undefined|Warning: Citation" $(DOC).log || echo "OK : $(DOC).pdf"

clean:
	rm -f $(DOC).aux $(DOC).bbl $(DOC).blg $(DOC).log $(DOC).out $(DOC).toc

.PHONY: clean
