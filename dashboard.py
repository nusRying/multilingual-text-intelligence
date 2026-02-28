import streamlit as st
import pandas as pd
import plotly.express as px
from src.ingestion.mock_api_connector import MockSocialMediaConnector
from src.preprocessing.cleaner import TextCleaner
from src.models.sentiment import SentimentAnalyzer
from src.models.topics import TopicEngine
from src.models.embeddings import EmbeddingGenerator
from src.utils.vector_store import LocalVectorStore
from src.models.search import SemanticSearchService

st.set_page_config(page_title="Multilingual Text Intelligence", layout="wide")

@st.cache_resource
def load_components():
    cleaner = TextCleaner()
    sentiment_analyzer = SentimentAnalyzer()
    embedding_gen = EmbeddingGenerator()
    vector_store = LocalVectorStore(dimension=384)
    search_service = SemanticSearchService(embedding_gen, vector_store)
    topic_engine = TopicEngine()
    return cleaner, sentiment_analyzer, embedding_gen, vector_store, search_service, topic_engine

cleaner, sentiment_analyzer, embedding_gen, vector_store, search_service, topic_engine = load_components()

st.title("🌍 Multilingual Text Intelligence System")
st.markdown("**English + Arabic | Transformer-Based NLP | Real-time Insights**")

# Sidebar for controls
st.sidebar.header("Data Ingestion")
data_source = st.sidebar.selectbox("Select Data Source", ["Mock API", "CSV Upload"])

texts_df = pd.DataFrame()

if data_source == "Mock API":
    keyword = st.sidebar.text_input("Keyword", "AI")
    num_samples = st.sidebar.slider("Number of samples", 5, 50, 20)
    if st.sidebar.button("Fetch Data"):
        connector = MockSocialMediaConnector()
        data = connector.fetch_data(keyword=keyword, limit=num_samples)
        texts_df = pd.DataFrame(data)
else:
    uploaded_file = st.sidebar.file_path_input("Choose a CSV file") # Note: streamlit doesn't have file_path_input, using file_uploader
    # uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    # if uploaded_file:
    #     texts_df = pd.read_csv(uploaded_file)
    st.sidebar.warning("CSV uploading is not fully implemented in this preview.")

if not texts_df.empty:
    st.subheader("Raw Data Preview")
    st.dataframe(texts_df.head())

    # Processing
    with st.spinner("Processing data (cleaning, sentiment, topics)..."):
        # 1. Cleaning & Sentiment
        results = []
        for text in texts_df['text']:
            clean_res = cleaner.clean(text)
            sent_res = sentiment_analyzer.analyze(clean_res['cleaned'])[0]
            results.append({
                "original": text,
                "cleaned": clean_res['cleaned'],
                "language": clean_res['language'],
                "sentiment": sent_res['sentiment'],
                "confidence": sent_res['confidence']
            })
        
        proc_df = pd.DataFrame(results)
        
        # 2. Add to Vector Store
        for i, row in proc_df.iterrows():
            emb = embedding_gen.generate(row['cleaned'])
            vector_store.add(emb, [{"id": str(i), "text": row['original']}])
            
        # 3. Topic Modeling
        topic_results = topic_engine.fit_transform(proc_df['cleaned'].tolist())
        
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Distribution")
        fig_sent = px.pie(proc_df, names='sentiment', color='sentiment',
                         color_discrete_map={'positive':'green', 'negative':'red', 'neutral':'gray'})
        st.plotly_chart(fig_sent, use_container_width=True)
        
    with col2:
        st.subheader("Language Breakdown")
        fig_lang = px.bar(proc_df['language'].value_counts().reset_index(), x='language', y='count',
                         labels={'language': 'Language', 'count': 'Count'}, color='language')
        st.plotly_chart(fig_lang, use_container_width=True)
        
    st.subheader("Discovered Topics")
    topic_info = pd.DataFrame(topic_results["info"])
    st.dataframe(topic_info)

    st.subheader("Semantic Search")
    query = st.text_input("Enter query to search across languages (e.g., 'مشكلة في النظام')")
    if query:
        search_res = search_service.search(query, top_k=5)
        st.write("Top Results:")
        for r in search_res:
            st.info(f"**Text:** {r['text']}  \n**Similarity Distance:** {r['distance']:.4f}")

else:
    st.info("👈 Fetch data from the sidebar to begin analysis.")
