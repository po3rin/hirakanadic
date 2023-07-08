from sudachipy import dictionary
from sudachipy import tokenizer
import jaconv
import fileinput
import argparse
import re

p = re.compile("[\u30A1-\u30FF]+")

mode = tokenizer.Tokenizer.SplitMode.B

parser = argparse.ArgumentParser(
    description="Allows Sudachi to normalize from hiragana to katakana from any compound word list"
)
parser.add_argument("file", help="kuromoji dict file path")
parser.add_argument("-o", "--out", help="output path")
parser.add_argument("-s", "--dict_type", help="sudachi dict type")
parser.add_argument("-m", "--split_mode", help="sudachi split mode", default="A")

parser.add_argument("-l", "--left_id", help="word left id", default=5146)
parser.add_argument("-r", "--right_id", help="word right id", default=5146)
parser.add_argument("-c", "--cost", help="connection cost", default=7000)


def cli():
    args = parser.parse_args()
    out = open(args.out, "wt")
    dict_type = args.dict_type
    split_mode = args.split_mode

    left_id = args.left_id
    right_id = args.right_id
    cost = args.cost

    n = HiraKanaNormalizer(split_mode, dict_type)

    with fileinput.input(files=args.file) as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            line = n.convert(line, left_id, right_id, cost)
            
            out.write(f"{line}")


class HiraKanaNormalizer:
    def __init__(self, split_mode="A ", dict_type="core", sudachi_setting=None):
        if split_mode == "A":
            self.split_mode = tokenizer.Tokenizer.SplitMode.A
        if split_mode == "B":
            self.split_mode = tokenizer.Tokenizer.SplitMode.B
        if split_mode == "C":
            self.split_mode = tokenizer.Tokenizer.SplitMode.C

        self.tokenizer = dictionary.Dictionary(
            dict=dict_type, config_path=sudachi_setting
        ).create()

        self.already = []

    def convert(
        self, text: str, left_id: int = 5646, right_id: int = 5646, cost: int = 7000
    ) -> str:
        result = ""
        kana = [
            m.surface()
            for m in self.tokenizer.tokenize(text, mode)
            if is_kana(m.surface()) and "名詞" in m.part_of_speech()
        ]
        for k in kana:
            if k in self.already:
                continue
            self.already.append(k)

            hira = kana2hira(k)
            result += f"{hira},{left_id},{right_id},{cost},{hira},名詞,普通名詞,一般,*,*,*,{k},{k},*,*,*,*,*\n"

        return result


def is_kana(word: str) -> bool:
    return p.fullmatch(word)


def kana2hira(word: str) -> bool:
    return jaconv.kata2hira(word)


if __name__ == '__main__':
    cli()
