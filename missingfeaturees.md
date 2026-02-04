You are updating the Groups page of the SunDevil Circle web app for ASU students. Keep the existing layout, styling, and card design exactly the same: same headings, card structure, typography, spacing, shadows, buttons, and “Join Group” behavior.
​

1. Preserve current layout and structure
Keep the “Need immediate support?” crisis banner, the top navigation bar, and the “Groups – Find or create a peer support group that fits your needs” header exactly as they are.
​

Keep the search bar (“Search groups”), support topic multi-select (“Support topics”), and “Sort by” dropdown with options: Best Match, Most members, Newest, A–Z, plus Clear and Apply controls.
​

Keep the “All Groups” section and the “Create a New Group” form at the bottom with the same fields: Group name, Description, Primary support topics (multi-select), Group type (Peer Support / Study/Accountability / Identity/Community / Social), Visibility (Public / Private), and Group Duration (Ongoing / Temporary).
​

Do not alter visual style, fonts, icons, colors, or card layout. Only add groups and fix search/filter behavior.

2. Ensure all groups are always visible (scrollable list)
Under “All Groups”, always render the full list of groups as cards in a scrollable list.

When no search query and no topic filters are applied, show all preset + user-created groups, ordered by the current “Sort by” selection.

When search or filters are applied, show the filtered results, but still as cards in the same list; do not hide the section or change the layout.

3. Fix the broken search behavior
Current bug: typing “finance” in the search field and clicking Search does not show the “Financial Stress” group in the results, even though it should match.
​

Implement correct search logic:

Search must match against at least:

group name (title)

group description

associated support topics (e.g., “Financial stress”, “Stress”, “Burnout”, etc.)

Example:

Query: “finance” or “financial” should match the “Financial Stress” group because its title and topics include “Financial Stress” / “Financial stress”.

Query: “career” should match “Career and Internships”.

Make search case-insensitive and robust to partial word matches (e.g., “finan” still finds “Financial”).

When search returns zero matches, show a friendly “No groups found” message plus a suggestion to “Clear filters” or “Create a New Group”.

4. Ensure support-topic filter works correctly
The “Support topics” multi-select must filter groups where any of the group’s topics match one of the selected topics (OR logic).

Example: selecting “Financial stress” must include the “Financial Stress” group; selecting “Stress” should include multiple groups like “Academic Pressure”, “Financial Stress”, “Health and Wellness”, “Career and Internships”, etc.

Filters must combine with search:

Search query + selected topics narrow down results together.

5. Keep and reuse existing preset groups
Use the existing groups as baseline presets (same text, same topics), ensuring they are always present unless explicitly deleted in the future admin UI.
​

Existing groups (do not rename or restyle unless specified):

Cultural Adjustment

Homesickness and Family

Academic Pressure

Language Barriers

Making Friends

Financial Stress

Health and Wellness

Career and Internships
​

Each keeps its current description and topic tags (e.g., “Financial stress / Stress”, “Career stress / time management / procrastination”).

6. Add the new preset groups (same card style & features)
Add the following new preset groups, using the same card layout as the existing ones (title, match %, badge like “Public”, description, topic pills, member count line, and “Join Group” button).
​

The new groups must behave exactly like existing groups:

can be joined/left

show up in search

honor topic filters

appear in all sorting modes (Best Match, Most members, Newest, A–Z).

Use reasonable placeholder match percentages (e.g., 40–70% “Good Fit” or “New Group”) and 0 members for now, unless your system auto-calculates these.

Core emotional/academic/connection groups (if not already present):

Anxiety & Overthinking

Description: “A space for students dealing with anxiety, overthinking, or constant worry. Share coping strategies and feel less alone.”

Topics: Anxiety, Social anxiety, Stress.

Depression & Low Mood

Description: “For students experiencing sadness, low energy, or feeling down. Connect with others who understand and support each other.”

Topics: Depression, Low mood, Motivation / concentration problems.

Loneliness & Making Friends (if separate from existing “Making Friends”)

