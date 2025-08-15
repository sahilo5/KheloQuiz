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
- [API](#api)
  - [Auth](#auth)
  - [Quizzes](#quizzes)
  - [Questions](#questions)
  - [User Responses](#user-responses)
  - [Examples](#examples)
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


