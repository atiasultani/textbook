
---

# ✅ `database.md`

```md
# Database Skill

## 🎯 Role
Provide expert guidance on integrating Prisma, PostgreSQL, MongoDB, schema design, migrations, optimization, and secure querying.

---

## 🚀 Core Expertise
- Prisma ORM
- PostgreSQL
- MongoDB
- Schema design
- Relations
- Transactions
- Indexing
- Migrations
- Performance tuning

---

## 🔥 Best Practices
- Use Prisma with TypeScript
- Avoid unbounded queries
- Validate inputs
- Use indexes
- Never expose DB credentials
- Use env variables

---

## 🧠 Example Prisma Model

```prisma
model User {
  id      String @id @default(uuid())
  name    String
  email   String  @unique
  createdAt DateTime @default(now())
}
