// NeuroSync — JARVIS HUD Theme
// Drop this file at src/theme/index.ts

export const Colors = {
  // Backgrounds
  bg:        '#060d12',   // deepest background
  bgCard:    '#0a1820',   // card / panel surface
  bgInput:   '#0d1f2b',   // input fields

  // Primary accent — cyan
  cyan:      '#00FFFF',
  cyanDim:   'rgba(0,255,255,0.6)',
  cyanFaint: 'rgba(0,255,255,0.15)',
  cyanBorder:'rgba(0,255,255,0.25)',

  // Secondary accents
  amber:     '#FFAA00',
  amberDim:  'rgba(255,170,0,0.6)',
  amberBorder:'rgba(255,170,0,0.25)',
  red:       '#FF4444',
  redBorder: 'rgba(255,68,68,0.25)',
  blue:      '#44AAFF',

  // Text
  textPrimary:   '#CCF0FF',   // body text on dark bg
  textSecondary: 'rgba(180,230,255,0.5)',
  textMuted:     'rgba(180,230,255,0.25)',

  // Divider
  divider: 'rgba(0,255,255,0.12)',
};

export const Fonts = {
  // Add these to your project:
  // npx expo install @expo-google-fonts/rajdhani @expo-google-fonts/share-tech-mono
  // OR link them via react-native.config.js if bare RN
  hud:   'ShareTechMono-Regular',   // numbers, values
  ui:    'Rajdhani-SemiBold',       // labels, headings
  uiReg: 'Rajdhani-Regular',       // body text in screens
};

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
};

export const Radius = {
  sm: 6,
  md: 8,
  lg: 12,
  pill: 99,
};

// Shared stylesheet fragments
export const SharedStyles = {
  screen: {
    flex: 1,
    backgroundColor: Colors.bg,
    padding: Spacing.lg,
    paddingTop: 56,
  },
  card: {
    backgroundColor: Colors.bgCard,
    borderWidth: 0.5,
    borderColor: Colors.cyanBorder,
    borderRadius: Radius.md,
    padding: Spacing.md,
  },
  sectionLabel: {
    fontSize: 10,
    color: Colors.textSecondary,
    letterSpacing: 3,
    marginBottom: Spacing.sm,
  },
};
