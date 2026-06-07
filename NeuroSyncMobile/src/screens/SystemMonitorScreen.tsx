import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import {api} from '../services/apiClient';

interface SystemStats {
  cpu: number;
  ram: number;
  ramTotal: number;
  ramUsed: number;
  disk: number;
  diskTotal: number;
  diskUsed: number;
  uptime: string;
  processes: number;
}

// Dummy data for now — will be replaced by real API
const DUMMY_STATS: SystemStats = {
  cpu: 34,
  ram: 61,
  ramTotal: 16,
  ramUsed: 9.8,
  disk: 47,
  diskTotal: 512,
  diskUsed: 240,
  uptime: '2h 34m',
  processes: 187,
};

function StatBar({value, color}: {value: number; color: string}) {
  return (
    <View style={styles.barBg}>
      <View style={[styles.barFill, {width: `${value}%` as any, backgroundColor: color}]} />
    </View>
  );
}

function StatCard({
  label,
  value,
  detail,
  color,
}: {
  label: string;
  value: number;
  detail: string;
  color: string;
}) {
  return (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <Text style={styles.cardLabel}>{label}</Text>
        <Text style={[styles.cardValue, {color}]}>{value}%</Text>
      </View>
      <StatBar value={value} color={color} />
      <Text style={styles.cardDetail}>{detail}</Text>
    </View>
  );
}

export default function SystemMonitorScreen({navigation}: any) {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState('');

  const fetchStats = async () => {
    try {
      const response = await api.get('/system/stats');
      setStats(response.data);
    } catch {
      // Backend not connected yet — show dummy data
      setStats(DUMMY_STATS);
    }
    setLastUpdated(new Date().toLocaleTimeString());
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchStats();
    setRefreshing(false);
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#00FF66" />
      }>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>System Monitor</Text>
      <Text style={styles.subtitle}>
        SUMIT-PC • Updated {lastUpdated || '...'}
      </Text>

      {stats ? (
        <>
          <StatCard
            label="CPU Usage"
            value={stats.cpu}
            detail={`${stats.processes} processes running`}
            color="#00FF66"
          />
          <StatCard
            label="RAM Usage"
            value={stats.ram}
            detail={`${stats.ramUsed} GB used of ${stats.ramTotal} GB`}
            color="#1E90FF"
          />
          <StatCard
            label="Disk Usage"
            value={stats.disk}
            detail={`${stats.diskUsed} GB used of ${stats.diskTotal} GB`}
            color="#FFA500"
          />

          <View style={styles.card}>
            <Text style={styles.cardLabel}>System Uptime</Text>
            <Text style={styles.uptimeValue}>{stats.uptime}</Text>
          </View>

          <Text style={styles.hint}>Pull down to refresh • Auto-updates every 5s</Text>
        </>
      ) : (
        <Text style={styles.loading}>Loading stats...</Text>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  backBtn: {marginBottom: 16},
  backText: {color: '#00FF66', fontSize: 16},
  title: {fontSize: 24, fontWeight: 'bold', color: '#FFFFFF', marginBottom: 4},
  subtitle: {fontSize: 13, color: '#888', marginBottom: 24},
  card: {backgroundColor: '#1E1E1E', borderRadius: 12, padding: 16, marginBottom: 14, borderWidth: 1, borderColor: '#2A2A2A'},
  cardHeader: {flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10},
  cardLabel: {color: '#888', fontSize: 14},
  cardValue: {fontSize: 18, fontWeight: 'bold'},
  barBg: {height: 8, backgroundColor: '#2A2A2A', borderRadius: 4, overflow: 'hidden', marginBottom: 8},
  barFill: {height: 8, borderRadius: 4},
  cardDetail: {color: '#555', fontSize: 12},
  uptimeValue: {color: '#00FF66', fontSize: 28, fontWeight: 'bold', marginTop: 6},
  hint: {color: '#444', fontSize: 12, textAlign: 'center', marginTop: 4, marginBottom: 40},
  loading: {color: '#888', textAlign: 'center', marginTop: 60, fontSize: 16},
});