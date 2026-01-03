import { describe, it, expect } from 'vitest';
import { formatDate, formatPhone, formatCurrency } from '../../src/utils/formatters';

describe('formatters', () => {
  describe('formatDate', () => {
    it('should format date correctly', () => {
      const date = new Date('2024-01-15');
      expect(formatDate(date)).toBe('15 Jan 2024');
    });
  });

  describe('formatPhone', () => {
    it('should format phone number', () => {
      expect(formatPhone('79991234567')).toBe('+7 (999) 123-45-67');
    });
  });

  describe('formatCurrency', () => {
    it('should format currency with symbol', () => {
      expect(formatCurrency(1000, 'RUB')).toBe('₽1,000.00');
    });
  });
});
