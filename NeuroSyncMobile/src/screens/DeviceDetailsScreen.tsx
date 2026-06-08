// src/screens/DeviceDetailsScreen.tsx — JARVIS HUD theme

import React from 'react';
import {View, Text, StyleSheet, ScrollView} from 'react-native';
import {Colors, Fonts, Spacing, Radius} from '../theme';
import {
  CornerBrackets,
  ScanlineOverlay,
  HudTopBar,
  HudButton,
  StatBarRow,
  HudDivider,
} from '../components/HudComponents';

function InfoRow({label, value}: {label: string; value: string}) {
  return (
    <View style={styles.infoRow}>
      <Text style={styles.infoLabel}>{label}</Text>
      <Text style={styles.infoValue}>{value}</Text>
    </View>
  );
}

export default function DeviceDetailsScreen({navigation, route}: any) {
  const device = route.params?.device || {};
  const deviceName = device.device_id || device.name || device.device_name || device.hostname || 'UNKNOWN';
  const deviceOs = device.os || 'WINDOWS 11';
  const deviceIp = device.ip_address || device.ip || '—';
  const lastSeen = device.last_seen || 'Just now';

  return (
    <View style={styles.container}>
      <ScanlineOverlay />
      <CornerBrackets />

      <HudTopBar
        title="DEVICE DETAILS"
        onBack={() => navigation.goBack()}
        rightLabel="ONLINE"
        pulse
      />

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
        {/* Device header */}
        <View style={styles.deviceHeader}>
          <View>
            <Text style={styles.deviceName}>{deviceName}</Text>
            <Text style={styles.deviceOs}>{deviceOs}  ·  64-BIT</Text>
          </View>
          <View style={styles.onlineBadge}>
            <View style={styles.badgeDot} />
            <Text style={styles.badgeText}>LIVE</Text>
          </View>
        </View>

        {/* Quick stats */}
        <View style={styles.quickStats}>
          <StatBarRow label="CPU" value={34} />
          <StatBarRow label="RAM" value={61} color={Colors.blue} />
          <StatBarRow label="DISK" value={47} color={Colors.amber} />
        </View>

        <HudDivider />

        {/* Info card */}
        <Text style={styles.sectionLabel}>DEVICE INFO</Text>
        <View style={styles.infoCard}>
          <InfoRow label="HOSTNAME" value={deviceName} />
          <InfoRow label="OS" value={deviceOs} />
          <InfoRow label="IP ADDRESS" value={deviceIp} />
          <InfoRow label="LAST SEEN" value={lastSeen} />
        </View>

        <HudDivider />

        {/* Control modules */}
        <Text style={styles.sectionLabel}>CONTROL MODULES</Text>

        <View style={styles.btnList}>
          <HudButton
            icon="🖥"
            label="REMOTE DASHBOARD"
            onPress={() => navigation.navigate('RemoteDashboard', {device})}
          />
          <HudButton
            icon="🖱️"
            label="MOUSE CONTROL"
            onPress={() => navigation.navigate('MouseControl', {device})}
          />
          <HudButton
            icon="⌨️"
            label="KEYBOARD"
            onPress={() => navigation.navigate('Keyboard', {device})}
          />
          <HudButton
            icon="📊"
            label="SYSTEM MONITOR"
            color={Colors.blue}
            onPress={() => navigation.navigate('SystemMonitor', {device})}
          />
          <HudButton
            icon="📁"
            label="FILE MANAGER"
            color={Colors.amber}
            onPress={() => navigation.navigate('FileManager', {device})}
          />
          <HudButton
            icon="🤖"
            label="AI ASSISTANT"
            color={Colors.cyan}
            onPress={() => navigation.navigate('AIAssistant', {device})}
          />
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: Colors.bg, padding: Spacing.lg, paddingTop: 56},
  scroll: {paddingBottom: 40},
  deviceHeader: {flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: Spacing.md},
  deviceName: {color: Colors.cyan, fontSize: 26, letterSpacing: 4, fontFamily: Fonts.ui},
  deviceOs: {color: Colors.textMuted, fontSize: 9, letterSpacing: 2.5, fontFamily: Fonts.uiReg, marginTop: 4},
  onlineBadge: {flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: `${Colors.cyan}15`, borderWidth: 0.5, borderColor: Colors.cyanBorder, borderRadius: Radius.pill, paddingHorizontal: 10, paddingVertical: 5},
  badgeDot: {width: 5, height: 5, borderRadius: 3, backgroundColor: Colors.cyan},
  badgeText: {color: Colors.cyan, fontSize: 9, letterSpacing: 2, fontFamily: Fonts.ui},
  quickStats: {marginBottom: Spacing.sm},
  sectionLabel: {color: Colors.textMuted, fontSize: 9, letterSpacing: 3, fontFamily: Fonts.uiReg, marginBottom: Spacing.sm},
  infoCard: {backgroundColor: Colors.bgCard, borderWidth: 0.5, borderColor: Colors.cyanBorder, borderRadius: Radius.md, overflow: 'hidden', marginBottom: Spacing.sm},
  infoRow: {flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 11, paddingHorizontal: Spacing.md, borderBottomWidth: 0.5, borderBottomColor: Colors.divider},
  infoLabel: {color: Colors.textSecondary, fontSize: 10, letterSpacing: 2, fontFamily: Fonts.uiReg},
  infoValue: {color: Colors.textPrimary, fontSize: 12, fontFamily: Fonts.hud, letterSpacing: 0.5},
  btnList: {gap: Spacing.sm},
});