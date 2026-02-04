MASTER IMPLEMENTATION PROMPT: SunDevil Circle Complete Overhaul
You are redesigning and implementing critical updates to the SunDevil Circle web application for ASU students. This is a mental health peer support platform that requires immediate attention to safety, comprehensiveness, and user experience.

CRITICAL INSTRUCTION: All changes must remain visually and structurally consistent with the existing UI design system (colors, fonts, spacing, card styles, button styles, layout patterns). Do not redesign the visual aesthetic — only implement the functional gaps and content improvements outlined below.

🚨 PRIORITY 1: FIX CRISIS RESOURCES BANNER (LIFE-CRITICAL)
Current Issue: The crisis banner only shows 4 resources and is missing critical emergency contacts including 911.

Required Implementation:

Create a prominent, always-visible crisis banner at the top of all pages (Dashboard, Explore/Connect Peers, Resources, Groups, Share Support Need). The banner must:

Display this exact list in this order:

Emergency: 911

Text: "Immediate danger, medical emergency, or someone is at risk right now (anywhere in the U.S.), 24/7."

Link behavior: tel:911 (clickable on mobile)

988 Suicide & Crisis Lifeline

Text: "Free, confidential support for mental health/substance-use crises; call, text, or chat 24/7/365 (U.S.)."

Call link: tel:988

Text link: sms:988

Chat link: https://988lifeline.org/chat (opens in new tab)

ASU/EMPACT 24-Hour Crisis Line: (480) 921-1006

Text: "ASU-dedicated urgent behavioral/mental health crisis support for students; 24/7."

Call link: tel:+14809211006

ASU Open Call & Open Chat (TELUS Health): 1-877-258-7429

Text: "ASU student counseling support by phone/chat; 24/7/365, usable from anywhere in the world."

Call link: tel:+18772587429

Add a "Chat" button linking to the ASU TELUS Health chat page

Crisis Text Line: Text HOME to 741741

Text: "Free, confidential crisis support via text in the U.S.; 24/7."

Link behavior: sms:741741?body=HOME (pre-fills SMS on mobile)

Add disclaimer text:
"SunDevil Circle is not an emergency service. For urgent safety or life-threatening situations, use the resources above."

Visual consistency: Use the existing banner design pattern (light mint/teal background, shield icon). Ensure all links are clearly clickable and work on both desktop and mobile.

📋 PRIORITY 2: EXPAND SUPPORT TOPICS TO FULL MENTAL HEALTH SPECTRUM
Current Issue: Only 9 generic topics exist (Homesickness, Academic Stress, Making Friends, Culture Shock, Language Barriers, Loneliness, Anxiety, Finances). This excludes critical mental health issues.

Required Implementation:

Replace the limited topic list with this complete 43-topic taxonomy across all interfaces (Share Support Need page, profile settings, Explore/Connect Peers filters, group creation):

Mental Health & Crisis

Suicide / self-harm

Crisis / panic attack

Depression

Anxiety

Social anxiety

Stress

Burnout

Sleep problems / insomnia

Eating disorders / disordered eating

Body image concerns

Trauma / PTSD

Grief & loss

Anger management

OCD

Phobias

Bipolar disorder

Psychosis / schizophrenia-spectrum concerns

Substance use (alcohol/drugs)

Addiction / dependence

ADHD / attention & focus problems

Autism spectrum / neurodiversity support

Relationships & Social

Relationship issues

Breakups

Family problems

Roommate conflict

Loneliness / isolation

Homesickness

Culture shock / adjustment issues

Discrimination / bias experiences

Identity concerns (sexuality / gender / faith)

Sexual assault / harassment

Domestic/dating violence

Safety concerns / violence risk

Academic & Career

Academic problems

Test anxiety

Time management / procrastination

Motivation / concentration problems

Career stress / "no direction"

Financial stress

Implementation notes:

Make these available as checkboxes in profile settings (multi-select)

Present as clickable topic buttons on "Share Your Support Need" page (the page currently called "Share Your Challenge")

Use in dropdown filter on Connect with Peers page (see Priority 3)

Enable for group topic tagging when creating groups

🔒 PRIORITY 3: ADD PRIVACY CONTROLS FOR SENSITIVE TOPICS
Current Issue: Profile topics are either public or not selected at all. No way to mark sensitive topics as "use for matching but hide from public profile."

Required Implementation:

On the Profile Settings page, for each support topic checkbox:

Add a secondary toggle/checkbox labeled: "Hide from my public profile" or "Private (for matching only)"

