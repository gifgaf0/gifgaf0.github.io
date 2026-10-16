# Build the paper: make (needs pdflatex, bibtex, latexmk; TeX Live 2023 tested)
main.pdf: main.tex refs.bib $(wildcard sections/*.tex)
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	latexmk -C

.PHONY: clean
