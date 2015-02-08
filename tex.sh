#!/bin/bash
inhalt=$(./descr_gen.sh $1 tex-export)
echo $inhalt
echo "\documentclass[14pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[ngerman]{babel}
\usepackage[T1]{fontenc}
\author{Lukas Winkler}
\begin{document}

\begin{tabular}{rl}
$inhalt
\end{tabular}
\end{document}" > IKEA.tex
pdflatex IKEA.tex
rm IKEA.tex IKEA.log IKEA.aux
