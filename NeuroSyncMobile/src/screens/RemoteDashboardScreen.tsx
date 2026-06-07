import React from 'react';
import {Text, TouchableOpacity, StyleSheet, ScrollView, Alert} from 'react-native';
import {sendCommand} from '../services/commandService';

const commands = [
  {id: 'notepad', label: '📝 Open Notepad', color: '#1E90FF'},
  {id: 'chrome', label: '🌐 Open Chrome', color: '#FF6B35'},
  {id: 'vscode', label: '💻 Open VS Code', color: '#007ACC'},
  {id: 'shutdown', label: '⛔ Shutdown', color: '#FF4444'},
  {id: 'restart', label: '🔄 Restart', color: '#FFA500'},
];

export default function RemoteDashboardScreen({navigation}: any) {
  const handleCommand = async (commandId: string) => {
    try {
      await sendCommand('sumit-pc', commandId);
      Alert.alert('Success', `Command "${commandId}" sent!`);
    } catch {
      Alert.alert('Error', 'Could not reach the device. Is the backend running?');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Remote Dashboard</Text>
      <Text style={styles.subtitle}>SUMIT-PC • Windows 11</Text>

      <Text style={styles.sectionLabel}>LAUNCH APPS</Text>
      {commands.slice(0, 3).map(cmd => (
        <TouchableOpacity
          key={cmd.id}
          style={[styles.commandBtn, {borderLeftColor: cmd.color}]}
          onPress={() => handleCommand(cmd.id)}>
          <Text style={styles.commandText}>{cmd.label}</Text>
          <Text style={styles.arrow}>→</Text>
        </TouchableOpacity>
      ))}

      <Text style={styles.sectionLabel}>POWER</Text>
      {commands.slice(3).map(cmd => (
        <TouchableOpacity
          key={cmd.id}
          style={[styles.commandBtn, {borderLeftColor: cmd.color}]}
          onPress={() => handleCommand(cmd.id)}>
          <Text style={styles.commandText}>{cmd.label}</Text>
          <Text style={styles.arrow}>→</Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  backBtn: {marginBottom: 24},
  backText: {color: '#00FF66', fontSize: 16},
  title: {fontSize: 28, fontWeight: 'bold', color: '#FFFFFF', marginBottom: 4},
  subtitle: {fontSize: 14, color: '#888888', marginBottom: 32},
  sectionLabel: {fontSize: 12, color: '#555555', fontWeight: 'bold', marginBottom: 12, letterSpacing: 1},
  commandBtn: {backgroundColor: '#1E1E1E', padding: 20, borderRadius: 12, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, borderLeftWidth: 4},
  commandText: {fontSize: 16, color: '#FFFFFF'},
  arrow: {color: '#555555', fontSize: 18},
});