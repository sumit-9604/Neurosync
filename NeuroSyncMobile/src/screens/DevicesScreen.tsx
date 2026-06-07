// src/screens/DevicesScreen.tsx — JARVIS HUD theme

import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { GoogleSignin } from '@react-native-google-signin/google-signin';
import { Colors, Fonts, Spacing, Radius } from '../theme';
import { CornerBrackets, ScanlineOverlay, HudDivider } from '../components/HudComponents';

export default function DevicesScreen({ navigation }: any) {
  const handleSignOut = () => {
    Alert.alert('SIGN OUT', 'Terminate current session?', [
      { text: 'CANCEL', style: 'cancel' },
      {
        text: 'CONFIRM',
        style: 'destructive',
        onPress: async () => {
          try {
            await GoogleSignin.signOut();
            navigation.replace('Login');
          } catch {
            Alert.alert('ERROR', 'Could not sign out. Try again.');
          }
        },
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <ScanlineOverlay />
      <CornerBrackets />

      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>NEUROSYNC</Text>
          <Text style={styles.subtitle}>DEVICE NETWORK</Text>
        </View>
        <TouchableOpacity style={styles.signOutBtn} onPress={handleSignOut}>
          <Text style={styles.signOutText}>⏻ SIGN OUT</Text>
        </TouchableOpacity>
      </View>

      <HudDivider />

      {/* Section label */}
      <Text style={styles.sectionLabel}>CONNECTED DEVICES</Text>

      {/* Device card */}
      <TouchableOpacity
        style={styles.deviceCard}
        onPress={() => navigation.navigate('DeviceDetails')}
        activeOpacity={0.8}>
        {/* left accent */}
        <View style={styles.cardAccent} />

        {/* status dot */}
        <View style={styles.statusIndicator}>
          <View style={styles.statusDot} />
          <View style={styles.statusRing} />
        </View>

        <View style={styles.deviceInfo}>
          <Text style={styles.deviceName}>SUMIT-PC</Text>
          <Text style={styles.deviceMeta}>WINDOWS 11  ·  ONLINE</Text>
        </View>

        <Text style={styles.chevron}>›</Text>
      </TouchableOpacity>

      {/* Empty state hint */}
      <Text style={styles.hint}>{'// TAP DEVICE TO ACCESS CONTROL PANEL'}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.bg,
    padding: Spacing.lg,
    paddingTop: 56,
  },

  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: Spacing.md,
  },
  title: {
    color: Colors.cyan,
    fontSize: 24,
    letterSpacing: 6,
    fontFamily: Fonts.ui,
  },
  subtitle: {
    color: Colors.textMuted,
    fontSize: 9,
    letterSpacing: 3,
    fontFamily: Fonts.uiReg,
    marginTop: 2,
  },
  signOutBtn: {
    borderWidth: 0.5,
    borderColor: Colors.redBorder,
    borderRadius: Radius.sm,
    paddingHorizontal: 12,
    paddingVertical: 7,
  },
  signOutText: {
    color: Colors.red,
    fontSize: 10,
    letterSpacing: 1.5,
    fontFamily: Fonts.uiReg,
  },

  sectionLabel: {
    color: Colors.textMuted,
    fontSize: 9,
    letterSpacing: 3,
    fontFamily: Fonts.uiReg,
    marginBottom: Spacing.md,
  },

  deviceCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.bgCard,
    borderWidth: 0.5,
    borderColor: Colors.cyanBorder,
    borderRadius: Radius.md,
    padding: Spacing.lg,
    overflow: 'hidden',
  },
  cardAccent: {
    position: 'absolute',
    left: 0, top: 0, bottom: 0,
    width: 2,
    backgroundColor: Colors.cyan,
  },
  statusIndicator: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.md,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.cyan,
    position: 'absolute',
  },
  statusRing: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 0.5,
    borderColor: Colors.cyanBorder,
  },
  deviceInfo: { flex: 1 },
  deviceName: {
    color: Colors.textPrimary,
    fontSize: 16,
    letterSpacing: 2,
    fontFamily: Fonts.ui,
  },
  deviceMeta: {
    color: Colors.textMuted,
    fontSize: 9,
    letterSpacing: 2,
    fontFamily: Fonts.uiReg,
    marginTop: 3,
  },
  chevron: {
    color: Colors.cyanDim,
    fontSize: 20,
    fontFamily: Fonts.uiReg,
  },

  hint: {
    color: Colors.textMuted,
    fontSize: 9,
    letterSpacing: 1,
    fontFamily: Fonts.hud,
    marginTop: Spacing.xl,
    textAlign: 'center',
  },
});
