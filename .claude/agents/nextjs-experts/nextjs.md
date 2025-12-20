# 🧠 Next.js Expert Knowledge Base

## ✅ Core Mastery
- Next.js 13+ App Router
- React Server Components & Client Components
- Dynamic vs Static Rendering
- Data Fetching, Cache, ISR, Revalidate
- Middleware
- Route Handlers / API Routes
- Server Actions
- Authentication (NextAuth, JWT, OAuth)
- Database Integration (Prisma / Mongo)
- CMS Integration (Sanity)
- Stripe Payments
- SEO + Performance
- Production Deployment (Vercel)

---

## ✅ Best Practices
- Prefer `/app` router for new apps
- Use Server Components by default
- Only use `use client` when:
  - interactivity needed
  - event handling
  - browser APIs
- Avoid unnecessary state
- Use TypeScript always
- Use environment variables properly
- Handle errors gracefully

---

## ✅ Recommended Tech Stack
- Next.js 13+ App Router
- TypeScript
- Tailwind CSS
- Prisma / PlanetScale / PostgreSQL
- NextAuth
- Stripe
- Sanity CMS
- Zustand or Context API

---

## 📁 Ideal Project Structure

app/
├─ layout.tsx
├─ page.tsx
├─ dashboard/
│ ├─ page.tsx
│ ├─ settings/
│ │ └─ page.tsx
├─ api/
│ ├─ auth/
│ │ └─ [...nextauth]/route.ts
│ └─ products/
│ └─ route.ts


---

## ✅ Example API Route

```ts
// app/api/products/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const products = [
    { id: 1, name: "Laptop" },
    { id: 2, name: "Phone" }
  ];

  return NextResponse.json(products);
}

✅ Example Server Component
export default async function Products() {
  const res = await fetch("https://api.example.com/products", {
    cache: "no-store"
  });

  const products = await res.json();

  return (
    <div>
      <h1>Products</h1>
      {products.map((p: any) => (
        <p key={p.id}>{p.name}</p>
      ))}
    </div>
  );
}

⚡ Performance Optimization

Avoid unnecessary client components

Use caching wisely

Reduce bundle size

Lazy load components

Optimize images with next/image

🚀 Deployment Best Practices

Use Vercel

Enable Edge runtime if needed

Use environment variables

Monitor with logging + metrics