import string

import praatio.utilities.errors
from praatio import textgrid
from praatio.praatio_scripts import alignBoundariesAcrossTiers
from praatio.utilities.constants import Interval
from collections import Counter

class GridText:
    def __init__(self, filename, translation, cyrillic_transcription):
        self.filename = filename
        self.translation = translation
        self.cyrillic_transcription = cyrillic_transcription
        #self.length =
        self.tiers = [translation, cyrillic_transcription]

    @classmethod
    def from_tg_file(cls, filepath, translation_name, cyrillic_transcription_name, align=False):

        if align:
            tg = alignBoundariesAcrossTiers(filepath, maxDifference=0.2)  # note! also merge blank values
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

    def transliterate(self, latin_transcription_name, transliteration_dict):
        latin_transcription_entries = [
            (start, stop, ' '.join([transliterate_string(word, transliteration_dict) for word in label.split()]))
            for start, stop, label in self.cyrillic_transcription.entryList]

        latin_transcription = self.cyrillic_transcription.new(name=latin_transcription_name,
                                                              entryList=latin_transcription_entries)

        return GridTextTranscribed(self.filename, self.translation, self.cyrillic_transcription, latin_transcription)

    def align_translation(self):  # add Interval class and rewrite (partially repeat code in tests)
        transcription_entries = self.cyrillic_transcription.entryList
        translation_entries = self.translation.entryList
        translation_entries_new = []
        translation_index = 0

        try:
            start_tl, stop_tl, label_tl = translation_entries[translation_index]
        except IndexError:
            start_tl, stop_tl, label_tl = 0, 0, ''

        for sentence_index, interval in enumerate(transcription_entries):
            start_tc, stop_tc, label_tc = interval
            new_label_tl = 'NO TRANSLATION'

            while start_tl <= start_tc and stop_tl <= stop_tc:
                if start_tc == start_tl and stop_tc == stop_tl:  # corresponding translation found (including empty)
                    new_label_tl = label_tl
                    break

                if translation_index + 1 < len(translation_entries):  # problem with the last entry
                    translation_index += 1
                    start_tl, stop_tl, label_tl = translation_entries[translation_index]
                else:
                    break

            translation_entries_new.append(Interval(start_tc, stop_tc, new_label_tl))

        self.translation.entryList = translation_entries_new

    def save_tg(self, save_path):
        tg = textgrid.Textgrid()
        for tier in self.tiers:
            tg.addTier(tier)
        tg.save(save_path, format="short_textgrid", includeBlankSpaces=True)


class GridTextTranscribed(GridText):
    concordance = Counter()

    def __init__(self, filename, translation, cyrillic_transcription, latin_transcription):
        super().__init__(filename, translation, cyrillic_transcription)
        self.latin_transcription = latin_transcription
        self.tiers.append(latin_transcription)

    @classmethod
    def from_tg_file(cls, filepath, translation_name, cyrillic_transcription_name, latin_transcription_name, align=False):

        tg = textgrid.openTextgrid(filepath, includeEmptyIntervals=True)

        if align:
            try:
                tg = alignBoundariesAcrossTiers(filepath, maxDifference=0.2)  # note! also merge blank values
                # !make it after loading cyr tg and tests!
            except praatio.utilities.errors.UnexpectedError:
                print(f'Alignment failed in {filepath}')

        translation, cyrillic_transcription, latin_transcription = tg.tierDict[translation_name], \
            tg.tierDict[cyrillic_transcription_name], \
            tg.tierDict[latin_transcription_name]

        return GridTextTranscribed(filepath, translation, cyrillic_transcription, latin_transcription)

    def add_to_concordance(self):
        words = ' '.join(GridTextTranscribed.get_labels(self.latin_transcription)).translate(str.maketrans('', '', string.punctuation)).split()
        GridTextTranscribed.concordance.update(words)


def get_translit_dictionary(dictionary_path, separator=';'):
    """parse the csv file with symbol pairs and transfer it to the dict type"""

    with open(dictionary_path, 'r', encoding='UTF-8') as f:
        raw_dictionary = [pair.split(separator) for pair in f.read().split('\n')]
    translit_dictionary = {pair[0]: pair[1] for pair in raw_dictionary if len(pair) == 2 and pair[0] != ''}
    translit_dictionary.update({key.capitalize(): translit_dictionary[key].capitalize()
                                for key in translit_dictionary.keys()})   # add capitals

    return translit_dictionary


def transliterate_string(word, translit_dictionary):
    """transliterates a string"""

    word = '^' + word
    translit_dictionary = dict(sorted(translit_dictionary.items(), reverse=True, key=lambda x: len(x[0])))

    for cyrillic_symbol in translit_dictionary.keys():
        latin_symbol = translit_dictionary[cyrillic_symbol]
        word = word.replace(cyrillic_symbol, latin_symbol)
    word = word.replace('^', '')
    return word


def transliterate_tg(tg_path, translit_dictionary, tier_names, latin_tier_name, replace_blanc_translation=False):
    """transliterates a TextGrid file"""

    tg = GridText.from_tg_file(tg_path, *tier_names)
    transliterated_tg = tg.transliterate(latin_tier_name, translit_dictionary)

    if replace_blanc_translation:
        tg.replace_blank_translation()

    output_path = tg_path.replace('cyrillic_textgrids', 'latin_textgrids')
    transliterated_tg.save_tg(output_path)
