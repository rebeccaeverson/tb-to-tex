import itertools
import unicodedata as u
import sys

missingParadigms = {field: 0 for field in ["perfect", "imperfect", "agent sing.", "agent plur.",
	"agent -aa sing.", "agent -aa plur."]}

class Entry:

	def __init__(self, fields):
		try:
			self.lx = fields['lx']
			self.ph = fields['ph'].strip('/')
			self.ps = fields.get('ps', "")
			self.hm = fields.get('hm', "")
			self.senses = fields['senses']
			self.pdl = fields['pdl']
			self.pdv = fields['pdv']
			self.sg = fields.get('sg', "")
			self.onep = fields.get('1p', "")
			self.twop = fields.get('2p', "")
			self.va = fields['va']
			self.subentries = fields['subentries']
		except KeyError as e:
			print(e)
			print(self.lx)

	def toTex(self):
		string = "\\tbLX{{{lex}}} \\tbHM{{{hom}}} \\tbPH{{{phone}}} \\tbPS{{{part}}} ".format(lex = self.lx,
			phone = self.ph, part = self.ps, hom = self.hm)
		for sense in self.senses:
			if 'sn' in sense:
				string += "\\tbSN "
			if 'ps' in sense:
				string += "\\tbPS{{{ps}}} ".format(ps = sense['ps'])
			string += "\\tbGE{{{eng}}} ".format(eng = sense['ge'])
			for example, translation in zip(sense['xv'], sense['xe']):
				if example != "":
					string += "\\tbXV{{{xv}}} \\tbXE{{{xe}}} ".format(xv = example, xe = translation)

		if self.ps == "v.~":
			#zip together paradigm labels and values, map values to labels in dictionary
			paradigmDict = {label: value for label, value in zip(self.pdl, self.pdv)}
	
			#count how many of each paradigm label is missing a value
			for paradigm in missingParadigms:
				if paradigmDict.get(paradigm, "") == "":
					missingParadigms[paradigm] += 1

			#include paradigm values for perfect, imperfect, agent sing., agent plur., 
			#agent -aa sing., and agent -aa plur. in that order. If one of the paradigm
			#values does not exist, replace with a dash.
			paradigmString = "{perf}, {imperf}, {agsing}, {agplur}, {aasing}, {aaplur} ".format(
				perf = paradigmDict.get("perfect", "-") or "-",
				imperf = paradigmDict.get("imperfect", "-") or "-",
				agsing = paradigmDict.get("agent sing.", "-") or "-",
				agplur = paradigmDict.get("agent plur.", "-") or "-",
				aasing = paradigmDict.get("agent -aa sing.", "-") or "-",
				aaplur = paradigmDict.get("agent -aa plur.", "-") or "-")

			string += "\\tbPD{{{paradigms}}} ".format(paradigms = paradigmString)

		if self.ps == "n~" or self.ps == "n.~":
			if self.sg != "":
				string += "\\tbSG{{{sing}}} ".format(sing = self.sg)
			if self.onep != "":
				string += "\\tbOP{{{onep}}} ".format(onep = self.onep)
			if self.twop != "":
				string += "\\tbTP{{{twop}}} ".format(twop = self.twop)

		if self.ps == "adj~" or self.ps == "adj.~":
			if self.onep != "":
				string += "\\tbOP{{{onep}}} ".format(onep = self.onep)
			if self.twop != "":
				string += "\\tbTP{{{twop}}} ".format(twop = self.twop)

		variantForms = ""
		for v in self.va:
			string += "\\tbVA{{{var}}}".format(var = v)

		for k, v in self.subentries:
			string += "\\tbSE{{{sub}}} \\tbGE{{{eng}}} ".format(sub = k, eng = v)

		return string

