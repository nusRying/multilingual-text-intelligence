from transformers import pipeline
import torch
from typing import List, Dict, Any, Union

class SentimentAnalyzer:
    """
    Multilingual sentiment analysis with Arabic-specific optimization.
    Uses AraBERT for Arabic and XLM-RoBERTa for other languages.
    """
    def __init__(self, 
                 multilingual_model: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment",
                 arabic_model: str = "aubmindlab/bert-base-arabertv02"):
        self.multilingual_model = multilingual_model
        self.arabic_model = arabic_model
        self.device = 0 if torch.cuda.is_available() else -1
        self._ml_analyzer = None
        self._ar_analyzer = None
        
        self.ml_label_map = {
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive"
        }
        # AraBERT (using a common sentiment head mapping)
        self.ar_label_map = {
            "LABEL_0": "neutral",
            "LABEL_1": "positive",
            "LABEL_2": "negative"
        }

    def _get_analyzer(self, is_arabic: bool):
        model_name = self.arabic_model if is_arabic else self.multilingual_model
        label_map = self.ar_label_map if is_arabic else self.ml_label_map
        
        # Check for ONNX model in a standard location (e.g., ./onnx_models/<model_name>)
        onnx_path = f"./onnx_models/{model_name.replace('/', '_')}"
        use_onnx = os.path.exists(onnx_path)

        if is_arabic:
            if self._ar_analyzer is None:
                print(f"Loading Arabic sentiment model: {model_name} (ONNX={use_onnx})...")
                self._ar_analyzer = pipeline(
                    "sentiment-analysis", 
                    model=onnx_path if use_onnx else model_name, 
                    device=self.device,
                    framework="pt" if not use_onnx else None # use default for ONNX
                )
            return self._ar_analyzer, label_map
        else:
            if self._ml_analyzer is None:
                print(f"Loading multilingual sentiment model: {model_name} (ONNX={use_onnx})...")
                self._ml_analyzer = pipeline(
                    "sentiment-analysis", 
                    model=onnx_path if use_onnx else model_name, 
                    device=self.device,
                    framework="pt" if not use_onnx else None
                )
            return self._ml_analyzer, label_map

    def analyze(self, texts: Union[str, List[str]], language: str = "en") -> List[Dict[str, Any]]:
        """
        Analyzes the sentiment of given text(s).
        """
        if isinstance(texts, str):
            texts = [texts]
        
        is_arabic = (language == "ar")
        analyzer, label_map = self._get_analyzer(is_arabic)
        
        with torch.no_grad():
            results = analyzer(texts)
        
        formatted_results = []
        for res in results:
            label = res['label']
            formatted_results.append({
                "sentiment": label_map.get(label, label),
                "confidence": float(res['score'])
            })
            
        return formatted_results
