.PHONY: pdf clean

pdf: $(shell find . -type f -name '*.tex')
	latexmk -pdf

clean: main.pdf
	latexmk -c
