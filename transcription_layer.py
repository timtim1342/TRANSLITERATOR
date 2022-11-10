import logging
from os import listdir
from os.path import join
from praatio import textgrid
from praatio.praatio_scripts import alignBoundariesAcrossTiers


def tg2tg_obj(file_name):
    tg = textgrid.openTextgrid(file_name, includeEmptyIntervals=True)
    return tg


def tg_obj2tg(tg, file_name):
    tg.save(file_name, format="short_textgrid", includeBlankSpaces=True)


def align_tg(file_name):  # note! also merge blank values
    tg_obj2tg(alignBoundariesAcrossTiers(file_name, maxDifference=0.1), file_name)


def replace_blank_translation(file_name):  # new_version to rewrite. save outside the func
    """
    Without this translation will move in the heap.
    Write NULL where there is smth in transcription, but corresponding translation is empty.
    """
    tg = tg2tg_obj(file_name)
    transcription_entries = tg.tierDict['1'].entryList
    translation_entries = tg.tierDict['2'].entryList
    new_translation_entries = [(start, stop, label) for start, stop, label in translation_entries]
    translation = tg.removeTier('2')

    logger = logging.getLogger('logger')
    logging.basicConfig(level=logging.INFO, filename="error_heap.log", filemode="w")
    logger.info(f'{file_name}')

    for start_tc, stop_tc, label_tc in transcription_entries:
        i = 0
        translation_found = False

        for start_tl, stop_tl, label_tl in translation_entries:
            if start_tc == start_tl:
                translation_found = True
                if label_tl == '' and len(label_tc) > 0:
                    new_translation_entries[i] = (start_tl, stop_tl, 'NULL')
                break
            i += 1

        if not translation_found:
            mess = f'No translation in {file_name} for {start_tc}, {stop_tc}, {label_tc}'
            print(mess)
            logger.warning(mess)
    logger.info(f'END\n')
    new_translation_entries.sort(key=lambda x: x[0])

    new_translation = translation.new(name='2', entryList=new_translation_entries)
    tg.addTier(new_translation)
    tg_obj2tg(tg, file_name)


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


def transliterator(word, transliteration_dict):
    for sym in transliteration_dict.keys():
        word = word.replace(sym, transliteration_dict[sym])
    if word.startswith(('e', 'ё')):
        word = 'j' + word
    elif word.startswith(('E', 'Ё')):
        word = 'J' + word
    return word


def translitirated_tg(tg):
    transliteration_dict = translit_dict()
    transcription = tg.tierDict['1']

    transcription_lat_entries = [(start, stop, ' '.join([transliterator(word, transliteration_dict) for word in label.split()]))
                                 for start, stop, label in transcription.entryList]

    transcription_lat = transcription.new(name='5', entryList=transcription_lat_entries)
    tg.addTier(transcription_lat)
    return tg


def translit_all():
    input_dir, output_dir = 'cyrillic_textgrids', 'latin_textgrids'

    for tg_name in listdir(input_dir):
        tg_input_path, tg_output_path = join(input_dir, tg_name), join(output_dir, tg_name)

        try:
            tg = tg2tg_obj(tg_input_path)
            new_tg = translitirated_tg(tg)
            tg_obj2tg(new_tg, tg_output_path)

        except Exception as ex:
            print(f' Error when transliterating {tg_name}: {ex}')

        # try:
        #     align_tg(tg_output_path)
        #
        # except Exception as ex:
        #     print(f' Error when aligning {tg_name}: {ex}')

        try:
            replace_blank_translation(tg_output_path)

        except Exception as ex:
            print(f' Error when replacing empty translation {tg_name}: {ex}')

def main():
    translit_all()

if __name__ == '__main__':
    main()
