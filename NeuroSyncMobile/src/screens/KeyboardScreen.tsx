import React, {useState} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  TextInput,
} from 'react-native';
import {sendCommand} from '../services/commandService';

const SPECIAL_KEYS = [
  {label: '⌫', value: 'backspace'},
  {label: 'Tab', value: 'tab'},
  {label: 'Enter', value: 'enter'},
  {label: 'Esc', value: 'escape'},
  {label: '⬆', value: 'up'},
  {label: '⬇', value: 'down'},
  {label: '⬅', value: 'left'},
  {label: '➡', value: 'right'},
  {label: 'Win', value: 'win'},
  {label: 'Del', value: 'delete'},
  {label: 'Space', value: 'space'},
  {label: 'Ctrl+C', value: 'ctrl+c'},
  {label: 'Ctrl+V', value: 'ctrl+v'},
  {label: 'Ctrl+Z', value: 'ctrl+z'},
  {label: 'Alt+F4', value: 'alt+f4'},
  {label: 'Ctrl+A', value: 'ctrl+a'},
];

export default function KeyboardScreen({navigation}: any) {
  const [text, setText] = useState('');
  const [status, setStatus] = useState('Ready');

  const sendKey = async (key: string) => {
    try {
      setStatus(`Sent: ${key}`);
      await sendCommand('sumit-pc', `key:${key}`);
      setTimeout(() => setStatus('Ready'), 1000);
    } catch {
      setStatus('Could not reach device');
    }
  };

  const sendText = async () => {
    if (!text.trim()) return;
    try {
      setStatus(`Typing: "${text}"`);
      await sendCommand('sumit-pc', `type:${text}`);
      setText('');
      setTimeout(() => setStatus('Ready'), 1000);
    } catch {
      setStatus('Could not reach device');
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Keyboard Control</Text>
      <Text style={styles.statusText}>{status}</Text>

      {/* Type text section */}
      <View style={styles.typeRow}>
        <TextInput
          style={styles.input}
          placeholder="Type text to send..."
          placeholderTextColor="#555"
          value={text}
          onChangeText={setText}
          autoCapitalize="none"
        />
        <TouchableOpacity style={styles.sendBtn} onPress={sendText}>
          <Text style={styles.sendBtnText}>Send</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.sectionLabel}>SPECIAL KEYS</Text>

      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.keyGrid}>
          {SPECIAL_KEYS.map(key => (
            <TouchableOpacity
              key={key.value}
              style={styles.keyBtn}
              onPress={() => sendKey(key.value)}>
              <Text style={styles.keyLabel}>{key.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  backBtn: {marginBottom: 16},
  backText: {color: '#00FF66', fontSize: 16},
  title: {fontSize: 24, fontWeight: 'bold', color: '#FFFFFF', marginBottom: 4},
  statusText: {fontSize: 13, color: '#888', marginBottom: 20},
  typeRow: {flexDirection: 'row', gap: 10, marginBottom: 24},
  input: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 12,
    padding: 14,
    color: '#FFFFFF',
    fontSize: 15,
  },
  sendBtn: {
    backgroundColor: '#00FF66',
    borderRadius: 12,
    paddingHorizontal: 18,
    justifyContent: 'center',
  },
  sendBtnText: {color: '#000', fontWeight: 'bold', fontSize: 15},
  sectionLabel: {fontSize: 12, color: '#555', fontWeight: 'bold', letterSpacing: 1, marginBottom: 14},
  keyGrid: {flexDirection: 'row', flexWrap: 'wrap', gap: 10},
  keyBtn: {
    backgroundColor: '#1E1E1E',
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 10,
    paddingVertical: 14,
    paddingHorizontal: 16,
    minWidth: '22%',
    alignItems: 'center',
  },
  keyLabel: {color: '#FFFFFF', fontSize: 14, fontWeight: '500'},
});