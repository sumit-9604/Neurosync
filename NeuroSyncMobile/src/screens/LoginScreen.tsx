import React, {useState} from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from 'react-native';

export default function LoginScreen({navigation}: any) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailLogin = () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter email and password');
      return;
    }
    navigation.replace('Devices');
  };

  const handleGoogleLogin = () => {
    Alert.alert('Coming Soon', 'Google Sign-In will be set up soon!');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>🧠 NEUROSYNC</Text>
      <Text style={styles.subtitle}>Sign in to continue</Text>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="#555"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Password"
          placeholderTextColor="#555"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity style={styles.loginBtn} onPress={handleEmailLogin}>
          <Text style={styles.loginBtnText}>Sign In</Text>
        </TouchableOpacity>

        <View style={styles.divider}>
          <View style={styles.dividerLine} />
          <Text style={styles.dividerText}>OR</Text>
          <View style={styles.dividerLine} />
        </View>

        <TouchableOpacity style={styles.googleBtn} onPress={handleGoogleLogin}>
          <Text style={styles.googleBtnText}>🔵 Continue with Google</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity>
        <Text style={styles.registerText}>
          Don't have an account? <Text style={styles.registerLink}>Register</Text>
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 24, justifyContent: 'center'},
  logo: {fontSize: 32, fontWeight: 'bold', color: '#00FF66', textAlign: 'center', letterSpacing: 2},
  subtitle: {fontSize: 14, color: '#888', textAlign: 'center', marginTop: 8, marginBottom: 40},
  form: {gap: 12},
  input: {backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#333', borderRadius: 12, padding: 16, color: '#FFFFFF', fontSize: 16},
  loginBtn: {backgroundColor: '#00FF66', padding: 16, borderRadius: 12, alignItems: 'center', marginTop: 8},
  loginBtnText: {color: '#000000', fontSize: 16, fontWeight: 'bold'},
  divider: {flexDirection: 'row', alignItems: 'center', gap: 12, marginVertical: 8},
  dividerLine: {flex: 1, height: 1, backgroundColor: '#333'},
  dividerText: {color: '#555', fontSize: 14},
  googleBtn: {backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#333', padding: 16, borderRadius: 12, alignItems: 'center'},
  googleBtnText: {color: '#FFFFFF', fontSize: 16},
  registerText: {color: '#888', textAlign: 'center', marginTop: 32},
  registerLink: {color: '#00FF66'},
});