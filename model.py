missingParadigms = {field: 0
                    for field in ["perfect", "imperfect", "agent sing.",
                                  "agent plur.", "agent -aa sing.",
                                  "agent -aa plur."]}

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