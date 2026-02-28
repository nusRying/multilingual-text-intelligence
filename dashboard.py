import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import umap
from io import BytesIO
from fpdf import FPDF
from src.ingestion.mock_api_connector import MockSocialMediaConnector
from src.ingestion.reddit_connector import RedditConnector
from src.ingestion.web_scraper import WebScraper
from src.ingestion.slack_connector import SlackConnector
from src.preprocessing.cleaner import TextCleaner
from src.models.sentiment import SentimentAnalyzer
from src.models.topics import TopicEngine
from src.models.embeddings import EmbeddingGenerator
from src.utils.vector_store import LocalVectorStore
from src.models.search import SemanticSearchService
from src.models.emotion import EmotionAnalyzer
from src.models.ner import NERAnalyzer
from src.models.classification import ZeroShotClassifier
from src.utils.alert_engine import AlertEngine
from src.utils.notifications import NotificationHub
from src.utils.monitor import monitor
from src.models.summarizer import TextSummarizer
from src.models.comparator import TextComparator
import time

st.set_page_config(page_title="Multilingual Text Intelligence", layout="wide")

@st.cache_resource
def load_components():
    cleaner = TextCleaner()
    sentiment_analyzer = SentimentAnalyzer()
    ner_analyzer = NERAnalyzer()
    emotion_analyzer = EmotionAnalyzer()
    classification_engine = ZeroShotClassifier()
    embedding_gen = EmbeddingGenerator()
    vector_store = LocalVectorStore(dimension=384)
    search_service = SemanticSearchService(embedding_gen, vector_store)
    topic_engine = TopicEngine()
    alert_engine = AlertEngine()
    notification_hub = NotificationHub()
    summarizer = TextSummarizer()
    comparator = TextComparator(embedding_gen)
    return cleaner, sentiment_analyzer, ner_analyzer, emotion_analyzer, classification_engine, embedding_gen, vector_store, search_service, topic_engine, alert_engine, notification_hub, summarizer, comparator

cleaner, sentiment_analyzer, ner_analyzer, emotion_analyzer, classification_engine, embedding_gen, vector_store, search_service, topic_engine, alert_engine, notification_hub, summarizer, comparator = load_components()

st.title("🌍 Multilingual Text Intelligence System")
st.markdown("**English + Arabic | Transformer-Based NLP | Real-time Insights**")

# Sidebar for controls
st.sidebar.header("Data Ingestion")
data_source = st.sidebar.selectbox("Select Data Source", ["Mock API", "Reddit Live", "Slack (Internal)", "Web Scraper", "CSV Upload"])

st.sidebar.header("Classification Settings")
custom_labels = st.sidebar.text_input("Custom Labels (comma-separated)", "Policy, Technology, Economics, Social")
labels = [l.strip() for l in custom_labels.split(",") if l.strip()]

st.sidebar.header("🚨 Alert Settings")
alert_threshold = st.sidebar.slider("Negative Sentiment Threshold (%)", 10, 100, 35)
alert_engine.threshold = alert_threshold / 100
enable_slack = st.sidebar.checkbox("Notify via Slack (Mock)")
if enable_slack: notification_hub.enable_channel("slack")
else: notification_hub.disable_channel("slack")

texts_df = pd.DataFrame()

if data_source == "Mock API":
    keyword = st.sidebar.text_input("Keyword", "AI")
    num_samples = st.sidebar.slider("Number of samples", 5, 50, 20)
    if st.sidebar.button("Fetch Data"):
        connector = MockSocialMediaConnector()
        data = connector.fetch_data(keyword=keyword, limit=num_samples)
        texts_df = pd.DataFrame(data)
elif data_source == "Reddit Live":
    keyword = st.sidebar.text_input("Subreddit/Topic", "technology")
    num_samples = st.sidebar.slider("Number of samples", 5, 50, 20)
    if st.sidebar.button("Fetch Reddit Data"):
        connector = RedditConnector()
        if not connector.reddit:
            st.sidebar.error("Reddit API credentials not found in .env!")
        else:
            data = connector.fetch_data(query=keyword, limit=num_samples)
            texts_df = pd.DataFrame(data)
