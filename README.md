# CopilotKB — Teams Knowledge Capture Agent

A pragmatic implementation guide for retaining useful decisions, actions, issues, risks and material facts from Microsoft Teams conversations using **Microsoft 365 Copilot Agent Builder**, **Teams Copilot** and **SharePoint**.

> **Status:** Implementation playbook, not a deployed agent. This project contains no Teams messages, Microsoft credentials, production configurations or client information. Repository is public: do not commit actual chat transcripts, project decisions, employee details or tenant URLs.

## Objective

Turn conversation content into durable, searchable project knowledge, with an auditable reference to the originating Teams message.

Typical question: “What did the team agree about a particular exception-handling approach, when, and on what evidence?”

A conversational answer alone is **not** a persistent knowledge register. For the initial implementation, use SharePoint as the system of record; the Copilot agent is the retrieval interface.

## Constraints and recommended design

Assume access to Microsoft 365 Copilot and its Agent Builder, but **not** standalone Copilot Studio agent creation or premium workflows.

| Requirement | Available MVP approach | Limitation |
| --- | --- | --- |
| Review one intended Teams conversation | Open **Copilot inside that Teams chat** | Chat access, history window and citation availability depend on tenant/policy/product behaviour |
| Extract useful information | Use the structured Teams extraction prompt | AI output requires human verification |
| Retain information beyond the chat | Store reviewed items in a SharePoint list | Manual copy/review for the MVP |
| Ask questions later | Agent Builder agent with that SharePoint list as knowledge | Retrieval accuracy and permissions still need testing |
| Automatic capture from Teams | Optional Power Automate flow, if allowed | Trigger availability, tenant policies and connector rights need verification |
| AI-based automatic consolidation | Future licensed workflow | Not provided by basic Agent Builder alone |

**Important retrieval distinction:** Selecting a particular Teams conversation as an Agent Builder knowledge source does not guarantee that a free-form user query will be scoped to the right chat. This project deliberately separates capture (Copilot opened from the intended chat) from retrieval (a curated SharePoint register). “Only use specified sources” is a source-prioritisation option, **not** an access-control or guaranteed retrieval boundary.

## Architecture

1. **Teams conversation** — original message-level evidence.
2. **Teams Copilot** — manually invoked from the specific intended conversation to produce a structured extraction.
3. **Human review** — verify the details, owner, decision status and evidence; resolve duplicates and contradictions.
4. **SharePoint: Project Knowledge Register** — persistent source of truth.
5. **Microsoft 365 Copilot Agent Builder: Project Knowledge Assistant** — reads the register and answers evidence-backed questions.

The MVP is **manually triggered**, not a background monitor.

## Quick start

### A. Create the SharePoint register

Create a SharePoint/Microsoft List named **Project Knowledge Register** in an appropriate site with organisation-approved access controls and retention settings.

Minimum columns:

| Column | Suggested type | Guidance |
| --- | --- | --- |
| Title | Single line text | Concise subject |
| Record Type | Choice | Decision / Action / Risk / Issue / Fact |
| Project | Choice or text | Workstream or project |
| Description | Multiple lines | Atomic, evidence-based summary |
| Status | Choice | Proposed / Confirmed / Closed / Superseded |
| Owner | Person | Blank when not stated |
| Event Date | Date | When discussed or decided, not automatically capture date |
| Source Chat | Single line text | Chat title or approved identifier |
| Source Link | Hyperlink | Exact message link where available |
| Last Reviewed | Date | Validation date |

See [SharePoint schema and governance](docs/knowledge-register.md) for suggested enhancements.

### B. Capture information from a specific Teams chat

1. Navigate to **the actual Teams chat** to be reviewed.
2. Open **Copilot in that conversation**, rather than asking an agent to guess the chat.
3. Use [the capture prompt](prompts/teams-extraction.md), specifying a defined start/end date.
4. Inspect the resulting records against the source messages; copy individual source links where available.
5. Add one SharePoint list item for each **distinct material record**.
6. Mark proposals as **Proposed** until confirmed by evidence. Flag unverified/ambiguous results rather than silently assigning owners or approvals.

Start with a **weekly manual capture** for one project conversation, then expand once the process is reliable. Teams Copilot's accessible history and historical message coverage may be limited; validate what it can actually read before depending on it as a complete archive.

### C. Configure the retrieval agent

1. Open **Microsoft 365 Copilot → Agents** and create or edit an agent.
2. Name it **Project Knowledge Assistant**.
3. In **Configure → Knowledge**, add the **specific SharePoint list** (not just a broad SharePoint site). Confirm the UI supports selecting the list in your tenant.
4. For this retrieval agent, **remove broad Teams chat knowledge sources** so it is not asked to guess which raw conversation to search.
5. Enable **Only use specified sources**, if available, while recognising that this is not a strict isolation guarantee.
6. Paste [the agent instructions](prompts/agent-instructions.md) into the agent's Instructions field.
7. Save and test in a fresh Copilot chat.

### D. Run an acceptance test

Create several **fictional or approved non-sensitive** SharePoint test entries, including a confirmed decision, a proposal, an open action, and a superseded decision. Verify that the agent:

- Locates the correct project item and cites a source.
- Does not promote a **Proposed** record to a **Confirmed** decision.
- Distinguishes an open action from one closed.
- Surfaces an older decision as **Superseded** rather than presenting it as current.
- Says “not found” when no supporting record exists.
- Does not expose records the user lacks permission to access.

If a test fails, review the source-list connection, indexing/access rights, fields and agent instructions; do not rely on prompts alone to enforce permissions.

## Operating model

- **Frequency:** once weekly to start, for one well-defined chat.
- **Input:** date-bounded conversation plus the standard capture prompt.
- **Human control:** reviewer validates every entry against source evidence.
- **Output:** atomic SharePoint rows, not an undifferentiated weekly narrative.
- **Change management:** prefer updating the status and linking related records over silently replacing historical decisions.
- **Governance:** follow corporate retention, confidentiality, access, privacy and data-classification requirements. Do not store regulated data in this public repository.

## Optional automation

If your Microsoft 365 entitlement allows **Power Automate** automated cloud flows and the Teams/SharePoint standard connectors:

1. Select a new-message trigger tied to a particular Teams chat, where supported.
2. Capture chat/message identifiers, body, sender and timestamp.
3. Optionally require a deliberate marker such as **#decision** or **#action**.
4. Create a draft or unverified SharePoint list record.
5. Validate duplicates and require review before labelling anything confirmed.

This basic flow can **capture** messages, but it does not automatically reconcile an entire multi-day conversation or make sound AI classifications. AI-assisted processing or enhanced orchestrations may require other licensing, permissions and governance approvals. See [optional automation plan](docs/automation-options.md).

## Definition of done for MVP

- [ ] SharePoint list created with permitted access and relevant retention policy.
- [ ] Chat-specific extraction tested against real source message links.
- [ ] At least five sample items reviewed and entered.
- [ ] Retrieval agent configured with the correct SharePoint list.
- [ ] Confirmed / Proposed / Superseded / not-found tests passed.
- [ ] Named reviewer and weekly operating cadence established.
- [ ] Licensing and tenant policy assumptions documented.

## References

Microsoft Learn documentation (feature availability depends on tenant settings and product changes):

- [Knowledge sources for Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge)
- [Microsoft Teams connector for Power Automate](https://learn.microsoft.com/en-us/connectors/teams/)
- [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepointonline/)
- [Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/)

_No automated workflow or Copilot agent is provisioned by these Markdown files. Follow the steps in your own approved Microsoft 365 environment._
