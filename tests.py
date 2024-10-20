from gridtext import GridText, GridTextTranscribed, transliterate_tg
from praatio import textgrid
from setup_logger import logger


class TestTextGridFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def test_tier_names(self, tier_names):
        """ check if there are tiers with given names in the textgrid """
        tg_tiers = textgrid.openTextgrid(self.filepath, includeEmptyIntervals=True).tierNameList

        if not set(tier_names).issubset(set(tg_tiers)):
            mess = f'One or more of the tier names {tier_names} is not found in {self.filepath}'
            logger.warning(mess)
            raise KeyError(mess)

class TestGridText:
    def __init__(self, test_tg):
        self.test_tg = test_tg

    def test_interval_boundaries(self):
        """ check if there are non-aligned boundaries between tiers"""
        transcription_entries = self.test_tg.cyrillic_transcription.entryList
        translation_entries = self.test_tg.translation.entryList
        for start_tc, stop_tc, label_tc in transcription_entries:  # make short
            for start_tl, stop_tl, label_tl in translation_entries:
                if start_tc == start_tl:
                    break

            else:
                mess = f'No corresponding translation in {self.test_tg.filename} for {start_tc}, {stop_tc}, {label_tc}'
                #print(mess)
                logger.warning(mess)

