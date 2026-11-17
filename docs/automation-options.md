# Power Automate extension — write JSON in SharePoint

This is **optional** and requires tenant permission to create Power Automate cloud flows. The MVP works with manual Teams Copilot extraction, the [JSON writer](../scripts/knowledge_store.py) and a SharePoint document library.

Microsoft 365 Copilot **Agent Builder cannot create custom external write actions by itself**. Do not misrepresent the retrieval agent as capable of modifying SharePoint.

## Verify licensing and policies first

1. Open [Power Automate](https://make.powerautomate.com) using your work account.
2. Check whether **Create → Automated cloud flow** or **Instant cloud flow** is available.
3. Verify that the Teams and SharePoint **standard connectors** are usable in the intended environment, and permitted by Data Loss Prevention (DLP), conditional access and business policies.
4. If blocked, use the manual MVP. Opening the Power Automate portal is not proof you have permission to create flows.

## Proposed deterministic file update flow

For controlled JSON submissions, create a flow which:

1. **Trigger:** A permitted manual trigger or a Teams-chat message trigger, if your tenant exposes the desired trigger.
2. **Identify source:** Use the exact Teams conversation ID where applicable; do not search arbitrary Teams chats by approximate names.
3. **Obtain the proposed records:** Either accept structured JSON records or capture explicitly tagged messages (\`#decision\`, \`#action\`). Merely triggering on a message does **not** automatically produce a credible summary of the whole discussion.
4. **Validate:** Parse the incoming JSON, check required fields, prevent duplicates, set review_status to Pending Review, and capture evidence/source links where available.
5. **Read:** SharePoint **Get file content** or **Get file content using path** retrieves \`knowledge.json\`.
6. **Merge:** Parse the existing JSON, append new UUID-keyed entries or intentionally revise existing IDs, and update the root \`updated_at\`.
7. **Write:** SharePoint **Update file** replaces the contents of \`knowledge.json\` with the complete updated valid JSON.
8. **Synchronise search representation:** Generate \`knowledge.txt\` deterministically from JSON, then use another **Update file** action. Consider separate maintenance if your flow cannot support a reliable text transformation.
9. **Review/audit:** Notify a reviewer, retain SharePoint version history and verify the new file version and agent search result.

**Important:** A file update is not an append operation. The flow performs **read → merge → rewrite**; there is a lost-update risk if two instances run concurrently. Configure serial execution for one file, and consider version/ETag guards or a queued writer. Test failure recovery and write conflicts before production use.

## Incremental capture is not historical reconstruction

- A new-message Teams trigger captures only messages exposed to it after the flow is enabled; it does not retroactively collect earlier messages.
- Message content alone may not prove a decision is confirmed. Use a reviewer to authorise status changes.
- Deep AI classification or automated conversation summarisation may require licensed AI capabilities, custom actions or additional service controls.

## Future enhancement

A more advanced implementation could add:
- Scheduled extraction with exact conversation IDs
- Idempotent ingestion keyed on Teams message IDs
- Decision reconciliation and historical linking
- Human approval before publishing confirmed information
- Partitioning by project/month to reduce single-file conflict and retrieval costs
- Retry handling, audit logs and failure notification

## References

- [SharePoint connector actions: Get file content, Update file](https://learn.microsoft.com/en-us/connectors/sharepoint/)
- [Teams connector](https://learn.microsoft.com/en-us/connectors/teams/)
- [Agent Builder actions limitation](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder)
