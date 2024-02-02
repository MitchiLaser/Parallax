% Load the scrrep class and provide the documentclass as a modified version
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{include/documentclass}
\LoadClass[
	a4paper,
	11pt,
	titlepage,
	toc=chapterentrywithdots
]{scrreprt}


% layout settings
\usepackage{fullpage}


% language and character setting
\usepackage[utf8]{inputenc}			% for using utf8 characters
\usepackage[T1]{fontenc}				% correct encoding (also searching for non-ascii characters
\usepackage{lmodern}						% font used by T1 font enc
\usepackage[english]{babel}			% language and letter spearation


% mathematical symbols
\usepackage{amsmath}						% math
\usepackage{amssymb}						% more math
\usepackage{nicefrac}						% fancy fractions
\usepackage{enumitem}						% itemization and enumeration
\usepackage{siunitx}						% proper handling of values with units
\sisetup{separate-uncertainty=true}


% support for pictures
\usepackage{graphicx}						% include pictures
\usepackage{svg}								% include svg files
\graphicspath{{./fig/}}					% include images in the mentioned directory by filename not by relative path
\usepackage{float}							% allow more precise positioning of figures


% hyperlink setup
\usepackage[
	raiselinks=true,
	bookmarks=true,
	hyperindex=true
]{hyperref}


% better referencing
\usepackage{varioref}						% intelligent page references
\usepackage{cleveref}						% intelligent reference for tables, figures, chapters, sections, ...
\crefname{figure}{Fig.}{Figs.}
\Crefname{figure}{Figure}{Figures}
\crefname{equation}{Eq.}{Eqs.}
\Crefname{equation}{Equation}{Equations}


% support To-Do notes in then document
\usepackage[colorinlistoftodos, prependcaption]{todonotes}


% TIKZ
\usepackage{tikz}
\usetikzlibrary{circuits.logic.IEC}
\usetikzlibrary {arrows.meta}
\usepackage[siunitx, european]{circuitikz}
