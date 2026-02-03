Overview

This project is a web application built for a hackathon setting with the following priorities:

Rapid iteration and stability

Clear separation of frontend and backend responsibilities

Privacy-first handling of sensitive user data

Compatibility with Replit for development and demo

Optional live AI integration with a safe fallback

The system is intentionally designed to be simple, explicit, and easy to reason about.

Backend
Language

Python 3.10+

Framework

Flask (server-rendered application)

Backend Responsibilities

Routing and request handling

Session management (non-persistent)

Group and chat logic (in-memory)

AI abstraction and safety enforcement

Resource suggestion logic

Moderation logic

Data Storage (Backend)

No database is used for general application state (groups, chat, issue text)

A local SQLite database is used ONLY for storing user credentials (hashed password and display name).

All backend data is stored in memory only for the duration of the session:

Display name / alias

User profile fields used for matching

Active groups and group messages

No sensitive personal issue data is persisted on the backend

Session Management

Flask sessions are used for:

display_name

is_international_freshman

preferred_language (optional)

primary_challenge (up to two values)

support_style

current_group

followup_count (max 5)

Sessions are short-lived and reset on server restart.

Frontend
Rendering Model

Server-side rendered HTML using Jinja templates

Minimal JavaScript used only where necessary

Local Data Storage

IndexedDB (required)

IndexedDB is used to store sensitive and user-owned data locally in the browser:

Issue text and reflection drafts

Issue history with timestamps

User preferences (for example, “do not show this again”)

This data:

Never leaves the user’s device by default

Can be deleted at any time via a “Delete my local data” action

Is autosaved every few seconds while typing

JavaScript Usage

Plain JavaScript only

No frontend frameworks (React, Vue, etc.)

JavaScript is limited to:

IndexedDB read/write logic

Form enhancement (autosave, restore drafts)

AI Integration
AI Role

Suggest support options and ASU resources based on user input

Recommend relevant peer group topics

Monitor chat messages for offensive language and severe distress signals

AI Architecture

AI logic is abstracted behind backend functions

The app must run without AI keys or external calls

Live AI (Optional)

Live AI calls are enabled only if:

An environment variable (for example, LIVE_AI=1) is set

A valid API endpoint and key are available

Live AI is expected to be hosted separately (for example, via Vercel)

A free-tier model is used for the hackathon

Fallback Requirement

If live AI is unavailable, the system must:

Fall back to deterministic, rule-based mock logic

Continue functioning without errors or degraded UX

AI Limits

Follow-up questions are capped at 5 per user session

AI output must be structured and non-clinical

AI must never provide diagnoses or medical advice

Groups and Chat
Group Model

Topic-based group rooms

Preset topic groups always exist

Users may create a new group only if no relevant active group exists

Group Storage

Groups and messages are stored in memory only

No long-term persistence of chat logs

Moderation

Offensive language: message is blocked and a warning is shown

Severe distress signals: message is allowed, but a banner suggests professional help and resources

A “Report” button exists in the UI (no backend workflow for hackathon)

Deployment and Environment
Development and Demo

Designed to run locally or on Replit

Must start with:

python app.py

External Services

Optional AI endpoint hosted separately (for example, Vercel)

Backend communicates with AI service via HTTP when enabled

Explicitly Forbidden Technologies

The following must NOT be used:

Databases (Postgres, MongoDB, Firebase, etc.)

Authentication systems (OAuth, Email verification, Password Recovery)
- Local username/password authentication IS allowed (demo continuity only)

Background job queues

WebSockets

Frontend frameworks

Analytics or tracking libraries

Persistent storage of sensitive issue data on the backend

Design Intent (For Code Generators)

Prefer clarity over cleverness

Keep logic deterministic where possible

Fail safely and visibly

Do not infer or store emotional states

Always assume hackathon constraints and live demo reliability