#escape characters in Latex
def escape(text):
	string = ""
	specialChars = ['_', '\\', '&', '#', '{', '}']

	#replacing inconsistent characters with the "standard" character - some entries were entered
	#into Word before Toolbox, and this copying over produced some 'weird' characters
	subs = {'GREEK SMALL LETTER EPSILON': 'LATIN SMALL LETTER OPEN E', 
			'COMBINING ACUTE TONE MARK': 'COMBINING ACUTE ACCENT',
			'COMBINING GRAVE TONE MARK': 'COMBINING GRAVE ACCENT',
			'COMBINING GREEK PERISPOMENI': 'COMBINING CIRCUMFLEX ACCENT',
			'GREEK TONOS': 'COMBINING ACUTE ACCENT',
			'GRAVE ACCENT': 'COMBINING GRAVE ACCENT',
			'GREEK SMALL LETTER IOTA': 'LATIN LETTER SMALL CAPITAL I'}
	
	#take the name of the characters from subs dicionary and turn them into the hex codes for
	#those letters
	hexsubs = {u.lookup(k).encode('utf8'): u.lookup(v).encode('utf8') for k,v in subs.items()}

	for k,v in hexsubs.items():
		text = text.replace(k, v)

	for c in text:
		if c in specialChars:
			string += '\\' + c
		else:
			string += c

	return string

def parseTB(text):

	ignored = ['dt', 'nq', 'pd', 'so', 'es', 'de', 'nt']
	#senses includes examples (xv, xe) even if there isn't an "sn" marker to go with them
	multiple = ['pdl', 'pdv', 'senses','subentries', 'va']
	#fields that can appear after 'sn' (included in the sense)
	snFields = ['ge', 'nt', 'xv', 'xe', 'ps']

	#split the file of Toolbox entries into a list of entries, where the beginning of each new 
	#entry is marked by the \lx character sequence (requires that the first field in each
	#Toolbox entry is \lx)
	tbEntries = text.replace('\r\n', '\n').split('\\lx')
	entries = []

	for tbEntry in tbEntries[1:]:
		#filter out all empty lines
		entryList = filter(lambda e: e != '', tbEntry.split('\n'))
		#add \lx field marker back to the first line
		
		lexeme = entryList[0]
		entryList[0] = '\\lx' + entryList[0]

		#changed from list to iterator to make sure each entry is accessed once
		entryList = iter(entryList)

		#create a dictionary for all of the markers, make the entry in the dictionary a list for all
		#of the markers that can appear multiple times in an entry
		fields = {marker: [] for marker in multiple}
		while True:
			try:
				entry = next(entryList)
			except StopIteration:
				break

			#parse to get the field marker and the field entry
			marker = entry.strip(' ').split(' ')[0].strip('\\')
			value = ' '.join(entry.strip(' ').split(' ')[1:])
			value = escape(value)

			#If the marker 'se' appears, parse the following 'ge' accordingly
			if marker == "se":
				engGloss = next(entryList)
				engGloss = engGloss.strip(' ').split(' ')
				assert engGloss[0].strip('\\') == "ge", "Subentry does not have English gloss: " + lexeme
				fields["subentries"].append((value, ' '.join(engGloss[1:])))

			#group sense number markers (ge, xv, xe) together in a dictionary for each sense
			#if there is no 'sn' field in the entry, then start with 'ge'
			if marker == "sn" or marker == "ge":
				fields["senses"].append({marker: value, "xv": [], "xe": []})
				for snEntry in entryList:
					#same as above
					snmarker = snEntry.strip(' ').split(' ')[0].strip('\\')
					snvalue = ' '.join(snEntry.strip(' ').split(' ')[1:])
					snvalue = escape(snvalue)

					if snmarker in snFields:
						if snmarker == "xv" or snmarker == "xe":
							#add the marker and field to the most recent dictionary in the list of senses
							fields["senses"][-1][snmarker].append(snvalue)
						else:
							fields["senses"][-1][snmarker] = snvalue
					else:
						#put most recent that has been iterated through back into the entry list
						entryList = itertools.chain([snEntry], entryList)
						break
				#go back to the outer loop
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

if __name__ == '__main__':
	tbfile = sys.argv[1]

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
