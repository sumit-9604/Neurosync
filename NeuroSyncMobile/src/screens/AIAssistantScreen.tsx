// src/screens/AIAssistantScreen.tsx — JARVIS HUD theme

import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import { api } from '../services/apiClient';
import { Colors, Fonts, Spacing, Radius } from '../theme';
import { CornerBrackets, ScanlineOverlay, HudTopBar, HudDivider } from '../components/HudComponents';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  timestamp: string;
}

const SUGGESTIONS = [
  'OPEN CHROME',
  'SCREENSHOT',
  'CPU USAGE?',
  'OPEN NOTEPAD',
];

export default function AIAssistantScreen({ navigation }: any) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      text: 'NEUROSYNC AI ONLINE. State your command for SUMIT-PC.',
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const listRef = useRef<FlatList>(null);

  const sendMessage = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      text: msg,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setTimeout(() => listRef.current?.scrollToEnd({ animated: true }), 100);

    try {
      const res = await api.post('/ai/command', { message: msg, device_id: 'sumit-pc' });
      const reply: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: res.data.reply || 'COMMAND EXECUTED.',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, reply]);
    } catch {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: 'ERR: CANNOT REACH SUMIT-PC. VERIFY DESKTOP AGENT IS RUNNING.',
        timestamp: new Date().toLocaleTimeString(),
      }]);
    } finally {
      setLoading(false);
      setTimeout(() => listRef.current?.scrollToEnd({ animated: true }), 100);
    }
  };

  const renderMessage = ({ item }: { item: Message }) => {
    const isUser = item.role === 'user';
    return (
      <View style={[styles.bubble, isUser ? styles.userBubble : styles.aiBubble]}>
        {!isUser && <View style={styles.aiAccent} />}
        <Text style={styles.bubbleRole}>{isUser ? 'YOU' : 'NEUROSYNC AI'}</Text>
        <Text style={[styles.bubbleText, isUser && styles.userText]}>{item.text}</Text>
        <Text style={styles.bubbleTime}>{item.timestamp}</Text>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <ScanlineOverlay />
      <CornerBrackets />

      <View style={styles.header}>
        <HudTopBar
          title="AI ASSISTANT"
          onBack={() => navigation.goBack()}
          rightLabel="SUMIT-PC"
          pulse
        />
      </View>

      <FlatList
        ref={listRef}
        data={messages}
        keyExtractor={item => item.id}
        renderItem={renderMessage}
        contentContainerStyle={styles.messageList}
        onContentSizeChange={() => listRef.current?.scrollToEnd({ animated: true })}
      />

      {loading && (
        <View style={styles.typingRow}>
          <ActivityIndicator size="small" color={Colors.cyan} />
          <Text style={styles.typingText}>PROCESSING COMMAND...</Text>
        </View>
      )}

      {/* Suggestion chips — only before first user message */}
      {messages.length <= 1 && (
        <View style={styles.chips}>
          {SUGGESTIONS.map(s => (
            <TouchableOpacity key={s} style={styles.chip} onPress={() => sendMessage(s)}>
              <Text style={styles.chipText}>{s}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      <HudDivider />

      {/* Input row */}
      <View style={styles.inputRow}>
        <Text style={styles.prompt}>›_</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter command..."
          placeholderTextColor={Colors.textMuted}
          value={input}
          onChangeText={setInput}
          multiline
          onSubmitEditing={() => sendMessage()}
          blurOnSubmit={false}
        />
        <TouchableOpacity
          style={[styles.sendBtn, (!input.trim() || loading) && styles.sendBtnOff]}
          onPress={() => sendMessage()}
          disabled={!input.trim() || loading}>
          <Text style={styles.sendBtnText}>TX</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  header: {
    paddingHorizontal: Spacing.lg,
    paddingTop: 56,
  },

  messageList: {
    padding: Spacing.lg,
    paddingTop: Spacing.sm,
    gap: Spacing.sm,
  },

  bubble: {
    maxWidth: '85%',
    borderRadius: Radius.md,
    padding: Spacing.md,
    borderWidth: 0.5,
    overflow: 'hidden',
    marginBottom: Spacing.sm,
  },
  aiBubble: {
    backgroundColor: Colors.bgCard,
    borderColor: Colors.cyanBorder,
    alignSelf: 'flex-start',
  },
  userBubble: {
    backgroundColor: `${Colors.cyan}18`,
    borderColor: `${Colors.cyan}55`,
    alignSelf: 'flex-end',
  },
  aiAccent: {
    position: 'absolute',
    left: 0, top: 0, bottom: 0,
    width: 2,
    backgroundColor: Colors.cyan,
  },
  bubbleRole: {
    color: Colors.textMuted,
    fontSize: 8,
    letterSpacing: 2,
    fontFamily: Fonts.uiReg,
    marginBottom: 4,
  },
  bubbleText: {
    color: Colors.textSecondary,
    fontSize: 13,
    fontFamily: Fonts.uiReg,
    lineHeight: 18,
    letterSpacing: 0.3,
  },
  userText: { color: Colors.cyan },
  bubbleTime: {
    color: Colors.textMuted,
    fontSize: 8,
    fontFamily: Fonts.hud,
    marginTop: 5,
    textAlign: 'right',
  },

  typingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
    paddingHorizontal: Spacing.lg,
    paddingBottom: Spacing.sm,
  },
  typingText: {
    color: Colors.textMuted,
    fontSize: 9,
    letterSpacing: 2,
    fontFamily: Fonts.hud,
  },

  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: Spacing.lg,
    gap: Spacing.sm,
    paddingBottom: Spacing.sm,
  },
  chip: {
    backgroundColor: Colors.bgCard,
    borderWidth: 0.5,
    borderColor: Colors.cyanBorder,
    borderRadius: Radius.pill,
    paddingHorizontal: 12,
    paddingVertical: 6,
  },
  chipText: {
    color: Colors.textSecondary,
    fontSize: 9,
    letterSpacing: 2,
    fontFamily: Fonts.ui,
  },

  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: Spacing.md,
    paddingHorizontal: Spacing.lg,
    gap: Spacing.sm,
  },
  prompt: {
    color: Colors.cyan,
    fontSize: 14,
    fontFamily: Fonts.hud,
  },
  input: {
    flex: 1,
    backgroundColor: Colors.bgCard,
    borderWidth: 0.5,
    borderColor: Colors.cyanBorder,
    borderRadius: Radius.sm,
    paddingHorizontal: 12,
    paddingVertical: 10,
    color: Colors.textPrimary,
    fontSize: 13,
    fontFamily: Fonts.hud,
    maxHeight: 90,
    letterSpacing: 0.5,
  },
  sendBtn: {
    width: 44,
    height: 44,
    borderRadius: Radius.sm,
    backgroundColor: `${Colors.cyan}22`,
    borderWidth: 1,
    borderColor: Colors.cyan,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendBtnOff: {
    backgroundColor: Colors.bgCard,
    borderColor: Colors.cyanBorder,
  },
  sendBtnText: {
    color: Colors.cyan,
    fontSize: 11,
    letterSpacing: 2,
    fontFamily: Fonts.ui,
  },
});
