# Knowledge register schema and operating controls

## Create the register

Create a Microsoft List / SharePoint list named **Project Knowledge Register** within an approved SharePoint site. Set permissions based on the sensitivity of the discussion and apply your organisation's information management and retention requirements.

### Minimum viable columns

| Column | Type | Required? | Description |
| --- | --- | --- | --- |
| Title | Single line text | Yes | Succinct label for one atomic record |
| Record Type | Choice | Yes | Decision / Action / Risk / Issue / Fact |
| Project | Choice or single line text | Yes | Consistent workstream identifier |
| Description | Multiple lines | Yes | Concise, evidence-based description |
| Status | Choice | Yes | Proposed / Confirmed / Closed / Superseded |
| Owner | Person | No | Only populate if the owner is identified |
| Event Date | Date | Yes if known | When discussed/decided; not necessarily capture date |
| Source Chat | Single line text | Yes | Chat title or approved conversation reference |
| Source Link | Hyperlink | Recommended | Link to the evidence-bearing Teams message |
| Last Reviewed | Date | Yes | Most recent human validation date |

Use SharePoint's created/modified audit fields alongside the above columns; do not overwrite event dates with data-entry timestamps.

### Recommended enhancements (after pilot)

| Column | Purpose |
| --- | --- |
| Review State | Draft / Needs Review / Verified |
| Reviewer | Person who validated the extraction |
| Related Record ID | Link previous or superseded records |
| Decision Rationale | Separate rationale from conclusion where useful |
| Due Date | For actions only, when explicitly committed |
| Classification | Organisational information classification |
| Record Version / Change Note | Explain material amendments |

**Status and verification are separate dimensions.** For example, an approved but unverified extraction should not be treated as a confirmed fact merely because AI labelled it Confirmed. During a pilot, if no Review State column exists, use a manual review gate before entering a record into the register.

## Examples — fictional only

| Title | Record Type | Status | Description | Owner |
| --- | --- | --- | --- | --- |
| Approve pilot scope | Decision | Confirmed | Fictional team explicitly agreed the pilot would use one test chat. | Not stated |
| Consider weekly reporting | Decision | Proposed | Fictional suggestion to review weekly reporting; no decision recorded. | Not stated |
| Validate source link coverage | Action | Proposed | Fictional request to check whether source links resolve. | Test owner |
| Earlier extraction approach | Decision | Superseded | Fictional prior choice replaced by a later confirmed approach. | Not stated |

These are examples only, not extracted from any actual team discussion.

## Weekly operating procedure

1. Select the exact Teams conversation and a bounded date range.
2. Run the standard extraction prompt from the chat's own Copilot panel.
3. Compare output to the messages and validate status, wording, owner and dates.
4. Search SharePoint for existing records on the same subject.
5. Create or update records, preserving source links and change history.
6. Mark uncertain records as draft / needs review; do not present them as confirmed.
7. Sample-test the retrieval agent using known source-backed records.
8. Record any gaps due to inaccessible chat history or missing permissions.

## Governance and control points

- **Source traceability:** Every important decision should link to its original Teams message whenever possible.
- **Permission inheritance:** Ensure the SharePoint register is not broader in access than the information it contains; Teams membership does not automatically match SharePoint permissions.
- **Data minimisation:** Capture only material information needed for future business use; avoid full transcripts and unnecessary personal data.
- **Retention and disposal:** Apply approved M365 retention/classification settings; GitHub is not the repository for business records.
- **Conflict resolution:** Keep old decisions discoverable with Superseded status and a link to replacement, rather than quietly changing historical facts.
- **Duplicate handling:** Check existing records first; automated deduplication is not part of the MVP.
- **Security verification:** Validate the agent's results using accounts with different permissions where policy allows.
- **Reliability:** Retrieval from a SharePoint list depends on indexing, permissions, licensing and available knowledge features, and should be acceptance-tested in the target tenant.

## Acceptance criteria

- Agent retrieves a known verified record and provides a correct record/source reference.
- Agent does not confuse **Proposed** with **Confirmed**.
- Agent recognises **Superseded** records and explains later confirmed replacements.
- Agent returns an evidence-based **no matching record found** response for absent content.
- Reviewer can navigate from the register to the original Teams message, where policy and permissions permit.
