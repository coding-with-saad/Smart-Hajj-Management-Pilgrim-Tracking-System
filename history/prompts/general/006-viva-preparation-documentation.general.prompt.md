---
id: 006
title: Viva Preparation Documentation
stage: general
date: 2026-05-13
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: none
branch: 001-frontend-ui-design
user: Malik Saad Khawar
command: /viva-prep
labels: ["viva", "documentation", "flask", "presentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - VIVA_PREP.md
 - app.py
tests:
 - Manual run verification
---

## Prompt

"This is my project. Tomorrow I have to prepare it for Viva as well. Create a markdown file that states what you have done in this project(fully detail) so far and write some commands that make it run."

## Response snapshot

Created a detailed `VIVA_PREP.md` guide summarizing all project achievements, architecture, and potential viva Q&A. Also created a functional `app.py` Flask file to make the project immediately runnable for the presentation.

## Outcome

- ✅ Impact: Comprehensive presentation materials and runnable prototype ready for Viva.
- 🧪 Tests: N/A
- 📁 Files: VIVA_PREP.md, app.py
- 🔁 Next prompts: Continue with MongoDB integration.
- 🧠 Reflection: Providing a runnable `app.py` is critical for the user to demonstrate the templates built in previous steps.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
