from data.index import Index


def test_len():
    users = Index(labels=["user 1", "user 2", "user 3", "user 4"], name="names")

    assert len(users) == 4
