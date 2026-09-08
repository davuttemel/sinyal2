from app.kap_sentiment import classify


def test_positive_kap():
    assert classify("Şirket yeni sözleşme imzaladı") == 1


def test_negative_kap():
    assert classify("Şirket bedelli sermaye artırımı kararı aldı") == -1


def test_unknown_kap_is_neutral():
    assert classify("Olağan genel kurul toplantı tarihi") == 0
