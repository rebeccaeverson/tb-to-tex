def createStyleFile(stylelist):
    rules = []
    for field, isBold, isEmph, size in stylelist:
        size = int(size)
        first_element = stylelist[0][0]
        line = '\\newcommand\\tb{0}[1] {{'.format(field.upper())
        brackets = 1
        if field == first_element:
            line += '\\item['
        if isBold:
            line += '\\textbf{'
            brackets += 1
        if isEmph:
            line += '\\emph{'
            brackets += 1
        if field == first_element:
            line += '\\fontsize{{{0}}}{{{1}}}\\selectfont #1{2}]}}'.format(size, 1.2*size, (brackets-1)*'}')
        else:
            line += '\\fontsize{{{0}}}{{{1}}}\\selectfont #1{2}'.format(size, 1.2*size, brackets*'}')
        rules.append(line)
    return rules