
export const Colors = {

  bg:         '#080B0F',
  bgCard:     '#0E1318',
  bgElevated: '#131A22',
  bgInput:    '#0C1016',


  violet:      '#7B5EFF',
  violetDim:   'rgba(123,94,255,0.55)',
  violetFaint: 'rgba(123,94,255,0.12)',
  violetBorder:'rgba(123,94,255,0.28)',


  magenta:      '#FF2D78',
  magentaDim:   'rgba(255,45,120,0.55)',
  magentaFaint: 'rgba(255,45,120,0.1)',
  magentaBorder:'rgba(255,45,120,0.28)',


  online:  '#00E5A0',
  offline: '#FF4466',
  warn:    '#FFB347',


  textPrimary:   '#E8E0FF',
  textSecondary: 'rgba(200,190,240,0.55)',
  textMuted:     'rgba(160,150,210,0.3)',


  grid:    'rgba(123,94,255,0.08)',
  divider: 'rgba(123,94,255,0.15)',
};

export const Fonts = {
  mono:    'SpaceMono-Regular',
  display: 'Rajdhani-Bold',
  ui:      'Rajdhani-SemiBold',
  body:    'Rajdhani-Regular',
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
  sm: 4,
  md: 8,
  lg: 14,
  pill: 99,
};

export const SharedStyles = {
  screen: {
    flex: 1,
    backgroundColor: Colors.bg,
    padding: Spacing.lg,
    paddingTop: 56,
  },
  card: {
    backgroundColor: Colors.bgCard,
    borderWidth: 1,
    borderColor: Colors.violetBorder,
    borderRadius: Radius.md,
    padding: Spacing.md,
  },
  label: {
    fontSize: 9,
    color: Colors.textMuted,
    letterSpacing: 3,
    fontFamily: Fonts.ui,
    textTransform: 'uppercase' as const,
  },
};
