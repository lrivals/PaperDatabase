# Compile les deux états de l'art : make ; nettoyage : make clean
DOCS = fpga vision-embarquee
COMMON = preamble.tex $(wildcard sec-*.tex) $(wildcard gloss-*.tex) refs.bib

all: $(DOCS:=.pdf)

%.pdf: %.tex $(COMMON)
	pdflatex -interaction=nonstopmode -halt-on-error $* >/dev/null
	makeglossaries $* >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $* >/dev/null
	bibtex $* >/dev/null
	makeglossaries $* >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $* >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error $* >/dev/null
	@grep -E "undefined|Warning: Citation" $*.log || echo "OK : $*.pdf"

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.glg *.glo *.gls *.ist *.plg *.pls *.plo *.mog *.mos *.moo *.meg *.mes *.meo

.PHONY: all clean
