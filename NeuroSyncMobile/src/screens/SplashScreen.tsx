import React, {useEffect} from 'react';
import {View, Text, StyleSheet} from 'react-native';

export default function SplashScreen({navigation}: any) {
  useEffect(() => {
    const timer = setTimeout(() => {
      navigation.navigate('Login');
    }, 2000);
    return () => clearTimeout(timer);
  }, [navigation]);

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>🧠 NEUROSYNC</Text>
      <Text style={styles.subtitle}>Connecting to Ecosystem...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', justifyContent: 'center', alignItems: 'center'},
  logo: {fontSize: 32, fontWeight: 'bold', color: '#00FF66', letterSpacing: 2},
  subtitle: {fontSize: 14, color: '#888888', marginTop: 10},
});