Description: “If you’re feeling lonely or like you don’t quite fit in yet, this group is for you. Talk, share, and connect with others looking for community.”

Topics: Loneliness / isolation, Social anxiety, Homesickness.

Identity & “Who Am I?” / Direction

Description: “A space to talk about purpose, direction, and identity—academic, career, cultural, or personal. You don’t need to have it all figured out.”

Topics: Identity concerns, Career stress / “no direction”, Academic problems.

Sleep Problems & Insomnia

Description: “Struggling to fall asleep, stay asleep, or rest well? Share tips and routines and feel supported around your sleep challenges.”

Topics: Sleep problems / insomnia, Stress, Anxiety.
​

General Check‑In / How You’re Doing

Title suggestion: “Check‑In & General Support”

Description: “A gentle space to share how you’re doing—good, bad, or in‑between—and get support from peers.”

Topics: Stress, Loneliness / isolation, General emotional support.

Safety / higher‑risk topics (with clear non‑crisis framing):

Coping with Suicidal Thoughts / Self‑Harm Urges

Description: “For talking about urges and staying safe, not for emergencies. If you’re in immediate danger, use the 24/7 crisis resources at the top of the page.”

Topics: Suicidal thoughts / self-harm, Safety planning, Depression.

Trauma & Assault Survivors (Peer Coping)

Description: “A trauma‑aware space for students living with the impact of past trauma or assault. Focus on coping, grounding, and not feeling alone.”

Topics: Trauma / PTSD, Sexual assault / harassment, Domestic/dating violence.

Substance Use & Cutting Back

Description: “For students who want to talk about alcohol or substance use, cutting back, or finding healthier coping strategies.”

Topics: Substance use, Addiction / dependence, Safety concerns.

Daily functioning / study-life groups:

Focus, ADHD & Procrastination

Description: “Trouble focusing, starting tasks, or finishing assignments? Connect with others navigating ADHD, attention, and procrastination.”

Topics: ADHD / attention problems, Time management / procrastination, Motivation / concentration problems.

Burnout & Overload

Description: “Feeling exhausted, drained, or overloaded by school and life? Share experiences and small steps to prevent or recover from burnout.”

Topics: Burnout, Stress, Academic problems.

Money & Financial Stress (if you want a second finance-focused group)

Description: “Talk about budgeting, financial aid, work hours, and money stress with peers who get it.”

Topics: Financial stress, Work–school balance, Basic needs.

You can add additional preset groups for:

International Students & Culture Shock

LGBTQ+ Students

Students of Color & Bias/Discrimination

Chronic Health & Disability Coping
using the same pattern (title, short supportive description, topic tags drawn from the topic list).

7. Match all new groups to the topic system
For every new preset group, assign support topics from the existing master topic list (e.g., Anxiety, Depression, Financial stress, Homesickness, etc.) so that:

AI matching can recommend them.

Topic filters and search behave consistently.

Do not invent a separate topic taxonomy; reuse the same topic names as used on other pages (e.g., intake, “We Hear You” issues, profile setup).

8. Keep “Create a New Group” fully functional and consistent
User-created groups should:

Appear in the same “All Groups” list, using the same card layout.

Be included in search and topic filters.

Be sortable by all “Sort by” modes.

Users cannot break the layout; enforce reasonable length constraints on titles and descriptions to fit the existing card design.

9. Testing and acceptance criteria
Consider the work done when all of these are true:

Typing “finance” or “financial” in Search and clicking Apply shows the “Financial Stress” group and any other finance-related groups.

Typing “sleep” shows “Sleep Problems & Insomnia” and “Health and Wellness”.

Selecting “Financial stress” in the Support topics filter shows all finance-related groups.

Selecting “Stress” shows multiple groups (Academic Pressure, Financial Stress, Health and Wellness, Career and Internships, Burnout & Overload, etc.).

All preset groups listed above are visible under “All Groups”, scrollable, and styled identically to existing cards.

Clearing search and filters returns the full list of groups.

