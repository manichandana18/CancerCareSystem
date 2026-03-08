import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  TextInput,
  Image,
  ScrollView,
  Alert,
  StatusBar,
  SafeAreaView,
  Dimensions,
  ActivityIndicator
} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const { width, height } = Dimensions.get('window');

// Colors
const colors = {
  primary: '#1e3a8a',
  secondary: '#3b82f6',
  accent: '#10b981',
  danger: '#ef4444',
  warning: '#f59e0b',
  light: '#f9fafb',
  dark: '#111827',
  border: '#e5e7eb',
};

// Main App Component
export default function CancerCareApp() {
  const [currentScreen, setCurrentScreen] = useState('dashboard');
  const [selectedMood, setSelectedMood] = useState('');
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  // Screen Components
  const renderDashboard = () => (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.userInfo}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>JD</Text>
          </View>
          <View style={styles.welcomeText}>
            <Text style={styles.welcomeTitle}>Welcome back, John!</Text>
            <Text style={styles.welcomeSubtitle}>How are you feeling today?</Text>
          </View>
        </View>
        <View style={styles.healthScore}>
          <Text style={styles.scoreNumber}>92</Text>
          <Text style={styles.scoreLabel}>Health Score</Text>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <TouchableOpacity style={styles.actionCard} onPress={() => setCurrentScreen('detection')}>
          <View style={styles.actionIcon}>
            <Icon name="microscope" size={24} color="white" />
          </View>
          <Text style={styles.actionTitle}>Scan</Text>
          <Text style={styles.actionSubtitle}>Upload medical image</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard} onPress={() => setCurrentScreen('mental')}>
          <View style={styles.actionIcon}>
            <Icon name="brain" size={24} color="white" />
          </View>
          <Text style={styles.actionTitle}>Mental Health</Text>
          <Text style={styles.actionSubtitle}>Track your mood</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard} onPress={() => setCurrentScreen('records')}>
          <View style={styles.actionIcon}>
            <Icon name="file-medical" size={24} color="white" />
          </View>
          <Text style={styles.actionTitle}>Records</Text>
          <Text style={styles.actionSubtitle}>View history</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard} onPress={() => setCurrentScreen('appointments')}>
          <View style={styles.actionIcon}>
            <Icon name="calendar-check" size={24} color="white" />
          </View>
          <Text style={styles.actionTitle}>Appointments</Text>
          <Text style={styles.actionSubtitle}>Schedule visits</Text>
        </TouchableOpacity>
      </View>

      {/* Recent Activity */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Activity</Text>
        <TouchableOpacity style={styles.recordItem}>
          <Text style={styles.recordTitle}>Cancer Scan - Lung</Text>
          <Text style={styles.recordDate}>2 days ago • 97% confidence</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.recordItem}>
          <Text style={styles.recordTitle}>Mood Check-in</Text>
          <Text style={styles.recordDate}>Yesterday • Feeling good</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  const renderDetection = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.screenTitle}>Cancer Detection</Text>
      
      <TouchableOpacity style={styles.uploadArea}>
        <Icon name="cloud-upload" size={60} color={colors.secondary} />
        <Text style={styles.uploadTitle}>Upload Medical Image</Text>
        <Text style={styles.uploadSubtitle}>Drag and drop or tap to browse</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.button, styles.cameraButton]}>
        <Icon name="camera" size={20} color="white" />
        <Text style={styles.buttonText}>Take Photo</Text>
      </TouchableOpacity>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Scans</Text>
        <TouchableOpacity style={styles.recordItem}>
          <Text style={styles.recordTitle}>Chest X-Ray</Text>
          <Text style={styles.recordDate}>2 days ago • No cancer detected</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.recordItem}>
          <Text style={styles.recordTitle}>Brain MRI</Text>
          <Text style={styles.recordDate}>1 week ago • Clear</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  const renderMentalHealth = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.screenTitle}>Mental Health</Text>
      
      <View style={styles.moodCard}>
        <Text style={styles.moodQuestion}>How are you feeling today?</Text>
        <View style={styles.moodTracker}>
          {['great', 'good', 'okay', 'bad', 'terrible'].map((mood, index) => (
            <TouchableOpacity
              key={mood}
              style={[
                styles.moodOption,
                selectedMood === mood && styles.selectedMood
              ]}
              onPress={() => {
                setSelectedMood(mood);
                Alert.alert('Mood Saved', `You're feeling ${mood} today!`);
              }}
            >
              <Text style={styles.moodEmoji}>
                {['😊', '🙂', '😐', '😔', '😢'][index]}
              </Text>
              <Text style={styles.moodLabel}>
                {['Great', 'Good', 'Okay', 'Bad', 'Terrible'][index]}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.quickActions}>
        <TouchableOpacity style={styles.actionCard}>
          <View style={styles.actionIcon}>
            <Icon name="spa" size={24} color="white" />
          </View>
          <Text style={styles.actionTitle}>Meditation</Text>
          <Text style={styles.actionSubtitle}>5 min session</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard}>
          <View style={styles.actionIcon}>
            <Icon name="comments" size={24} color="white" />
          </View>
          <Text style={styles.actionTitle}>Support</Text>
          <Text style={styles.actionSubtitle}>Talk to someone</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Mood History</Text>
        <TouchableOpacity style={styles.recordItem}>
          <Text style={styles.recordTitle}>Yesterday - Good 😊</Text>
          <Text style={styles.recordDate}>Feeling positive and motivated</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.recordItem}>
          <Text style={styles.recordTitle}>2 days ago - Okay 😐</Text>
          <Text style={styles.recordDate}>Some anxiety about treatment</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  const renderRecords = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.screenTitle}>Medical Records</Text>
      
      <TouchableOpacity style={styles.recordItem}>
        <Text style={styles.recordTitle}>Blood Test Results</Text>
        <Text style={styles.recordDate}>Oct 15, 2024 • Dr. Smith</Text>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: '85%' }]} />
        </View>
        <Text style={styles.recordNote}>All values normal</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.recordItem}>
        <Text style={styles.recordTitle}>Cancer Screening</Text>
        <Text style={styles.recordDate}>Oct 10, 2024 • Dr. Johnson</Text>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: '97%' }]} />
        </View>
        <Text style={styles.recordNote}>No cancer detected</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.recordItem}>
        <Text style={styles.recordTitle}>MRI Scan</Text>
        <Text style={styles.recordDate}>Sep 28, 2024 • Dr. Williams</Text>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: '100%' }]} />
        </View>
        <Text style={styles.recordNote}>Clear results</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.recordItem}>
        <Text style={styles.recordTitle}>Prescription</Text>
        <Text style={styles.recordDate}>Sep 15, 2024 • Dr. Brown</Text>
        <Text style={styles.recordNote}>Vitamin D supplements</Text>
      </TouchableOpacity>
    </ScrollView>
  );

  const renderAppointments = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.screenTitle}>Appointments</Text>
      
      <TouchableOpacity style={[styles.button, styles.bookButton]}>
        <Icon name="plus" size={20} color="white" />
        <Text style={styles.buttonText}>Book New Appointment</Text>
      </TouchableOpacity>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Upcoming</Text>
        <TouchableOpacity style={styles.appointmentCard}>
          <Text style={styles.appointmentTime}>Tomorrow, 10:00 AM</Text>
          <Text style={styles.appointmentDoctor}>Dr. Sarah Johnson - Oncologist</Text>
          <Text style={styles.appointmentType}>Follow-up consultation</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.appointmentCard}>
          <Text style={styles.appointmentTime}>Oct 25, 2:30 PM</Text>
          <Text style={styles.appointmentDoctor}>Dr. Michael Chen - Radiologist</Text>
          <Text style={styles.appointmentType}>MRI Scan</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Past</Text>
        <TouchableOpacity style={[styles.appointmentCard, { opacity: 0.7 }]}>
          <Text style={styles.appointmentTime}>Oct 10, 11:00 AM</Text>
          <Text style={styles.appointmentDoctor}>Dr. Emily Davis - General Practitioner</Text>
          <Text style={styles.appointmentType}>Annual checkup</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  const renderSettings = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.screenTitle}>Settings</Text>
      
      <TouchableOpacity style={styles.settingsItem}>
        <View style={styles.settingsLeft}>
          <View style={styles.settingsIcon}>
            <Icon name="user" size={20} color="white" />
          </View>
          <View>
            <Text style={styles.settingsTitle}>Profile</Text>
            <Text style={styles.settingsSubtitle}>John Doe</Text>
          </View>
        </View>
        <Icon name="chevron-right" size={20} color={colors.border} />
      </TouchableOpacity>

      <TouchableOpacity style={styles.settingsItem}>
        <View style={styles.settingsLeft}>
          <View style={styles.settingsIcon}>
            <Icon name="bell" size={20} color="white" />
          </View>
          <View>
            <Text style={styles.settingsTitle}>Notifications</Text>
            <Text style={styles.settingsSubtitle}>Push notifications</Text>
          </View>
        </View>
        <TouchableOpacity
          style={[styles.toggleSwitch, notifications && styles.toggleSwitchActive]}
          onPress={() => setNotifications(!notifications)}
        >
          <View style={[styles.toggleSwitchKnob, notifications && styles.toggleSwitchKnobActive]} />
        </TouchableOpacity>
      </TouchableOpacity>

      <TouchableOpacity style={styles.settingsItem}>
        <View style={styles.settingsLeft}>
          <View style={styles.settingsIcon}>
            <Icon name="lock" size={20} color="white" />
          </View>
          <View>
            <Text style={styles.settingsTitle}>Privacy</Text>
            <Text style={styles.settingsSubtitle}>Data sharing settings</Text>
          </View>
        </View>
        <Icon name="chevron-right" size={20} color={colors.border} />
      </TouchableOpacity>

      <TouchableOpacity style={styles.settingsItem}>
        <View style={styles.settingsLeft}>
          <View style={styles.settingsIcon}>
            <Icon name="moon" size={20} color="white" />
          </View>
          <View>
            <Text style={styles.settingsTitle}>Dark Mode</Text>
            <Text style={styles.settingsSubtitle}>Theme settings</Text>
          </View>
        </View>
        <TouchableOpacity
          style={[styles.toggleSwitch, darkMode && styles.toggleSwitchActive]}
          onPress={() => setDarkMode(!darkMode)}
        >
          <View style={[styles.toggleSwitchKnob, darkMode && styles.toggleSwitchKnobActive]} />
        </TouchableOpacity>
      </TouchableOpacity>
    </ScrollView>
  );

  // Render current screen
  const renderScreen = () => {
    switch (currentScreen) {
      case 'dashboard': return renderDashboard();
      case 'detection': return renderDetection();
      case 'mental': return renderMentalHealth();
      case 'records': return renderRecords();
      case 'appointments': return renderAppointments();
      case 'settings': return renderSettings();
      default: return renderDashboard();
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor={colors.primary} />
      {renderScreen()}
      
      {/* Bottom Navigation */}
      <View style={styles.bottomNav}>
        <TouchableOpacity style={styles.navItem} onPress={() => setCurrentScreen('dashboard')}>
          <Icon name="home" size={24} color={currentScreen === 'dashboard' ? colors.secondary : colors.border} />
          <Text style={[styles.navLabel, { color: currentScreen === 'dashboard' ? colors.secondary : colors.border }]}>Home</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.navItem} onPress={() => setCurrentScreen('detection')}>
          <Icon name="microscope" size={24} color={currentScreen === 'detection' ? colors.secondary : colors.border} />
          <Text style={[styles.navLabel, { color: currentScreen === 'detection' ? colors.secondary : colors.border }]}>Scan</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.navItem} onPress={() => setCurrentScreen('mental')}>
          <Icon name="brain" size={24} color={currentScreen === 'mental' ? colors.secondary : colors.border} />
          <Text style={[styles.navLabel, { color: currentScreen === 'mental' ? colors.secondary : colors.border }]}>Mental</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.navItem} onPress={() => setCurrentScreen('appointments')}>
          <Icon name="calendar" size={24} color={currentScreen === 'appointments' ? colors.secondary : colors.border} />
          <Text style={[styles.navLabel, { color: currentScreen === 'appointments' ? colors.secondary : colors.border }]}>Visits</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.navItem} onPress={() => setCurrentScreen('settings')}>
          <Icon name="cog" size={24} color={currentScreen === 'settings' ? colors.secondary : colors.border} />
          <Text style={[styles.navLabel, { color: currentScreen === 'settings' ? colors.secondary : colors.border }]}>Settings</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// Styles
