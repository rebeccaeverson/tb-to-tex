from model import missingParadigms, Entry
from parse import parseTB, parseStyle


def user_input_style(tbfile, stylefile):
	tb = open(tbfile)
	text = tb.read()
	style = open(stylefile)
	output = open('texConvert.tex', 'w')
	entries = parseTB(text)
	stylelist = parseStyle(style)

	for entry in entries:
		output.write(entry.toCustomTex(stylelist) + '\n')


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
