import React, {useRef, useState} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  PanResponder,
  Dimensions,
} from 'react-native';
import {sendCommand} from '../services/commandService';

const {width} = Dimensions.get('window');

export default function MouseControlScreen({navigation}: any) {
  const [status, setStatus] = useState('Touch to move mouse');
  const lastPos = useRef({x: 0, y: 0});

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onMoveShouldSetPanResponder: () => true,
      onPanResponderGrant: (_, gs) => {
        lastPos.current = {x: gs.x0, y: gs.y0};
      },
      onPanResponderMove: (_, gs) => {
        const dx = Math.round(gs.dx);
        const dy = Math.round(gs.dy);
        setStatus(`Moving: ${dx}, ${dy}`);
        sendCommand('sumit-pc', `mouse_move:${dx}:${dy}`).catch(() => {});
        lastPos.current = {x: gs.moveX, y: gs.moveY};
      },
      onPanResponderRelease: () => {
        setStatus('Touch to move mouse');
      },
    }),
  ).current;

  const handleClick = async (button: string) => {
    try {
      setStatus(`${button} click sent`);
      await sendCommand('sumit-pc', `mouse_click:${button}`);
      setTimeout(() => setStatus('Touch to move mouse'), 1000);
    } catch {
      setStatus('Could not reach device');
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Mouse Control</Text>
      <Text style={styles.statusText}>{status}</Text>

      {/* Trackpad area */}
      <View style={styles.trackpad} {...panResponder.panHandlers}>
        <Text style={styles.trackpadHint}>Drag to move cursor</Text>
      </View>

      {/* Click buttons */}
      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={styles.clickBtn}
          onPress={() => handleClick('left')}>
          <Text style={styles.clickBtnText}>Left Click</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.clickBtn, styles.scrollBtn]}
          onPress={() => handleClick('scroll_up')}>
          <Text style={styles.clickBtnText}>↑ Scroll</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.clickBtn, styles.scrollBtn]}
          onPress={() => handleClick('scroll_down')}>
          <Text style={styles.clickBtnText}>↓ Scroll</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.clickBtn, styles.rightBtn]}
          onPress={() => handleClick('right')}>
          <Text style={styles.clickBtnText}>Right Click</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  backBtn: {marginBottom: 16},
  backText: {color: '#00FF66', fontSize: 16},
  title: {fontSize: 24, fontWeight: 'bold', color: '#FFFFFF', marginBottom: 4},
  statusText: {fontSize: 13, color: '#888', marginBottom: 20},
  trackpad: {
    width: '100%',
    height: width * 0.75,
    backgroundColor: '#1E1E1E',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#333',
    justifyContent: 'center',
    alignItems: 'center',
  },
  trackpadHint: {color: '#444', fontSize: 14},
  buttonRow: {flexDirection: 'row', gap: 10, marginTop: 20},
  clickBtn: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    borderWidth: 1,
    borderColor: '#00FF66',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  rightBtn: {borderColor: '#FF4444'},
  scrollBtn: {borderColor: '#FFA500'},
  clickBtnText: {color: '#FFFFFF', fontSize: 14, fontWeight: '500'},
});