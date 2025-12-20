# Authentication Skill

## 🎯 Role
Build secure authentication systems in Next.js using NextAuth, JWT, sessions, OAuth, and middleware protection.

---

## 🚀 Authentication Types
- Email + Password
- OAuth (Google, GitHub)
- Credentials Provider
- JWT Tokens
- Session-Based Login
- Protected Routes
- Middleware guard

---

## 🔥 Rules
- Never store JWT in localStorage
- Prefer HttpOnly cookies
- Hash passwords with bcrypt
- Always verify token server-side
- Protect API routes

---

## 🛡️ Middleware Example

```ts
import { NextResponse } from "next/server";

export function middleware(req) {
  const token = req.cookies.get("token");
  if (!token) return NextResponse.redirect(new URL("/login", req.url));
  return NextResponse.next();
}
