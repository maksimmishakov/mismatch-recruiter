# Testing & QA Guide - MisMatch Recruiter

## Overview
Comprehensive testing strategy covering unit, integration, and E2E tests with 80%+ coverage targets.

## Test Structure

```
frontend/__tests__/
├── utils/
│   ├── validators.test.ts
│   ├── formatters.test.ts
│   ├── security.test.ts
│   └── helpers.test.ts
├── components/
│   ├── Button.test.tsx
│   ├── Card.test.tsx
│   ├── Form.test.tsx
│   └── ...
└── hooks/
    ├── useDebounce.test.ts
    ├── useTheme.test.ts
    └── ...
```

## Running Tests

### Unit Tests (Vitest)
```bash
cd frontend
npm run test                 # Run all tests
npm run test:ui            # Interactive UI
npm run test:coverage      # Coverage report
```

### Coverage Targets
- Lines: 80%
- Functions: 80%
- Branches: 75%
- Statements: 80%

## Test Categories

### 1. Utility Function Tests
- Validators (email, password, phone, URL)
- Formatters (currency, date, time)
- Security (sanitization, CSRF, rate limiting)
- Helpers (debounce, throttle, lazy load)

### 2. Component Tests
- Button (variants, loading states, disabled)
- Card (with/without title, hoverable)
- Form (validation, submission, errors)
- Input (sanitization, focus states)
- Modal (open/close, overlay)
- Theme Toggle (light/dark/auto)

### 3. Hook Tests
- useDebounce (delay, value updates)
- useThrottle (rate limiting)
- useLocalStorage (persist, retrieve)
- useTheme (light/dark toggle)
- useInfiniteScroll (callback on intersect)

### 4. Integration Tests
- Form submission with API
- Authentication flow
- Navigation between pages
- Data fetching and caching
- Error handling

### 5. E2E Tests (Cypress)
- Complete user workflows
- Dashboard interaction
- Candidate CRUD operations
- Job posting workflow
- Match viewing and actions

## Test Examples

### Unit Test
```typescript
import { describe, it, expect } from 'vitest'
import { isValidEmail } from '@utils/validators'

describe('isValidEmail', () => {
  it('should validate correct email', () => {
    expect(isValidEmail('test@example.com')).toBe(true)
  })
  
  it('should reject invalid email', () => {
    expect(isValidEmail('invalid')).toBe(false)
  })
})
```

### Component Test
```typescript
import { render, screen } from '@testing-library/react'
import Button from '@components/common/Button'

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
})
```

### Hook Test
```typescript
import { renderHook, act } from '@testing-library/react'
import { useDebounce } from '@utils/hooks'

describe('useDebounce', () => {
  it('should debounce value', async () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 100),
      { initialProps: { value: 'test' } }
    )
    
    expect(result.current).toBe('test')
  })
})
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run test:coverage
```

## Coverage Goals

- **Phase 8:** 60%+ coverage (utilities, components)
- **Phase 8+:** 80%+ coverage (all components, hooks)
- **Before Launch:** 90%+ coverage

## Best Practices

1. **Test-Driven Development**
   - Write tests before implementation
   - Ensure tests fail first
   - Implement to pass tests

2. **Descriptive Test Names**
   - Use `should...` pattern
   - Be specific about behavior
   - Example: `should return error for empty email`

3. **Test Isolation**
   - Each test independent
   - No shared state
   - Clean up after tests

4. **Mock External Dependencies**
   - Mock API calls
   - Mock localStorage
   - Mock timer functions

5. **Accessibility Testing**
   - Test ARIA labels
   - Test keyboard navigation
   - Test screen reader compatibility

## Performance Testing

```bash
# Lighthouse
npm run lighthouse

# Performance budgets
- JS bundle: < 150KB
- CSS bundle: < 50KB
- TTI: < 2s
- FCP: < 1s
```

## Continuous Improvement

- Monitor coverage reports
- Track test execution time
- Update tests with code changes
- Regular code review for test quality