const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: 'white',
  },
  container: {
    flex: 1,
    backgroundColor: 'white',
    padding: 20,
    paddingBottom: 100,
  },
  header: {
    backgroundColor: colors.primary,
    padding: 20,
    borderRadius: 15,
    marginBottom: 20,
  },
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarText: {
    color: 'white',
    fontSize: 20,
    fontWeight: '600',
  },
  welcomeText: {
    flex: 1,
    marginLeft: 15,
  },
  welcomeTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 5,
  },
  welcomeSubtitle: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: 14,
  },
  healthScore: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  scoreNumber: {
    color: 'white',
    fontSize: 32,
    fontWeight: '700',
    marginBottom: 5,
  },
  scoreLabel: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: 14,
  },
  quickActions: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  actionCard: {
    width: '48%',
    backgroundColor: colors.light,
    padding: 20,
    borderRadius: 15,
    alignItems: 'center',
    marginBottom: 15,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  actionIcon: {
    width: 50,
    height: 50,
    backgroundColor: colors.primary,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  actionTitle: {
    fontWeight: '600',
    color: colors.dark,
    marginBottom: 5,
  },
  actionSubtitle: {
    fontSize: 12,
    color: colors.border,
    textAlign: 'center',
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.dark,
    marginBottom: 15,
  },
  recordItem: {
    backgroundColor: colors.light,
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: colors.secondary,
  },
  recordTitle: {
    fontWeight: '600',
    color: colors.dark,
    marginBottom: 5,
  },
  recordDate: {
    fontSize: 12,
    color: colors.border,
    marginBottom: 5,
  },
  recordNote: {
    fontSize: 12,
    color: colors.border,
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: colors.border,
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 5,
  },
  progressFill: {
    height: '100%',
    backgroundColor: colors.accent,
    borderRadius: 4,
  },
  screenTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.dark,
    marginBottom: 20,
  },
  uploadArea: {
    backgroundColor: colors.light,
    borderWidth: 2,
    borderColor: colors.border,
    borderStyle: 'dashed',
    borderRadius: 15,
    padding: 40,
    alignItems: 'center',
    marginBottom: 20,
  },
  uploadTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.dark,
    marginTop: 15,
    marginBottom: 5,
  },
  uploadSubtitle: {
    color: colors.border,
    textAlign: 'center',
  },
  button: {
    backgroundColor: colors.primary,
    padding: 15,
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  cameraButton: {
    backgroundColor: colors.secondary,
  },
  bookButton: {
    backgroundColor: colors.accent,
  },
  buttonText: {
    color: 'white',
    fontWeight: '600',
    marginLeft: 10,
  },
  moodCard: {
    backgroundColor: colors.light,
    padding: 20,
    borderRadius: 15,
    marginBottom: 20,
  },
  moodQuestion: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.dark,
    marginBottom: 15,
    textAlign: 'center',
  },
  moodTracker: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  moodOption: {
    alignItems: 'center',
  },
  selectedMood: {
    transform: [{ scale: 1.2 }],
  },
  moodEmoji: {
    fontSize: 32,
    marginBottom: 5,
  },
  moodLabel: {
    fontSize: 12,
    color: colors.border,
  },
  appointmentCard: {
    backgroundColor: colors.light,
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: colors.accent,
  },
  appointmentTime: {
    fontWeight: '600',
    color: colors.accent,
    marginBottom: 5,
  },
  appointmentDoctor: {
    color: colors.dark,
    marginBottom: 5,
  },
  appointmentType: {
    fontSize: 12,
    color: colors.border,
  },
  settingsItem: {
    backgroundColor: colors.light,
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingsLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingsIcon: {
    width: 40,
    height: 40,
    backgroundColor: colors.primary,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
  },
  settingsTitle: {
    fontWeight: '600',
    color: colors.dark,
  },
  settingsSubtitle: {
    fontSize: 12,
    color: colors.border,
  },
  toggleSwitch: {
    width: 50,
    height: 25,
    backgroundColor: colors.border,
    borderRadius: 25,
  },
  toggleSwitchActive: {
    backgroundColor: colors.accent,
  },
  toggleSwitchKnob: {
    width: 21,
    height: 21,
    backgroundColor: 'white',
    borderRadius: 50,
    marginTop: 2,
    marginLeft: 2,
  },
  toggleSwitchKnobActive: {
    marginLeft: 27,
  },
  bottomNav: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: colors.border,
    paddingVertical: 10,
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  navItem: {
    alignItems: 'center',
    paddingVertical: 5,
  },
  navLabel: {
    fontSize: 12,
    marginTop: 5,
  },
});
