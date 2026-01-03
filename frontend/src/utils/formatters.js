// Format number as currency
export const formatCurrency = (value, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency,
    }).format(value);
};
// Format number with commas
export const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(value);
};
// Format date
export const formatDate = (date, format = 'short') => {
    const d = typeof date === 'string' ? new Date(date) : date;
    const options = {
        short: { year: 'numeric', month: 'short', day: 'numeric' },
        long: { year: 'numeric', month: 'long', day: 'numeric' },
        full: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
    }[format] || { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Intl.DateTimeFormat('en-US', options).format(d);
};
// Format time ago
export const formatTimeAgo = (date) => {
    const d = typeof date === 'string' ? new Date(date) : date;
    const now = new Date();
    const seconds = Math.floor((now.getTime() - d.getTime()) / 1000);
    const intervals = [
        ['year', 31536000],
        ['month', 2592000],
        ['week', 604800],
        ['day', 86400],
        ['hour', 3600],
        ['minute', 60],
    ];
    for (const [name, sec] of intervals) {
        const interval = Math.floor(seconds / sec);
        if (interval >= 1)
            return `${interval} ${name}${interval > 1 ? 's' : ''} ago`;
    }
    return 'just now';
};
// Format email
export const formatEmail = (email) => {
    return email.toLowerCase().trim();
};
// Format percentage
export const formatPercentage = (value, decimals = 0) => {
    return `${(value * 100).toFixed(decimals)}%`;
};
// Truncate text
export const truncateText = (text, length = 100) => {
    if (text.length <= length)
        return text;
    return `${text.substring(0, length)}...`;
};
