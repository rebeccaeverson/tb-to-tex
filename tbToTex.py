from model import missingParadigms, Entry
from parse import parseTB, parseStyle
from customStyle import createStyleFile


def user_input_style(tbfile, stylefile):
    tb = open(tbfile)
    text = tb.read()
    style = open(stylefile)
    output = open('texConvert.tex', 'w')
    entries = parseTB(text)
    stylelist = parseStyle(style)
    rules = createStyleFile(stylelist)

    tex_style_file = open('dict.sty', 'w')
    tex_style_file.write('\\ProvidesPackage{dict}[2009]\n')
    tex_style_file.write('\\NeedsTeXFormat{LaTeX2e}[2001/06/01]\n')
    tex_style_file.write('\\RequirePackage{textcomp}\n')
    tex_style_file.write('\\RequirePackage{paralist}\n\n')
    for rule in rules:
        tex_style_file.write(rule + '\n')

    for entry in entries:
       output.write(entry.toCustomTex(stylelist) + '\n')

    tb.close()
    style.close()
    output.close()
    tex_style_file.close()


def main(tbfile):
    file = open(tbfile)
    outputfile = open("texConvert.tex", 'w')
    text = file.read()
    entries = parseTB(text)
    print(len(entries))

    for entry in entries:
        outputfile.write(entry.toTex() + '\n')

    print("Number of verb entries with missing paradigm information:")
    for paradigm in missingParadigms:
        print(paradigm + ": " + str(missingParadigms[paradigm]))


if __name__ == '__main__':
    main(sys.argv[1])
