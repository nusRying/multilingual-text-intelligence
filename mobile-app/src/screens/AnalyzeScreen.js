import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../theme';
import api from '../services/api';

export default function AnalyzeScreen() {
  const [text, setText] = useState('');
  const [categories, setCategories] = useState('Policy, Technology, Economics, Social');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const cats = categories.split(',').map(c => c.trim()).filter(Boolean);
      const data = await api.analyze(text, cats);
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to connect to API');
    } finally {
      setLoading(false);
    }
  };

  const handleSummarize = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.summarize(text);
      setResult(prev => ({ ...prev, summary: data.summary }));
    } catch (e) {
      setError(e.message || 'Failed to summarize');
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (s) => {
    if (s === 'positive') return theme.colors.positive;
    if (s === 'negative') return theme.colors.negative;
    return theme.colors.neutral;
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.header}>📝 Analyze Text</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter or paste text here (English or Arabic)..."
          placeholderTextColor={theme.colors.textMuted}
          multiline
          numberOfLines={5}
          value={text}
          onChangeText={setText}
          textAlignVertical="top"
        />

        <TextInput
          style={styles.catInput}
          placeholder="Custom categories (comma-separated)"
          placeholderTextColor={theme.colors.textMuted}
          value={categories}
          onChangeText={setCategories}
        />

        <View style={styles.buttonRow}>
          <TouchableOpacity style={styles.analyzeBtn} onPress={handleAnalyze} disabled={loading} activeOpacity={0.8}>
            {loading ? <ActivityIndicator color="#fff" /> : (
              <>
                <Ionicons name="flash" size={18} color="#fff" />
                <Text style={styles.btnText}>Analyze</Text>
              </>
            )}
          </TouchableOpacity>
          <TouchableOpacity style={styles.summarizeBtn} onPress={handleSummarize} disabled={loading} activeOpacity={0.8}>
            <Ionicons name="document-text" size={18} color="#fff" />
            <Text style={styles.btnText}>Summarize</Text>
          </TouchableOpacity>
        </View>

        {error && (
          <View style={styles.errorCard}>
            <Ionicons name="alert-circle" size={20} color={theme.colors.danger} />
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}

        {result && (
          <View style={styles.resultsContainer}>
            <Text style={styles.resultsTitle}>Analysis Results</Text>

            {/* Sentiment */}
            <View style={styles.resultCard}>
              <View style={styles.resultHeader}>
                <Text style={styles.resultLabel}>Sentiment</Text>
                <View style={[styles.badge, { backgroundColor: getSentimentColor(result.sentiment) + '30' }]}>
                  <Text style={[styles.badgeText, { color: getSentimentColor(result.sentiment) }]}>
                    {result.sentiment?.toUpperCase()}
                  </Text>
                </View>
              </View>
              <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: `${(result.sentiment_confidence * 100)}%`, backgroundColor: getSentimentColor(result.sentiment) }]} />
              </View>
              <Text style={styles.confidenceText}>{(result.sentiment_confidence * 100).toFixed(1)}% confidence</Text>
            </View>

            {/* Emotion */}
            <View style={styles.resultCard}>
              <View style={styles.resultHeader}>
                <Text style={styles.resultLabel}>Emotion</Text>
                <View style={[styles.badge, { backgroundColor: theme.colors.primary + '30' }]}>
                  <Text style={[styles.badgeText, { color: theme.colors.primaryLight }]}>
                    {result.emotion?.toUpperCase()}
                  </Text>
                </View>
              </View>
              <Text style={styles.confidenceText}>{(result.emotion_confidence * 100).toFixed(1)}% confidence</Text>
            </View>

            {/* Category */}
            <View style={styles.resultCard}>
              <View style={styles.resultHeader}>
                <Text style={styles.resultLabel}>Category</Text>
                <View style={[styles.badge, { backgroundColor: theme.colors.accent + '30' }]}>
                  <Text style={[styles.badgeText, { color: theme.colors.accent }]}>
                    {result.category}
                  </Text>
                </View>
              </View>
              <Text style={styles.confidenceText}>{(result.category_confidence * 100).toFixed(1)}% confidence</Text>
            </View>

            {/* Language */}
            <View style={styles.resultCard}>
              <View style={styles.resultHeader}>
                <Text style={styles.resultLabel}>Language Detected</Text>
                <Text style={styles.resultValue}>{result.language === 'ar' ? '🇸🇦 Arabic' : '🇬🇧 English'}</Text>
              </View>
            </View>

            {/* Entities */}
            {result.entities && result.entities.length > 0 && (
              <View style={styles.resultCard}>
                <Text style={styles.resultLabel}>Named Entities</Text>
                <View style={styles.entityGrid}>
                  {result.entities.map((e, i) => (
                    <View key={i} style={styles.entityChip}>
                      <Text style={styles.entityText}>{e.word} ({e.entity_group})</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}

            {/* Summary */}
            {result.summary && (
              <View style={styles.resultCard}>
                <Text style={styles.resultLabel}>AI Summary</Text>
                <Text style={styles.summaryText}>{result.summary}</Text>
              </View>
            )}
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  scroll: { padding: theme.spacing.lg },
  header: { fontSize: theme.fontSize.xl, fontWeight: '700', color: theme.colors.text, marginBottom: theme.spacing.lg },
  input: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, color: theme.colors.text, fontSize: theme.fontSize.md, minHeight: 120, borderWidth: 1, borderColor: theme.colors.border },
  catInput: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, color: theme.colors.text, fontSize: theme.fontSize.sm, marginTop: theme.spacing.sm, borderWidth: 1, borderColor: theme.colors.border },
  buttonRow: { flexDirection: 'row', gap: 10, marginTop: theme.spacing.md },
  analyzeBtn: { flex: 1, flexDirection: 'row', backgroundColor: theme.colors.primary, borderRadius: theme.borderRadius.md, padding: 14, justifyContent: 'center', alignItems: 'center', gap: 8 },
  summarizeBtn: { flex: 1, flexDirection: 'row', backgroundColor: theme.colors.surfaceLight, borderRadius: theme.borderRadius.md, padding: 14, justifyContent: 'center', alignItems: 'center', gap: 8 },
  btnText: { color: '#fff', fontSize: theme.fontSize.md, fontWeight: '600' },
  errorCard: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: theme.colors.danger + '15', borderRadius: theme.borderRadius.sm, padding: theme.spacing.md, marginTop: theme.spacing.md },
  errorText: { color: theme.colors.danger, fontSize: theme.fontSize.sm, flex: 1 },
  resultsContainer: { marginTop: theme.spacing.lg },
  resultsTitle: { fontSize: theme.fontSize.lg, fontWeight: '700', color: theme.colors.text, marginBottom: theme.spacing.md },
  resultCard: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, marginBottom: theme.spacing.sm },
  resultHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  resultLabel: { fontSize: theme.fontSize.sm, color: theme.colors.textSecondary, fontWeight: '600' },
  resultValue: { fontSize: theme.fontSize.md, color: theme.colors.text, fontWeight: '600' },
  badge: { borderRadius: 20, paddingHorizontal: 12, paddingVertical: 4 },
  badgeText: { fontSize: theme.fontSize.sm, fontWeight: '700' },
  progressBar: { height: 6, backgroundColor: theme.colors.surfaceLight, borderRadius: 3, marginTop: theme.spacing.sm },
  progressFill: { height: 6, borderRadius: 3 },
  confidenceText: { fontSize: theme.fontSize.xs, color: theme.colors.textMuted, marginTop: 4 },
  entityGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: theme.spacing.sm },
  entityChip: { backgroundColor: theme.colors.surfaceLight, borderRadius: 16, paddingHorizontal: 10, paddingVertical: 4 },
  entityText: { fontSize: theme.fontSize.xs, color: theme.colors.primaryLight },
  summaryText: { fontSize: theme.fontSize.md, color: theme.colors.text, marginTop: theme.spacing.sm, lineHeight: 22 },
});
