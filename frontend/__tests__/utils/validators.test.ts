import { describe, it, expect } from 'vitest'
import { isValidEmail, isValidPassword, isEmpty, validateRequired } from '@utils/validators'

describe('Validators', () => {
  describe('isValidEmail', () => {
    it('should validate correct email', () => {
      expect(isValidEmail('test@example.com')).toBe(true)
      expect(isValidEmail('user+tag@domain.co.uk')).toBe(true)
    })

    it('should reject invalid email', () => {
      expect(isValidEmail('invalid')).toBe(false)
      expect(isValidEmail('user@')).toBe(false)
      expect(isValidEmail('@domain.com')).toBe(false)
    })
  })

  describe('isValidPassword', () => {
    it('should validate strong password', () => {
      expect(isValidPassword('SecurePass123!')).toBe(true)
      expect(isValidPassword('Password@456')).toBe(true)
    })

    it('should reject weak password', () => {
      expect(isValidPassword('weak')).toBe(false)
      expect(isValidPassword('nouppercaseornum!')).toBe(false)
      expect(isValidPassword('NOSPECIALCHAR123')).toBe(false)
    })
  })

  describe('isEmpty', () => {
    it('should detect empty values', () => {
      expect(isEmpty('')).toBe(true)
      expect(isEmpty(null)).toBe(true)
      expect(isEmpty(undefined)).toBe(true)
      expect(isEmpty([])).toBe(true)
    })

    it('should detect non-empty values', () => {
      expect(isEmpty('text')).toBe(false)
      expect(isEmpty([1])).toBe(false)
    })
  })

  describe('validateRequired', () => {
    it('should return error for empty value', () => {
      const result = validateRequired('', 'Email')
      expect(result).toBe('Email is required')
    })

    it('should return null for non-empty value', () => {
      const result = validateRequired('test@example.com', 'Email')
      expect(result).toBeNull()
    })
  })
})