Behavior:

When enabled: Topic is used by AI/matching algorithm but NOT displayed on the user's public profile card in Connect with Peers

When disabled (default): Topic is visible on profile cards

Add explanatory text: "Private topics help us match you with the right peers, but won't be shown publicly on your profile."

Visual consistency: Use the existing checkbox/toggle design pattern from the current profile page

🤖 PRIORITY 4: IMPLEMENT AI-POWERED PEER MATCHING
Current Issue: "Explore Peers" page has basic filters (5 pills) with no intelligence, search, or matching. No AI despite claims.

Required Implementation:

Rename "Explore Peer Supporters" to "Connect with Peer Supporters" everywhere (nav, buttons, page title).

On the Connect with Peers page:

Replace the horizontal pill filter bar with:

A multi-select dropdown for support topics (using the 43-topic list from Priority 2)

A search bar for searching by name, major, interests, or keywords

Keep visual design consistent with existing filters (same colors/styling)

Add AI-powered matching and sorting:

Default view: "Recommended for you" section at the top

Calculate match scores (0-100 or "High/Good/Fair Match") based on:

Overlap between user's "topics I'm experiencing" and peers' "topics I can support with"

Shared major, year, role (e.g., international student, transfer)

Shared languages

Shared communities/identities (if opted in)

Shared interests/hobbies

Display match indicator on each peer card: "95% Match" or "Best Fit" / "Good Fit" / "New Peer"

Sort by match score descending by default

Allow manual re-sorting: "Best Match" / "Recently Active" / "Alphabetical"

Respect privacy:

Never display topics marked "Hide from my public profile"

Use hidden topics internally for matching only

Peer cards show:

Name/nickname

Role (e.g., "International Freshman")

Languages spoken

Non-private support topics (as tags)

Match label (e.g., "Best Fit for you")

"Connect" button

Visual consistency: Maintain the existing card design, typography, and button styles. Only add the match indicator and reorganize filtering UI.

👥 PRIORITY 5: BUILD COMPLETE GROUPS SYSTEM
Current Issue: Groups page returns 404. Feature is completely missing despite being mentioned throughout the app.

Required Implementation:

Create /groups page with full functionality:

A. Group Discovery/Browse Page

List of all public groups (searchable/filterable)

Each group card shows:

Group name

Short description

Primary support topics (as tags)

Visibility badge: "Public" or "Private"

Member count

"Join" button (for public) or "Request Access" (for private)

Search bar and topic filter dropdown (using 43-topic list)

B. Group Creation Flow

Button: "Create New Group"

Form fields:

Group name (required)

Description (required)

Primary support topics: Multi-select from 43-topic list (required)

Group type: Dropdown (e.g., "Peer Support", "Study/Accountability", "Identity/Community", "Social")

Visibility toggle: Public (discoverable in groups list) or Private (invite-only, not listed)

"Create Group" button

C. Invite People to Group (AI-powered recommendations)

In group settings, "Invite People" button opens modal/page

Show recommended people to invite based on:

Match between group's topics and people's "topics I'm experiencing" or "topics I can support with"

Profile similarity (major, year, interests)

Display sections:

