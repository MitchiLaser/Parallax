.PHONY: pdf clean

pdf: $(shell find . -type f -name '*.tex')
	pdflatex main.tex
	pdflatex main.tex
	pdflatex main.tex

clean: main.pdf
	latexmk -c
