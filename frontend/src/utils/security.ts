// XSS Prevention - Sanitize HTML
export const sanitizeHTML = (html: string): string => {
  const div = document.createElement('div')
  div.textContent = html
  return div.innerHTML
}

// Sanitize user input
export const sanitizeInput = (input: string): string => {
  return input
    .replace(/[<>]/g, '') // Remove dangerous characters
    .trim()
}

// Escape HTML special characters
export const escapeHTML = (text: string): string => {
  const map: { [key: string]: string } = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  }
  return text.replace(/[&<>"']/g, (char) => map[char])
}

// Validate CSRF token
export const validateCSRFToken = (token: string): boolean => {
  return token && token.length > 0 && /^[a-zA-Z0-9\-_]+$/.test(token)
}

// Generate CSRF token (UUID-like)
export const generateCSRFToken = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

// Rate limiting check
export const checkRateLimit = (key: string, maxAttempts: number = 5, windowMs: number = 60000): boolean => {
  const stored = localStorage.getItem(`rate_limit_${key}`)
  const now = Date.now()

  if (!stored) {
    localStorage.setItem(`rate_limit_${key}`, JSON.stringify({ count: 1, timestamp: now }))
    return true
  }

  const { count, timestamp } = JSON.parse(stored)
  const isWithinWindow = now - timestamp < windowMs

  if (isWithinWindow) {
    if (count >= maxAttempts) return false
    localStorage.setItem(`rate_limit_${key}`, JSON.stringify({ count: count + 1, timestamp }))
  } else {
    localStorage.setItem(`rate_limit_${key}`, JSON.stringify({ count: 1, timestamp: now }))
  }

  return true
}

// Check for SQL injection patterns
export const checkSQLInjection = (input: string): boolean => {
  const sqlInjectionPattern = /('|(\-\-)|(;)|(\|\|)|(\*)|(\/\*)|(\/)|xp_|sp_)/gi
  return !sqlInjectionPattern.test(input)
}

// Validate file upload
export const validateFileUpload = (file: File, maxSize: number = 5 * 1024 * 1024, allowedTypes: string[] = ['image/jpeg', 'image/png', 'application/pdf']): { valid: boolean; error?: string } => {
  if (file.size > maxSize) {
    return { valid: false, error: `File size exceeds ${maxSize / 1024 / 1024}MB limit` }
  }
  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: `File type ${file.type} is not allowed` }
  }
  return { valid: true }
}
