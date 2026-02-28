import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../theme';
import api from '../services/api';

export default function CompareScreen() {
  const [textA, setTextA] = useState('');
  const [textB, setTextB] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCompare = async () => {
    if (!textA.trim() || !textB.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.compare(textA, textB);
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to connect to API');
    } finally {
      setLoading(false);
    }
  };

  const getSimilarityColor = (sim) => {
    if (sim > 0.7) return theme.colors.positive;
    if (sim > 0.4) return theme.colors.warning;
    return theme.colors.danger;
  };

  const getSimilarityLabel = (sim) => {
    if (sim > 0.7) return 'Very Similar';
    if (sim > 0.4) return 'Moderately Similar';
    return 'Dissimilar';
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.header}>⚖️ Compare Texts</Text>
        <Text style={styles.description}>Compare any two texts — even across languages!</Text>

        <Text style={styles.label}>Text A</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter first text..."
          placeholderTextColor={theme.colors.textMuted}
          multiline
          numberOfLines={4}
          value={textA}
          onChangeText={setTextA}
          textAlignVertical="top"
        />

        <Text style={styles.label}>Text B</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter second text..."
          placeholderTextColor={theme.colors.textMuted}
          multiline
          numberOfLines={4}
          value={textB}
          onChangeText={setTextB}
          textAlignVertical="top"
        />

        <TouchableOpacity style={styles.compareBtn} onPress={handleCompare} disabled={loading} activeOpacity={0.8}>
          {loading ? <ActivityIndicator color="#fff" /> : (
            <>
              <Ionicons name="git-compare" size={18} color="#fff" />
              <Text style={styles.btnText}>Compare</Text>
            </>
          )}
        </TouchableOpacity>

        {error && (
          <View style={styles.errorCard}>
            <Ionicons name="alert-circle" size={20} color={theme.colors.danger} />
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}

        {result && (
          <View style={styles.resultContainer}>
            {/* Similarity Score */}
            <View style={styles.scoreCard}>
              <Text style={styles.scoreLabel}>Semantic Similarity</Text>
              <Text style={[styles.scoreValue, { color: getSimilarityColor(result.similarity) }]}>
                {(result.similarity * 100).toFixed(1)}%
              </Text>
              <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: `${result.similarity * 100}%`, backgroundColor: getSimilarityColor(result.similarity) }]} />
              </View>
              <View style={[styles.verdictBadge, { backgroundColor: getSimilarityColor(result.similarity) + '20' }]}>
                <Ionicons 
                  name={result.is_similar ? 'checkmark-circle' : 'close-circle'} 
                  size={18} 
                  color={getSimilarityColor(result.similarity)} 
                />
                <Text style={[styles.verdictText, { color: getSimilarityColor(result.similarity) }]}>
                  {getSimilarityLabel(result.similarity)}
                </Text>
              </View>
            </View>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  scroll: { padding: theme.spacing.lg },
  header: { fontSize: theme.fontSize.xl, fontWeight: '700', color: theme.colors.text },
  description: { fontSize: theme.fontSize.sm, color: theme.colors.textSecondary, marginTop: 4, marginBottom: theme.spacing.lg },
  label: { fontSize: theme.fontSize.sm, fontWeight: '600', color: theme.colors.textSecondary, marginTop: theme.spacing.md, marginBottom: 6 },
  input: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, color: theme.colors.text, fontSize: theme.fontSize.md, minHeight: 90, borderWidth: 1, borderColor: theme.colors.border },
  compareBtn: { flexDirection: 'row', backgroundColor: theme.colors.accent, borderRadius: theme.borderRadius.md, padding: 14, justifyContent: 'center', alignItems: 'center', gap: 8, marginTop: theme.spacing.lg },
  btnText: { color: '#fff', fontSize: theme.fontSize.md, fontWeight: '600' },
  errorCard: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: theme.colors.danger + '15', borderRadius: theme.borderRadius.sm, padding: theme.spacing.md, marginTop: theme.spacing.md },
  errorText: { color: theme.colors.danger, fontSize: theme.fontSize.sm, flex: 1 },
  resultContainer: { marginTop: theme.spacing.lg },
  scoreCard: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.lg, padding: theme.spacing.lg, alignItems: 'center' },
  scoreLabel: { fontSize: theme.fontSize.sm, color: theme.colors.textSecondary, fontWeight: '600' },
  scoreValue: { fontSize: 48, fontWeight: '800', marginVertical: theme.spacing.sm },
  progressBar: { height: 8, width: '100%', backgroundColor: theme.colors.surfaceLight, borderRadius: 4, marginTop: theme.spacing.sm },
  progressFill: { height: 8, borderRadius: 4 },
  verdictBadge: { flexDirection: 'row', alignItems: 'center', gap: 6, borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, marginTop: theme.spacing.md },
  verdictText: { fontSize: theme.fontSize.md, fontWeight: '700' },
});
