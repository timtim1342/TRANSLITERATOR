from os import walk
from os.path import join
from gridtext import transliterate_tg, get_translit_dictionary

# import logging
# from os import listdir, walk
# from os.path import join
from gridtext import GridText, GridTextTranscribed
# from heap import make_heap
from tests import TestGridText, TestTextGridFile
#
#
# if name == 'main':
#     for root, dirs, files in walk('cyrillic_textgrids'):
#         for filename in files:
#
#             # try:
#             #     test_test = TestTextGridFile(path_to_test_tg)
#             #     test_test.test_tier_names(tiernames)
#             # except KeyError as ex:
#             #     print(ex)
#             tiernames = ['2', '1']
#             path_to_test_tg = join('cyrillic_textgrids', filename)
#
#             # replace blank translation of russian in transcription
#             try:
#                 test_tg = GridText.from_tg_file(path_to_test_tg, *tiernames)
#                 test_tg.replace_blank_translation()
#             except:
#                 print(path_to_test_tg)
#                 raise StopIteration
#             # transliterate
#             translit_dict = get_translit_dict('transl_dict.csv')
#             transliterated_test_tg = test_tg.transliterate_tg('3', translit_dict)
#             print(GridTextTranscribed.get_labels(transliterated_test_tg.latin_transcription))
#
#             # save
#             path_to_test_tg_save = join('latin_textgrids', filename)
#             transliterated_test_tg.save_tg(path_to_test_tg_save)
#
#             # align boundaries and save
#             tiernames.append('3')
#             transliterated_test_tg = GridTextTranscribed.from_tg_file(path_to_test_tg_save, *tiernames, align=False)
#             transliterated_test_tg.save_tg(path_to_test_tg_save)
#
#             # test boundaries
#             test_test = TestGridText(transliterated_test_tg)
#             test_test.test_interval_boundaries()
#
#             # # heap
#             # path_to_test_tg = join('latin_textgrids', 'tkt2019_aishat_a.TextGrid')
#             # make_heap(transliterated_test_tg)

tier_names = ['2', '1']  # [translation tier, transcription tier]
latin_tier = '3'
translit_dictionary = get_translit_dictionary('transl_dict_kina.csv')  # name of transliteration dictionary

for root, dirs, files in walk('cyrillic_textgrids'):
    for filename in files:
        print(f'start of transliteration: {filename}')

        try:
            path_to_tg = join('cyrillic_textgrids', filename)

            # Test 1: tier names
            test_test = TestTextGridFile(path_to_tg)
            test_test.test_tier_names(tier_names)

            # Transliterate and save
            transliterate_tg(path_to_tg, translit_dictionary, tier_names, latin_tier)

            # Align
            latin_tier_names = ['2', '1', '3']
            transliterated_tg = GridTextTranscribed.from_tg_file(path_to_tg.replace('cyrillic_textgrids', 'latin_textgrids'), *latin_tier_names, align=True)

            # Test 2: no translation
            test_test = TestGridText(transliterated_tg)
            test_test.test_interval_boundaries()

            # Save
            transliterated_tg.save_tg(path_to_tg.replace('cyrillic_textgrids', 'latin_textgrids'))

            print(f'Transliterartion DONE: {filename}')

        except Exception as ex:
            print(f'Exception:\n{ex}')