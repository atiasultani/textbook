<!-- Sync Impact Report:
Version change: 0.0.0 → 1.0.0
List of modified principles: All principles added
Added sections: Purpose, Scope, Key Features, Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .claude/commands/sp.adr.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.analyze.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.checklist.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.clarify.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.constitution.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.git.commit_pr.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.implement.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.phr.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.plan.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.specify.md: ✅ updated (no specific changes needed, general template)
  - .claude/commands/sp.tasks.md: ✅ updated (no specific changes needed, general template)
Follow-up TODOs: Update plan-template.md, spec-template.md, and tasks-template.md to align with new principles and sections.
-->
# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity
The project prioritizes straightforward design, implementation, and user experience. Solutions must be easy to understand, maintain, and use. Avoid unnecessary complexity and aim for elegance in design.

### II. Accuracy
All information presented in the textbook and provided by the RAG chatbot must be factually correct and technically sound. Rigorous verification of content is mandatory.

### III. Minimalism
Focus on core functionality and essential content. Eliminate redundancies, unnecessary features, and overhead to ensure a lightweight and efficient system.

### IV. Fast Builds
The build process for the Docusaurus textbook must be optimized for speed. Minimize dependencies and build-time computations to ensure rapid iteration and deployment.

### V. Free-tier Architecture
All chosen technologies and services must be compatible with free-tier usage to minimize operational costs and ensure accessibility for all users. This includes database, hosting, and AI services.

### VI. RAG Answers ONLY from Book Text
The RAG chatbot must strictly derive its answers from the content of the textbook. It must not hallucinate or use external knowledge sources for its responses.

## Project Overview

### Purpose
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course. The book must serve as a fast, simple, high-quality learning resource built with a modern Docusaurus UI and a fully integrated free-tier RAG chatbot.

### Scope and Dependencies
- In Scope:
  - 6 short chapters:
    1. Introduction to Physical AI
    2. Basics of Humanoid Robotics
    3. ROS 2 Fundamentals
    4. Digital Twin Simulation (Gazebo + Isaac)
    5. Vision-Language-Action Systems
    6. Capstone: Simple AI-Robot Pipeline
  - Clean UI
  - Free-tier friendly
  - Lightweight embeddings
- Out of Scope: N/A
- External Dependencies: Docusaurus, Qdrant, Neon, FastAPI

### Key Features
- Docusaurus textbook
- RAG chatbot (Qdrant + Neon + FastAPI)
- Select-text → Ask AI
- Optional Urdu / Personalize features

### Constraints
- No heavy GPU usage
- Minimal embeddings

### Success Criteria
- Build success
- Accurate chatbot
- Clean UI
- Smooth GitHub Pages deployment

## Governance
This constitution serves as the foundational document for the Physical AI & Humanoid Robotics — Essentials project. All architectural decisions, design choices, and implementation efforts must adhere to the principles and guidelines outlined herein. Amendments to this constitution require careful consideration, documentation, and approval from core stakeholders. All pull requests and code reviews must verify compliance with these principles. Complexity must always be justified against the core principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
