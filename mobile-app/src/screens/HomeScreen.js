import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, StatusBar } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../theme';

export default function HomeScreen({ navigation }) {
  const features = [
    { icon: 'analytics-outline', title: 'Analyze Text', subtitle: 'Sentiment, Emotion, NER, Classification', screen: 'Analyze', color: theme.colors.primary },
    { icon: 'git-compare-outline', title: 'Compare Texts', subtitle: 'Cross-lingual semantic similarity', screen: 'Compare', color: theme.colors.accent },
    { icon: 'settings-outline', title: 'Settings', subtitle: 'Configure API connection', screen: 'Settings', color: theme.colors.warning },
  ];

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />
      <ScrollView contentContainerStyle={styles.scroll}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.logo}>🌍</Text>
          <Text style={styles.title}>Text Intelligence</Text>
          <Text style={styles.subtitle}>Multilingual NLP • English & Arabic</Text>
        </View>

        {/* Stats Cards */}
        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Ionicons name="language-outline" size={24} color={theme.colors.primary} />
            <Text style={styles.statValue}>2</Text>
            <Text style={styles.statLabel}>Languages</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="flash-outline" size={24} color={theme.colors.accent} />
            <Text style={styles.statValue}>8</Text>
            <Text style={styles.statLabel}>AI Models</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="layers-outline" size={24} color={theme.colors.warning} />
            <Text style={styles.statValue}>6</Text>
            <Text style={styles.statLabel}>API Endpoints</Text>
          </View>
        </View>

        {/* Feature Cards */}
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        {features.map((f, i) => (
          <TouchableOpacity key={i} style={styles.featureCard} onPress={() => navigation.navigate(f.screen)} activeOpacity={0.8}>
            <View style={[styles.iconContainer, { backgroundColor: f.color + '20' }]}>
              <Ionicons name={f.icon} size={28} color={f.color} />
            </View>
            <View style={styles.featureText}>
              <Text style={styles.featureTitle}>{f.title}</Text>
              <Text style={styles.featureSubtitle}>{f.subtitle}</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={theme.colors.textMuted} />
          </TouchableOpacity>
        ))}

        {/* Capabilities */}
        <Text style={styles.sectionTitle}>Capabilities</Text>
        <View style={styles.capGrid}>
          {['Sentiment', 'Emotions', 'NER', 'Topics', 'Summarize', 'Categories'].map((cap, i) => (
            <View key={i} style={styles.capChip}>
              <Text style={styles.capText}>{cap}</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  scroll: { padding: theme.spacing.lg },
  header: { alignItems: 'center', paddingVertical: theme.spacing.xl },
  logo: { fontSize: 48 },
  title: { fontSize: theme.fontSize.xxl, fontWeight: '800', color: theme.colors.text, marginTop: theme.spacing.sm },
  subtitle: { fontSize: theme.fontSize.sm, color: theme.colors.textSecondary, marginTop: theme.spacing.xs },
  statsRow: { flexDirection: 'row', justifyContent: 'space-between', marginVertical: theme.spacing.lg },
  statCard: { flex: 1, backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, alignItems: 'center', marginHorizontal: 4 },
  statValue: { fontSize: theme.fontSize.xl, fontWeight: '700', color: theme.colors.text, marginTop: 4 },
  statLabel: { fontSize: theme.fontSize.xs, color: theme.colors.textSecondary, marginTop: 2 },
  sectionTitle: { fontSize: theme.fontSize.lg, fontWeight: '700', color: theme.colors.text, marginTop: theme.spacing.lg, marginBottom: theme.spacing.md },
  featureCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, marginBottom: theme.spacing.sm },
  iconContainer: { width: 48, height: 48, borderRadius: theme.borderRadius.sm, justifyContent: 'center', alignItems: 'center' },
  featureText: { flex: 1, marginLeft: theme.spacing.md },
  featureTitle: { fontSize: theme.fontSize.md, fontWeight: '600', color: theme.colors.text },
  featureSubtitle: { fontSize: theme.fontSize.xs, color: theme.colors.textSecondary, marginTop: 2 },
  capGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  capChip: { backgroundColor: theme.colors.surfaceLight, borderRadius: 20, paddingHorizontal: 14, paddingVertical: 6 },
  capText: { fontSize: theme.fontSize.sm, color: theme.colors.primaryLight },
});
