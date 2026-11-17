# Teams chat extraction prompt

**Use location:** Open **Copilot from within the specific Microsoft Teams conversation** to be reviewed. Do not rely on a standalone agent to infer which chat you intended.

Copy the prompt below, replace the date placeholders, run it, then verify every material result against the originating messages before saving to SharePoint.

---

Review **this Teams conversation** for the period **[START DATE] through [END DATE]**, inclusive. Confirm the conversation being reviewed and the date range used.

Extract material information suitable for a persistent project knowledge register.

Identify:
- Confirmed decisions and their rationale
- Actions, action owners and deadlines, where explicitly stated
- Risks and issues raised
- Material technical or business facts
- Changes to previously agreed positions, including superseded decisions

Return a table with exactly these columns:

| Title | Record Type | Description | Status | Owner | Event Date | Source Message |
| --- | --- | --- | --- | --- | --- | --- |

Rules:
1. Create one row for each distinct material item. Do not combine unrelated decisions or actions.
2. Record Type must be one of: **Decision, Action, Risk, Issue, Fact**.
3. Status must be one of: **Proposed, Confirmed, Closed, Superseded**, using the most appropriate available status.
4. Use **Confirmed** only where the conversation explicitly supports agreement or approval. A suggestion or unchallenged comment is not automatically confirmed.
5. Do not invent people, approval, action ownership, deadlines, dates or rationale.
6. If an owner, event date or source link is not ascertainable, use **Not stated** or **Unable to verify**; do not guess.
7. Quote sparingly and preserve the exact meaning of the discussion.
8. Give source message links or native citations for every item where possible. If Copilot cannot link to the source, mark the row **Needs manual source check**.
9. Highlight contradictory statements or later changes to an earlier position.
10. Do not include irrelevant social conversation, routine status updates with no lasting significance, sensitive information not necessary for the record, or speculative conclusions.
11. Do not claim completeness if some of the period is inaccessible. State what message history was actually available and what remains unchecked.

After the table, provide:
- **Items requiring validation** (ambiguous status, owner, rationale or date)
- **Potential duplicates** (if they can be identified from the available context)
- **Coverage limitations** (unavailable messages, limited history or missing citations)

---

## Review and save

1. Check every material fact and decision against the original Teams source.
2. Obtain the original message link using **More options → Copy link** where Copilot's citation is insufficient.
3. Copy reviewed rows into the SharePoint **Project Knowledge Register** list, one item per record.
4. Assign the correct Project and Source Chat values.
5. Leave status as Proposed or mark the record for review if it is not clearly agreed.
6. Check the register for duplicate or superseded items; link related records instead of deleting history.

This is a **human-reviewed extraction workflow**, not proof that Copilot has accessed the complete historical chat.
