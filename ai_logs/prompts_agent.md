
# prompts_agent.md

Note: The content below is a simulated "vibe coding" log and model thinking summary for demonstration purposes. It is a human-curated example and NOT an actual GPT-5.1 raw output or private model log. Please label it as "example/simulated" when presenting externally.

## Prompt (Example)

You are the VibeBuyer AI Solution Architect. Goal: given a natural language user requirement and a product catalog, select a compatible Starter Stack of 1-3 items with strong cost/ROI characteristics. Output strict JSON fields: `thought_process`, `stack_name`, `selected_ids`, `roi_analysis`, `total_vibe_score`. Language can be `en|zh|ja`.

## Simulated GPT-style Thinking (Summary)

- Identify user goal: fast SaaS MVP focused on Auth, DB, deployment and basic analytics.
- Filter rules: prefer ecosystem compatibility (Next.js/React + Supabase/Vercel) and budget sensitivity (lower monthly cost preferred).
- Candidate scoring: rank by `vibe_score`, ecosystem fit, and monthly cost to estimate ROI.
- Example stack composition: `[Vercel Pro (id=1), Supabase Managed Tier (id=9), Mixpanel Starter (id=19)]`.

## Simulated Output (Example JSON)

```json
{
  "thought_process": "User needs a fast-to-launch MVP; prefer low maintenance cost and strong ecosystem compatibility. Vercel + Supabase + Mixpanel covers deployment, backend, and product analytics with reasonable cost and fast integration.",
  "stack_name": "Lean SaaS Starter Kit",
  "selected_ids": [1, 9, 19],
  "roi_analysis": "Saves ~40 developer-hours for integration and setup; monthly operational costs are modest, suitable for early PMF validation.",
  "total_vibe_score": 28.1
}
```

## Notes

- This file is intended as an illustrative artifact supporting `agent.py` behavior. Replace with real LLM logs and timestamps for production auditing.
