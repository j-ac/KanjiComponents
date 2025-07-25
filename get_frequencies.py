import MeCab
import get_kanjidict
import get_mecab_data as get_mecab
import jp_utils as jp

import sys
import pprint
import re
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
    # Maps this in the kanji_component dictionary:
    # 受 -> 又 and 授 -> 又 
    # 
    # And this in kanji_readings dictionary:
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

# Turns a word which may contain a mix of hiragana, katakana and kanji into just the readings of the kanji, in katakana.
# Eg 楽しい -> タノ
def word_to_kanji_readings(word, data) -> str:
    # Example: 楽しい 
    if "form" in data:
        form = data["form"]                 # eg タノシイ
    else:
        return

    kata = jp.hiragana_to_katakana(word)    # eg 楽しい　-> 楽シイ

    # Kanji within a word are always contiguous. So matching the first group of .* kanji will always grab the full set of kanji in the word.
    regex_str = ""
    i = 0
    # Append all non-kanji characters at onset, if any.
    while i < len(kata) and not jp.is_kanji(kata[i]):
        regex_str += kata[i]
        i += 1
    
    # Add capture group for all contiguous kanji
    if i < len(kata) and jp.is_kanji(kata[i]):
        regex_str += ("(.*)")
        i += 1

    # Skip over any additional kanji, as the previous capture group captures all contiguous
    while i < len(kata) and jp.is_kanji(kata[i]):
        i += 1

    # append the rest of the string (if any)
    regex_str += kata[i:]


    match = re.match(regex_str, form)

    if match is not None and len(match.groups()) >= 1:
        #print(word + "\t" + match[1] + "\n")
        return match[1]

# Given a word, returns that word with only its kanji characters. Assumes kanji are contiguous (which should always be true) 
def as_kanji_only(word) -> str:
    return "".join(char for char in word if 0x4E00 <= ord(char) <= 0x9FFF)


# Given a kanji word, and its katakana readings. Increment the recorded frequencies for the readings used.
def analyze_reading_use(word, kana, kanji_dict):
    original_word = word
    word = as_kanji_only(word)
    if kana is not None:
        print("kanji are: " + word + "\treading is " + kana)

        for kanji in word:
            for reading in kanji_dict.get(kanji):
                if  kana.startswith(reading):
                    kana.removeprefix(reading)
                    break
                    
            print("Failed to find a reading for " + kanji + "in " + original_word)




def get_freqs(kanji_component, kanji_readings, kanji_dict):
    tagger = MeCab.Tagger(f"-r /dev/null -d {get_mecab.default_path}")

    with open(sys.argv[1], 'r') as corpus:
        for sentence in corpus: 
            sentence_data = get_mecab.get_mecab_data(sentence, verbose=False, tagger=tagger)
            for word in sentence_data.keys():
                reading = word_to_kanji_readings(word, sentence_data[word])
                analyze_reading_use(word, reading, kanji_dict)

                
                

# kanji_component: 受 -> 又 and 授 -> 又 ...
# kanji_readings: 受 -> ["ジュ"] and 授 -> ["ジュ"] ...
kanji_component, kanji_readings = process_toml()
kanji_dict = get_kanjidict.get_readings_dictionary()
get_freqs(kanji_component, kanji_readings, kanji_dict)