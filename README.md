# CopilotKB — 10-minute proof of concept

**Goal:** Ask a Microsoft 365 Copilot agent questions about decisions and actions captured from a specified Teams chat.

**What works now:** Agent Builder reads a `knowledge.txt` file in SharePoint; Teams Copilot extracts new records; you manually add records to `knowledge.json` and refresh the text copy.

**What does NOT work yet:** Agent Builder alone cannot automatically read every new Teams message or write to SharePoint. This proof of concept is **manual capture + agent retrieval**. It needs no Copilot Studio or Power Automate.

## 1. Download files and upload to SharePoint

1. In GitHub select **Code → Download ZIP**, then unzip this repository.
2. In an approved SharePoint **document library**, make a folder called `CopilotKB`.
3. Upload the two files `knowledge.json` and `knowledge.txt` **from the repository root** to that folder. They already contain **two clearly marked fictional test records**.
4. Do **not** upload real Teams conversations or confidential records to this **public GitHub repository**. Store real knowledge files only in your approved SharePoint location.

## 2. Create the agent in Microsoft 365 Copilot

1. Open [Microsoft 365 Copilot](https://m365.cloud.microsoft/chat) → **Agents** → **New agent** → **Skip to configure** (or edit an existing agent).
2. **Name:** `CopilotKB`
3. **Description:** `Finds decisions, actions, risks, issues and project facts stored in a SharePoint knowledge file, with status and source references.`
4. **Instructions:** Copy **all text** from [agent-instructions.txt](agent-instructions.txt) into **Instructions**.
5. **Knowledge → Browse / Attach cloud files:** select **the SharePoint copy of `knowledge.txt`**, not your local file and not `knowledge.json`.
6. Remove other Teams chats or broad sources. Set **Search all websites: Off**. Set **Only use specified sources: On** if the option is present.
7. **Create / Save** the agent.

## 3. Test it

In the agent, ask:

- `What was agreed about the pilot scope?` → should find fictional record `DEMO-001`.
- `Was a daily digest approved?` → should say `DEMO-002` is only **Proposed**.
- `What did we agree about a topic not in the file?` → should report no supporting record.

If the agent finds no record, check that the **SharePoint cloud file** is attached, the knowledge source has finished preparing/indexing, and you have access to the file. Do not try to add `knowledge.json` as the agent's knowledge source: `.json` is not on Microsoft's documented Agent Builder supported-file list; `.txt` is.

## 4. Capture information from a real Teams chat

1. In Teams, open the **specific chat** you want to analyse, then open **Copilot inside that chat**.
2. Paste [capture-prompt.txt](capture-prompt.txt), replacing `[PROJECT]`, `[START DATE]` and `[END DATE]`.
3. Check the output against the messages. Ensure every decision, owner, deadline and source link is correct.
4. In your **local downloaded copy** of `knowledge.json`, delete the two `DEMO ONLY` entries and paste the new JSON record objects into the `records` array. Keep valid JSON syntax. Set `review_status` to `Verified` and `last_reviewed` to today's date **only for records actually checked**.
5. Save the JSON file. Make `knowledge.txt` an **exact copy of the JSON text** (yes, including braces). On a Mac, from the unzipped repository folder, run: `cp knowledge.json knowledge.txt`. Alternatively, copy/paste all of the JSON text into `knowledge.txt`.
6. Upload **both** updated files into the same SharePoint folder, choosing **Replace** when prompted. Keep SharePoint file version history enabled.
7. In the agent, ask about one of the captured records. If the update isn't visible, recheck the configured knowledge file and allow it to finish processing.

**Every subsequent capture:** append new unique-ID record objects to `knowledge.json`, copy it over `knowledge.txt`, and replace both SharePoint files. Do not upload business data back to this public repo.

## Files

- [agent-instructions.txt](agent-instructions.txt) — paste directly into Agent Builder
- [capture-prompt.txt](capture-prompt.txt) — paste into Copilot **inside the selected Teams chat**
- [knowledge.json](knowledge.json) — portable source data, with fictional test entries
- [knowledge.txt](knowledge.txt) — identical JSON content in a `.txt` file for Agent Builder

## Why two identical knowledge files?

This is intentional for the POC: the JSON remains portable; the `.txt` copy can be read as an Agent Builder knowledge file. You don't need Python, an updater script, a SharePoint list or a separate format-conversion process.

**Source notes:** Microsoft's [Agent Builder knowledge-source guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge) and [Agent Builder overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder).
