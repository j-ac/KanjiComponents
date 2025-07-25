# Import necessary libraries
import xml.etree.ElementTree as ET
import pprint
import jp_utils as jp
from typing import Dict, List

# Generates a dictionary relating a kanji to it's readings
def get_readings_dictionary(verbose: bool = False) -> Dict[str, List[str]]:
    print("Processing kanjidic2.xml into an in-memory dictionary")
    # Path to kanjidic2.xml https://www.edrdg.org/wiki/index.php/KANJIDIC_Project
    # (The UTF-8 version of kanjidic)
    kanjidic_file = 'dictionaries/kanjidic2.xml'

    # Parse the XML file
    tree = ET.parse(kanjidic_file)
    root = tree.getroot()
    # Build dictionary in memory
    kanji_data = {}
    for character in root.findall('character'):
        kanji = character.find('literal').text
        readings_group = character.find('reading_meaning')

        if readings_group is None:
            if verbose:
                print(f"Kanjidic: Found kanji with no readings: {kanji}")
            continue

        readings_subgroup = readings_group.find('rmgroup')
        readings = readings_subgroup.findall('reading')
        
        on_readings = [r.text for r in readings if r.attrib.get('r_type') == 'ja_on']
        kun_readings = [r.text for r in readings if r.attrib['r_type'] == 'ja_kun']

        kun_readings = [kun.replace(".", "") for kun in kun_readings]
        kun_readings = [kun.replace("-", "") for kun in kun_readings]
        kun_readings = [jp.hiragana_to_katakana(kun) for kun in kun_readings]

            
        kanji_data[kanji] = on_readings + kun_readings

    print("Done!")
    return kanji_data

if __name__ == "__main__":
    demo_kanji = '飲'
    print(f"Demoing get_readings_dictionary with kanji: {demo_kanji}")
    kanji_data = get_readings_dictionary(verbose=True)

    if demo_kanji in kanji_data:
        print(f"Kanji: {demo_kanji}")
        pprint.pprint(f"readings: {kanji_data[demo_kanji]}")
    else:
        print(f"Kanji {demo_kanji} not found in kanjidic.")