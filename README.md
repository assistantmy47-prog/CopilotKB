# CopilotKB — Portable Teams Knowledge Capture

A practical implementation guide for extracting decisions, actions, issues, risks and material facts from a specific Microsoft Teams conversation, retaining them in a **portable JSON file stored in an approved SharePoint document library**, and retrieving them later through Microsoft 365 Copilot Agent Builder.

> **Project state:** Documentation, JSON schema, example records and a local writer utility only. No live Copilot agent, Power Automate flow or SharePoint folder has been provisioned. This is a **public repository**: never commit organisation-specific Teams data, personal data, credentials, tenant URLs or actual project records.

## The design

\`\`\`text
Specified Teams chat
    |
    v
Copilot opened INSIDE that Teams chat
    |
    v
Date-bounded structured extraction prompt
    |
    v
Human validation against source messages
    |
    v
SharePoint DOCUMENT LIBRARY
  - knowledge.json  <- portable authoritative store
  - knowledge.txt   <- generated, readable search mirror
    |
    v
Microsoft 365 Copilot Agent Builder retrieval agent
  - Knowledge source: knowledge.txt
  - Answers with source references and statuses
\`\`\`

### Why two files?

- **\`knowledge.json\`** is a stable versioned structure for migration, processing, and deterministic writes.
- **\`knowledge.txt\`** is a derived readable file for reliable Agent Builder grounding. JSON is supported in some Microsoft 365 Copilot experiences, but is **not currently listed as an Agent Builder knowledge-file type**. Text is listed.
- Copilot Agent Builder is primarily a **retrieval / reasoning layer**, not a writable data pipeline. It cannot author the custom action needed to update a SharePoint JSON file.
- To write automatically, you would need an authorised **Power Automate** flow or other approved writer. Without it, the pilot uses a human-review step and file replacement/synchronisation.

## Implementation files

| File | Purpose |
| --- | --- |
| [docs/json-store.md](docs/json-store.md) | Complete SharePoint file workflow, governance, concurrency and automation pathway |
| [schema/knowledge.schema.json](schema/knowledge.schema.json) | Portable JSON Schema (v1) |
| [data/knowledge.template.json](data/knowledge.template.json) | Empty file to initialise in SharePoint |
| [examples/knowledge.example.json](examples/knowledge.example.json) | Fictional sample data only |
| [scripts/knowledge_store.py](scripts/knowledge_store.py) | Local JSON merge/upsert and TXT mirror generation tool |
| [prompts/teams-extraction.md](prompts/teams-extraction.md) | Prompt for the Copilot panel INSIDE the specific Teams conversation |
| [prompts/agent-instructions.md](prompts/agent-instructions.md) | Agent Builder instructions for retrieval from the TXT mirror |
| [docs/knowledge-register.md](docs/knowledge-register.md) | Data definitions, review policy and acceptance tests |
| [docs/automation-options.md](docs/automation-options.md) | Optional Power Automate path, subject to permissions |

## Quick start

1. Create an approved SharePoint document library folder, e.g. \`Documents/CopilotKB/\`. Turn on version history and verify access settings.
2. Copy [data/knowledge.template.json](data/knowledge.template.json) into SharePoint as \`knowledge.json\`.
3. Open the **exact Teams chat**, choose **Open Copilot**, and use [the extraction prompt](prompts/teams-extraction.md) with a bounded date range. Review all results and copy message source links.
4. Save the JSON extraction output (a record or \`records\` array) to a local \`new-records.json\`.
5. Run the standard-library Python utility against your working copy of \`knowledge.json\`:

   \`\`\`bash
   python scripts/knowledge_store.py upsert \
     --store knowledge.json --input new-records.json --mirror knowledge.txt
   \`\`\`

6. Upload or synchronise **both** files back to the SharePoint library. The utility itself does not connect to SharePoint.
7. In **Microsoft 365 Copilot → Agents → Edit → Configure → Knowledge**, add the specific SharePoint **\`knowledge.txt\`** file; use [the retrieval instructions](prompts/agent-instructions.md).
8. Test responses for a known confirmed decision, an unapproved proposal, a superseded decision and a nonexistent record. Check that source links and statuses are correct.

## Example of a JSON record

\`\`\`json
{
  "id": "110e8400-e29b-41d4-a716-446655440001",
  "title": "Pilot scope limited to one fictional Teams chat",
  "record_type": "Decision",
  "project": "DEMO-PROJECT",
  "description": "In a fictional exercise, the test team approved a one-chat pilot.",
  "status": "Confirmed",
  "owner": null,
  "event_date": "2026-11-13",
  "source_chat": "Fictional Example Chat",
  "source_link": null,
  "last_reviewed": "2026-11-16",
  "review_status": "Verified",
  "created_at": "2026-11-16T15:00:00Z",
  "updated_at": "2026-11-16T15:00:00Z"
}
\`\`\`

Production records may include \`rationale\`, \`due_date\`, \`tags\` and \`related_record_ids\` as defined in the schema. **Never claim an unlinked fictional record is evidence of a real decision.**

## Design guardrails

- **Source verification:** AI extraction is unverified until a person checks the underlying Teams discussion.
- **Data provenance:** Preserve the originating Teams message link wherever available.
- **No ungrounded approvals:** “Proposed” and “Confirmed” must remain distinct.
- **Temporal consistency:** Keep records and indicate when an older decision is superseded.
- **Concurrency:** A single JSON file has overwrite risk; keep one editor/writer during the pilot, and use SharePoint version history.
- **Content boundaries:** Do not publish internal chat extracts or upload regulated/confidential records to this public repository.
- **Indexing:** After replacing \`knowledge.txt\`, allow indexing time and validate that Agent Builder is using its latest version.
- **Scope:** A source-prioritisation toggle is not guaranteed source isolation, and agent conversation memory is not a persistent database.

## Roadmap

1. **MVP:** One chat, weekly manual extraction, JSON updates, TXT retrieval mirror.
2. **Optional low-code write:** Power Automate standard SharePoint connector reads/updates JSON, plus generation of the TXT mirror.
3. **Enhanced automation:** Licensed AI processing, approval workflows, deduplication and incremental ingestion.
4. **Scale:** Partition the JSON store by workstream/date while retaining the same schema.

## Microsoft references

- [Agent Builder limitations](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder)
- [Agent Builder knowledge sources](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge)
- [Power Automate SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepoint/)
