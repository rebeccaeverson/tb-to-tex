# Toolbox -> LaTeX PDF Formatting Script
Translate Toolbox dictionary files into LaTeX-formatted, publishable dictionaries

Author: Becky Everson

Concept:

This set of files takes a Toolbox database (.db file) and turns it into a PDF formatted in a better way than Toolbox's .rtf export. The python script "tbToTex.py" takes an object-oriented approach at dictionary structure. Each lexeme is an Entry object, and each Entry has a list of attributes (part of speech, phonetic form, lists of examples and translations, etc.). This script creates a new Entry object every time it finds a line that begins with "\lx", which is the field marker in Toolbox for "lexeme". It then parses the following lines until it hits another "\lx" line.

Instructions for running:

1. Through command line, locate the correct directory with the following files:
	tbToTex.py - script that takes Toolbox file and converts it to a .tex file
	main.tex - main LaTeX file
	dict.sty - file that dictates how to format the new LaTeX commands formed from the dictionary fields
	runTBtoTex - the script that will run these other programs in order
2. Run script with: python runTBtoTex.py <your .tb file>
3. A file called "texConvert.tex" will be generated and used with main.tex and dict.sty
4. A new PDF will be formed, called "main.pdf". This is the newly formatted dictionary.