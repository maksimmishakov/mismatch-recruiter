// Email validation
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Password validation (min 8 chars, 1 uppercase, 1 number, 1 special char)
export const isValidPassword = (password: string): boolean => {
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
  return passwordRegex.test(password)
}

// Phone validation
export const isValidPhone = (phone: string): boolean => {
  const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/
  return phoneRegex.test(phone.replace(/\s/g, ''))
}

// URL validation
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// Check if empty
export const isEmpty = (value: any): boolean => {
  return !value || (typeof value === 'string' && value.trim() === '') || (Array.isArray(value) && value.length === 0)
}

// Validate required fields
export const validateRequired = (value: any, fieldName: string = 'Field'): string | null => {
  if (isEmpty(value)) {
    return `${fieldName} is required`
  }
  return null
}

// Validate min length
export const validateMinLength = (value: string, minLength: number, fieldName: string = 'Field'): string | null => {
  if (value && value.length < minLength) {
    return `${fieldName} must be at least ${minLength} characters`
  }
  return null
}

// Validate max length
export const validateMaxLength = (value: string, maxLength: number, fieldName: string = 'Field'): string | null => {
  if (value && value.length > maxLength) {
    return `${fieldName} must not exceed ${maxLength} characters`
  }
  return null
}
