tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#4F46E5',
        neutral: {
          100: '#F5F7FA',
          200: '#E4E7EC',
          500: '#667085',
          700: '#344054',
          900: '#101828'
        }
      },
      fontFamily: {
        inter: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'md': '8px',
        'lg': '12px'
      },
      boxShadow: {
        soft: '0 1px 2px rgba(0, 0, 0, 0.06)',
        hover: '0 4px 12px rgba(0, 0, 0, 0.08)'
      }
    },
  }
}