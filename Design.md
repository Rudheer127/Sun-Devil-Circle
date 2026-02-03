DESIGN.md
Product Overview

This application is a peer-support and resource navigation platform designed specifically for international freshman students at ASU.

The goal is to reduce isolation and friction during early transition by:

Allowing students to express challenges once without retyping painful thoughts

Providing AI-assisted support options and ASU resources

Enabling safe, topic-based peer discussions

Maintaining strong privacy, safety, and ethical boundaries

This is not a therapy product and does not provide medical or clinical advice.

Target Users

Primary users:

International freshman students at ASU

Secondary users (future expansion):

Other student transition groups (transfer students, first-generation students, etc.)

Core User Flow
0. Authentication (Login/Signup)

The user must log in or sign up before accessing the platform.

Signup Requirements:

Unique username

Password (cannot be empty)

Password confirmation

This authentication is for demo continuity only (so a user can return to their session). There is no email verification or password recovery.

1. Profile Setup

The user:

Enters a display name or alias

Confirms they are an international freshman

Optionally provides:

Preferred language

Primary challenge category (select up to two)

Support style preference (listening, sharing, mixed)

This information is used only to personalize suggestions and group recommendations.

2. Issue Input

The user writes about their current challenge in free text.

Design guarantees:

The user writes their issue once

The text is autosaved locally using IndexedDB

Drafts and past issues persist across sessions on the same device

The user can delete all local data at any time

No issue text is permanently stored on the backend.

3. Resource Page (Central Decision Hub)

After submitting an issue, the user is taken to the resource page.

This page:

Acknowledges the user’s input using neutral, non-clinical language

Displays AI-suggested:

Support options

ASU resources (ASU-first, limited list)

Clearly shows a disclaimer that suggestions are informational, not professional advice

Inline AI Follow-up Q and A

The user may ask follow-up questions directly on this page

Follow-up questions are capped at 5 per session

AI responses:

Are short and structured

Do not diagnose or provide medical advice

Use the user’s language, not clinical terms

After the limit is reached, the user is informed they can continue later or explore peer groups

4. Decision: Peer Connection

From the resource page, the user may:

Join an existing topic-based group

Create a new group only if no relevant active group exists

Leave and return later

Group recommendations are suggested based on:

Issue category

Profile fields

AI-supported but deterministic matching logic

5. Group Chat

Group chats are:

Topic-based

Open to multiple users

Temporary by design:

No permanent identity or social graph

Membership is fluid

Groups become inactive when unused

Users may participate in multiple groups.

Data Ownership and Storage
Local Storage (IndexedDB)

Stored locally in the user’s browser:

Issue text and drafts

Issue history with timestamps

User preferences (for example, “do not show this again”)

Properties:

Data never leaves the device by default

Data is fully user-controlled

One-click deletion is always available

Backend Storage (In-Memory Only)

Stored temporarily on the backend:

Display name or alias

Non-sensitive profile fields

Active groups and messages

Properties:

No database for chat/issue data

SQLite used ONLY for user credentials

No long-term persistence

Reset on server restart

Never Stored

The system must never store:

AI interpretations or inferred emotional states

Diagnoses or mental health labels

Long-term chat history by default

AI Role and Boundaries

AI is a support navigator and safety layer, not an authority.

AI is used to:

Suggest support options and resources

Recommend relevant peer group topics

Monitor chat messages for:

Offensive language

Severe distress signals

AI must:

Use neutral, non-clinical language

Avoid advice that sounds like therapy

Respect hard interaction limits

Fail safely if unavailable

Safety and Moderation
Offensive Language

Messages containing offensive or inappropriate language are blocked

The user is shown a neutral warning explaining why

Severe Distress Signals

Messages are allowed

A banner is shown suggesting professional help and ASU resources

Chat is not locked

Reporting

A “Report” button exists in the UI

No backend workflow is implemented for the hackathon

Transparency and Trust

The interface must clearly communicate:

AI is used only for suggestions and safety

Personal issue data is stored locally, not centrally

Data is not reused or analyzed beyond the current experience

Design Principles

Minimize emotional friction

Preserve user dignity and control

Prefer clarity over complexity

Design for hackathon reliability

Enable future scaling without redesign