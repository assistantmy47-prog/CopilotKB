# Optional automation — licensing-dependent

The baseline CopilotKB procedure works with **Microsoft 365 Copilot Agent Builder + Teams Copilot + SharePoint** and manual review. Automation is an optional extension, not a prerequisite.

## Entitlement check

Open [Power Automate](https://make.powerautomate.com) with your work account and check whether you can create an **automated cloud flow**.

If creating flows is blocked by licensing, environment restrictions, data loss prevention (DLP) policies or admin controls, continue with the manual MVP.

> Teams and SharePoint connectors are generally **standard** Power Automate connectors, but trigger/action availability, user rights and tenant policy can differ. Do not assume full Teams history extraction or AI processing is licensed because the portal opens.

## Candidate phase-2 flow (deterministic chat targeting)

| Stage | Candidate operation | Notes |
| --- | --- | --- |
| 1. Select | Specific chat / conversation ID | Validate exactly which chat the connection can access |
| 2. Trigger | New Teams chat message | Check that a trigger for the chosen chat type is actually available |
| 3. Parse | Message text, sender, sent time and message ID/link | Preserve traceability and handle edited/deleted messages according to policy |
| 4. Filter | Explicit marker such as #decision or #action | Avoid indiscriminate capture of all correspondence |
| 5. Persist | Create SharePoint list item | Initially write as draft / needs review |
| 6. Review | Human validates and changes status | Do not auto-promote to Confirmed |

**Do not treat a new-message trigger as historical backfill**: a separate, permitted retrieval mechanism would be needed to process older messages.

## AI-assisted phase 3 (only if approved)

An additional licensed AI action/service could classify messages, deduplicate records, identify action owners, reconcile changing decisions and produce structured output for human approval. Copilot Studio, AI Builder, Power Automate premium or usage-based services may be relevant depending on tenant entitlements.

Potential controls:
- Prompt/version control for extraction and status definitions
- Confidence and evidence quality thresholds
- Validation prior to SharePoint writes
- Retry/dead-letter handling to avoid lost messages
- Audit trail of modifications
- Access rights consistent with the Teams source and SharePoint destination
- Removal of unnecessary personal or protected information

## Practical progression

1. **Pilot:** One chat, one week, manual Copilot extraction and SharePoint validation.
2. **Standardise:** Reusable prompt, agreed fields, record ownership and recurring cadence.
3. **Semi-automate:** Flow captures deliberately tagged messages to draft list items.
4. **Enhance:** Licensed AI processing and reconciliation after measured retrieval quality.

## References

- [Microsoft Teams connector](https://learn.microsoft.com/en-us/connectors/teams/)
- [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepointonline/)
- [Microsoft 365 Copilot Agent Builder knowledge](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge)
