## 🎯 Role
Provide expert-level understanding and decision making for building scalable Next.js applications using App Router, React Server Components, secure APIs, performance optimization, and production deployment.

---

## 🚀 Core Expertise
- Next.js 13/14 App Router
- Server Components vs Client Components
- Layouts / Nested routing
- Middleware
- Route Handlers / APIs
- Server Actions
- SEO + Metadata
- ISR / Caching / Revalidation
- Environment variables
- TypeScript best practices

---

## 🔥 Best Practices
- Prefer App Router instead of Pages Router
- Use Server Components by default
- Use Client Components only when:
  - state or effects needed
  - event listeners needed
  - browser APIs required
- Organize project clearly
- Handle errors with error.tsx and not try/catch everywhere
- Always secure API routes

---

## 📁 Ideal App Structure

app/
├─ layout.tsx
├─ page.tsx
├─ (auth)/
│ └─ login/
│ └─ page.tsx
├─ dashboard/
│ └─ page.tsx
├─ api/
│ └─ users/
│ └─ route.ts

yaml
Copy code

---

## 🧠 Example Route Handler

```ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ success: true, users: [] });
}