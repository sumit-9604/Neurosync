import React from 'react';
import {View, Text, TouchableOpacity, StyleSheet, Alert} from 'react-native';
import {GoogleSignin} from '@react-native-google-signin/google-signin';

export default function DevicesScreen({navigation}: any) {
  const handleSignOut = async () => {
    Alert.alert(
      'Sign Out',
      'Are you sure you want to sign out?',
      [
        {text: 'Cancel', style: 'cancel'},
        {
          text: 'Sign Out',
          style: 'destructive',
          onPress: async () => {
            try {
              await GoogleSignin.signOut();
              navigation.replace('Login');
            } catch {
              Alert.alert('Error', 'Could not sign out. Try again.');
            }
          },
        },
      ],
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>NeuroSync</Text>
        <TouchableOpacity onPress={handleSignOut} style={styles.signOutBtn}>
          <Text style={styles.signOutText}>Sign Out</Text>
        </TouchableOpacity>
      </View>

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
  header: {flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8},
  title: {fontSize: 28, fontWeight: 'bold', color: '#00FF66'},
  signOutBtn: {backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#FF4444', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 8},
  signOutText: {color: '#FF4444', fontSize: 13, fontWeight: '500'},
  sectionTitle: {fontSize: 16, color: '#888888', marginBottom: 20},
  card: {backgroundColor: '#1E1E1E', padding: 20, borderRadius: 12, flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: '#333'},
  statusDot: {width: 12, height: 12, borderRadius: 6, backgroundColor: '#00FF66', marginRight: 16},
  deviceName: {fontSize: 18, fontWeight: 'bold', color: '#FFFFFF'},
  deviceInfo: {fontSize: 13, color: '#888888', marginTop: 4},
});