"People who may benefit from this group" (their topics align with group's topics)

"People who can support this group" (they marked group topics as "can support with")

Include search bar for manual invite by name/email/username

Show match strength indicator (e.g., "High relevance", "Good fit")

D. Group Privacy Toggle

Group owner can switch Public ↔ Private anytime in settings

Confirmation prompt when switching to Public: "This will make your group discoverable. Are you sure?"

Switching to Private removes from public discovery but keeps existing members

E. Group Page View

Shows members, posts/messages, group description, topics

"Leave Group" button

Owner sees "Settings" and "Invite People" buttons

Visual consistency: Use the existing card design system, color palette, and button styles. Groups should feel like a natural extension of the current UI.

🗑️ PRIORITY 6: REMOVE GAMIFICATION METRICS
Current Issue: Dashboard shows "0/5 Follow-up questions used", "0 Groups joined", "0 Messages sent" — these feel like achievements/scores rather than support-focused metrics. The 5-question limit is artificial and harmful.

Required Changes:

Remove these three counters entirely from the dashboard:

"Follow-up questions used"

"Groups joined"

"Messages sent"

Remove the 5-question limit on AI follow-up questions:

Allow unlimited follow-up questions

Remove the "0/5 questions used" counter from the "Ask AI for More Help" section

This is a support tool, not a game — there should be no artificial scarcity

Keep the dashboard clean and supportive:

Focus on action cards: "Share Your Support Need", "Browse Resources", "Connect with Peer Supporters"

Show personalized recommendations: "Recommended peers for you", "Suggested groups"

Remove any numeric counters or progress bars that feel like gamification

Rationale: Students seeking mental health support should not feel like they're "using up" resources or being tracked/scored. The focus must be on care and accessibility, not metrics.

📝 PRIORITY 7: RENAME & REFRAME CALL-TO-ACTION BUTTONS
Current Issue: "Share Another Challenge" sounds too enthusiastic and achievement-oriented. "Explore Peer Supporters" is passive/clinical.

Required Changes:

"Share Another Challenge" → "Need help with something else?"

Alternative: "How else can we support you?"

Alternative: "Share another concern"

Tone: Gentle, caring, open-ended inquiry (not "Share another challenge!" which feels forced)

"Explore Peer Supporters" → "Connect with Peer Supporters"

More action-oriented and supportive than "explore"

Use consistently across nav, dashboard, buttons, page titles

"Share Your Challenge" (page title) → "Share Your Support Need" or "Tell Us How We Can Help"

Less clinical, more person-centered

Update page title, breadcrumb, and any references

"Get Personalized Support" (submit button) → Keep as-is (this is good)

Visual consistency: Buttons maintain the same styling (maroon primary buttons, white secondary buttons), only text changes.

✅ ADDITIONAL FIXES FROM DETAILED ASSESSMENT
A. Navigation Confusion

"Resources" link in nav currently redirects to /issue (Share Your Challenge page) — this is broken

Fix: "Resources" should go to /resources-hub consistently

B. Crisis Banner Interactivity

Ensure ALL phone/text links work correctly on both desktop and mobile

Test click behavior: tel: links on mobile, sms: with pre-filled body, external links open in new tabs

C. Profile Page Topic Checkboxes

Currently shows 8 topics (Homesickness, Loneliness, Anxiety, Culture Shock, Academics, Relationships, Identity, Finances)

Expand to full 43-topic list with categorized sections (use collapsible accordions if needed to avoid overwhelming users)

Add privacy toggle to each (see Priority 3)

📐 DESIGN SYSTEM CONSISTENCY REQUIREMENTS
YOU MUST:

Use existing maroon/burgundy (#8B1538 or similar) for primary buttons and brand elements

Use existing mint/teal background for crisis banner

Maintain current card style: white background, subtle shadow, rounded corners

Keep existing typography (font families, sizes, weights)

Use existing icon style (emoji-based icons for topics, UI icons for nav)

Match existing spacing/padding patterns

Use existing button styles: solid maroon primary, outlined secondary

Keep existing form input styles (rounded, bordered)

Maintain existing navigation bar design

YOU MUST NOT:

Change color palette

Redesign card layouts

Change typography system

Add flashy animations or modern UI trends that clash with current design

Alter logo or branding elements

🎯 IMPLEMENTATION CHECKLIST
When you are done implementing:

✅ Crisis banner shows all 7 resources with working links (911, 988, EMPACT, TELUS, Crisis Text Line)
✅ All 43 support topics are available in profile, Share Support Need, filters, and group creation
✅ Profile settings allow marking topics as "Hide from public profile"
✅ Connect with Peers page has dropdown filter + search bar (not horizontal pills)
✅ Connect with Peers shows AI-recommended matches with match scores
✅ Privacy-marked topics are used for matching but hidden from public profile cards
✅ /groups page exists with full CRUD functionality
✅ Group creation allows topic selection and public/private toggle
✅ Group invite screen shows AI-recommended people based on topic match
✅ "Follow-up questions used", "Groups joined", "Messages sent" counters are removed
✅ 5-question limit on AI follow-up is removed
✅ "Share Another Challenge" renamed to "Need help with something else?"
✅ "Explore Peer Supporters" renamed to "Connect with Peer Supporters" everywhere
✅ "Share Your Challenge" page renamed to "Share Your Support Need"
✅ All navigation links work correctly (Resources → resources-hub)
✅ All UI changes match existing design system (colors, fonts, spacing, components)

🛡️ SAFETY & ETHICS NOTES
Always keep the crisis banner visible and accessible

Never hide or deprioritize emergency resources

Treat sensitive topics (suicide, assault, trauma) with utmost care in UI language

Ensure AI matching respects privacy: never expose private topics publicly

Group recommendations must not expose private information

All safety disclaimers ("This is peer