elif data_source == "Web Scraper":
    url = st.sidebar.text_input("Article URL")
    if st.sidebar.button("Scrape Intelligence"):
        connector = WebScraper()
        data = connector.fetch_data(url=url)
        if not data:
            st.sidebar.warning("Failed to scrape URL or no content found.")
        else:
            texts_df = pd.DataFrame(data)
elif data_source == "Slack (Internal)":
    channel = st.sidebar.text_input("Slack Channel ID", "C12345")
    if st.sidebar.button("Fetch Slack Messages"):
        connector = SlackConnector()
        if not connector.client:
            st.sidebar.error("SLACK_BOT_TOKEN not found in .env!")
        else:
            data = connector.fetch_data(channel_id=channel)
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
        # 1. Full Pipeline Processing
        results = []
        for text in texts_df['text']:
            start_time = time.time()
            clean_res = cleaner.clean(text)
            lang = clean_res['language']
            sent_res = sentiment_analyzer.analyze(clean_res['cleaned'], language=lang)[0]
            emo_res = emotion_analyzer.analyze(clean_res['cleaned'])[0]
            ner_res = ner_analyzer.extract_entities(clean_res['cleaned'])[0]
            class_res = classification_engine.classify(clean_res['cleaned'], labels)
            
            # Log latency
            duration = (time.time() - start_time) * 1000
            monitor.log_inference("Full Pipeline", duration, len(text), lang)
            
            # Simple entity list for display
            ents = [f"{e['word']} ({e['entity_group']})" for e in ner_res]
            
            results.append({
                "original": text,
                "cleaned": clean_res['cleaned'],
                "language": lang,
                "sentiment": sent_res['sentiment'],
                "sentiment_conf": sent_res['confidence'],
                "emotion": emo_res['emotion'],
                "emotion_conf": emo_res['confidence'],
                "category": class_res['label'],
                "category_conf": class_res['score'],
                "entities": ", ".join(ents)
            })
        
        proc_df = pd.DataFrame(results)
        
        # 2. Add to Vector Store
        for i, row in proc_df.iterrows():
            emb = embedding_gen.generate(row['cleaned'])
            vector_store.add(emb, [{"id": str(i), "text": row['original']}])
            
        # 3. Topic Modeling
        topic_results = topic_engine.fit_transform(proc_df['cleaned'].tolist())
        
        # 4. Check for Alert Spikes
        active_alert = alert_engine.check_for_spikes(proc_df, topic=keyword if data_source != "Web Scraper" else "Web Content")
        if active_alert:
            notification_hub.notify(active_alert)

    # Alert Center
    if alert_engine.get_history():
        st.header("🔔 Alert Center")
        for alert in reversed(alert_engine.get_history()[-5:]): # Show last 5
            severity_color = "red" if alert['severity'] == "CRITICAL" else "orange"
            st.markdown(f":{severity_color}[**{alert['severity']}**] | **{alert['topic']}** | {alert['message']} ({alert['timestamp'][:16]})")
        st.divider()
        
    # Visualizations
    col1, col2, col3 = st.columns(3)
    
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

    with col3:
        st.subheader("Category Distribution")
        fig_cat = px.pie(proc_df, names='category', title="Custom Categories")
        st.plotly_chart(fig_cat, use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Emotion Analysis")
        fig_emo = px.bar(proc_df['emotion'].value_counts().reset_index(), x='emotion', y='count',
                        color='emotion', title="Detected Emotions")
        st.plotly_chart(fig_emo, use_container_width=True)
        
    with col4:
        st.subheader("Top Named Entities")
        # Flatten and count entities
        all_ents = []
        for row in results:
            if row['entities']:
                all_ents.extend(row['entities'].split(", "))
        if all_ents:
            ent_counts = pd.Series(all_ents).value_counts().reset_index()
            ent_counts.columns = ['Entity', 'Count']
            fig_ent = px.bar(ent_counts.head(10), x='Count', y='Entity', orientation='h',
                            color='Entity', title="Most Frequent Entities")
            st.plotly_chart(fig_ent, use_container_width=True)
        else:
            st.write("No entities detected in this sample.")
        
    st.subheader("Discovered Topics")
    topic_info = pd.DataFrame(topic_results["info"])
    st.dataframe(topic_info)

    # Topic Mapping (UMAP)
    st.subheader("Interactive Topic Map (UMAP)")
    if len(proc_df) >= 5: # UMAP needs some data
        with st.spinner("Generating UMAP projection..."):
            # Get embeddings for all texts
            embs = []
            for text in proc_df['cleaned']:
                embs.append(embedding_gen.generate(text).flatten())
            embs = np.array(embs)
            
            # Reduce to 2D
            reducer = umap.UMAP(n_neighbors=min(15, len(embs)-1), min_dist=0.1, n_components=2)
            embedding_2d = reducer.fit_transform(embs)
            
            viz_df = pd.DataFrame(embedding_2d, columns=['x', 'y'])
            viz_df['text'] = proc_df['original']
            viz_df['sentiment'] = proc_df['sentiment']
            
            fig_umap = px.scatter(viz_df, x='x', y='y', hover_data=['text'], color='sentiment',
                                title="Text Embedding Projection")
            st.plotly_chart(fig_umap, use_container_width=True)
    else:
        st.info("Insufficient data for UMAP projection (minimum 5 samples required).")

    # Export Section
    st.subheader("📊 Export Reports")
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        csv_data = proc_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Excel (CSV)", data=csv_data, file_name="analysis_report.csv", mime="text/csv")
    
    with col_ex2:
        if st.button("📄 Generate PDF Summary"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Multilingual Text Intelligence Report", ln=True, align='C')
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Total Records: {len(proc_df)}", ln=True)
            pdf.cell(200, 10, txt=f"Positive: {(proc_df['sentiment']=='positive').sum()}", ln=True)
            pdf.cell(200, 10, txt=f"Negative: {(proc_df['sentiment']=='negative').sum()}", ln=True)
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 Download PDF", data=pdf_output, file_name="report.pdf", mime="application/pdf")

    st.subheader("Semantic Search")
    query = st.text_input("Enter query to search across languages (e.g., 'مشكلة في النظام')")
    if query:
        search_res = search_service.search(query, top_k=5)
        st.write("Top Results:")
        for r in search_res:
            st.info(f"**Text:** {r['text']}  \n**Similarity Distance:** {r['distance']:.4f}")

    # Executive Summary
    st.divider()
    st.subheader("📝 Executive Summary")
    if st.button("Generate AI Summary"):
        with st.spinner("Generating summary..."):
            executive_summary = summarizer.summarize_batch(proc_df['cleaned'].tolist())
            st.success(executive_summary)

    # Duplicate Detection
    st.subheader("🔍 Near-Duplicate Detection")
    if st.button("Scan for Duplicates"):
        with st.spinner("Scanning for near-duplicates..."):
            dupes = comparator.find_duplicates(proc_df['cleaned'].tolist(), threshold=0.85)
            if dupes:
                st.warning(f"Found {len(dupes)} near-duplicate pair(s)!")
                for d in dupes:
                    st.markdown(f"- **Texts {d['index_a']+1} & {d['index_b']+1}** | Similarity: `{d['similarity']}`")
            else:
                st.info("No near-duplicates found.")

    # Ad-Hoc Text Comparison
    st.subheader("⚖️ Compare Two Texts")
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        text_a = st.text_area("Text A", height=100)
    with comp_col2:
        text_b = st.text_area("Text B", height=100)
    if st.button("Compare") and text_a and text_b:
        comp_result = comparator.compare(text_a, text_b)
        sim = comp_result['similarity']
        color = "green" if sim > 0.7 else ("orange" if sim > 0.4 else "red")
        st.metric("Semantic Similarity", f"{sim:.2%}")
        st.markdown(f":{color}[{'Very Similar' if sim > 0.7 else ('Moderately Similar' if sim > 0.4 else 'Dissimilar')}]")

    # Infrastructure & MLOps View
    st.divider()
    with st.expander("🛠 Infrastructure & MLOps Health"):
        stats = monitor.get_summary()
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Avg Latency", f"{stats['avg_latency_ms']:.2f}ms")
        col_m2.metric("Total Requests", stats['total_calls'])
        col_m3.metric("Supported Languages", len(stats.get('languages', [])))
        
        if monitor.metrics_history:
            m_df = pd.DataFrame(monitor.metrics_history)
            fig_lat = px.line(m_df, y='latency_ms', title="Inference Latency Over Time (ms)")
            st.plotly_chart(fig_lat, use_container_width=True)

else:
    st.info("👈 Fetch data from the sidebar to begin analysis.")
