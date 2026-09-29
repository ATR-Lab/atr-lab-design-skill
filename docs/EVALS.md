# Evaluations

How the skill was tested, what the results were, and how to re-run the tests after a change. Everything lives in
[`atr-lab-design-workspace/`](../atr-lab-design-workspace/).

## Method

The method follows Anthropic's skill-creator process. Five realistic lab requests (`evals/evals.json`) were each run
twice, by fresh Claude agents working independently:

- **with the skill:** the agent was told to read `atr-lab-design/SKILL.md` and follow it. It was not allowed to read
  `research/`, `build/` or `.claude/`, so it could only use what ships inside the skill.
- **without the skill (baseline):** the same prompt, with the lab's original files in `assets/`, web search and the
  general Anthropic pptx skill.

| # | Eval | What it asks for |
|---|---|---|
| 1 | `sponsor-intro-deck` | A 6-8 slide PowerPoint introducing the lab to a prospective industry sponsor |
| 2 | `nasa-quad-chart` | A NASA-format quad chart for a (fictional) haptics paper, with grant and program |
| 3 | `k12-instagram-post` | An Instagram image, caption and alt text for a middle school summer workshop |
| 4 | `flyer-brand-review` | Review and fix a student's flyer with about 18 planted brand defects |
| 5 | `vendobot-paper-announcement` | A LinkedIn post and a news blurb for the lab's HRI 2026 paper, without inventing results |

`grade.py` scores each run automatically. It checks:

- files and slide counts
- template layouts
- forbidden facts (`@atr_kent`, the wrong college, the old room and phone)
- fonts and type sizes
- NASA headings, DOI and acknowledgement
- image size and palette share
- AP time style
- lint errors from `brand_check.py`

A reviewer then added judgment assertions after looking at every render: invented claims, visual quality and
figure quality. The results are in each iteration's `benchmark.md` and `benchmark.json`.

## Results

| Iteration | Evals | With skill | Without skill | Delta |
|---|---|---|---|---|
| 1 | all 5 | **96%** (47/49) | 68% (33/49) | +29 points |
| 2 | 2 and 3 (after fixes) | **100%** (21/21) | 71% (15/21) | +29 points |

In iteration 1 a skill run took about 510 s and 210k tokens on average, against 495 s and 133k tokens without it.
The extra tokens are the references it reads.

**What the baselines got wrong:**

- They repeated the non-existent handle **@atr_kent**, the director's office room and phone as the lab's contact, and
  the wrong college and building. The flyer "fix" kept all of them.
- They presented the director's **career funding total** and pre-lab media counts as lab statistics.
- They used Arial or other non-brand fonts, blank layouts instead of the template, sub-14 pt slide text, "9 AM - 3 PM"
  instead of AP style, and shortened NASA's required headings.

**What the skill runs got wrong in iteration 1, and was fixed:**

- A NASA quad with a single result came out as a thin one-bar chart. Fix: `quad_chart.py` now has a big-number
  **callout** figure and warns on single-point charts and nearly empty panels.
- The K-12 Instagram card was correct but subdued, and its illustration looked detached. Fix: a new gold
  **`outreach`** template, with the illustration standing on a "stage".
- Copy could not be linted directly. Fix: `brand_check.py` now reads `.md` and `.txt`, including serial-comma,
  "KSU", "&" and naming rules.
- Smaller fixes: alt-text guidance (key message first, no hard character cap claimed), a stale "4:3 quad variant"
  reference, a hint for underfilled slides in `new_deck.py`, and AP month style in the quad examples.

## Re-running

1. Create `iteration-N/eval-<name>/{with_skill,without_skill}/run-1/outputs/` for each eval and copy
   `eval_metadata.json` from iteration 1.
2. Run each prompt with a fresh agent in each configuration, as described above. Save `timing.json` (tokens and
   duration) next to `outputs/`.
3. Grade: `python atr-lab-design-workspace/grade.py atr-lab-design-workspace/iteration-N`. Add judgment
   assertions to `grading.json` with `"judgment": true` after looking at the renders.
4. Aggregate and review with the skill-creator tools: `python -m scripts.aggregate_benchmark <iteration dir>
   --skill-name atr-lab-design`, then `eval-viewer/generate_review.py <iteration dir> --static review.html`
   (add `--previous-workspace` to compare iterations).
