import React, {useState} from 'react';
import {registerUser} from '../services/authService';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
} from 'react-native';

export default function RegisterScreen({navigation}: any) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleRegister = async () => {
  if (!name || !email || !password || !confirmPassword) {
    Alert.alert('Error', 'Please fill in all fields');
    return;
  }
  if (password !== confirmPassword) {
    Alert.alert('Error', 'Passwords do not match');
    return;
  }
  if (password.length < 6) {
    Alert.alert('Error', 'Password must be at least 6 characters');
    return;
  }
  try {
    await registerUser(email, password);
    Alert.alert('Success', 'Account created!', [
      {text: 'OK', onPress: () => navigation.replace('Login')},
    ]);
  } catch {
    Alert.alert('Error', 'Registration failed. Email may already exist.');
  }
};

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.logo}>🧠 NEUROSYNC</Text>
      <Text style={styles.subtitle}>Create your account</Text>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Full Name"
          placeholderTextColor="#555"
          value={name}
          onChangeText={setName}
          autoCapitalize="words"
        />
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
        <TextInput
          style={styles.input}
          placeholder="Confirm Password"
          placeholderTextColor="#555"
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          secureTextEntry
        />

        <TouchableOpacity style={styles.registerBtn} onPress={handleRegister}>
          <Text style={styles.registerBtnText}>Create Account</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.loginText}>
          Already have an account?{' '}
          <Text style={styles.loginLink}>Sign In</Text>
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212'},
  content: {padding: 24, justifyContent: 'center', flexGrow: 1},
  logo: {fontSize: 32, fontWeight: 'bold', color: '#00FF66', textAlign: 'center', letterSpacing: 2},
  subtitle: {fontSize: 14, color: '#888', textAlign: 'center', marginTop: 8, marginBottom: 40},
  form: {gap: 12},
  input: {backgroundColor: '#1E1E1E', borderWidth: 1, borderColor: '#333', borderRadius: 12, padding: 16, color: '#FFFFFF', fontSize: 16},
  registerBtn: {backgroundColor: '#00FF66', padding: 16, borderRadius: 12, alignItems: 'center', marginTop: 8},
  registerBtnText: {color: '#000000', fontSize: 16, fontWeight: 'bold'},
  loginText: {color: '#888', textAlign: 'center', marginTop: 32},
  loginLink: {color: '#00FF66'},
});