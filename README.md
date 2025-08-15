# KheloQuiz

An AI-powered quiz web application built with **Django**, **Django REST Framework**, **PostgreSQL**, and **Tailwind CSS**. Users can generate quizzes from topics (optionally subtopics), attempt them (MCQ or Fill‑in‑the‑Blank), and track results over time. This README documents setup, configuration, data model, API, and common workflows.

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Data Model](#data-model)
  - [Entity Relationship Overview](#entity-relationship-overview)
- [Scoring & Evaluation Logic](#scoring--evaluation-logic)
- [Session & Authentication](#session--authentication)
- [Admin Panel](#admin-panel)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Overview
KheloQuiz enables dynamic quiz creation by entering **topic** (and optional **subtopic**). Questions may be AI‑generated (e.g., via Gemini 2.5) or curated. The app persists quizzes, questions, user answers, and evaluations in PostgreSQL and provides history for each user.

---

## Architecture
- **Django + DRF** expose REST APIs for auth, quiz creation, retrieval, answering, and evaluation.
- **PostgreSQL** stores normalized relational data.
- **Tailwind CSS** styles Django templates or a lightweight frontend.
- **(Optional) AI layer** generates questions which are stored as standard `Question` objects.

---
## Features
- Create quizzes tied to a user (**topic**, **name**, **subtopic**, **date**, **total marks**)
- Add questions (**MCQ** with options JSON, or **Fill‑in‑the‑Blank**)
- Submit answers, auto‑evaluate correctness and marks
- View quiz history and detailed results per user
- Django Admin management for content and users
- Extensible AI question generation pipeline

---

## Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Frontend:** Django Templates + Tailwind CSS (or plug in any SPA)
- **Auth:** Django session auth (or JWT if enabled)
- **AI:** Gemini 2.5 (optional integration layer)

---

## Prerequisites
- Python 3.10+
- PostgreSQL 13+
- (Optional) Node.js 18+ if you plan to build Tailwind via npm

---
## Data Model

### Entity Relationship Overview
The data model consists of the following main entities:

- **User**: Represents a registered user who can create and take quizzes.
- **Quiz**: Contains metadata about a quiz such as title, description, and creator.
- **Question**: Stores questions related to a quiz along with multiple choice options.
- **UserResponse**: Tracks user answers for a given quiz and question.

## Scoring & Evaluation Logic
- The system checks each answer against the correct answer stored in Question.answer.
- Marks the answer as correct or incorrect in UserResponse.is_correct.
- Calculates the final score as the number of correct answers divided by total questions.
- Stores evaluation results for later retrieval.

## Admin Panel
- Accessible at /admin/
- Superusers can manage users, quizzes, questions, and responses.
- Provides a GUI for non-technical management of quiz content.

## Deployment

- Backend is deployed using Railway.
- Steps followed:
-- Push code to GitHub.
-- Connect Railway project to GitHub repository.
-- Configure environment variables in Railway (e.g., DATABASE_URL).
-- Deploy and run python manage.py migrate to set up the database.
-- Collect static files with python manage.py collectstatic.
