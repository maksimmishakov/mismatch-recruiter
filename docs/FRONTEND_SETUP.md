# MisMatch React Frontend - Setup & Development Guide

## 📦 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/              # Reusable components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── layout/              # Layout structure
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── MainLayout.tsx
│   │   └── dashboard/           # Feature-specific (todo)
│   ├── pages/                   # Page components
│   │   ├── DashboardPage.tsx
│   │   ├── CandidatesPage.tsx
│   │   ├── JobsPage.tsx
│   │   ├── MatchesPage.tsx
│   │   └── NotFoundPage.tsx
│   ├── services/
│   │   └── api.ts              # Axios API client
│   ├── hooks/                   # Custom hooks (todo)
│   ├── contexts/                # React contexts (todo)
│   ├── store/                   # Zustand stores (todo)
│   ├── utils/                   # Utility functions
│   ├── styles/
│   │   └── globals.css         # Global Tailwind styles
│   ├── types/                   # TypeScript types (todo)
│   ├── App.tsx                 # Root component with routing
│   ├── main.tsx                # React DOM render
│   └── vite-env.d.ts
├── package.json                 # Dependencies
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite build config
├── tailwind.config.ts          # Tailwind CSS config
├── postcss.config.js           # PostCSS config
└── index.html                  # HTML entry point
```

## 🚀 Quick Start

### Install Dependencies

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

Server runs on `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Run Tests

```bash
npm run test
```

## 🛠️ Technology Stack

- **React 18.2**: UI library
- **TypeScript 5.x**: Type safety
- **Vite 4.x**: Build tool (fast development)
- **Tailwind CSS 3.x**: Utility-first styling
- **React Router v6**: Page routing
- **Axios**: HTTP client
- **Zustand**: State management (todo)
- **React Query**: Data fetching & caching (todo)
- **Vitest**: Unit testing (todo)

## 📝 Key Files

### App.tsx
Root component with React Router configuration. All routes go through `MainLayout` wrapper.

### components/layout/MainLayout.tsx
Wrapper component providing sidebar + header + outlet for page content.

### services/api.ts
Axios instance with:
- Bearer token auto-injection from localStorage
- 401 error handling (auto logout)
- 10s request timeout

## 🔌 API Integration

API calls use the configured client in `services/api.ts`:

```typescript
import api from '@services/api'

// GET
const response = await api.get('/candidates')

// POST
const result = await api.post('/candidates', { name: 'John' })

// Error handling
try {
  await api.get('/data')
} catch (error) {
  console.error('Request failed:', error)
}
```

## 🎨 Styling

Using **Tailwind CSS** with custom components defined in `globals.css`:

```css
.btn-primary    /* Blue primary button */
.btn-secondary  /* Gray secondary button */
.card           /* White card with shadow */
.input          /* Form input field */
```

## 🗂️ Creating New Components

### Common Component Example (Button)

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

export default function Button({ variant = 'primary', ...props }: ButtonProps) {
  // Implementation
}
```

### Page Component Example

```typescript
export default function MyPage() {
  return (
    <div className="p-8">
      <h1>Page Title</h1>
      {/* Content */}
    </div>
  )
}
```

## 🔄 Routing

All routes configured in `App.tsx`:

```typescript
<Route element={<MainLayout />}>
  <Route path="/" element={<DashboardPage />} />
  <Route path="/candidates" element={<CandidatesPage />} />
  <Route path="/jobs" element={<JobsPage />} />
  <Route path="/matches" element={<MatchesPage />} />
</Route>
```

## 📚 Next Steps (TODO)

- [ ] Install dependencies: `npm install`
- [ ] Create hooks for data fetching
- [ ] Setup Zustand state management
- [ ] Integrate with backend API
- [ ] Create feature-specific components
- [ ] Add form components with validation
- [ ] Setup testing suite
- [ ] Add dark mode support
- [ ] Implement WebSocket for real-time updates

## 🐛 Debugging

### Enable DevTools
React and Redux DevTools browser extensions recommended:
- React Developer Tools
- Redux DevTools

### Common Issues

**Port 3000 already in use:**
```bash
npm run dev -- --port 3001
```

**Module not found:**
Check path aliases in `vite.config.ts` match `tsconfig.json`

**Tailwind not loading:**
Ensure `globals.css` is imported in `main.tsx`

## 📖 Useful Resources

- [React Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Vite Guide](https://vitejs.dev/guide)
- [React Router](https://reactrouter.com)
