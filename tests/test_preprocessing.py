from src.preprocessing.cleaner import TextCleaner

def test_language_detection():
    cleaner = TextCleaner()
    assert cleaner.detect_language("Hello world") == "en"
    assert cleaner.detect_language("مرحبا بكم في هذا النظام") == "ar"

def test_clean_english():
    cleaner = TextCleaner()
    text = "Visit https://google.com! This is AMAZING...   "
    cleaned = cleaner.clean_english(text)
    assert cleaned == "visit this is amazing"

def test_clean_arabic():
    cleaner = TextCleaner()
    # Test with Tashkeel, Alef variations, Tatweel, and punctuation
    text = "الـمـُدَرِّسُ المتميزُ! أقرأ الكتابَ في مدرسةٍ."
    cleaned = cleaner.clean_arabic(text)
    # Tashkeel removed, Alef normalized, Tatweel removed, punctuation removed
    # Expected: المدرس المتميز اقرا الكتاب في مدرسه
    assert "المدرس" in cleaned
    assert "اقرا" in cleaned
    assert "مدرسه" in cleaned
    assert "!" not in cleaned

def test_clean_wrapper():
    cleaner = TextCleaner()
    res_en = cleaner.clean("Hello World!")
    assert res_en["language"] == "en"
    assert res_en["cleaned"] == "hello world"
    
    res_ar = cleaner.clean("مرحبا!")
    assert res_ar["language"] == "ar"
    assert "مرحبا" in res_ar["cleaned"]
def test_language_detection_urdu():
    cleaner = TextCleaner()
    res = cleaner.detect_language("یہ ایک اردو جملہ ہے۔")
    assert res == 'ur'

def test_urdu_cleaning():
    cleaner = TextCleaner()
    raw = "یہ سسٹم بہت اچھا ہے! ۔ ؟"
    # Urdu clean removes ۔ and ؟
    cleaned = cleaner.clean_urdu(raw)
    assert "!" not in cleaned
    assert "۔" not in cleaned
    assert "؟" not in cleaned
    assert "سسٹم" in cleaned
