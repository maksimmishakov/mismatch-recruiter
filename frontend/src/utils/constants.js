// API Configuration
export const API_BASE_URL = process.env.VITE_API_URL || '/api';
export const API_TIMEOUT = 10000;
// Cache configuration
export const CACHE_DURATION = {
    SHORT: 5 * 60 * 1000, // 5 minutes
    MEDIUM: 30 * 60 * 1000, // 30 minutes
    LONG: 24 * 60 * 60 * 1000, // 24 hours
};
// Debounce/Throttle delays
export const DELAYS = {
    DEBOUNCE_SEARCH: 300,
    DEBOUNCE_INPUT: 500,
    THROTTLE_SCROLL: 200,
    THROTTLE_RESIZE: 300,
};
// Pagination
export const PAGINATION = {
    DEFAULT_PAGE_SIZE: 25,
    PAGE_SIZE_OPTIONS: [10, 25, 50, 100],
    MAX_PAGE_SIZE: 100,
};
// Routes
export const ROUTES = {
    HOME: '/',
    DASHBOARD: '/',
    CANDIDATES: '/candidates',
    JOBS: '/jobs',
    MATCHES: '/matches',
    NOT_FOUND: '*',
};
// Local storage keys
export const STORAGE_KEYS = {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    USER_PREFERENCES: 'user_preferences',
    THEME: 'theme',
    RECENT_SEARCHES: 'recent_searches',
};
// Status codes
export const STATUS = {
    PENDING: 'pending',
    ACTIVE: 'active',
    INACTIVE: 'inactive',
    COMPLETED: 'completed',
    FAILED: 'failed',
};
// Skills list
export const COMMON_SKILLS = [
    'React',
    'TypeScript',
    'Node.js',
    'Python',
    'SQL',
    'AWS',
    'Docker',
    'Git',
    'GraphQL',
    'REST API',
];
