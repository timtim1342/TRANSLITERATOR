import logging
from os import listdir
from os.path import join
from gridtext import GridText, GridTextTranscribed, transliterate
from heap import make_heap
from tests import TestGridText, TestTextGridFile





def translit_dict():  # old_version to rewrite
    with open('transl_dict.csv', 'r', encoding='UTF-8') as f:
        txt = f.read()
    txt_list = txt.split('\n')
    txt_list = [i.split(',') for i in txt_list]
    translit_dict = {i[0]: i[1] for i in txt_list if len(i) == 2 and i[0] != ''}

    translit_dict_cap = {}
    for key in translit_dict.keys(): #  ad capitals
        translit_dict_cap[key.capitalize()] = translit_dict[key].capitalize()
    translit_dict.update(translit_dict_cap)

    return translit_dict


if __name__ == '__main__':
    path_to_test_tg = join('cyrillic_textgrids', 'tkt2019_aishat_a.TextGrid')
    tiernames = ['2', '1']

    # try:
    #     test_test = TestTextGridFile(path_to_test_tg)
    #     test_test.test_tier_names(tiernames)
    # except KeyError as ex:
    #     print(ex)

    # replace blank translation of russian in transcription
    test_tg = GridText.from_tg_file(path_to_test_tg, *tiernames)
    test_tg.replace_blank_translation()

    # transliterate
    transliterated_test_tg = test_tg.transliterate_tg('3', translit_dict())
    print(GridTextTranscribed.get_labels(transliterated_test_tg.latin_transcription))

    # save
    path_to_test_tg_save = join('latin_textgrids', 'test_tkt2019_aishat_a.TextGrid')
    transliterated_test_tg.save_tg(path_to_test_tg_save)

    # align boundaries and save
    tiernames.append('3')
    transliterated_test_tg = GridTextTranscribed.from_tg_file(path_to_test_tg_save, *tiernames, align=True)
    transliterated_test_tg.save_tg(path_to_test_tg_save)

    # test boundaries
    test_test = TestGridText(transliterated_test_tg)
    test_test.test_interval_boundaries()

    # # heap
    # path_to_test_tg = join('latin_textgrids', 'tkt2019_aishat_a.TextGrid')
    # make_heap(transliterated_test_tg)
