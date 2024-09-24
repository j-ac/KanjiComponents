from typing import Dict
import MeCab
import pprint

default_path = "/var/lib/mecab/dic/unidic"
def get_mecab_data(text: str, path_to_unidic: str= default_path, verbose:bool = True) -> Dict:
    tagger = MeCab.Tagger(f"-r /dev/null -d {path_to_unidic}") # Not sure how expensive this is. Oh well
    parsed = tagger.parse(text).split("\n")

    field_data = {}
    for row in parsed:
        if row == "EOS": break
        word = row[0:row.find('\t')]
        fields = row[row.find("\t")+1:].split(",")

        field_data[word] = {}

        # Meanings of each field can be found at
        # https://pypi.org/project/unidic/
        if len(fields) < 28:
            print(f"\"{word}\" did not have complete data.")
            continue

        field_data[word]["pos1"] = fields[0]
        field_data[word]["pos2"] = fields[1]
        field_data[word]["pos3"] = fields[2]
        field_data[word]["cType"] = fields[3]
        field_data[word]["cForm"] = fields[4]
        field_data[word]["lForm"] = fields[5]
        field_data[word]["lemma"] = fields[6]
        field_data[word]["orth"] = fields[7]
        field_data[word]["pron"] = fields[8]
        field_data[word]["orthBase"] = fields[9]
        field_data[word]["pronBase"] = fields[10]
        field_data[word]["goshu"] = fields[11]
        field_data[word]["iType"] = fields[12]
        field_data[word]["iForm"] = fields[13]
        field_data[word]["fType"] = fields[14]
        field_data[word]["fForm"] = fields[15]
        field_data[word]["iConType"] = fields[16]
        field_data[word]["fConType"] = fields[17]
        field_data[word]["type"] = fields[18]
        field_data[word]["kana"] = fields[19]
        field_data[word]["kanaBase"] = fields[20]
        field_data[word]["form"] = fields[21]
        field_data[word]["formBase"] = fields[22]
        field_data[word]["aType"] = fields[23]
        field_data[word]["aConType"] = fields[24]
        field_data[word]["aModType"] = fields[25]
        field_data[word]["lid"] = fields[26]
        field_data[word]["lemma_id"] = fields[27]

    if verbose:
        pprint.pprint(field_data, sort_dicts=False)

    return field_data

if __name__ == "__main__":
    print(f"Demoing get_mecab_data() with the input 銀行に行きます。")
    get_mecab_data(text="銀行に行きます。")