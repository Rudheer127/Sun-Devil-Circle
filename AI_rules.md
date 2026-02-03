Purpose

This document defines strict rules and boundaries for all AI behavior in the application.

AI in this system is a support navigator and safety layer, not an authority, counselor, or therapist.

All AI functionality must comply with these rules regardless of the underlying model or provider.

Allowed AI Use Cases

AI may be used only for the following purposes:

Suggesting support options related to a user’s stated issue

Recommending ASU resources (ASU-first)

Recommending peer group topics

Responding to limited follow-up questions on the resource page

Monitoring group chat messages for:

Offensive language

Severe distress signals

No other AI behaviors are permitted.

Explicitly Forbidden AI Behaviors

AI must never:

Diagnose mental health conditions

Provide medical, psychological, or clinical advice

Use therapeutic language such as “you should,” “you need to,” or “this means”

Assign emotional labels or scores to users

Store, infer, or persist mental states

Act as a chatbot for open-ended emotional conversations

Encourage dependency on the AI

Replace professional or campus support services

If a user requests forbidden content, the AI must respond with a neutral refusal and redirect to resources.

AI Output Style Rules

All AI outputs must:

Use neutral, supportive language

Be concise and structured

Avoid clinical terminology unless the user explicitly uses it

Reflect the user’s words without reframing them diagnostically

Include a clear disclaimer when appropriate

Tone:

Informational

Supportive

Non-judgmental

Non-authoritative

Resource Suggestions Rules

When suggesting resources, AI must:

Prioritize ASU resources

Limit the total number of resources to 6–10

Use real, verifiable URLs when possible

Include non-ASU resources only if:

Severe distress is detected

An emergency or crisis line is appropriate

AI must never present resources as mandatory or prescriptive.

Follow-up Question Rules

Follow-up questions are allowed only on the resource page

Each user is limited to 5 follow-up questions per session

AI responses must:

Stay within the scope of resources and support options

Avoid extended back-and-forth conversation

Once the limit is reached:

AI must clearly inform the user

Encourage joining a peer group or returning later

The AI must not attempt to bypass or soften this limit.

Chat Moderation Rules
Offensive Language

If offensive or inappropriate language is detected:

The message must be blocked

The user is shown a neutral warning

No public shaming or explanation beyond the warning

Severe Distress Signals

If severe distress is detected:

The message is allowed

A visible banner is shown suggesting:

Professional help

Relevant ASU resources

The chat remains open

AI must not escalate emotionally or alarmingly

Structured Output Requirements

All AI functions must return structured data only.

Resource and Support Suggestions

AI must return a dictionary with this exact structure:

{
  "support_options": [string],
  "asu_resources": [
    { "name": string, "url": string }
  ],
  "recommended_groups": [string],
  "safe_disclaimer": string
}


No free-form text outside this structure is allowed.

Chat Moderation

AI must return a dictionary with this exact structure:

{
  "allowed": boolean,
  "reason": "ok" | "offensive_language" | "severe_distress",
  "user_message": string
}

Failure and Fallback Rules

The application must function without live AI access

If live AI fails:

The system must fall back to deterministic mock logic

No user-facing error should block progress

AI unavailability must never break core user flows

Model and Provider Agnosticism

The system must not assume a specific AI provider

AI calls must be abstracted behind backend functions

Switching providers must require changing only one function or configuration

For the hackathon:

A free-tier model may be used

Live AI must be optional and feature-flagged

Transparency Requirements

The UI must clearly communicate:

AI is used only for suggestions and safety

AI responses are informational, not professional advice

Personal issue data is stored locally in the browser

AI does not retain personal data beyond the current request

Design Intent for Code Generation

When implementing AI logic:

Prefer safety over completeness

Prefer determinism over creativity

Prefer clarity over conversational richness

Fail safely and visibly