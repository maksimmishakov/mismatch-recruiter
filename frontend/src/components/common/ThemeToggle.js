import { useTheme } from '@contexts/ThemeContext';
export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme();
    const getIcon = () => {
        if (theme === 'light')
            return '🌙';
        if (theme === 'dark')
            return '☀️';
        return '🔄';
    };
    return (<button onClick={toggleTheme} className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition" aria-label="Toggle theme" title={`Current theme: ${theme}`}>
      {getIcon()}
    </button>);
}
