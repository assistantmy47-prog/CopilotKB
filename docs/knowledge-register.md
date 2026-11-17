# Knowledge register — portable JSON v1

## Storage

**Do not create a SharePoint List for the MVP.** Store \`knowledge.json\` and a derived \`knowledge.txt\` side-by-side in a restricted SharePoint **document library**, with version history enabled.

Use [the implementation guide](json-store.md), [the JSON Schema](../schema/knowledge.schema.json), [the empty template](../data/knowledge.template.json), and [the fictional example](../examples/knowledge.example.json).

## Field definitions

| Field | JSON type | Purpose |
| --- | --- | --- |
| \`id\` | UUID string | Immutable, portable record identifier |
| \`title\` | string | Concise descriptive heading |
| \`record_type\` | enum | Decision, Action, Risk, Issue, Fact |
| \`project\` | string | Project/workstream identifier |
| \`description\` | string | Evidence-based, atomic information |
| \`status\` | enum | Proposed, Confirmed, Closed, Superseded |
| \`owner\` | string or null | Only if explicitly assigned |
| \`event_date\` | YYYY-MM-DD or null | When the original event occurred |
| \`source_chat\` | string | Source conversation identifier/title |
| \`source_link\` | URL or null | Original Teams message link |
| \`last_reviewed\` | YYYY-MM-DD or null | Human verification date |
| \`review_status\` | enum | Pending Review, Verified, Rejected |
| \`created_at\` | UTC ISO timestamp | When the register record was first created |
| \`updated_at\` | UTC ISO timestamp | When the register record was last changed |
| \`rationale\` | string or null | Explicit explanation for a decision |
| \`due_date\` | YYYY-MM-DD or null | Due date for an action when stated |
| \`related_record_ids\` | array of UUIDs | Related or superseding items |
| \`tags\` | array of strings | Searchable subject terms |

The file root contains \`schema_version\`, \`updated_at\` and \`records\`. \`schema_version\` starts at \`1.0.0\`. The [schema](../schema/knowledge.schema.json) is the formal contract; optional enhancements must not be invented in extracted data without a schema update.

**Review and business status are different dimensions.** A record can be *Proposed* and *Verified* if the human reviewer confirms that the team discussed a proposal but did not approve it. Conversely, an AI summary labelled *Confirmed* remains *Pending Review* until the original messages have been checked.

## Weekly operating procedure

1. Open the intended Teams chat and select Copilot from within it.
2. Run the date-bounded [JSON extraction prompt](../prompts/teams-extraction.md).
3. Review all material entries, source evidence, decisions, status, named owners and deadlines.
4. Copy candidate JSON into \`new-records.json\` in an approved working area.
5. Check for duplicates and historical relationships in the existing \`knowledge.json\`.
6. Mark reviewed entries as Verified and populate last_reviewed only after checking the source.
7. Use [the writer](../scripts/knowledge_store.py) to merge and regenerate the TXT mirror.
8. Upload or sync **both** files to SharePoint. Verify the Copilot agent is grounding answers in the updated \`knowledge.txt\`.
9. Preserve superseded records, link to replacements and keep SharePoint version history.

## Ownership and governance

- **Single writer initially:** Avoid overlapping updates to the JSON file; the writer creates a local backup but cannot prevent SharePoint sync conflicts.
- **Source traceability:** Use specific Teams message URLs when possible, not chat-only links.
- **Uncertain data:** Keep unknown owner/date/url values as null. Do not fabricate.
- **Retention and privacy:** Follow corporate recordkeeping, classification and least-privilege access rules.
- **Provenance:** Do not present a generated text mirror as the authoritative record.
- **Permission check:** SharePoint folder permissions do not automatically match the originating Teams chat's membership.
- **Durability:** Do not use GitHub or the agent's chat history for production records.

## Acceptance criteria

- JSON validates against versioned schema and has unique record IDs.
- The TXT mirror reflects the latest JSON content.
- A verified confirmed decision can be found in Copilot with its source.
- Proposed, pending-review and superseded entries are differentiated.
- The agent reports missing records without fabricating evidence.
- Manual review is required before unverified outputs are represented as approved outcomes.
- Source access is constrained by the approved SharePoint library permissions.

## When to migrate

Once the records grow or multiple users need concurrent writes, split the store into project/time-based JSON files or move storage to a transactional system (SharePoint List, Dataverse, database), preserving the JSON export schema so migration is straightforward.
