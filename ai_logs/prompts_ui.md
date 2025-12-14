
# prompts_ui.md

Note: The content below is a simulated UI copy and "vibe coding" interaction log, provided as an example (not an actual LLM raw stream). Label as "example/simulated" when showing externally.

## Prompt (Example)

You are a frontend copy and interaction assistant. Produce multilingual copy for the Streamlit UI: hero text, button labels, input placeholders, and post-generation states (progress, success). Output language should respect user choice `en|zh|ja`.

## Simulated UI Thinking (Summary)

- Goal: Keep messaging concise and value-focused (time saved, low cost, on-chain verifiability).
- Key copy rules: hero lines should be short and action-oriented; primary buttons should clearly state actions (e.g., "Generate Stack ⚡", "Purchase All"); success feedback should include BscScan links and an optional verification screenshot.

## Example Snippets

- Hero (EN): "Build Faster. Procure Smarter."  
- Button (ZH example mapping): "一键购买全套" (displayed when language is Chinese)
- Success message: show `Transaction Complete!` with a BscScan link and a thumbnail for `success_verify.png`.

## Notes

- Map these example strings into the `UI_TEXT` constant; for production, externalize to an i18n resource file.
