# Teams chat extraction prompt — JSON output

**Where to run:** Open Copilot **inside the specific Teams conversation**. Replace the date placeholders. Do not ask a separate general agent to guess the conversation.

Copy the following prompt:

---

Review **this Teams conversation** for the period **[START DATE] through [END DATE]** inclusive.

Extract material information suitable for long-term project knowledge capture:
- Explicitly confirmed decisions and rationale
- Proposed decisions (clearly distinguished from approvals)
- Action items, named owners and due dates where stated
- Risks, issues and durable material facts
- Changes to prior decisions, including superseded decisions

**Output a valid JSON object** with one property named \`records\`, containing an array. Create **one record per distinct fact, decision, action, risk or issue**.

Use this structure for every record:

\`\`\`json
{
  "title": "Short description",
  "record_type": "Decision",
  "project": "[PROJECT NAME]",
  "description": "Grounded, concise summary",
  "status": "Proposed",
  "owner": null,
  "event_date": null,
  "source_chat": "[THIS CHAT'S NAME]",
  "source_link": null,
  "last_reviewed": null,
  "review_status": "Pending Review",
  "rationale": null,
  "due_date": null,
  "related_record_ids": [],
  "tags": []
}
\`\`\`

Permitted values:
- \`record_type\`: Decision, Action, Risk, Issue, Fact
- \`status\`: Proposed, Confirmed, Closed, Superseded
- \`review_status\`: **Pending Review** only; it must be human-verified before being changed to Verified
- If owner, date, rationale or source link is unknown, use \`null\` — **do not fabricate**.
- Use ISO \`YYYY-MM-DD\` format for dates.

Rules:
1. Only use **this** Teams chat. Do not silently substitute a different conversation.
2. Explicit consent/agreement is required for the status Confirmed; silence or speculation is not confirmation.
3. Each record must be atomic. Do not combine unrelated issues.
4. Preserve the original message source URL when retrievable. If not available, use null and flag it for validation separately.
5. Do not invent personal names, deadlines, dates, approvals, citations or prior record IDs.
6. Do not assign stable \`id\`, \`created_at\` or \`updated_at\` fields: the knowledge-store writer will supply them.
7. Do not include sensitive personal information or unrelated social discussion.
8. Be honest about incomplete chat history and coverage limitations.

**After the JSON**, provide short plain-language review notes indicating:
- Which source links are missing
- Which items appear ambiguous or might be duplicates
- Which part of the requested time period could not be accessed

Do not put explanation inside the JSON object itself.

---

## Save and validate

1. Copy the JSON object (without explanatory notes) to \`new-records.json\`.
2. Verify extracted information against the actual Teams messages.
3. Update \`review_status\` to \`Verified\` **only after independent human review**. Populate \`last_reviewed\` with the review date.
4. Merge into the portable \`knowledge.json\` with \`scripts/knowledge_store.py\`, which creates UUIDs/timestamps and a TXT mirror.
5. Upload both files to an approved SharePoint library (or sync using an authorised SharePoint client).

The prompt generates **candidate records**, not verified evidence and not an automatic SharePoint write.
