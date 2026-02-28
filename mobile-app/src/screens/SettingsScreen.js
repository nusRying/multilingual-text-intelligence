import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { theme } from '../theme';
import api from '../services/api';

export default function SettingsScreen() {
  const [apiUrl, setApiUrl] = useState('http://10.0.2.2:8000');
  const [status, setStatus] = useState('unknown');
  const [checking, setChecking] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    const stored = await AsyncStorage.getItem('api_url');
    if (stored) setApiUrl(stored);
  };

  const saveSettings = async () => {
    await AsyncStorage.setItem('api_url', apiUrl);
    Alert.alert('Saved', 'API URL updated successfully!');
  };

  const checkConnection = async () => {
    setChecking(true);
    try {
      await api.healthCheck();
      setStatus('connected');
    } catch (e) {
      setStatus('error');
    } finally {
      setChecking(false);
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.header}>⚙️ Settings</Text>

        {/* API Configuration */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>API Server</Text>
          <TextInput
            style={styles.input}
            placeholder="http://your-server:8000"
            placeholderTextColor={theme.colors.textMuted}
            value={apiUrl}
            onChangeText={setApiUrl}
            autoCapitalize="none"
          />
          <View style={styles.buttonRow}>
            <TouchableOpacity style={styles.saveBtn} onPress={saveSettings} activeOpacity={0.8}>
              <Ionicons name="save" size={18} color="#fff" />
              <Text style={styles.btnText}>Save</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.testBtn} onPress={checkConnection} disabled={checking} activeOpacity={0.8}>
              <Ionicons name="pulse" size={18} color="#fff" />
              <Text style={styles.btnText}>{checking ? 'Testing...' : 'Test'}</Text>
            </TouchableOpacity>
          </View>

          {/* Connection Status */}
          {status !== 'unknown' && (
            <View style={[styles.statusCard, { backgroundColor: status === 'connected' ? theme.colors.positive + '15' : theme.colors.danger + '15' }]}>
              <Ionicons
                name={status === 'connected' ? 'checkmark-circle' : 'close-circle'}
                size={20}
                color={status === 'connected' ? theme.colors.positive : theme.colors.danger}
              />
              <Text style={[styles.statusText, { color: status === 'connected' ? theme.colors.positive : theme.colors.danger }]}>
                {status === 'connected' ? 'Connected to API server' : 'Cannot reach API server'}
              </Text>
            </View>
          )}
        </View>

        {/* Info */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About This App</Text>
          <View style={styles.infoCard}>
            <Text style={styles.infoTitle}>Multilingual Text Intelligence</Text>
            <Text style={styles.infoText}>A full-stack NLP system supporting English and Arabic text analysis with 8 AI models.</Text>
            <Text style={styles.infoVersion}>Version 1.0.0 • Phase 9</Text>
          </View>
        </View>

        {/* Tips */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Setup</Text>
          <View style={styles.tipCard}>
            <Ionicons name="information-circle" size={20} color={theme.colors.primary} />
            <Text style={styles.tipText}>
              1. Start your FastAPI server{'\n'}
              2. Use your machine's IP if on same WiFi{'\n'}
              3. Use 10.0.2.2 for Android Emulator
            </Text>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  scroll: { padding: theme.spacing.lg },
  header: { fontSize: theme.fontSize.xl, fontWeight: '700', color: theme.colors.text, marginBottom: theme.spacing.lg },
  section: { marginBottom: theme.spacing.xl },
  sectionTitle: { fontSize: theme.fontSize.md, fontWeight: '700', color: theme.colors.textSecondary, marginBottom: theme.spacing.sm },
  input: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md, color: theme.colors.text, fontSize: theme.fontSize.md, borderWidth: 1, borderColor: theme.colors.border },
  buttonRow: { flexDirection: 'row', gap: 10, marginTop: theme.spacing.md },
  saveBtn: { flex: 1, flexDirection: 'row', backgroundColor: theme.colors.primary, borderRadius: theme.borderRadius.md, padding: 12, justifyContent: 'center', alignItems: 'center', gap: 6 },
  testBtn: { flex: 1, flexDirection: 'row', backgroundColor: theme.colors.surfaceLight, borderRadius: theme.borderRadius.md, padding: 12, justifyContent: 'center', alignItems: 'center', gap: 6 },
  btnText: { color: '#fff', fontSize: theme.fontSize.sm, fontWeight: '600' },
  statusCard: { flexDirection: 'row', alignItems: 'center', gap: 8, borderRadius: theme.borderRadius.sm, padding: theme.spacing.md, marginTop: theme.spacing.md },
  statusText: { fontSize: theme.fontSize.sm, fontWeight: '600' },
  infoCard: { backgroundColor: theme.colors.surface, borderRadius: theme.borderRadius.md, padding: theme.spacing.md },
  infoTitle: { fontSize: theme.fontSize.md, fontWeight: '700', color: theme.colors.text },
  infoText: { fontSize: theme.fontSize.sm, color: theme.colors.textSecondary, marginTop: 6, lineHeight: 20 },
  infoVersion: { fontSize: theme.fontSize.xs, color: theme.colors.textMuted, marginTop: theme.spacing.sm },
  tipCard: { flexDirection: 'row', gap: 10, backgroundColor: theme.colors.primary + '10', borderRadius: theme.borderRadius.md, padding: theme.spacing.md },
  tipText: { fontSize: theme.fontSize.sm, color: theme.colors.textSecondary, flex: 1, lineHeight: 22 },
});
