# Import necessary libraries
import xml.etree.ElementTree as ET
from typing import Dict, List

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
        
        on_readings = [r.text for r in readings if r.attrib['r_type'] == 'ja_on']
        
        kanji_data[kanji] = {'on_readings': on_readings}

    print("Done!")
    print(type(kanji_data))
    return kanji_data


if __name__ == "__main__":
    demo_kanji = '行'
    print(f"Demoing get_readings_dictionary with kanji: {demo_kanji}")
    kanji_data = get_readings_dictionary(verbose=True)

    if demo_kanji in kanji_data:
        print(f"Kanji: {demo_kanji}")
        print(f"On readings: {kanji_data[demo_kanji]['on_readings']}")
    else:
        print(f"Kanji {demo_kanji} not found in kanjidic.")