import itertools
import unicodedata as u

from model import Entry


# escape characters in Latex
def escape(text):
    string = ""
    specialChars = ['_', '\\', '&', '#', '{', '}']

    # replacing inconsistent characters with the "standard" character - some
    # entries were entered into Word before Toolbox, and this copying over
    # produced some 'weird' characters
    subs = {'GREEK SMALL LETTER EPSILON': 'LATIN SMALL LETTER OPEN E',
            'COMBINING ACUTE TONE MARK': 'COMBINING ACUTE ACCENT',
            'COMBINING GRAVE TONE MARK': 'COMBINING GRAVE ACCENT',
            'COMBINING GREEK PERISPOMENI': 'COMBINING CIRCUMFLEX ACCENT',
            'GREEK TONOS': 'COMBINING ACUTE ACCENT',
            'GRAVE ACCENT': 'COMBINING GRAVE ACCENT',
            'GREEK SMALL LETTER IOTA': 'LATIN LETTER SMALL CAPITAL I'}

    # take the name of the characters from subs dicionary and turn them into
    # the hex codes for those letters
    hexsubs = {u.lookup(k).encode('utf8'): u.lookup(v).encode('utf8')
               for k, v in subs.items()}

    for k, v in hexsubs.items():
        text = text.replace(k, v)

    for c in text:
        if c in specialChars:
            string += '\\' + c
        else:
            string += c

    return string


def parseStyle(stylefile):
    # Take a custom style template and return a list of
    # rules in tuple form
    stylelist = []
    counter = 0
    for line in stylefile:
        rules = line.strip('\n').split(',')
        label = rules[0]
        isBold = rules[1] == 'true'
        isEmph = rules[2] == 'true'
        textSize = rules[3]
        stylelist.append((label, isBold, isEmph, textSize))
    return stylelist


def parseTB(text):

    ignored = ['dt', 'nq', 'pd', 'so', 'es', 'de', 'nt']
    # senses includes examples (xv, xe) even if there isn't an "sn" marker to
    # go with them
    multiple = ['pdl', 'pdv', 'senses', 'subentries', 'va']
    # fields that can appear after 'sn' (included in the sense)
    snFields = ['ge', 'nt', 'xv', 'xe', 'ps']

    # split the file of Toolbox entries into a list of entries, where the
    # beginning of each new entry is marked by the \lx character sequence
    # (requires that the first field in each Toolbox entry is \lx)
    tbEntries = text.replace('\r\n', '\n').split('\\lx')
    entries = []

    for tbEntry in tbEntries[1:]:
        # filter out all empty lines
        entryList = filter(lambda e: e != '', tbEntry.split('\n'))
        # add \lx field marker back to the first line

        lexeme = entryList[0]
        entryList[0] = '\\lx' + entryList[0]

        # changed from list to iterator to make sure each entry is accessed once
        entryList = iter(entryList)

        # create a dictionary for all of the markers, make the entry in the
        # dictionary a list for all of the markers that can appear multiple
        # times in an entry
        fields = {marker: [] for marker in multiple}
        while True:
            try:
                entry = next(entryList)
            except StopIteration:
                break

            # parse to get the field marker and the field entry
            marker = entry.strip(' ').split(' ')[0].strip('\\')
            value = ' '.join(entry.strip(' ').split(' ')[1:])
            value = escape(value)

            # If the marker 'se' appears, parse the following 'ge' accordingly
            if marker == "se":
                engGloss = next(entryList)
                engGloss = engGloss.strip(' ').split(' ')
                assert engGloss[0].strip('\\') == "ge", "Subentry does not have English gloss: " + lexeme
                fields["subentries"].append((value, ' '.join(engGloss[1:])))

            # group sense number markers (ge, xv, xe) together in a dictionary
            # for each sense if there is no 'sn' field in the entry, then start
            # with 'ge'
            if marker == "sn" or marker == "ge":
                fields["senses"].append({marker: value, "xv": [], "xe": []})
                for snEntry in entryList:
                    # same as above
                    snmarker = snEntry.strip(' ').split(' ')[0].strip('\\')
                    snvalue = ' '.join(snEntry.strip(' ').split(' ')[1:])
                    snvalue = escape(snvalue)

                    if snmarker in snFields:
                        if snmarker == "xv" or snmarker == "xe":
                            # add the marker and field to the most recent
                            # dictionary in the list of senses
                            fields["senses"][-1][snmarker].append(snvalue)
                        else:
                            fields["senses"][-1][snmarker] = snvalue
                    else:
                        # put most recent that has been iterated through back
                        # into the entry list
                        entryList = itertools.chain([snEntry], entryList)
                        break
                # go back to the outer loop
                assert "ge" in fields["senses"][-1], "English gloss not in sense: " + lexeme
                continue

            if marker in ignored:
                continue

            elif marker in multiple:
                if marker == 'va' and value != '':
                    fields[marker].append(value)
                elif marker != 'va':
                    fields[marker].append(value)

            else:
                fields[marker] = value

        entries.append(Entry(fields))

    return entries