import React from 'react';
import {View, Text, TouchableOpacity, StyleSheet} from 'react-native';

export default function DevicesScreen({navigation}: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>NeuroSync</Text>
      <Text style={styles.sectionTitle}>Connected Devices</Text>
      <TouchableOpacity
        style={styles.card}
        onPress={() => navigation.navigate('DeviceDetails')}>
        <View style={styles.statusDot} />
        <View>
          <Text style={styles.deviceName}>SUMIT-PC</Text>
          <Text style={styles.deviceInfo}>Windows 11 • Online</Text>
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  title: {fontSize: 28, fontWeight: 'bold', color: '#00FF66', marginBottom: 8},
  sectionTitle: {fontSize: 16, color: '#888888', marginBottom: 20},
  card: {backgroundColor: '#1E1E1E', padding: 20, borderRadius: 12, flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: '#333'},
  statusDot: {width: 12, height: 12, borderRadius: 6, backgroundColor: '#00FF66', marginRight: 16},
  deviceName: {fontSize: 18, fontWeight: 'bold', color: '#FFFFFF'},
  deviceInfo: {fontSize: 13, color: '#888888', marginTop: 4},
});