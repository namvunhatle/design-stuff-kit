# Keep sessions affordable

Every turn resends the whole transcript. Three habits account for most of the cost in design sessions, in this order:

1. **Long sessions without a reset.** Turn 60 costs many times more than turn 5 for the same question. When a screen or task is done, record the outcome in the project's memory files, then suggest `/clear`. A `/compact` re-reads and rewrites the whole history, so it is not a cheaper substitute for a clean break.
2. **Figma screenshots.** Each image costs roughly 1.5–2k tokens and stays in the transcript for the rest of the session. Verify geometry with numeric queries first, and capture screenshots at meaningful checkpoints rather than after every change. When a tool suggests screenshot loops, keep them to the minimum needed to judge the result.
3. **Broad Figma reads.** `figma_get_file_data` on a whole file returns a very large JSON payload. Query specific node IDs, pages, or sections. Save large REST responses to a file and search them instead of reading them into the conversation.

Subagents are not free either: each starts a separate context and re-reads its inputs. Use one when work is self-contained or needs a parallel scan, and do small edits in the main session. See `model-selection` for switching models mid-session.
