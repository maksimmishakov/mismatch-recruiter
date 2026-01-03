import React, { createContext, useState, useEffect } from 'react';
export const ThemeContext = createContext(undefined);
export function ThemeProvider({ children }) {
    const [theme, setThemeState] = useState(() => {
        const saved = localStorage.getItem('theme');
        return saved || 'auto';
    });
    const [isDark, setIsDark] = useState(() => {
        if (theme === 'auto') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        return theme === 'dark';
    });
    useEffect(() => {
        localStorage.setItem('theme', theme);
        if (theme === 'auto') {
            const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
            setIsDark(isDarkMode);
            document.documentElement.classList.toggle('dark', isDarkMode);
        }
        else {
            const isDarkMode = theme === 'dark';
            setIsDark(isDarkMode);
            document.documentElement.classList.toggle('dark', isDarkMode);
        }
    }, [theme]);
    const toggleTheme = () => {
        setThemeState((prev) => {
            if (prev === 'light')
                return 'dark';
            if (prev === 'dark')
                return 'auto';
            return 'light';
        });
    };
    const setTheme = (newTheme) => {
        setThemeState(newTheme);
    };
    return (<ThemeContext.Provider value={{ theme, isDark, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>);
}
export function useTheme() {
    const context = React.useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within ThemeProvider');
    }
    return context;
}
