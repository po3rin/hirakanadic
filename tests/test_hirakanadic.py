from hirakanadic.cli import HiraKanaNormalizer

def test_hirakanadic_cli(capsys):
    sudachi_dict_lines = []
    c = HiraKanaNormalizer()

    expect = "これすてろーる,5646,5646,7000,これすてろーる,名詞,普通名詞,一般,*,*,*,コレステロール,コレステロール,*,*,*,*,*\n"
    assert c.convert("コレステロール値") == expect

    # duplicate
    expect = ""
    assert c.convert("コレステロール") == expect

    expect = ""
    assert c.convert("コレステロール値コレステロール") == expect
