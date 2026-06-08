/* eslint-disable react-native/no-inline-styles */
import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  Alert,
} from 'react-native';
import {api} from '../services/apiClient';

interface FileItem {
  name: string;
  type: 'folder' | 'file';
  size: string;
  modified: string;
  extension: string;
}

const DUMMY_FILES: FileItem[] = [
  {name: 'Documents', type: 'folder', size: '--', modified: 'Today', extension: ''},
  {name: 'Downloads', type: 'folder', size: '--', modified: 'Today', extension: ''},
  {name: 'Desktop', type: 'folder', size: '--', modified: 'Yesterday', extension: ''},
  {name: 'Pictures', type: 'folder', size: '--', modified: '3 days ago', extension: ''},
  {name: 'project_report.pdf', type: 'file', size: '2.4 MB', modified: 'Today', extension: 'pdf'},
  {name: 'notes.txt', type: 'file', size: '12 KB', modified: 'Today', extension: 'txt'},
  {name: 'budget.xlsx', type: 'file', size: '340 KB', modified: 'Yesterday', extension: 'xlsx'},
  {name: 'setup.exe', type: 'file', size: '78 MB', modified: '2 days ago', extension: 'exe'},
  {name: 'photo.png', type: 'file', size: '4.1 MB', modified: '3 days ago', extension: 'png'},
];

function getFileIcon(item: FileItem): string {
  if (item.type === 'folder') return '📁';
  const icons: Record<string, string> = {
    pdf: '📄',
    txt: '📝',
    xlsx: '📊',
    xls: '📊',
    doc: '📃',
    docx: '📃',
    exe: '⚙️',
    png: '🖼️',
    jpg: '🖼️',
    mp4: '🎬',
    mp3: '🎵',
    zip: '🗜️',
  };
  return icons[item.extension] || '📄';
}

export default function FileManagerScreen({navigation}: any) {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [currentPath, setCurrentPath] = useState('C:\\Users\\Sumit');
  const [pathHistory, setPathHistory] = useState<string[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  const fetchFiles = async (path: string) => {
    try {
      const response = await api.get(`/files?path=${encodeURIComponent(path)}`);
      setFiles(response.data);
    } catch {
      setFiles(DUMMY_FILES);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchFiles(currentPath);
    setRefreshing(false);
  };

  useEffect(() => {
    fetchFiles(currentPath);
  }, [currentPath]);

  const handleItemPress = (item: FileItem) => {
    if (item.type === 'folder') {
      setPathHistory(prev => [...prev, currentPath]);
      setCurrentPath(`${currentPath}\\${item.name}`);
    } else {
      Alert.alert(
        item.name,
        `Size: ${item.size}\nModified: ${item.modified}`,
        [
          {text: 'Cancel', style: 'cancel'},
          {
            text: 'Open on PC',
            onPress: async () => {
              try {
                await api.post('/files/open', {path: `${currentPath}\\${item.name}`});
                Alert.alert('Success', `Opening ${item.name} on PC`);
              } catch {
                Alert.alert('Error', 'Could not reach device');
              }
            },
          },
        ],
      );
    }
  };

  const handleBack = () => {
    if (pathHistory.length > 0) {
      const prev = pathHistory[pathHistory.length - 1];
      setPathHistory(h => h.slice(0, -1));
      setCurrentPath(prev);
    } else {
      navigation.goBack();
    }
  };

  const renderItem = ({item}: {item: FileItem}) => (
    <TouchableOpacity style={styles.fileRow} onPress={() => handleItemPress(item)}>
      <Text style={styles.fileIcon}>{getFileIcon(item)}</Text>
      <View style={styles.fileInfo}>
        <Text style={styles.fileName}>{item.name}</Text>
        <Text style={styles.fileMeta}>
          {item.type === 'folder' ? 'Folder' : item.size} • {item.modified}
        </Text>
      </View>
      {item.type === 'folder' && <Text style={styles.chevron}>›</Text>}
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={handleBack} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>File Manager</Text>
      <Text style={styles.pathText} numberOfLines={1}>{currentPath}</Text>

      <FlatList
        data={files}
        keyExtractor={item => item.name}
        renderItem={renderItem}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#00FF66" />
        }
        ItemSeparatorComponent={Separator}
        ListEmptyComponent={EmptyList}
      />
    </View>
  );
}
function Separator() {
  return <View style={{height: 1, backgroundColor: '#1E1E1E'}} />;
}

function EmptyList() {
  return <Text style={{color: '#555', textAlign: 'center', marginTop: 60}}>No files found</Text>;
}
const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#121212', padding: 20, paddingTop: 60},
  backBtn: {marginBottom: 16},
  backText: {color: '#00FF66', fontSize: 16},
  title: {fontSize: 24, fontWeight: 'bold', color: '#FFFFFF', marginBottom: 4},
  pathText: {fontSize: 12, color: '#555', marginBottom: 20, fontFamily: 'monospace'},
  fileRow: {flexDirection: 'row', alignItems: 'center', paddingVertical: 14},
  fileIcon: {fontSize: 24, marginRight: 14},
  fileInfo: {flex: 1},
  fileName: {color: '#FFFFFF', fontSize: 15, fontWeight: '500'},
  fileMeta: {color: '#555', fontSize: 12, marginTop: 2},
  chevron: {color: '#444', fontSize: 22},
  separator: {height: 1, backgroundColor: '#1E1E1E'},
  empty: {color: '#555', textAlign: 'center', marginTop: 60},
});