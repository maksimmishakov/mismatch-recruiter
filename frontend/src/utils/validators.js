// Email validation
export const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};
// Password validation (min 8 chars, 1 uppercase, 1 number, 1 special char)
export const isValidPassword = (password) => {
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
};
// Phone validation
export const isValidPhone = (phone) => {
    const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
};
// URL validation
export const isValidUrl = (url) => {
    try {
        new URL(url);
        return true;
    }
    catch {
        return false;
    }
};
// Check if empty
export const isEmpty = (value) => {
    return !value || (typeof value === 'string' && value.trim() === '') || (Array.isArray(value) && value.length === 0);
};
// Validate required fields
export const validateRequired = (value, fieldName = 'Field') => {
    if (isEmpty(value)) {
        return `${fieldName} is required`;
    }
    return null;
};
// Validate min length
export const validateMinLength = (value, minLength, fieldName = 'Field') => {
    if (value && value.length < minLength) {
        return `${fieldName} must be at least ${minLength} characters`;
    }
    return null;
};
// Validate max length
export const validateMaxLength = (value, maxLength, fieldName = 'Field') => {
    if (value && value.length > maxLength) {
        return `${fieldName} must not exceed ${maxLength} characters`;
    }
    return null;
};
