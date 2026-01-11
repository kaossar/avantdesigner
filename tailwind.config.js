/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './app/**/*.{js,ts,jsx,tsx,mdx}',
        './src/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        container: {
            center: true,
            padding: {
                DEFAULT: '1.5rem',
                sm: '2rem',
                lg: '4rem',
                xl: '5rem',
                '2xl': '6rem',
            },
        },
        extend: {
            colors: {
                primary: {
                    50: '#f0f5fa',
                    100: '#e1ebf5',
                    200: '#c4d7eb',
                    300: '#9ab8df',
                    400: '#6d93d2',
                    500: '#4a72c5',
                    600: '#3556a5',
                    700: '#2a4484',
                    800: '#102a43',
                    900: '#0a1c2e',
                },
                slate: {
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    200: '#e2e8f0',
                    300: '#cbd5e1',
                    400: '#94a3b8',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                    800: '#1e293b',
                    900: '#0f172a',
                },
            },
        },
    },
    plugins: [],
};
