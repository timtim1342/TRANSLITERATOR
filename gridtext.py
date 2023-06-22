from praatio import textgrid
from praatio.praatio_scripts import alignBoundariesAcrossTiers
from praatio.utilities.constants import Interval


class GridText:
    def __init__(self, filename, translation, cyrillic_transcription):
        self.filename = filename
        self.translation = translation
        self.cyrillic_transcription = cyrillic_transcription
        self.length = 5
        self.tiers = [translation, cyrillic_transcription]

    @classmethod
    def from_tg_file(cls, filepath, translation_name, cyrillic_transcription_name, align=False):

        if align:
            tg = alignBoundariesAcrossTiers(filepath, maxDifference=0.1)  # note! also merge blank values
            # !make it after loading cyr tg and tests!
        else:
            tg = textgrid.openTextgrid(filepath, includeEmptyIntervals=True)

        translation, cyrillic_transcription = tg.tierDict[translation_name], tg.tierDict[cyrillic_transcription_name]

        return GridText(filepath, translation, cyrillic_transcription)

    @classmethod
    def get_labels(cls, layer):
        entries = layer.entryList
        labels = [label for _, _, label in entries]

        return labels

    def transliterate_tg(self, latin_transcription_name, transliteration_dict):
        latin_transcription_entries = [
            (start, stop, ' '.join([transliterate(word, transliteration_dict) for word in label.split()]))
            for start, stop, label in self.cyrillic_transcription.entryList]

        latin_transcription = self.cyrillic_transcription.new(name=latin_transcription_name,
                                                              entryList=latin_transcription_entries)

        return GridTextTranscribed(self.filename, self.translation, self.cyrillic_transcription, latin_transcription)

    def replace_blank_translation(self):  # add Interval class and rewrite (repeat code in tests)
        transcription_entries = self.cyrillic_transcription.entryList
        translation_entries = self.translation.entryList

        for start_tc, stop_tc, label_tc in transcription_entries:
            for i, interval in enumerate(translation_entries):
                start_tl, stop_tl, label_tl = interval
                if start_tc == start_tl and label_tl == '' and len(label_tc) > 0:
                    self.translation.entryList[i] = Interval(start_tl, stop_tl, label_tc)
                    break

    def save_tg(self, save_path):
        tg = textgrid.Textgrid()
        for tier in self.tiers:
            tg.addTier(tier)
        tg.save(save_path, format="short_textgrid", includeBlankSpaces=True)


class GridTextTranscribed(GridText):
    concordance = {}

    def __init__(self, filename, translation, cyrillic_transcription, latin_transcription):
        super().__init__(filename, translation, cyrillic_transcription)
        self.latin_transcription = latin_transcription
        self.tiers.append(latin_transcription)

    @classmethod
    def from_tg_file(cls, filepath, translation_name, cyrillic_transcription_name, latin_transcription_name, align=False):

        if align:
            tg = alignBoundariesAcrossTiers(filepath, maxDifference=0.1)  # note! also merge blank values
            # !make it after loading cyr tg and tests!
        else:
            tg = textgrid.openTextgrid(filepath, includeEmptyIntervals=True)

        translation, cyrillic_transcription, latin_transcription = tg.tierDict[translation_name], \
            tg.tierDict[cyrillic_transcription_name], \
            tg.tierDict[latin_transcription_name]

        return GridTextTranscribed(filepath, translation, cyrillic_transcription, latin_transcription)

    def add_to_concordance(self):
        pass

def get_translit_dict(filename):  # old_version to rewrite
    with open(filename, 'r', encoding='UTF-8') as f:
        txt = f.read()
    txt_list = txt.split('\n')
    txt_list = [i.split(',') for i in txt_list]
    translit_dict = {i[0]: i[1] for i in txt_list if len(i) == 2 and i[0] != ''}

    translit_dict_cap = {}
    for key in translit_dict.keys(): #  ad capitals
        translit_dict_cap[key.capitalize()] = translit_dict[key].capitalize()
    translit_dict.update(translit_dict_cap)

    return translit_dict

def transliterate(word, transliteration_dict):
    word = '^' + word.replace('!', '1')  # .replace in case of Mehweb
    transliteration_dict = dict(sorted(transliteration_dict.items(), reverse=True, key=lambda x: len(x[0])))
    for sym in transliteration_dict.keys():
        word = word.replace(sym, transliteration_dict[sym])
    word = word.replace('^', '')
    return word

