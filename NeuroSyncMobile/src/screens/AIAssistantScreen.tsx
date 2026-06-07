import React, {useState, useRef} from 'react';
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
import {api} from '../services/apiClient';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  timestamp: string;
}

const SUGGESTIONS = [
  'Open Chrome',
  'Take a screenshot',
  'What is my CPU usage?',
  'Open Notepad and type Hello',
];

export default function AIAssistantScreen({navigation}: any) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      text: 'Hi! I am your NeuroSync AI assistant. Tell me what you want to do on SUMIT-PC and I will handle it.',
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const listRef = useRef<FlatList>(null);

  const sendMessage = async (text?: string) => {
    const messageText = text || input.trim();
    if (!messageText) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      text: messageText,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    setTimeout(() => listRef.current?.scrollToEnd({animated: true}), 100);

    try {
      const response = await api.post('/ai/command', {
        message: messageText,
        device_id: 'sumit-pc',
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: response.data.reply || 'Command executed successfully!',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: 'Could not reach SUMIT-PC. Make sure the desktop agent is running and backend is connected.',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setTimeout(() => listRef.current?.scrollToEnd({animated: true}), 100);
    }
  };

  const renderMessage = ({item}: {item: Message}) => (
    <View
      style={[
        styles.messageBubble,
        item.role === 'user' ? styles.userBubble : styles.assistantBubble,
      ]}>
      <Text style={[styles.messageText, item.role === 'user' && {color: '#000000'}]}>
        {item.text}
      </Text>
      <Text style={[styles.timestamp, item.role === 'user' && {color: '#00000066'}]}>
        {item.timestamp}
      </Text>
    </View>
  );

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>AI Assistant</Text>
        <View style={styles.onlineIndicator}>
          <View style={styles.onlineDot} />
          <Text style={styles.onlineText}>SUMIT-PC</Text>
        </View>
      </View>

      <FlatList
        ref={listRef}
        data={messages}
        keyExtractor={item => item.id}
        renderItem={renderMessage}
        contentContainerStyle={styles.messageList}
        onContentSizeChange={() => listRef.current?.scrollToEnd({animated: true})}
      />

      {loading && (
        <View style={styles.typingIndicator}>
          <ActivityIndicator size="small" color="#00FF66" />
          <Text style={styles.typingText}>Processing command...</Text>
        </View>
      )}

      {/* Suggestion chips */}
      {messages.length <= 1 && (
        <View style={styles.suggestions}>
          {SUGGESTIONS.map(s => (
            <TouchableOpacity
              key={s}
              style={styles.chip}
              onPress={() => sendMessage(s)}>
              <Text style={styles.chipText}>{s}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Tell AI what to do..."
          placeholderTextColor="#555"
          value={input}
          onChangeText={setInput}
          multiline
          onSubmitEditing={() => sendMessage()}
        />
        <TouchableOpacity
          style={[styles.sendBtn, !input.trim() && styles.sendBtnDisabled]}
          onPress={() => sendMessage()}
          disabled={!input.trim() || loading}>
          <Text style={styles.sendBtnText}>↑</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212'},
  header: {paddingTop: 60, paddingHorizontal: 20, paddingBottom: 16, borderBottomWidth: 1, borderBottomColor: '#1E1E1E'},
  backText: {color: '#00FF66', fontSize: 16, marginBottom: 8},
  title: {fontSize: 22, fontWeight: 'bold', color: '#FFFFFF'},
  onlineIndicator: {flexDirection: 'row', alignItems: 'center', marginTop: 4},
  onlineDot: {width: 8, height: 8, borderRadius: 4, backgroundColor: '#00FF66', marginRight: 6},
  onlineText: {color: '#888', fontSize: 13},
  messageList: {padding: 16, paddingBottom: 8},
  messageBubble: {maxWidth: '80%', padding: 14, borderRadius: 16, marginBottom: 12},
  userBubble: {backgroundColor: '#00FF66', alignSelf: 'flex-end', borderBottomRightRadius: 4},
  assistantBubble: {backgroundColor: '#1E1E1E', alignSelf: 'flex-start', borderBottomLeftRadius: 4, borderWidth: 1, borderColor: '#2A2A2A'},
  messageText: {fontSize: 15, color: '#000000'},
  timestamp: {fontSize: 11, color: '#00000066', marginTop: 4, alignSelf: 'flex-end'},
  typingIndicator: {flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingBottom: 8, gap: 8},
  typingText: {color: '#555', fontSize: 13},
  suggestions: {flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 16, gap: 8, marginBottom: 8},
  chip: {backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#333', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20},
  chipText: {color: '#888', fontSize: 13},
  inputRow: {flexDirection: 'row', padding: 16, gap: 10, borderTopWidth: 1, borderTopColor: '#1E1E1E'},
  input: {flex: 1, backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#333', borderRadius: 24, paddingHorizontal: 16, paddingVertical: 10, color: '#FFFFFF', fontSize: 15, maxHeight: 100},
  sendBtn: {width: 46, height: 46, borderRadius: 23, backgroundColor: '#00FF66', justifyContent: 'center', alignItems: 'center'},
  sendBtnDisabled: {backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#333'},
  sendBtnText: {color: '#000000', fontSize: 20, fontWeight: 'bold'},
});