from scripts.humor_data import load_local_examples, normalize_label, split_examples


def test_normalize_label_variants():
    assert normalize_label(1) == 1
    assert normalize_label(0) == 0
    assert normalize_label("funny") == 1
    assert normalize_label("not_funny") == 0


def test_load_local_examples_csv(tmp_path):
    path = tmp_path / "labels.csv"
    path.write_text("text,label\nhello,1\nworld,0\n")
    examples = load_local_examples(str(path))
    assert len(examples) == 2
    assert examples[0]["text"] == "hello"


def test_load_local_examples_jsonl(tmp_path):
    path = tmp_path / "labels.jsonl"
    path.write_text('{"text": "hi", "label": 1}\n')
    examples = load_local_examples(str(path))
    assert len(examples) == 1
    assert examples[0]["label"] == 1


def test_split_examples_ratio(tmp_path):
    examples = [{"text": str(i), "label": 0} for i in range(10)]
    train, val = split_examples(examples, 0.2, 7)
    assert len(train) + len(val) == 10
    assert len(val) >= 1
