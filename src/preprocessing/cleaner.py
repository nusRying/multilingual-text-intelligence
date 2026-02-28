import re
import string
from langdetect import detect, DetectorFactory
from typing import Dict, Any, Optional

# Ensure consistent language detection
DetectorFactory.seed = 0

class TextCleaner:
    """
    Multilingual text cleaning and normalization for English and Arabic.
    """
    
    @staticmethod
    def detect_language(text: str) -> str:
        try:
            return detect(text)
        except:
            return "unknown"

    @staticmethod
    def clean_english(text: str) -> str:
        # Lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def clean_arabic(text: str) -> str:
        # Remove diacritics (tashkeel)
        tashkeel_pattern = re.compile(r'[\u064B-\u0652]')
        text = re.sub(tashkeel_pattern, '', text)
        
        # Normalize Alef variations
        text = re.sub(r'[إأآ]', 'ا', text)
        
        # Normalize Ya/Alif Maqsura
        text = re.sub(r'ى', 'ي', text)
        
        # Normalize Te-Marbuta
        text = re.sub(r'ة', 'ه', text)
        
        # Remove elongation (tatweel)
        text = re.sub(r'\u0640', '', text)
        
        # Remove punctuation
        arabic_punctuation = '؟،؛«»'
        all_punct = string.punctuation + arabic_punctuation
        text = text.translate(str.maketrans('', '', all_punct))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def clean_urdu(text: str) -> str:
        # Normalize Urdu variations of He (ہ vs ہ) and Ye (ی vs ی)
        # Standardize to common forms if needed, but primarily handle punctuation
        
        # Remove punctuation
        urdu_punctuation = '۔؟،؛«»'
        all_punct = string.punctuation + urdu_punctuation
        text = text.translate(str.maketrans('', '', all_punct))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def clean(self, text: str, lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Detects language and applies appropriate cleaning.
        """
        if not lang or lang == "unknown":
            lang = self.detect_language(text)
        
        cleaned_text = text
        if lang == 'en':
            cleaned_text = self.clean_english(text)
        elif lang == 'ar':
            cleaned_text = self.clean_arabic(text)
        elif lang == 'ur':
            cleaned_text = self.clean_urdu(text)
        else:
            # Fallback basic cleaning
            cleaned_text = text.strip()
            
        return {
            "original": text,
            "cleaned": cleaned_text,
            "language": lang
        }
