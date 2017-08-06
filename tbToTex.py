from model import missingParadigms, Alphabet
from parse import parseTB, parseStyle
from customStyle import createStyleFile
import sys


def user_input_style(stylefile):
    with open(stylefile) as style, open('dict.sty', 'w') as tex_style_file:
        stylelist = parseStyle(style)
        rules = createStyleFile(stylelist)

        tex_style_file.write('\\ProvidesPackage{dict}[2009]\n')
        tex_style_file.write('\\NeedsTeXFormat{LaTeX2e}[2001/06/01]\n')
        tex_style_file.write('\\RequirePackage{textcomp}\n')
        tex_style_file.write('\\RequirePackage{paralist}\n\n')
        for rule in rules:
            tex_style_file.write(rule + '\n')

    return stylelist


def user_alphabet(alph_file):
    with open(alph_file) as alph:
        letters = alph.read().decode('utf8').split()
    return Alphabet(letters)


def main(tbfile, stylelist=None, alphabet=None):
    with open(tbfile) as tb, open('texConvert.tex', 'w') as tex:
        tbtext = tb.read()
        entries = parseTB(tbtext, alphabet)
        print(len(entries))

        for entry in sorted(entries):
            tex.write(entry.toTex(stylelist) + '\n')

        print("Number of verb entries with missing paradigm information:")
        for paradigm in missingParadigms:
            print(paradigm + ": " + str(missingParadigms[paradigm]))


if __name__ == '__main__':
    main(sys.argv[1])
