import { describe, it, expect } from 'vitest';
import { sanitizeInput, validateToken, hashPassword } from '../../src/utils/security';

describe('security', () => {
  describe('sanitizeInput', () => {
    it('should remove XSS payload', () => {
      const malicious = '<script>alert(1)</script>';
      const clean = sanitizeInput(malicious);
      expect(clean).not.toContain('<script>');
    });

    it('should preserve safe HTML', () => {
      const safe = 'John Doe';
      expect(sanitizeInput(safe)).toBe('John Doe');
    });
  });

  describe('validateToken', () => {
    it('should validate JWT format', () => {
      const validToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U';
      expect(validateToken(validToken)).toBe(true);
    });
  });
});
