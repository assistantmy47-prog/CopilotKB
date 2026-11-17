# Portable JSON knowledge store in SharePoint

## Design decision

**SharePoint document library**, not a SharePoint List, is the storage location.

- **knowledge.json** — portable system of record using [the v1 schema](../schema/knowledge.schema.json).
- **knowledge.txt** — generated search mirror for Microsoft 365 Copilot Agent Builder.
- **knowledge.json.bak** — local pre-write backup created by the included utility (do not treat this as a substitute for SharePoint version history).

The JSON file is for storage and interchange. Copilot's general chat can work with JSON, but current **Agent Builder knowledge-file documentation does not list \`.json\` among supported file formats**. Agent Builder and SharePoint agents list \`.txt\`; point the agent to \`knowledge.txt\`. Do not assume the \`.json\` file is fully indexed or that Copilot can write to it.

## Proposed SharePoint location

\`<approved site>/Shared Documents/CopilotKB/knowledge.json\`
\`<approved site>/Shared Documents/CopilotKB/knowledge.txt\`

This is an example path; use the approved site and library in your tenant. Restrict access to appropriate project participants, apply retention/sensitivity settings, and enable document version history.

**Never copy real Teams messages, personally identifiable information or internal project decisions into this public Git repository.** The repository contains documentation, schema and fictional examples only.

## File structure

The top-level object contains:
- \`schema_version\`: \`1.0.0\` (explicit for future migrations)
- \`updated_at\`: ISO 8601 UTC timestamp or null for an empty file
- \`records\`: an array of knowledge records

Each record contains the earlier SharePoint-list concepts plus a persistent \`id\` (UUID), \`review_status\`, creation/update timestamps, and optional \`rationale\`, \`due_date\`, \`related_record_ids\` and \`tags\`.

The **record type** classifies a Decision / Action / Risk / Issue / Fact. The **status** records Proposed / Confirmed / Closed / Superseded. The separate **review_status** indicates Pending Review / Verified / Rejected. Only verified records should be treated as reliable business facts.

The example at [examples/knowledge.example.json](../examples/knowledge.example.json) is entirely fictional; the initial production file should start from [data/knowledge.template.json](../data/knowledge.template.json).

## Minimum viable workflow without Power Automate

1. Create the \`CopilotKB\` folder in an approved SharePoint document library.
2. Copy \`data/knowledge.template.json\` into that folder as \`knowledge.json\`.
3. Open the intended Teams chat and run [the JSON extraction prompt](../prompts/teams-extraction.md) for a bounded period.
4. Review each proposed item against the underlying messages; obtain source links and ensure statuses are supported.
5. Save the **records array** from the extraction as \`new-records.json\` locally, or in a controlled SharePoint-synced working folder.
6. Use the included Python standard-library tool to merge into your local/synced copy of \`knowledge.json\` and produce \`knowledge.txt\`:

   \`\`\`bash
   python scripts/knowledge_store.py upsert \
     --store knowledge.json \
     --input new-records.json \
     --mirror knowledge.txt
   \`\`\`

7. Upload/replace **both** \`knowledge.json\` and \`knowledge.txt\` in the SharePoint library, or allow the approved SharePoint sync client to sync both files.
8. Add the **\`knowledge.txt\` SharePoint file** as the agent's specific knowledge source. Validate source freshness and evidence links in a new agent session.

The tool adds UUIDs and metadata where absent, rejects unsupported fields, detects duplicate IDs, and writes a local \`.bak\` backup on changes. It **does not** upload directly to SharePoint; the upload/synchronization step needs to occur in your M365 environment. It does not perform semantic deduplication or independently verify decisions.

### Revision policy

For corrections, supply a record with its existing UUID plus the revised fields, and run the command with \`--allow-update\`. Do not generate a new UUID for a revised record. Review the source evidence and preserve historical relationships using \`related_record_ids\`.

### Concurrency

A single JSON file is susceptible to lost updates when two users/processes overwrite it at the same time. For the MVP, assign **one editor** or require an explicit check-out/update process, enable SharePoint versioning and avoid editing while another sync is in progress.

For automation, serialize writes and/or implement a version/ETag precondition; never run uncontrolled parallel read-modify-write operations against one file.

### Size and performance

One file is suitable for a small pilot. If the knowledge base grows, partition by project or period (e.g. \`logistics-2026-11.json\` + matching TXT) and track an index, while keeping the exact same v1 record schema. Splitting preserves portability and makes agent retrieval more manageable.

## Optional standard-connector Power Automate solution

If flow creation is permitted, a write workflow could:

1. Receive approved/structured JSON records (from a permitted trigger or controlled manual submission).
2. **Get file content** of \`knowledge.json\` using the SharePoint connector.
3. Parse the JSON; validate the record fields and duplicate IDs.
4. Append records to the \`records\` array; update \`updated_at\`.
5. **Update file** to replace \`knowledge.json\` with the serialized object.
6. Regenerate/update \`knowledge.txt\` (requires a deterministic render step).
7. Log failures and notify a reviewer.

Microsoft documents **Get file content**, **Get file content using path**, and **Update file** actions in the standard SharePoint connector. However, **Copilot Agent Builder alone cannot invoke this custom write action**. The flow is a separate capability and must be permitted in your tenant.

If no automation is allowed, keep the explicit manual review/update step; do not imply the agent already writes to SharePoint.

## Security/operations

- Source links may not be available in every Copilot response; do not fabricate URLs.
- A \`Verified\` value means a human has actually checked the record, not that Copilot asserted confidence.
- Apply appropriate site permissions/retention and evaluate whether the original Teams data can lawfully be copied into a new storage location.
- SharePoint document versioning helps recovery, but does not eliminate write conflicts.
- Do not store tokens, connection secrets or tenant-specific private addresses in the GitHub repository.

## References

- [Agent Builder overview and actions limitation](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder)
- [Agent Builder knowledge files and supported types](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge)
- [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepoint/)
- [File formats in Microsoft Copilot (distinct from Agent Builder knowledge)](https://support.microsoft.com/en-us/microsoft-365-copilot/file-formats-supported-by-microsoft-365-copilot)
