# coding=utf-8

missingParadigms = {field: 0
                    for field in ["perfect", "imperfect", "agent sing.",
                                  "agent plur.", "agent -aa sing.",
                                  "agent -aa plur."]}

double_char = ['gb', 'gy', 'kp', 'ky', 'ny', u'ŋm']
alphabet = [
    'a', 'b', 'd', 'e', u'ɛ', 'f', 'g', 'gb', 'gy', 'h', 'i', 'k',
    'kp', 'ky', 'l', 'm', 'n', 'ny', u'ŋ', u'ŋm', 'o', u'ɔ', 'p', 'r', 's',
    't', 'u', 'v', 'w', 'y', 'z']


class Entry:
    def __init__(self, fields):
        try:
            self.lx = fields['lx']
            #self.ph = fields['ph'].strip('/')
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

    def __lt__(self, other):
        lx1 = self.lx.decode('utf8').lower()
        lx2 = other.lx.decode('utf8').lower()
        ph1 = self.ph.decode('utf8').lower()
        ph2 = other.ph.decode('utf8').lower()

        idx1 = 0
        idx2 = 0

        while idx1 < len(lx1) and idx2 < len(lx2):
            if lx1[idx1:idx1+2] in double_char:
                char1 = lx1[idx1:idx1+2]
            else:
                char1 = lx1[idx1]
            if lx2[idx2:idx2+2] in double_char:
                char2 = lx2[idx2:idx2+2]
            else:
                char2 = lx2[idx2]

            try:
                pos1 = alphabet.index(char1)
            except ValueError:
                idx1 += len(char1)
                continue
            try:
                pos2 = alphabet.index(char2)
            except ValueError:
                idx2 += len(char2)
                continue

            if pos1 == pos2:
                idx1 += len(char1)
                idx2 += len(char2)
            else:
                return pos1 < pos2

        return len(lx1) < len(lx2)

    def toCustomTex(self, styledict):
        string = ''
        for item in styledict:
            label = item[0].upper()
            if label == 'GE':
                ge = self.senses[0]['ge']
                string += '\\tb{0}{{{value}}} '.format(label, value=ge)
            else:
                string += '\\tb{0}{{{value}}} '.format(label, value=getattr(self, item[0]))
        return string

    def toTex(self):
        string = "\\tbLX{{{lex}}} \\tbHM{{{hom}}} " \
                 "\\tbPH{{{phone}}} \\tbPS{{{part}}} ".format(lex=self.lx,
                                                              phone=self.ph,
                                                              part=self.ps,
                                                              hom=self.hm)
        for sense in self.senses:
            if 'sn' in sense:
                string += "\\tbSN "
            if 'ps' in sense:
                string += "\\tbPS{{{ps}}} ".format(ps=sense['ps'])
            string += "\\tbGE{{{eng}}} ".format(eng=sense['ge'])
            for example, translation in zip(sense['xv'], sense['xe']):
                if example != "":
                    string += "\\tbXV{{{xv}}} \\tbXE{{{xe}}} ".format(xv=example, xe=translation)

        if self.ps == "v.~":
            # zip together paradigm labels and values, map values to labels in dictionary
            paradigmDict = {label: value for label, value in zip(self.pdl, self.pdv)}

            # count how many of each paradigm label is missing a value
            for paradigm in missingParadigms:
                if paradigmDict.get(paradigm, "") == "":
                    missingParadigms[paradigm] += 1

            # include paradigm values for perfect, imperfect, agent sing.,
            # agent plur., agent -aa sing., and agent -aa plur. in that order.
            # If one of the paradigm values does not exist, replace with a dash.
            paradigmString = "{perf}, {imperf}, {agsing}, {agplur}, {aasing}, {aaplur} ".format(
                perf=paradigmDict.get("perfect", "-") or "-",
                imperf=paradigmDict.get("imperfect", "-") or "-",
                agsing=paradigmDict.get("agent sing.", "-") or "-",
                agplur=paradigmDict.get("agent plur.", "-") or "-",
                aasing=paradigmDict.get("agent -aa sing.", "-") or "-",
                aaplur=paradigmDict.get("agent -aa plur.", "-") or "-")

            string += "\\tbPD{{{paradigms}}} ".format(paradigms=paradigmString)

        if self.ps == "n~" or self.ps == "n.~":
            if self.sg != "":
                string += "\\tbSG{{{sing}}} ".format(sing=self.sg)
            if self.onep != "":
                string += "\\tbOP{{{onep}}} ".format(onep=self.onep)
            if self.twop != "":
                string += "\\tbTP{{{twop}}} ".format(twop=self.twop)

        if self.ps == "adj~" or self.ps == "adj.~":
            if self.onep != "":
                string += "\\tbOP{{{onep}}} ".format(onep=self.onep)
            if self.twop != "":
                string += "\\tbTP{{{twop}}} ".format(twop=self.twop)

        variantForms = ""
        for v in self.va:
            string += "\\tbVA{{{var}}}".format(var=v)

        for k, v in self.subentries:
            string += "\\tbSE{{{sub}}} \\tbGE{{{eng}}} ".format(sub=k, eng=v)

        return string