import sys
# Return true if the character is a kanji
def is_kanji(char):
    return '\u4E00' <= char <= '\u9FAF'

def is_hiragana(char):
    return '\u3041' <= char <= '\u3096'
# Return the input string where all hiragana characters are katakana equivalents
# Any characters that are not hiragana remain unaffected.
def hiragana_to_katakana(s):
    ret = ""
    for char in s:
        if is_hiragana(char):
            ret += chr(ord(char) + 0x60)
        else:
            ret += char
        
    return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
        text = "あいうえお　カキクケコ　日本語。"
    else:
        text = sys.argv[1]
    
    print("Demoing hiragana_to_katakana")
    print(f"{text}")
    print(hiragana_to_katakana(text))

            