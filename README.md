# 🌍 Multilingual Text Intelligence System

A high-performance NLP pipeline designed for **English** and **Arabic** text processing. This system provides a unified interface for data cleaning, sentiment analysis, topic modeling, and semantic search, leveraging state-of-the-art transformer models.

---

## 🚀 Advanced Features

- **Granular NLP**: Named Entity Recognition (NER) and 7-category Emotion Detection.
- **Arabic Optimization**: AraBERT integration for high-precision Arabic sentiment analysis.
- **Production Scaling**: Pinecone vector database support and ONNX Runtime inference optimization.
- **Interactive Analytics**: 2D Topic Mapping (UMAP) and automated trend alerts.
- **Live Data**: Reddit live ingestion connector.
- **Docker Ready**: Full containerized deployment with `docker-compose`.

---

## 🏗 System Architecture

The system follows a modular pipeline:

1.  **Ingestion**: Fetch data from various sources (Mock APIs, CSVs, Reddit).
2.  **Preprocessing**: Clean and normalize text, detect language.
3.  **Embeddings**: Generate dense vectors using HuggingFace Transformers.
4.  **Task Models**: Sentiment (ML/AR), Emotions, NER, and Topics.
5.  **Interface**: Dashboard (Streamlit) and API (FastAPI).

---

## 🛠 Tech Stack

- **Language**: Python 3.9+
- **NLP Frameworks**: `transformers`, `sentence-transformers`, `torch`, `praw`
- **Web Framework**: `FastAPI`
- **Visualization**: `Streamlit`, `Plotly`, `umap-learn`
- **Data Handling**: `pandas`, `numpy`, `fpdf2`
- **Inference**: `onnxruntime`
- **Vector Search**: Pinecone / Local FAISS

---

## 🚦 Getting Started

### 1. Installation

Clone the repository:

```bash
git clone https://github.com/nusRying/multilingual-text-intelligence.git
cd multilingual-text-intelligence
```

### 2. Run with Docker (Recommended)

```bash
docker-compose up --build
```

This starts the API (8000) and Dashboard (8501) automatically.

### 3. Manual Setup

Create and activate a virtual environment:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run services:

```bash
python main.py             # API at http://127.0.0.1:8000
streamlit run dashboard.py  # Dashboard at http://localhost:8501
```

### 4. Performance Optimization

To convert models to ONNX for faster inference:

```bash
python scripts/optimize_onnx.py --model aubmindlab/bert-base-arabertv02 --output ./onnx_models/arabert
```

---

## 📂 Project Structure

```text
├── src/
│   ├── ingestion/     # Data connectors (Mock APIs, CSV, Reddit)
│   ├── models/        # Sentiment, Emotions, NER, Topics, Search
│   ├── preprocessing/ # English and Arabic text cleaners
│   └── utils/         # Vector store (Local/Pinecone) and helpers
├── scripts/           # Optimization scripts (ONNX)
├── tests/             # Pytest suite
├── dashboard.py       # Streamlit application
├── main.py            # FastAPI service
├── Dockerfile         # Container definition
├── docker-compose.yml # Service orchestration
└── requirements.txt   # Project dependencies
```

---

## 🧪 Testing

Run the test suite:

```bash
python -m pytest
```

---

## 📄 License

This project is licensed under the MIT License.
