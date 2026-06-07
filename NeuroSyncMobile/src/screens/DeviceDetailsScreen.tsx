import React from 'react';
import {View, Text, TouchableOpacity, StyleSheet} from 'react-native';

export default function DeviceDetailsScreen({navigation}: any) {
  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.deviceName}>SUMIT-PC</Text>
      <Text style={styles.status}>🟢 Online</Text>

      <View style={styles.infoCard}>
        <InfoRow label="Hostname" value="SUMIT-PC" />
        <InfoRow label="OS" value="Windows 11" />
        <InfoRow label="Last Seen" value="Just now" />
        <InfoRow label="IP Address" value="192.168.1.x" />
      </View>

      <TouchableOpacity
        style={styles.controlBtn}
        onPress={() => navigation.navigate('RemoteDashboard')}>
        <Text style={styles.controlBtnText}>Open Remote Dashboard →</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.mouseBtn}
        onPress={() => navigation.navigate('MouseControl')}>
        <Text style={styles.mouseBtnText}>🖱️ Mouse Control →</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.mouseBtn}
        onPress={() => navigation.navigate('Keyboard')}>
        <Text style={styles.mouseBtnText}>⌨️ Keyboard Control →</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.mouseBtn}
        onPress={() => navigation.navigate('SystemMonitor')}>
        <Text style={styles.mouseBtnText}>📊 System Monitor →</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.mouseBtn}
        onPress={() => navigation.navigate('FileManager')}>
        <Text style={styles.mouseBtnText}>📁 File Manager →</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.mouseBtn}
        onPress={() => navigation.navigate('AIAssistant')}>
        <Text style={styles.mouseBtnText}>🤖 AI Assistant →</Text>
      </TouchableOpacity>
    </View>
  );
}

function InfoRow({label, value}: {label: string; value: string}) {
  return (
    <View style={styles.row}>
      <Text style={styles.label}>{label}</Text>
      <Text style={styles.value}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  backBtn: {marginBottom: 24},
  backText: {color: '#00FF66', fontSize: 16},
  deviceName: {fontSize: 28, fontWeight: 'bold', color: '#FFFFFF', marginBottom: 8},
  status: {fontSize: 16, color: '#00FF66', marginBottom: 24},
  infoCard: {backgroundColor: '#1E1E1E', borderRadius: 12, padding: 16, borderWidth: 1, borderColor: '#333'},
  row: {flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#2A2A2A'},
  label: {color: '#888888', fontSize: 14},
  value: {color: '#FFFFFF', fontSize: 14, fontWeight: '500'},
  controlBtn: {marginTop: 24, backgroundColor: '#00FF66', padding: 16, borderRadius: 12, alignItems: 'center'},
  controlBtnText: {color: '#000000', fontSize: 16, fontWeight: 'bold'},
  mouseBtn: {marginTop: 12, backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#00FF66', padding: 16, borderRadius: 12, alignItems: 'center'},
  mouseBtnText: {color: '#00FF66', fontSize: 16, fontWeight: 'bold'},
});