import MeCab
import get_kanjidict
import get_mecab_data as get_mecab

import sys
import pprint
import tomllib
from typing import Dict, Tuple

MIN_VERSION = (3,11)
if sys.version_info < MIN_VERSION:
    print(f"FAILURE: This script requires Python {MIN_VERSION[0]}.{MIN_VERSION[1]} or higher. Exiting.")
    sys.exit(1)

def process_toml(debug_toml:bool=True, debug_kanji_to_component:bool=True) -> Tuple[Dict[str,str], Dict[str,str]]:
    # Read over the Toml and create a mapping from used_in -> component. And used_in -> readings list Eg:
    #
    # This toml:
    # component = "又"
    # used_in = ["受", "授"]
    # readings = ["ジュ"]
    #
    # Creates this mapping:
    # 受 -> 又 and 授 -> 又 
    # 
    # 受 -> ["ジュ"] and 授 -> ["ジュ"]
    print("Processing Toml")

    with open('phonetic.toml', 'rb') as f:
        kanji_data = tomllib.load(f)['useful']
    
    if debug_toml:
        print("Processed Phonetic.toml into in-memory dictionary:")
        pprint.pprint(kanji_data, sort_dicts=False)

    kanji_component = {}
    kanji_readings = {}
    for entry in kanji_data:
        for kanji in entry['used_in']:
            kanji_component[kanji] = entry['component']
            kanji_readings[kanji] = entry['readings']

    if debug_kanji_to_component:
        print("kanji_component dictionary:")
        pprint.pprint(kanji_component, sort_dicts=False)
        print("============================")
        print("kanji_readings:")
        pprint.pprint(kanji_readings, sort_dicts=False)

    return kanji_component, kanji_readings




def get_freqs(kanji_component, kanji_readings, kanji_dict):
    tagger = MeCab.Tagger(f"-r /dev/null -d {get_mecab.default_path}")

    with open(sys.argv[1], 'r') as corpus:
        for sentence in corpus: 
            get_mecab.get_mecab_data(sentence, verbose=False, tagger=tagger)
 


kanji_component, kanji_readings = process_toml()
kanji_dict = get_kanjidict.get_readings_dictionary()
get_freqs(kanji_component, kanji_readings, kanji_dict)