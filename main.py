from os import walk
from os.path import join
from gridtext import GridTextTranscribed, transliterate_tg, get_translit_dictionary
from heap import make_heap, counts
from tests import TestGridText, TestTextGridFile

tier_names = ['2', '1']  # [translation tier, transcription tier]
latin_tier = '3'
translit_dictionary = get_translit_dictionary('transl_dict_tukita.csv', separator=',')  # name of transliteration dictionary

with open("text_heap.html", 'w', encoding="UTF-16") as html:
    pass

for root, dirs, files in walk('cyrillic_textgrids'):
    for filename in files:
        #print(f'start of transliteration: {filename}')

        try:
            path_to_tg = join('cyrillic_textgrids', filename)
            path_to_transliterated_tg = path_to_tg.replace('cyrillic_textgrids', 'latin_textgrids')

            # Test 1: tier names
            test_test = TestTextGridFile(path_to_tg)
            test_test.test_tier_names(tier_names)

            # Transliterate and save
            transliterate_tg(path_to_tg, translit_dictionary, tier_names, latin_tier)

            # Align
            latin_tier_names = ['2', '1', '3']
            transliterated_tg = GridTextTranscribed.from_tg_file(path_to_transliterated_tg,
                                                                 *latin_tier_names,
                                                                 align=True)  # note! also merge blank values

            # Test 2: no translation
            test_test = TestGridText(transliterated_tg)
            test_test.test_interval_boundaries()

            # Save
            transliterated_tg.save_tg(path_to_transliterated_tg)

            # Align translation and transcription by fulfilling empty translation intervals
            transliterated_tg.align_translation()

            #print(f'Transliterartion DONE: {filename}')

            # Heap (light version)
            make_heap(transliterated_tg)

            # Count unique words
            transliterated_tg.add_to_concordance()

        except Exception as ex:
            print(f'Exception in {filename}:\n{ex}')

    # Heap statistics
    counts(GridTextTranscribed.concordance)
