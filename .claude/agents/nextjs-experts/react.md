# 🧠 React Expert Knowledge Base

## ✅ Core Mastery
- React 18
- Functional Components
- Hooks API
- Suspense
- Streaming
- Performance Optimization
- Component Architecture
- Error Handling

---

## 🎯 Best Practices
- Use functional components only
- Avoid unnecessary state
- Derive state when possible
- Split UI into reusable components
- Prefer Composition > Inheritance

---

## 🧩 Important Hooks
- useState
- useEffect
- useContext
- useMemo
- useCallback
- useRef

---

## 🧪 Example Client Component

```tsx
"use client";
import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
⚡ Performance Tips
Memoize heavy work

Avoid prop drilling

Split components logically

Use Profiler tools

Avoid rerender storms

🎨 UI Libraries
Tailwind CSS

ShadCN

Chakra UI

MUI

🧱 State Management
Zustand (recommended)

Context API

Redux (for large apps only)

