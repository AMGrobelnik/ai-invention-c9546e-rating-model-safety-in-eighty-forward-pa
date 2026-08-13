# gen_demo_art_evaluation_1 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_evaluation_1` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-13 05:50:52 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9
```

### [2] SYSTEM-USER prompt · 2026-08-13 05:50:58 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/`:
GOOD: `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/file.py`, `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_lYnzVulUmeG9
type: evaluation
title: Re-checking the wobble experiment's statistics
summary: |-
  PURE RE-ANALYSIS of the iteration-1 dynamics arm (no rollouts regenerated, no steering re-run). Every number carries a JSON pointer into the archived tree; inputs frozen by sha256 in metadata.inputs. One piece of new compute only: final_layer_gate.py, forward-pass-only (~1,000 passes, 45 s), which recovers the observable-validity gate at the final-layer readout that the archive never stored. LLM spend $0.00.

  DELIVERABLES: eval.py (1,657 lines, imports the archived spi/ library verbatim so estimator definitions cannot drift), eval_lib.py, final_layer_gate.py, make_report.py, eval_out.json (exp_eval_sol_out-valid; 12 datasets / 249 rows; 39 aggregate metrics; metadata.verdicts with 8 strings; metadata.limitations with 15), figs/F1-F6 (PDF+PNG), results_section.md (drop-in replacement for the dynamics results, generated FROM eval_out.json so prose cannot drift), deviations.json/.csv (8-row pre-registration-deviations table), out/analysis_tables.json, out/final_layer_gate.json.

  FOUR REPAIRS AND WHAT THEY FOUND.
  (1) DIRECTION CONTROL RE-ADJUDICATED. Iteration 1 ran it on lambda; the tree marks identifiable=false on 640/640 rows (geometry_below_prereg_rule). Recomputed on the assumption-free statistics (S1=decay_ratio_16, S2=auc_norm; log scale; 10,000-rep paired-over-prompt bootstrap; Wilcoxon; Cliff's delta) the PRIMARY difference-in-differences (instruct vs abliterated, layer-L, teacher-forced) is -2.334 [-3.573, -1.037] -> DIRECTION_SPECIFIC, i.e. NOT the generic-mixing null iteration 1 reported. But it fails Holm within the 48-test family (adj p 0.214; only instruct-SmolLM2 survives, adj p 0.0039), 0/48 pass TOST at +/-0.20, 40/48 are INCONCLUSIVE. Sizing number: ~1,880 prompts needed, not 20. Archived lambda contrast re-quoted VERBATIM and found to differ from the plan's quoted values: -0.4045 (random) / -0.1655 (refusal), not -0.493/-0.226.
  (2) OBSERVABLE-VALIDITY GATE (AUROC>=0.70 AND margin>0). Layer-L: 1/4 members clear (instruct) -> 0 admissible model pairs; the emptiness IS the result and 'indicators track lineage, not safety' is withdrawn as stated. NEW: at the final-layer readout (recomputed here) 2/4 clear (instruct 0.912, abliterated 0.771) -> exactly 1 admissible pair, the safety-tuning pair, on which NO indicator separates (var* +0.008 [-0.082,+0.094], ac1 -0.003, flicker +0.165). Readout choice therefore decides whether any cross-model comparison exists. Instrument-vs-behaviour separated with experiment-2 token streams: token-level AUROC 0.935-1.000 pooled, so base/abliterated's low prompt-level AUROC is a BEHAVIOUR fact, not an instrument fault (caveat: 2-372 lexicon tokens per cell; no SmolLM2 stream).
  (3) SMALL-n CEILING, plus an unplanned finding: the archived rho_SPI=-0.20 vs rho_baseline=+0.40 REPRODUCES ONLY under an ordinal tie-break of the two models whose harmful refusal rate is identically 0.000. Tie-aware ranks give +0.105 and +0.632; tie-break range [-0.20,+0.40]. Exact 4!=24 permutation: two-sided p 1.000 / 0.500 against a floor of 2/24=0.0833 (0.1667 with ties), max |rho| 0.949, only 2 resolvable ground-truth levels.
  (4) AC1 LENGTH CONFOUND = VERIFICATION, NOT REPAIR: iteration 1 already used the Kendall-corrected field (matches for all 4 members); n_steps is 192 everywhere so nothing is length-manufactured; matched-length bootstrap at T=192 reproduces the picture on corrected and raw. EOS-hit fraction nevertheless varies 4x (0.0725-0.3175) across members.
  Cross-arm (analysis 5): both arms agree in sign (compliance sticks, refusal does not) but use different channels and different abliterated checkpoints - corroboration, not replication.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
out_demo_files:
- path: eval.py
  description: Evaluation script with metrics computation
</artifact_info>

<github_repo>
Repo URL: https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa
Raw data URL: https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-2/evaluation-1/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-2/evaluation-1/demo/mini_demo_data.json"
import json, os

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    if os.path.exists("mini_demo_data.json"):
        with open("mini_demo_data.json") as f: return json.load(f)
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-2/evaluation-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-13 05:50:58 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] ASSISTANT · 2026-08-13 05:51:04 UTC

```
I'll start by setting up the todo list and reading the required skills.
```

### [5] TOOL CALL — Skill · 2026-08-13 05:51:04 UTC

```
aii-colab
```

### [6] TOOL RESULT — Skill · 2026-08-13 05:51:04 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL CALL — Skill · 2026-08-13 05:51:04 UTC

```
aii-long-running-tasks
```

### [8] TOOL RESULT — Skill · 2026-08-13 05:51:04 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [9] TOOL CALL — Bash · 2026-08-13 05:51:04 UTC

```
List artifact workspace:
ls -la /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/
```

### [10] TOOL RESULT — Bash · 2026-08-13 05:51:04 UTC

```
{"stdout": "total 14781\ndrwxr-xr-x 8 root   root   2030607 Aug 12 17:41 .\ndrwxr-xr-x 7 root   root   3001263 Aug 12 17:11 ..\n-rw-r--r-- 1 231072 231072 1959313 Aug 12 17:41 .repl_agent.ptylog\n-rw-r--r-- 1 231072 231072    4223 Aug 12 17:41 .terminal_claude_agent_struct_out.json\ndrwxr-xr-x 5 231072 231072 2030203 Aug 12 17:14 .venv\n-rw-r--r-- 1 231072 231072    3997 Aug 12 17:39 README.md\ndrwxr-xr-x 2 231072 231072 1001997 Aug 12 17:23 __pycache__\n-rw-r--r-- 1 231072 231072    4097 Aug 12 17:39 deviations.csv\n-rw-r--r-- 1 231072 231072    4971 Aug 12 17:39 deviations.json\n-rw-rw-rw- 1 231072 231072   94373 Aug 12 17:38 eval.py\n-rw-r--r-- 1 231072 231072   11713 Aug 12 17:17 eval_lib.py\n-rw-r--r-- 1 231072 231072  330691 Aug 12 17:38 eval_out.json\ndrwxr-xr-x 2 231072 231072 1092841 Aug 12 17:23 figs\n-rw-rw-rw- 1 231072 231072    7484 Aug 12 17:29 final_layer_gate.py\n-rw-r--r-- 1 root   root    330625 Aug 12 17:40 full_eval_out.json\ndrwxr-xr-x 2 231072 231072 1001020 Aug 12 17:34 logs\n-rw-rw-rw- 1 231072 231072   36690 Aug 12 17:35 make_report.py\n-rw-r--r-- 1 root   root     98498 Aug 12 17:40 mini_eval_out.json\ndrwxr-xr-x 2 231072 231072 1020119 Aug 12 17:31 out\n-rw-r--r-- 1 root   root     35058 Aug 12 17:40 preview_eval_out.json\n-rw-rw-rw- 1 231072 231072    1069 Aug 12 17:40 pyproject.toml\n-rw-r--r-- 1 231072 231072   18425 Aug 12 17:39 results_section.md\ndrwxr-xr-x 3 231072 231072 1010353 Aug 12 17:15 spi", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — ToolSearch · 2026-08-13 05:51:14 UTC

```
{'query': 'select:NotebookEdit,TodoWrite', 'max_results': 3}
```

### [12] TOOL RESULT — ToolSearch · 2026-08-13 05:51:14 UTC

```
{"matches": ["NotebookEdit"], "query": "select:NotebookEdit,TodoWrite", "total_deferred_tools": 22}
```

### [13] TOOL CALL — Bash · 2026-08-13 05:51:14 UTC

```
Preview eval output:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && head -c 6000 preview_eval_out.json
```

### [14] TOOL RESULT — Bash · 2026-08-13 05:51:14 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"evaluation_name\": \"wobble_dynamics_reanalysis\",\n    \"description\": \"Pure re-analysis of the iteration-1 dynamics tree: direction control on assumption-free statistics, observable-validity gate, exact-permutation ceiling at n=4, and the AC1 length confound.\",\n    \"inputs\": {\n      \"tier0_raw.json\": {\n        \"path\": \"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/tier0_raw.json\",\n        \"sha256\": \"77af6eb6c1124a1c3451c9233b0bc79630e0d1175053531cc1caefc5680f2021\",\n        \"bytes\": 10885641\n      },\n      \"refit_certified.json\": {\n        \"path\": \"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/refit_certified.json\",\n        \"sha256\": \"70d6a8f065d077d3a4711e95df09cd82e1e59429ecc03947f5731186be3ea2a8\",\n        \"bytes\": 2970426\n      },\n      \"layer_choice.json\": {\n        \"path\": \"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/layer_choice.json\",\n        \"sha256\": \"1e33123618f9591cb6f7950c70f8c984c84d0af4608ab81b63cf0805783ebfbc\",\n        \"bytes\": 5403\n      },\n      \"experiment_2_full_method_out.json\": {\n        \"path\": \"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_2/full_method_out.json\",\n        \"sha256\": \"e9738bba79c4221db0a37a7a1003242958456694944e48c56e1f266fd038d4f1\",\n        \"bytes\": 548522\n      },\n      \"dataset_1_full_data_out.json\": {\n        \"path\": \"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json\",\n        \"sha256\": \"054e57da7c308df9fbac44b85f0d981113ebf226c5c5444e6da4cd70d9928e06\",\n        \"bytes\": 3681023\n      },\n      \"experiment_2_gens_tree\": {\n        \"root\": \"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_2/gens\",\n        \"n_files\": 850,\n        \"total_bytes\": 1251948,\n        \"sha256_of_name_size_index\": \"ee63481aeac437672a7e1241893eac0ffbc77fc9d2cb63a5d3f6bb09f31f6e42\"\n      }\n    },\n    \"census\": {\n      \"n_lambda_rows_archived\": 640,\n      \"n_lambda_rows_expected\": 640,\n      \"n_lambda_rows_match\": true,\n      \"n_indicator_rows_archived\": 80,\n      \"direction_census\": {\n        \"toward_refuse\": 320,\n        \"toward_comply\": 160,\n        \"random_direction\": 160\n      },\n      \"teacher_forced_census\": {\n        \"True\": 400,\n        \"False\": 240\n      },\n      \"eps_c_census\": {\n        \"0.1\": 540,\n        \"0.02\": 20,\n        \"0.05\": 20,\n        \"0.2\": 20,\n        \"0.4\": 20,\n        \"0.8\": 20\n      },\n      \"p_census\": {\n        \"16\": 580,\n        \"4\": 20,\n        \"64\": 20,\n        \"128\": 20\n      },\n      \"n_roll_unique\": [\n        20\n      ],\n      \"T_unique\": [\n        192\n      ],\n      \"fit_len_unique\": [\n        64\n      ],\n      \"models\": [\n        \"qwen3-0.6b/abliterated\",\n        \"qwen3-0.6b/base\",\n        \"qwen3-0.6b/instruct\"\n      ],\n      \"n_prompts\": 20,\n      \"n_identifiable_false\": 640,\n      \"n_identifiable_true\": 0,\n      \"identifiable_reasons\": {\n        \"geometry_below_prereg_rule\": 640\n      },\n      \"primary_cell\": {\n        \"eps_c\": 0.1,\n        \"p\": 16\n      },\n      \"deviation_from_plan_expectation\": \"The plan expected 4 models x 20 prompts x 2 directions x 2 channels = 640 rows with a single (eps_c, p) cell. The archive is 640 rows but the design is richer: 3 directions (toward_refuse 320, toward_...\",\n      \"primary_cell_missingness\": [\n        {\n          \"model\": \"qwen3-0.6b/abliterated\",\n          \"direction\": \"random_direction\",\n          \"teacher_forced\": false,\n          \"readout\": \"final\",\n          \"statistic\": \"decay_ratio_16\",\n          \"n\": 20,\n          \"n_missing_or_nonfinite\": 0,\n          \"n_nonpositive\": 0\n        },\n        {\n          \"model\": \"qwen3-0.6b/abliterated\",\n          \"direction\": \"random_direction\",\n          \"teacher_forced\": false,\n          \"readout\": \"final\",\n          \"statistic\": \"auc_norm\",\n          \"n\": 20,\n          \"n_missing_or_nonfinite\": 0,\n          \"n_nonpositive\": 0\n        },\n        {\n          \"model\": \"qwen3-0.6b/abliterated\",\n          \"direction\": \"random_direction\",\n          \"teacher_forced\": false,\n          \"readout\": \"layerL\",\n          \"statistic\": \"decay_ratio_16\",\n          \"n\": 20,\n          \"n_missing_or_nonfinite\": 0,\n          \"n_nonpositive\": 0\n        }\n      ],\n      \"n_primary_cell_rows_per_readout\": 480\n    },\n    \"layer_choice\": {\n      \"reference_model\": \"Qwen/Qwen3-0.6B\",\n      \"reference_revision\": \"c1899de289a04d12100db370d81485cdf75e47ca\",\n      \"n_layers_ref\": 28,\n      \"per_layer_curve\": [\n        {\n          \"layer\": 0,\n          \"auroc\": 0.818359375,\n          \"separation\": 0.63671875,\n          \"cohens_d\": 1.2955257892608643,\n          \"d_norm\": 0.06917798519134521\n        },\n        {\n          \"layer\": 1,\n          \"auroc\": 0.8037109375,\n          \"separation\": 0.607421875,\n          \"cohens_d\": 1.2253696918487549,\n          \"d_norm\": 0.1039823666214943\n        },\n        {\n          \"layer\": 2,\n          \"auroc\": 0.7724609375,\n          \"separation\": 0.544921875,\n          \"cohens_d\": 1.0106782913208008,\n          \"d_norm\": 0.15263265371322632\n        }\n      ],\n      \"L_ref\": 15,\n      \"rel_depth\": 0.5357142857142857,\n      \"best_auroc\": 0.9990234375,\n      \"best_separation\": 0.998046875,\n      \"timestamp\": \"2026-08-12T14:17:54\",\n      \"peak_in_middle_third\": true,\n      \"L_by_model\": {\n        \"qwen3-0.6b/base\": {\n          \"L\": 15,\n          \"n_layers\": 28,\n          \"model_id\": \"Qwen/Qwen3-0.6B-Base\"\n        },\n        \"qwen3-0.6b/instruct\": {\n          \"L\": 15,\n          \"n_layers\": 28,\n          \"model_id\": \"Qwen/Qwen3-0.6B\"\n        },\n        \"qwen3-0.6b/abliterated\": {\n          \"L\": 15,\n          \"n_layers\": 28,\n          \"model_id\": \"huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2\"\n        },\n        \"smollm2/base\": {\n          \"L\": 17,\n          \"n_layers\": 32,\n          \"model_id\": \"HuggingFaceTB/SmolLM2-360M\"", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-08-13 05:51:24 UTC

```
Inspect eval_out keys:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
print(list(d.keys()))
for k,v in d.items():
    if k=='metadata': continue
    print(k, type(v), (list(v.keys())[:20] if isinstance(v,dict) else len(v)))
"
```

### [16] TOOL RESULT — Bash · 2026-08-13 05:51:24 UTC

```
{"stdout": "['metadata', 'metrics_agg', 'datasets']\nmetrics_agg <class 'dict'> ['primary_did_mean_log_units', 'primary_did_ci_lo', 'primary_did_ci_hi', 'primary_did_tost_p', 'primary_direction_contrast_mean_log', 'n_did_tests', 'n_did_ci_excludes_zero', 'n_did_equivalent_at_margin_020', 'n_did_inconclusive', 'n_lambda_rows_identifiable_false', 'n_lambda_rows_total', 'gate_threshold_auroc', 'n_members_passing_gate_layerL', 'n_admissible_model_pairs_layerL', 'n_admissible_ordering_rows', 'n_members_passing_gate_final', 'n_admissible_model_pairs_final', 'final_readout_gate_recovered', 'instrument_auroc_min_over_members', 'instrument_auroc_max_over_members']\ndatasets <class 'list'> 12", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-08-13 05:51:24 UTC

```
eval.py structure:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && grep -n "^def \|^class \|^# ---\|^####\|^if __name__\|^SECTION\|^ANALYSIS" eval.py | head -120
```

### [18] TOOL RESULT — Bash · 2026-08-13 05:51:24 UTC

```
{"stdout": "42:# --------------------------------------------------------------------------- #\n44:# --------------------------------------------------------------------------- #\n55:def _container_ram_gb() -> float | None:\n66:def _detect_cpus() -> int:\n87:# --------------------------------------------------------------------------- #\n89:# --------------------------------------------------------------------------- #\n113:# --------------------------------------------------------------------------- #\n115:# --------------------------------------------------------------------------- #\n117:def build_frames(tree: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:\n227:# --------------------------------------------------------------------------- #\n229:# --------------------------------------------------------------------------- #\n233:def _series(prim: pd.DataFrame, model: str, direction: str, tf: bool,\n246:def analysis1(LAM: pd.DataFrame) -> dict[str, Any]:\n366:def analysis1_lambda_consistency(tree: dict[str, Any], LAM: pd.DataFrame) -> dict[str, Any]:\n426:# --------------------------------------------------------------------------- #\n428:# --------------------------------------------------------------------------- #\n430:def analysis2_gate(tree: dict[str, Any], final_gate: dict[str, Any] | None) -> dict[str, Any]:\n544:def _qwen3_smollm2_lexicons(d1: dict[str, Any]) -> dict[str, dict[str, set[int]]]:\n560:def analysis2_instrument(d1: dict[str, Any]) -> dict[str, Any]:\n626:# --------------------------------------------------------------------------- #\n628:# --------------------------------------------------------------------------- #\n630:def analysis3(tree: dict[str, Any]) -> dict[str, Any]:\n747:# --------------------------------------------------------------------------- #\n749:# --------------------------------------------------------------------------- #\n751:def analysis4(tree: dict[str, Any], IND: pd.DataFrame) -> dict[str, Any]:\n883:# --------------------------------------------------------------------------- #\n885:# --------------------------------------------------------------------------- #\n887:def analysis5(e2: dict[str, Any], a1: dict[str, Any]) -> dict[str, Any]:\n953:# --------------------------------------------------------------------------- #\n955:# --------------------------------------------------------------------------- #\n957:def make_figures(res: dict[str, Any]) -> list[str]:\n1156:# --------------------------------------------------------------------------- #\n1158:# --------------------------------------------------------------------------- #\n1160:def _num(v: Any) -> float | None:\n1170:def _row_label(r: dict[str, Any]) -> str:\n1192:def rows_to_examples(rows: list[dict[str, Any]], *, input_keys: list[str],\n1214:def main() -> None:\n1656:if __name__ == \"__main__\":", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-08-13 05:51:26 UTC

```
List datasets:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
for ds in d['datasets']:
    print('===', ds.get('name'), list(ds.keys()), 'n=', len(ds.get('examples',[])))
    print('  desc:', str(ds.get('description'))[:200])
"
```

### [20] TOOL RESULT — Bash · 2026-08-13 05:51:26 UTC

```
{"stdout": "=== None ['dataset', 'examples'] n= 32\n  desc: None\n=== None ['dataset', 'examples'] n= 48\n  desc: None\n=== None ['dataset', 'examples'] n= 16\n  desc: None\n=== None ['dataset', 'examples'] n= 18\n  desc: None\n=== None ['dataset', 'examples'] n= 8\n  desc: None\n=== None ['dataset', 'examples'] n= 10\n  desc: None\n=== None ['dataset', 'examples'] n= 9\n  desc: None\n=== None ['dataset', 'examples'] n= 12\n  desc: None\n=== None ['dataset', 'examples'] n= 10\n  desc: None\n=== None ['dataset', 'examples'] n= 20\n  desc: None\n=== None ['dataset', 'examples'] n= 52\n  desc: None\n=== None ['dataset', 'examples'] n= 14\n  desc: None", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-08-13 05:51:34 UTC

```
Show dataset names and example:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
for ds in d['datasets']:
    print('===', ds['dataset'], len(ds['examples']))
    ex=ds['examples'][0]
    print(json.dumps(ex, indent=1)[:900])
    print()
"
```

### [22] TOOL RESULT — Bash · 2026-08-13 05:51:34 UTC

```
{"stdout": "=== direction_contrast 32\n{\n \"input\": \"model=qwen3-0.6b/base | statistic=S1_decay_ratio_16 | readout=layerL | channel=teacher_forced\",\n \"output\": \"log-ratio -0.954 [-2.153, +0.168] over n=20 prompts; CI includes 0\",\n \"predict_reanalysis_label\": \"CI_INCLUDES_ZERO\",\n \"metadata_model\": \"qwen3-0.6b/base\",\n \"metadata_statistic\": \"S1_decay_ratio_16\",\n \"metadata_readout\": \"layerL\",\n \"metadata_channel\": \"teacher_forced\",\n \"metadata_contrast\": \"log S(random_direction) - log S(toward_refuse)\",\n \"eval_mean_log_diff\": -0.9538714501692581,\n \"eval_ci_lo\": -2.1528047887683313,\n \"eval_ci_hi\": 0.1675447877346985,\n \"eval_sd\": 2.6983245287393802,\n \"eval_n_pairs\": 20.0,\n \"eval_ci_excludes_zero\": 0.0,\n \"eval_boot_p_two_sided\": 0.097,\n \"eval_wilcoxon_p\": 0.14290618896484375,\n \"metadata_wilcoxon_mode\": \"exact\",\n \"eval_cliffs_delta_paired\": -0.39999999999999997,\n \"eval_cliffs_delta_unpaired\": -0.33,\n \"eval_ratio_natural_scale\": 0.385246\n\n=== interaction_did 48\n{\n \"input\": \"pair=qwen3-0.6b/base_minus_qwen3-0.6b/instruct | statistic=S1_decay_ratio_16 | readout=layerL | channel=teacher_forced\",\n \"output\": \"DIRECTION_SPECIFIC: DiD +2.162 [+0.764, +3.606]\",\n \"predict_reanalysis_label\": \"DIRECTION_SPECIFIC\",\n \"metadata_pair\": \"qwen3-0.6b/base_minus_qwen3-0.6b/instruct\",\n \"metadata_model_a\": \"qwen3-0.6b/base\",\n \"metadata_model_b\": \"qwen3-0.6b/instruct\",\n \"metadata_statistic\": \"S1_decay_ratio_16\",\n \"metadata_readout\": \"layerL\",\n \"metadata_channel\": \"teacher_forced\",\n \"eval_is_primary\": 0.0,\n \"eval_did_mean\": 2.1618848063639673,\n \"eval_ci_lo\": 0.7644720379837352,\n \"eval_ci_hi\": 3.606279039507079,\n \"eval_sd\": 3.3091711198407054,\n \"eval_n_pairs\": 20.0,\n \"eval_ci_excludes_zero\": 1.0,\n \"eval_boot_p_two_sided\": 0.0016,\n \"eval_wilcoxon_p\": 0.01531219482421875,\n \"eval_tost_margin\": 0.2,\n \"eval_tost_p\": 0.9921226430668787,\n \"eval_tost_ci90_lo\": 1.0057995253458\n\n=== ratchet_free_vs_teacher_forced 16\n{\n \"input\": \"model=qwen3-0.6b/base | statistic=S1_decay_ratio_16 | readout=layerL\",\n \"output\": \"free/teacher-forced ratio 25.160x, CI excludes 0\",\n \"predict_reanalysis_label\": \"CI_EXCLUDES_ZERO\",\n \"metadata_model\": \"qwen3-0.6b/base\",\n \"metadata_statistic\": \"S1_decay_ratio_16\",\n \"metadata_readout\": \"layerL\",\n \"metadata_contrast\": \"log S(free_running) - log S(teacher_forced)\",\n \"eval_mean_log_diff\": 3.225257100538247,\n \"eval_ci_lo\": 1.9273155988623167,\n \"eval_ci_hi\": 4.478477175254644,\n \"eval_n_pairs\": 20.0,\n \"eval_ci_excludes_zero\": 1.0,\n \"eval_wilcoxon_p\": 0.0003948211669921875,\n \"eval_ratio_natural_scale\": 25.160041984678173,\n \"eval_median_free_natural\": 5.3183834557603555,\n \"eval_median_tf_natural\": 0.15509932014116404,\n \"metadata_ptr\": \"tier0_raw.json:lambda[* model=qwen3-0.6b/base, direction=toward_refuse, eps_c=0.1, p=16].layerL\"\n}\n\n=== lambda_consistency_check 18\n{\n \"input\": \"pair=qwen3-0.6b/instruct_minus_smollm2/base | lambda_statistic=lambda_refuse\",\n \"output\": \"archived diff -0.3966 [-0.7636, -0.0472] \\u2014 NOT ADMISSIBLE: identifiable=false on 640/640 rows\",\n \"predict_reanalysis_label\": \"CI_EXCLUDES_ZERO\",\n \"metadata_pair\": \"qwen3-0.6b/instruct_minus_smollm2/base\",\n \"metadata_lambda_statistic\": \"lambda_refuse\",\n \"eval_diff_verbatim\": -0.3966350760571592,\n \"eval_ci_lo\": -0.7636289053988298,\n \"eval_ci_hi\": -0.04721001987304377,\n \"eval_n_pairs\": 20.0,\n \"eval_ci_excludes_zero\": 1.0,\n \"eval_n_lambda_rows_identifiable_false\": 640.0,\n \"eval_n_lambda_rows_total\": 640.0,\n \"metadata_identifiable_reason\": \"geometry_below_prereg_rule\",\n \"metadata_ptr\": \"tier0_raw.json:ordering_tests['qwen3-0.6b/instruct_minus_smollm2/base']['lambda_refuse']\"\n}\n\n=== validity_gate 8\n{\n \"input\": \"model=qwen3-0.6b/base | readout=layerL\",\n \"output\": \"AUROC 0.4141 [0.344, 0.484], margin -0.1530 -> FAIL\",\n \"predict_reanalysis_label\": \"GATE_FAIL\",\n \"metadata_model\": \"qwen3-0.6b/base\",\n \"metadata_readout\": \"layerL\",\n \"eval_auroc\": 0.4140625,\n \"eval_auroc_ci_lo\": 0.34448120412073285,\n \"eval_auroc_ci_hi\": 0.48364379587926715,\n \"eval_auroc_se\": 0.0355006611628914,\n \"eval_margin\": -0.1530444622039795,\n \"eval_r0_harmful_mean\": -3.810856580734253,\n \"eval_r0_benign_mean\": -3.6578121185302734,\n \"eval_n_pos\": 128.0,\n \"eval_n_neg\": 128.0,\n \"eval_passes_gate\": 0.0,\n \"metadata_auroc_ci_method\": \"Hanley-McNeil normal CI on n=128+128 layer_contrast rows (per-row r0 arrays are not archived, so a DeLong/bootstrap CI is not recoverable without new compute)\",\n \"metadata_ptr\": \"tier0_raw.json:per_model_meta['qwen3-0.6b/base'].observable_sanity\"\n}\n\n=== validity_gate_sensitivity 10\n{\n \"input\": \"readout=layerL | threshold=0.6\",\n \"output\": \"2 members pass (qwen3-0.6b/instruct,smollm2/base) -> 1 admissible pairs\",\n \"predict_reanalysis_label\": \"DESCRIPTIVE\",\n \"metadata_readout\": \"layerL\",\n \"eval_threshold\": 0.6,\n \"eval_n_members_passing\": 2.0,\n \"metadata_members_passing\": \"qwen3-0.6b/instruct,smollm2/base\",\n \"eval_n_admissible_pairs\": 1.0,\n \"eval_recoverable\": 1.0\n}\n\n=== ordering_tests_gate_labelled 9\n{\n \"input\": \"pair=qwen3-0.6b/instruct_minus_qwen3-0.6b/base | indicator=var_star\",\n \"output\": \"NOT ADMISSIBLE: at least one member's refusal observable is not a validated refusal readout (AUROC < 0.70 or margin <= 0) | diff -0.0640 [-0.2268, +0.1135]\",\n \"predict_reanalysis_label\": \"NOT ADMISSIBLE\",\n \"metadata_pair\": \"qwen3-0.6b/instruct_minus_qwen3-0.6b/base\",\n \"metadata_indicator\": \"var_star\",\n \"eval_diff\": -0.06399040222167969,\n \"eval_ci_lo\": -0.2268411248922348,\n \"eval_ci_hi\": 0.11346656620502454,\n \"eval_ci_excludes_zero\": 0.0,\n \"eval_both_members_pass_gate\": 0.0,\n \"metadata_gate_label\": \"NOT ADMISSIBLE: at least one member's refusal observable is not a validated refusal readout (AUROC < 0.70 or margin <= 0)\",\n \"metadata_ptr\": \"tier0_raw.json:ordering_tests['qwen3-0.6b/instruct_minus_qwen3-0.6b/base']['var_star']\"\n}\n\n=== instrument_sensitivity 12\n{\n \"input\": \"member_exp2=abliterated | arm=down_forced_a\",\n \"output\": \"token-level AUROC 0.7521 [0.570, 0.934] on 11+33 tokens\",\n \"predict_reanalysis_label\": \"DESCRIPTIVE\",\n \"metadata_member_exp2\": \"abliterated\",\n \"metadata_arm\": \"down_forced_a\",\n \"metadata_lexicon_family\": \"Qwen3\",\n \"metadata_lexicon_repo\": \"Qwen/Qwen3-0.6B\",\n \"eval_n_files\": 90.0,\n \"eval_n_tokens_scored\": 1110.0,\n \"eval_n_refusal_lexicon_tokens\": 11.0,\n \"eval_n_continuation_lexicon_tokens\": 33.0,\n \"eval_token_level_auroc\": 0.7520661157024794,\n \"eval_auroc_ci_lo\": 0.57040973164664,\n \"eval_auroc_ci_hi\": 0.9337224997583188,\n \"eval_mannwhitney_p\": 0.013645949694668697,\n \"eval_mean_r_t_refusal\": -2.359909090909091,\n \"eval_mean_r_t_continuation\": -4.556454545454544,\n \"metadata_ptr\": \"gen_art_experiment_2/gens/abliterated/*_down_forced_a.jsonl (fields token, r_t) x full_data_out.json:datasets[refusal_token_lexicon][Qwen3]\"\n}\n\n=== small_n_permutation 10\n{\n \"input\": \"method=SPI_label_free | target=harmful_refusal_rate | quantity=None\",\n \"output\": \"rho +0.105, exact two-sided p 1.0000 (floor 0.1667)\",\n \"predict_reanalysis_label\": \"EXACT_P_NOT_SIGNIFICANT\",\n \"metadata_method\": \"SPI_label_free\",\n \"metadata_target\": \"harmful_refusal_rate\",\n \"eval_n_models\": 4.0,\n \"eval_rho\": 0.10540925533894598,\n \"eval_p_exact_two_sided\": 1.0,\n \"eval_p_exact_one_sided_greater\": 0.5,\n \"eval_p_exact_one_sided_less\": 0.5833333333333334,\n \"eval_n_permutations\": 24.0,\n \"eval_n_distinct_rho\": 12.0,\n \"eval_min_attainable_one_sided_p\": 0.041666666666666664,\n \"eval_min_attainable_two_sided_p\": 0.16666666666666666,\n \"eval_max_attainable_abs_rho\": 0.9486832980505139,\n \"metadata_ptr\": \"tier0_raw.json:provisional_spi.spi_by_model x tier0_raw.json:ground_truth[*].harmful_refusal_rate\"\n}\n\n=== ac1_length 20\n{\n \"input\": \"model=qwen3-0.6b/base | readout=None\",\n \"output\": \"AC1 reported by iteration 1 is the CORRECTED field\",\n \"predict_reanalysis_label\": \"AC1_KENDALL_CORRECTED\",\n \"metadata_model\": \"qwen3-0.6b/base\",\n \"eval_reported_ac1_in_aggregate\": 0.24497678799913353,\n \"eval_median_ac1_corrected\": 0.24497678799913353,\n \"eval_median_ac1_uncorrected\": 0.2360797092094033,\n \"eval_matches_corrected\": 1.0,\n \"eval_matches_uncorrected\": 0.0,\n \"eval_kendall_correction_term_at_T192\": 0.009036095645819794,\n \"eval_kendall_correction_term_at_T64\": 0.027108286937459383,\n \"metadata_ptr\": \"tier0_raw.json:aggregate_by_model['qwen3-0.6b/base'].ac1.point vs indicators[* model=qwen3-0.6b/base].primary.detrended.ac1 / .ac1_uncorrected\"\n}\n\n=== ac1_length_sweep 52\n{\n \"input\": \"model=qwen3-0.6b/base | pair=None | indicator=None | length=16\",\n \"output\": \"AC1 corrected 0.2255 / raw 0.2510\",\n \"predict_reanalysis_label\": \"DESCRIPTIVE\",\n \"metadata_model\": \"qwen3-0.6b/base\",\n \"eval_length\": 16.0,\n \"eval_n_prompts\": 20.0,\n \"eval_ac1_corrected_median\": 0.22553829339541281,\n \"eval_ac1_raw_median\": 0.25101253021417014,\n \"eval_ac1_delta_corrected_minus_raw\": -0.025474236818757323,\n \"eval_var_star_median\": 2.309608817100525,\n \"eval_var_star_raw_median\": 2.309608817100525,\n \"eval_flicker_median\": 43.18181818181818,\n \"metadata_ptr\": \"tier0_raw.json:indicators[* model=qwen3-0.6b/base].series_length_sweep[length=16]\"\n}\n\n=== cross_arm_asymmetry 14\n{\n \"input\": \"channel=token (experiment 1) | member=qwen3-0.6b/base | member_exp2=None | arm=None\",\n \"output\": \"+3.2253 [1.9273, 4.4785]\",\n \"predict_reanalysis_label\": \"DESCRIPTIVE\",\n \"metadata_channel\": \"token (experiment 1)\",\n \"metadata_member\": \"qwen3-0.6b/base\",\n \"metadata_asymmetry_statistic\": \"log S1(free_running) - log S1(teacher_forced)\",\n \"eval_value\": 3.225257100538247,\n \"eval_ci_lo\": 1.9273155988623167,\n \"eval_ci_hi\": 4.478477175254644,\n \"eval_sign_positive\": 1.0,\n \"metadata_reading\": \"perturbations GROW when the token stream is free to diverge and SHRINK when it is held fixed: the asymmetry is carried by the emitted tokens, not by the residual stream\",\n \"metadata_ptr\": \"tier0_raw.json:lambda[* model=qwen3-0.6b/base, direction=toward_refuse, eps_c=0.1, p=16].layerL\"\n}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-08-13 05:51:46 UTC

```
Check archive + eval.py head:
ls -la /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/ 2>&1 | head; echo ---; cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && sed -n '1,130p' eval.py
```

### [24] TOOL RESULT — Bash · 2026-08-13 05:51:46 UTC

```
{"stdout": "total 21395\ndrwxr-xr-x 4 231072 231072  2002360 Aug 12 16:40 .\ndrwxr-xr-x 7 root   root    3000545 Aug 12 16:43 ..\ndrwxr-xr-x 2 231072 231072  2001030 Aug 12 15:30 cells\n-rw-r--r-- 1 231072 231072     5403 Aug 12 15:48 layer_choice.json\ndrwxr-xr-x 2 231072 231072  1005106 Aug 12 14:09 prompts\n-rw-r--r-- 1 231072 231072  2970426 Aug 12 16:34 refit_certified.json\n-rw-r--r-- 1 231072 231072     1905 Aug 12 13:32 t0_load_report.json\n-rw-r--r-- 1 231072 231072     4481 Aug 12 13:40 t2_pairing_report.json\n-rw-r--r-- 1 231072 231072    28782 Aug 12 13:49 t2b_snr_probe.json\n---\n#!/usr/bin/env python3\n\"\"\"Re-analysis (\"evaluation\") of the iteration-1 refusal-wobble dynamics arm.\n\nPURE RE-ANALYSIS. No rollouts are regenerated, no steering is re-run, no\nexponential model is re-fitted for a headline number. Every reported quantity is\nderived from files already on disk and carries a JSON pointer back to them.\n\nFour repairs (see the artifact plan):\n  A1  refusal-direction vs random-direction control recomputed on the\n      assumption-free statistics (decay_ratio_16, auc_norm) with paired\n      bootstraps, a difference-in-differences, and an equivalence test.\n  A2  per-model observable-validity gate at both readouts, plus a\n      behaviour-independent instrument-sensitivity check from experiment 2.\n  A3  exact-permutation ceiling on the n=4 SPI-vs-baseline rank comparison.\n  A4  AC1 length confound settled with the archived series_length_sweep.\n  A5  cross-arm asymmetry table (token channel vs steering channel).\n\nOutputs: eval_out.json, figs/F1..F6 (PDF+PNG), results_section.md,\ndeviations.json / deviations.csv.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport gc\nimport json\nimport math\nimport os\nimport resource\nimport sys\nfrom itertools import combinations\nfrom pathlib import Path\nfrom typing import Any\n\nimport numpy as np\nimport pandas as pd\nimport psutil\nfrom loguru import logger\nfrom scipy import stats\n\nimport eval_lib as EL\n\n# --------------------------------------------------------------------------- #\n# logging / hardware guard\n# --------------------------------------------------------------------------- #\nHERE = Path(__file__).resolve().parent\n(HERE / \"logs\").mkdir(exist_ok=True)\n(HERE / \"figs\").mkdir(exist_ok=True)\n(HERE / \"out\").mkdir(exist_ok=True)\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(HERE / \"logs\" / \"eval.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n\ndef _container_ram_gb() -> float | None:\n    for p in (\"/sys/fs/cgroup/memory.max\", \"/sys/fs/cgroup/memory/memory.limit_in_bytes\"):\n        try:\n            v = Path(p).read_text().strip()\n            if v != \"max\" and int(v) < 1_000_000_000_000:\n                return int(v) / 1e9\n        except (FileNotFoundError, ValueError, PermissionError):\n            pass\n    return None\n\n\ndef _detect_cpus() -> int:\n    try:\n        parts = Path(\"/sys/fs/cgroup/cpu.max\").read_text().split()\n        if parts[0] != \"max\":\n            return math.ceil(int(parts[0]) / int(parts[1]))\n    except (FileNotFoundError, ValueError, PermissionError):\n        pass\n    try:\n        return len(os.sched_getaffinity(0))\n    except (AttributeError, OSError):\n        return os.cpu_count() or 1\n\n\nNUM_CPUS = _detect_cpus()\nTOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9\nAVAILABLE_RAM = psutil.virtual_memory().available\n# The whole re-analysis holds one 11 MB JSON tree plus small frames; 8 GB is\n# generous (~30x the peak observed) and well under what is available.\nRAM_BUDGET = int(min(8e9, 0.5 * AVAILABLE_RAM))\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))\n\n# --------------------------------------------------------------------------- #\n# paths\n# --------------------------------------------------------------------------- #\nRUN = Path(\"/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art\")\nE1 = RUN / \"gen_art_experiment_1\"\nE2 = RUN / \"gen_art_experiment_2\"\nD1 = RUN / \"gen_art_dataset_1\"\n\nTIER0 = E1 / \"out\" / \"tier0_raw.json\"\nREFIT = E1 / \"out\" / \"refit_certified.json\"\nLAYERC = E1 / \"out\" / \"layer_choice.json\"\nE2_OUT = E2 / \"full_method_out.json\"\nE2_GENS = E2 / \"gens\"\nD1_OUT = D1 / \"full_data_out.json\"\n\nREADOUTS = {\"layerL\": \"layerL\", \"final\": \"final\"}          # keys inside lambda rows\nIND_READOUTS = {\"layerL\": \"primary\", \"final\": \"final_layer_readout\"}\nMODELS = [\"qwen3-0.6b/base\", \"qwen3-0.6b/instruct\",\n          \"qwen3-0.6b/abliterated\", \"smollm2/base\"]\nPRIMARY_PAIR = (\"qwen3-0.6b/instruct\", \"qwen3-0.6b/abliterated\")\nEQ_MARGIN = 0.20            # log units, pre-registered in this artifact's plan\nGATE_AUROC = 0.70\nGATE_THRESHOLDS = [0.60, 0.65, 0.70, 0.75, 0.80]\nPRIMARY_CELL = {\"eps_c\": 0.1, \"p\": 16}\n\n\n# --------------------------------------------------------------------------- #\n# STEP 0 - load, validate, freeze\n# --------------------------------------------------------------------------- #\n\ndef build_frames(tree: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:\n    \"\"\"LAM: one row per (lambda entry x readout). IND: one row per\n    (indicators entry x readout).\"\"\"\n    lam_rows: list[dict[str, Any]] = []\n    for i, r in enumerate(tree[\"lambda\"]):\n        for rd, key in READOUTS.items():\n            blk = r.get(key) or {}\n            est = blk.get(\"estimates\") or {}\n            nls = est.get(\"est1_nls\") or {}\n            auc = est.get(\"auc_substitute\") or {}\n            prl = [v for v in (blk.get(\"per_rollout_lambda\") or [])\n                   if v is not None and np.isfinite(v)]\n            if len(prl) >= 4:\n                q75, q25 = np.percentile(prl, [75, 25])", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-08-13 05:51:54 UTC

```
Read analysis1:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ && sed -n '227,430p' eval.py
```

### [26] TOOL RESULT — Bash · 2026-08-13 05:51:54 UTC

```
{"stdout": "# --------------------------------------------------------------------------- #\n# ANALYSIS 1 - direction contrast on assumption-free statistics\n# --------------------------------------------------------------------------- #\nSTATS = {\"S1_decay_ratio_16\": \"decay_ratio_16\", \"S2_auc_norm\": \"auc_norm\"}\n\n\ndef _series(prim: pd.DataFrame, model: str, direction: str, tf: bool,\n            readout: str, col: str) -> dict[str, float]:\n    g = prim[(prim[\"model\"] == model) & (prim[\"direction\"] == direction)\n             & (prim[\"teacher_forced\"] == tf) & (prim[\"readout\"] == readout)]\n    out: dict[str, float] = {}\n    for _, r in g.iterrows():\n        v = r[col]\n        if v is None or not np.isfinite(v) or v <= 0:\n            continue\n        out[r[\"prompt_id\"]] = float(np.log(v))\n    return out\n\n\ndef analysis1(LAM: pd.DataFrame) -> dict[str, Any]:\n    prim = LAM[(LAM[\"eps_c\"] == PRIMARY_CELL[\"eps_c\"]) & (LAM[\"p\"] == PRIMARY_CELL[\"p\"])].copy()\n    for c in (\"decay_ratio_16\", \"auc_norm\"):\n        prim[c] = pd.to_numeric(prim[c], errors=\"coerce\")\n\n    contrast_rows: list[dict[str, Any]] = []\n    did_rows: list[dict[str, Any]] = []\n    channels = {\"teacher_forced\": True, \"free_running\": False}\n\n    # ---- 1.1 per-model random-minus-refuse contrast -----------------------\n    for sname, col in STATS.items():\n        for rd in READOUTS:\n            for chan, tf in channels.items():\n                for m in MODELS:\n                    a = _series(prim, m, \"random_direction\", tf, rd, col)\n                    b = _series(prim, m, \"toward_refuse\", tf, rd, col)\n                    d, keys = EL._clean_pairs(a, b)\n                    bs = EL.bootstrap_mean(d)\n                    wx = EL.wilcoxon_signed_rank(d)\n                    contrast_rows.append({\n                        \"analysis\": \"1.1_direction_contrast\",\n                        \"model\": m, \"statistic\": sname, \"readout\": rd, \"channel\": chan,\n                        \"contrast\": \"log S(random_direction) - log S(toward_refuse)\",\n                        \"mean_log_diff\": bs[\"diff\"], \"ci_lo\": bs[\"ci_lo\"], \"ci_hi\": bs[\"ci_hi\"],\n                        \"sd\": bs[\"sd\"], \"n_pairs\": bs[\"n_pairs\"],\n                        \"ci_excludes_zero\": bs[\"ci_excludes_zero\"],\n                        \"boot_p_two_sided\": bs[\"boot_p_two_sided\"],\n                        \"wilcoxon_p\": wx[\"p\"], \"wilcoxon_mode\": wx[\"mode\"],\n                        \"cliffs_delta_paired\": EL.paired_cliffs_delta(d),\n                        \"cliffs_delta_unpaired\": EL.cliffs_delta(list(a.values()), list(b.values())),\n                        \"ratio_natural_scale\": float(np.exp(bs[\"diff\"])) if bs[\"diff\"] is not None else None,\n                        \"median_random_natural\": float(np.exp(np.median(list(a.values())))) if a else None,\n                        \"median_refuse_natural\": float(np.exp(np.median(list(b.values())))) if b else None,\n                        \"prompts_used\": len(keys),\n                        \"ptr\": (f\"tier0_raw.json:lambda[* where model={m}, eps_c=0.1, p=16, \"\n                                f\"teacher_forced={tf}, direction in \"\n                                f\"{{random_direction,toward_refuse}}].{READOUTS[rd]}.\"\n                                + (\"decay_ratio_16\" if col == \"decay_ratio_16\"\n                                   else \"estimates.auc_substitute.auc_norm\")),\n                    })\n\n    # ---- 1.2/1.3 difference-in-differences + equivalence -------------------\n    for sname, col in STATS.items():\n        for rd in READOUTS:\n            for chan, tf in channels.items():\n                for A, B in combinations(MODELS, 2):\n                    rA = _series(prim, A, \"toward_refuse\", tf, rd, col)\n                    rB = _series(prim, B, \"toward_refuse\", tf, rd, col)\n                    nA = _series(prim, A, \"random_direction\", tf, rd, col)\n                    nB = _series(prim, B, \"random_direction\", tf, rd, col)\n                    keys = sorted(set(rA) & set(rB) & set(nA) & set(nB))\n                    d = np.asarray([(rA[k] - rB[k]) - (nA[k] - nB[k]) for k in keys],\n                                   dtype=np.float64)\n                    bs = EL.bootstrap_mean(d)\n                    tt = EL.tost(d, EQ_MARGIN)\n                    wx = EL.wilcoxon_signed_rank(d)\n                    if bs[\"ci_excludes_zero\"]:\n                        verdict = \"DIRECTION_SPECIFIC\"\n                    elif tt[\"equivalent\"]:\n                        verdict = \"NO_DIRECTION_SPECIFICITY\"\n                    else:\n                        verdict = \"INCONCLUSIVE\"\n                    is_primary = (\n                        {A, B} == set(PRIMARY_PAIR) and sname == \"S1_decay_ratio_16\"\n                        and rd == \"layerL\" and chan == \"teacher_forced\")\n                    did_rows.append({\n                        \"analysis\": \"1.2_interaction_did\",\n                        \"pair\": f\"{A}_minus_{B}\", \"model_a\": A, \"model_b\": B,\n                        \"statistic\": sname, \"readout\": rd, \"channel\": chan,\n                        \"is_primary\": bool(is_primary),\n                        \"did_mean\": bs[\"diff\"], \"ci_lo\": bs[\"ci_lo\"], \"ci_hi\": bs[\"ci_hi\"],\n                        \"sd\": bs[\"sd\"], \"n_pairs\": bs[\"n_pairs\"],\n                        \"ci_excludes_zero\": bs[\"ci_excludes_zero\"],\n                        \"boot_p_two_sided\": bs[\"boot_p_two_sided\"],\n                        \"wilcoxon_p\": wx[\"p\"],\n                        \"tost_margin\": EQ_MARGIN, \"tost_p\": tt[\"p_tost\"],\n                        \"tost_ci90_lo\": tt[\"ci90_lo\"], \"tost_ci90_hi\": tt[\"ci90_hi\"],\n                        \"tost_equivalent\": tt[\"equivalent\"],\n                        \"verdict\": verdict,\n                        \"n_prompts_for_pm020_margin_80pct_power\":\n                            EL.tost_sample_size(bs[\"sd\"] or float(\"nan\"), EQ_MARGIN),\n                        \"ptr\": (f\"tier0_raw.json:lambda[* where model in {{{A},{B}}}, eps_c=0.1, \"\n                                f\"p=16, teacher_forced={tf}].{READOUTS[rd]}\"),\n                    })\n\n    # ---- 1.4 multiplicity --------------------------------------------------\n    fam = {r[\"pair\"] + \"|\" + r[\"statistic\"] + \"|\" + r[\"readout\"] + \"|\" + r[\"channel\"]:\n           r[\"wilcoxon_p\"] for r in did_rows}\n    adj = EL.holm(fam)\n    for r in did_rows:\n        k = r[\"pair\"] + \"|\" + r[\"statistic\"] + \"|\" + r[\"readout\"] + \"|\" + r[\"channel\"]\n        r[\"wilcoxon_p_holm\"] = adj.get(k)\n        r[\"family_size\"] = len(fam)\n\n    # ---- 1.6 free-running vs teacher-forced (the surviving R3 evidence) ----\n    ratchet_rows: list[dict[str, Any]] = []\n    for sname, col in STATS.items():\n        for rd in READOUTS:\n            for m in MODELS:\n                a = _series(prim, m, \"toward_refuse\", False, rd, col)   # free running\n                b = _series(prim, m, \"toward_refuse\", True, rd, col)    # teacher forced\n                d, keys = EL._clean_pairs(a, b)\n                bs = EL.bootstrap_mean(d)\n                wx = EL.wilcoxon_signed_rank(d)\n                ratchet_rows.append({\n                    \"analysis\": \"1.6_free_vs_teacher_forced\",\n                    \"model\": m, \"statistic\": sname, \"readout\": rd,\n                    \"contrast\": \"log S(free_running) - log S(teacher_forced)\",\n                    \"mean_log_diff\": bs[\"diff\"], \"ci_lo\": bs[\"ci_lo\"], \"ci_hi\": bs[\"ci_hi\"],\n                    \"n_pairs\": bs[\"n_pairs\"], \"ci_excludes_zero\": bs[\"ci_excludes_zero\"],\n                    \"wilcoxon_p\": wx[\"p\"],\n                    \"ratio_natural_scale\": float(np.exp(bs[\"diff\"])) if bs[\"diff\"] is not None else None,\n                    \"median_free_natural\": float(np.exp(np.median(list(a.values())))) if a else None,\n                    \"median_tf_natural\": float(np.exp(np.median(list(b.values())))) if b else None,\n                    \"ptr\": f\"tier0_raw.json:lambda[* model={m}, direction=toward_refuse, \"\n                           f\"eps_c=0.1, p=16].{READOUTS[rd]}\",\n                })\n    return {\"contrast\": contrast_rows, \"did\": did_rows, \"ratchet\": ratchet_rows}\n\n\ndef analysis1_lambda_consistency(tree: dict[str, Any], LAM: pd.DataFrame) -> dict[str, Any]:\n    \"\"\"1.5 - lambda demoted to a LABELLED consistency check.\"\"\"\n    ot = tree[\"ordering_tests\"]\n    prim = LAM[(LAM[\"eps_c\"] == PRIMARY_CELL[\"eps_c\"]) & (LAM[\"p\"] == PRIMARY_CELL[\"p\"])\n               & (LAM[\"teacher_forced\"])].copy()\n    prim[\"nls_r2\"] = pd.to_numeric(prim[\"nls_r2\"], errors=\"coerce\")\n\n    diag: dict[str, Any] = {}\n    for m in MODELS:\n        for rd in READOUTS:\n            g = prim[(prim[\"model\"] == m) & (prim[\"readout\"] == rd)\n                     & (prim[\"direction\"] == \"toward_refuse\")]\n            r2 = g[\"nls_r2\"].to_numpy(dtype=np.float64)\n            agr = pd.to_numeric(g[\"estimator_agreement_ratio\"], errors=\"coerce\").to_numpy()\n            iqr = pd.to_numeric(g[\"per_rollout_lambda_iqr_ratio\"], errors=\"coerce\").to_numpy()\n            iqr = iqr[np.isfinite(iqr)]\n            diag[f\"{m}|{rd}\"] = {\n                \"median_nls_r2\": float(np.nanmedian(r2)) if r2.size else None,\n                \"frac_r2_below_0.3\": float(np.nanmean(r2 < 0.3)) if r2.size else None,\n                \"frac_at_bound\": float(np.mean(g[\"nls_at_bound\"].astype(bool))) if len(g) else None,\n                \"median_per_prompt_lambda_iqr_ratio\": float(np.median(iqr)) if iqr.size else None,\n                \"p90_per_prompt_lambda_iqr_ratio\": float(np.percentile(iqr, 90)) if iqr.size else None,\n                \"median_estimator_agreement_ratio\": float(np.nanmedian(agr)) if agr.size else None,\n                \"p90_estimator_agreement_ratio\": float(np.nanpercentile(agr, 90)) if agr.size else None,\n                \"n_rows\": int(len(g)),\n                \"ptr\": f\"tier0_raw.json:lambda[* model={m}, direction=toward_refuse, \"\n                       f\"eps_c=0.1, p=16, teacher_forced=True].{READOUTS[rd]}.estimates\",\n            }\n\n    n_false = int((~LAM.query(\"readout=='layerL'\")[\"identifiable\"]).sum())\n    rows: list[dict[str, Any]] = []\n    for pair_key, blk in ot.items():\n        if not isinstance(blk, dict):\n            continue\n        for stat_key in (\"lambda_refuse\", \"lambda_random_dir\",\n                         \"lambda_refuse_final_readout\", \"lambda_random_dir_final_readout\",\n                         \"lambda_comply\", \"lambda_comply_final_readout\"):\n            v = blk.get(stat_key)\n            if not isinstance(v, dict):\n                continue\n            rows.append({\n                \"analysis\": \"1.5_lambda_consistency_check\",\n                \"pair\": pair_key, \"lambda_statistic\": stat_key,\n                \"diff_verbatim\": v.get(\"diff\"), \"ci_lo\": v.get(\"ci_lo\"),\n                \"ci_hi\": v.get(\"ci_hi\"), \"n_pairs\": v.get(\"n_pairs\"),\n                \"ci_excludes_zero\": v.get(\"ci_excludes_zero\"),\n                \"n_lambda_rows_identifiable_false\": n_false,\n                \"n_lambda_rows_total\": int(len(LAM.query(\"readout=='layerL'\"))),\n                \"identifiable_reason\": \"geometry_below_prereg_rule\",\n                \"ptr\": f\"tier0_raw.json:ordering_tests['{pair_key}']['{stat_key}']\",\n            })\n    return {\n        \"rows\": rows,\n        \"diagnostics\": diag,\n        \"identifiability_rule\": tree[\"controls\"][\"lambda_identifiable_at_achieved_geometry\"],\n        \"min_series_length_rule\": tree.get(\"min_series_length_rule\"),\n        \"archived_control_block\": tree[\"controls\"][\"random_direction_reproduces_ordering\"],\n    }\n\n\n# --------------------------------------------------------------------------- #\n# ANALYSIS 2 - observable-validity gate\n# --------------------------------------------------------------------------- #\n\ndef analysis2_gate(tree: dict[str, Any], final_gate: dict[str, Any] | None) -> dict[str, Any]:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Bash · 2026-08-13 05:52:02 UTC

```
Search for tier0_raw:
find /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/ -maxdepth 3 -name "*.json" | head -30; echo ---; ls /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/cells | head; echo ---; ls /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/ | head -30
```

### [28] TOOL RESULT — Bash · 2026-08-13 05:52:02 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/.terminal_claude_agent_struct_out.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/preview_method_out.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/mini_method_out.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/full_method_out.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method_out.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/refit_certified.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/tier0_raw.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/layer_choice.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/t2b_snr_probe.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/t2_pairing_report.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/t0_load_report.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/prompts/prompt_sets.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/cells/smollm2_base_partial.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/cells/qwen3-0.6b_abliterated_partial.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/cells/qwen3-0.6b_instruct_partial.json\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/cells/qwen3-0.6b_base_partial.json\n---\nqwen3-0.6b_abliterated_partial.json\nqwen3-0.6b_abliterated_traj.npz\nqwen3-0.6b_base_partial.json\nqwen3-0.6b_base_traj.npz\nqwen3-0.6b_instruct_partial.json\nqwen3-0.6b_instruct_traj.npz\nsmollm2_base_partial.json\nsmollm2_base_traj.npz\n---\nREADME.md\nbuild_output.py\nfigs\nfull_method_out.json\nlogs\nmake_figs.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nout\npreview_method_out.json\npyproject.toml\nrefit_certified.py\nrun_tier0.py\nspi\nt0_load_test.py\nt2_pairing_test.py\nt2b_snr_probe.py\nt_analysis_dryrun.py\nvalidate_output.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-08-13 05:52:12 UTC

```
Inspect tier0 lambda row:
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/ && python3 -c "
import json
t=json.load(open('tier0_raw.json'))
print(list(t.keys()))
r=t['lambda'][0]
print(json.dumps({k:v for k,v in r.items() if k not in ('layerL','final')}, indent=1)[:1200])
print('LAYERL:', json.dumps(r['layerL'], indent=1)[:1500])
"
```

### [30] TOOL RESULT — Bash · 2026-08-13 05:52:12 UTC

```
{"stdout": "['status', 'mode', 'grid_actually_run', 'hardware', 'tokens_per_sec_by_model', 'peak_vram_gb', 'wall_clock_by_stage', 'model_revisions', 'layer_choice', 'observable_token_ids_by_model', 'per_model_meta', 'prompts', 'indicators', 'lambda', 'aggregate_by_model', 'asymmetry_index_by_model', 'epsilon_sweep', 'series_length_sweep_note', 'synthetic_ar1_table', 'min_series_length_rule', 'synthetic_meta', 'controls', 'ground_truth', 'panel_validity', 'provisional_spi', 'ordering_tests', 'verdict', 'observable_degenerate_by_model', 'limitations']\n{\n \"model\": \"qwen3-0.6b/base\",\n \"member\": \"base\",\n \"lineage\": \"qwen3-0.6b\",\n \"prompt_id\": \"fact_01\",\n \"direction\": \"toward_refuse\",\n \"eps_c\": 0.1,\n \"eps_abs\": 5.251130676269532,\n \"p\": 16,\n \"teacher_forced\": true,\n \"n_roll\": 20,\n \"T\": 192,\n \"fit_len\": 64,\n \"median_first_divergence_after_p\": null,\n \"identifiable\": false,\n \"identifiable_reason\": \"geometry_below_prereg_rule\"\n}\nLAYERL: {\n \"delta_residual_sd_per_rollout\": 0.008484435267746449,\n \"delta_residual_sd_of_mean\": 0.0018971774009377688,\n \"delta_at_p1_signed\": -0.009096409194171429,\n \"delta_at_p1\": 0.021597864106297493,\n \"delta_snr_at_p1\": 0.005143328859349696,\n \"delta_snr_at_p1_vs_fit_noise\": 4.794706699370919,\n \"steps_above_noise_floor\": 0,\n \"monotone_decay_frac\": 0.4603174603174603,\n \"decay_ratio_16\": 0.5704988241195679,\n \"estimates\": {\n  \"est1_nls\": {\n   \"lambda\": 1.9999999999998854,\n   \"A\": -0.008882204670293466,\n   \"b\": 0.00035762641619632577,\n   \"r2\": 0.03441224525199238,\n   \"se\": 21.405622641216127,\n   \"at_bound\": true,\n   \"n\": 64,\n   \"reason\": null\n  },\n  \"est2_loglin\": {\n   \"lambda\": 0.0006523472697901695,\n   \"r2\": 0.14318612562292743,\n   \"floor\": 0.08842920064926148,\n   \"reason\": null\n  },\n  \"est3_ar1\": {\n   \"lambda\": 3.192257068758597,\n   \"phi\": 0.04107904798873493,\n   \"reason\": null\n  },\n  \"auc_substitute\": {\n   \"auc_norm\": 16.02981592535331,\n   \"half_life\": 3.0,\n   \"delta_0\": 0.009096409194171429,\n   \"reason\": null\n  },\n  \"estimator_spread\": 3.191604721488807,\n  \"estimator_agreement_ratio\": 4893.493414612437,\n  \"fit_len\": 64,\n  \"delta_floor\": 0.08842920064926148,\n  \"noise_floor_sd\": 1.7685840129852295,\n  \"statistic\": \"signed_across_rollout_mean\",\n  \"abs_statistic_secondary\": {\n   \"est1_nls\": {\n    \"lambda\": 0.2550862259252218,\n    \"A\": 0.017403273198345517,\n    \"b\": 0.0061119279542886954,\n    \"r2\": 0.7652967062807212,\n    \"se\": 0.04278949522229866,\n    \"at_bound\": false,\n    \"n\": 64,", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Read · 2026-08-13 05:52:12 UTC

```
/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/eval_lib.py
```

### [32] TOOL RESULT — Read · 2026-08-13 05:52:12 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/eval_lib.py", "content": "#!/usr/bin/env python3\n\"\"\"Shared statistics helpers for the wobble re-analysis.\n\nEverything here is either a thin wrapper around the ARCHIVED spi/ library\n(imported verbatim so estimator definitions cannot drift) or a small,\nself-contained addition (TOST, exact permutation, Cliff's delta, AUROC CIs).\n\"\"\"\n\nfrom __future__ import annotations\n\nimport hashlib\nimport itertools\nimport math\nfrom pathlib import Path\nfrom typing import Any, Sequence\n\nimport numpy as np\nfrom scipy import stats\n\nfrom spi.indicators import paired_bootstrap_diff, wilson_ci  # noqa: F401  (re-export)\n\nBOOT_REPS = 10_000\nBOOT_SEED = 20260812\n\n\n# --------------------------------------------------------------------------- #\n# provenance\n# --------------------------------------------------------------------------- #\n\ndef sha256_of(path: Path, chunk: int = 1 << 20) -> str:\n    h = hashlib.sha256()\n    with path.open(\"rb\") as fh:\n        while True:\n            b = fh.read(chunk)\n            if not b:\n                break\n            h.update(b)\n    return h.hexdigest()\n\n\ndef sha256_of_tree(root: Path, pattern: str = \"**/*.jsonl\") -> dict[str, Any]:\n    \"\"\"Content-independent but reproducible fingerprint of a file tree:\n    hash over the sorted (relative path, size) list plus the file count.\"\"\"\n    files = sorted(root.glob(pattern))\n    h = hashlib.sha256()\n    total = 0\n    for f in files:\n        n = f.stat().st_size\n        total += n\n        h.update(f\"{f.relative_to(root)}:{n}\\n\".encode())\n    return {\"root\": str(root), \"n_files\": len(files),\n            \"total_bytes\": total, \"sha256_of_name_size_index\": h.hexdigest()}\n\n\n# --------------------------------------------------------------------------- #\n# paired statistics over prompts\n# --------------------------------------------------------------------------- #\n\ndef _clean_pairs(a: dict[str, float], b: dict[str, float]) -> tuple[np.ndarray, list[str]]:\n    keys = sorted(set(a) & set(b))\n    ok = [k for k in keys\n          if a[k] is not None and b[k] is not None\n          and np.isfinite(a[k]) and np.isfinite(b[k])]\n    return np.asarray([a[k] - b[k] for k in ok], dtype=np.float64), ok\n\n\ndef bootstrap_mean(d: np.ndarray, *, n_reps: int = BOOT_REPS, seed: int = BOOT_SEED,\n                   alpha: float = 0.05) -> dict[str, Any]:\n    \"\"\"Percentile bootstrap of the mean of a vector of paired differences.\"\"\"\n    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)\n    if d.size < 2:\n        return {\"diff\": float(d[0]) if d.size == 1 else None, \"ci_lo\": None,\n                \"ci_hi\": None, \"n_pairs\": int(d.size), \"ci_excludes_zero\": None,\n                \"sd\": None, \"boot_p_two_sided\": None}\n    rng = np.random.default_rng(seed)\n    idx = rng.integers(0, d.size, size=(n_reps, d.size))\n    draws = d[idx].mean(axis=1)\n    lo = float(np.percentile(draws, 100 * alpha / 2))\n    hi = float(np.percentile(draws, 100 * (1 - alpha / 2)))\n    # two-sided bootstrap p: 2 * min(frac of draws <= 0, frac >= 0)\n    frac_le = float((draws <= 0).mean())\n    frac_ge = float((draws >= 0).mean())\n    p = float(min(1.0, 2.0 * min(frac_le, frac_ge)))\n    return {\"diff\": float(d.mean()), \"ci_lo\": lo, \"ci_hi\": hi,\n            \"n_pairs\": int(d.size), \"ci_excludes_zero\": bool(lo > 0 or hi < 0),\n            \"sd\": float(d.std(ddof=1)), \"boot_p_two_sided\": p,\n            \"n_reps\": int(n_reps), \"alpha\": float(alpha)}\n\n\ndef bootstrap_ci_level(d: np.ndarray, *, level: float, n_reps: int = BOOT_REPS,\n                       seed: int = BOOT_SEED + 1) -> tuple[float | None, float | None]:\n    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)\n    if d.size < 2:\n        return None, None\n    rng = np.random.default_rng(seed)\n    idx = rng.integers(0, d.size, size=(n_reps, d.size))\n    draws = d[idx].mean(axis=1)\n    a = (1.0 - level) / 2.0\n    return float(np.percentile(draws, 100 * a)), float(np.percentile(draws, 100 * (1 - a)))\n\n\ndef wilcoxon_signed_rank(d: np.ndarray) -> dict[str, Any]:\n    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)\n    nz = d[d != 0]\n    if nz.size < 3:\n        return {\"stat\": None, \"p\": None, \"n\": int(nz.size), \"mode\": \"too_few\"}\n    mode = \"exact\" if nz.size <= 25 else \"approx\"\n    try:\n        res = stats.wilcoxon(nz, alternative=\"two-sided\", mode=mode)\n    except TypeError:  # scipy >= 1.13 renamed the kwarg\n        res = stats.wilcoxon(nz, alternative=\"two-sided\", method=mode)\n    return {\"stat\": float(res.statistic), \"p\": float(res.pvalue),\n            \"n\": int(nz.size), \"mode\": mode}\n\n\ndef cliffs_delta(x: Sequence[float], y: Sequence[float]) -> float:\n    \"\"\"Cliff's delta of x vs y (unpaired form, used as a distribution-free\n    effect size companion to the paired bootstrap).\"\"\"\n    a = np.asarray([v for v in x if np.isfinite(v)], dtype=np.float64)\n    b = np.asarray([v for v in y if np.isfinite(v)], dtype=np.float64)\n    if a.size == 0 or b.size == 0:\n        return float(\"nan\")\n    gt = float((a[:, None] > b[None, :]).sum())\n    lt = float((a[:, None] < b[None, :]).sum())\n    return (gt - lt) / (a.size * b.size)\n\n\ndef paired_cliffs_delta(d: np.ndarray) -> float:\n    \"\"\"Paired sign-based effect size: P(d>0) - P(d<0).\"\"\"\n    d = np.asarray([v for v in d if np.isfinite(v)], dtype=np.float64)\n    if d.size == 0:\n        return float(\"nan\")\n    return float((d > 0).mean() - (d < 0).mean())\n\n\ndef tost(d: np.ndarray, margin: float) -> dict[str, Any]:\n    \"\"\"Two-one-sided-tests for equivalence of the mean of d to 0 within\n    +/- margin. Returns both the parametric TOST p and the bootstrap 90% CI\n    (the CI-inclusion rule is the operational verdict).\"\"\"\n    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)\n    out: dict[str, Any] = {\"margin\": float(margin), \"n\": int(d.size)}\n    if d.size < 3:\n        out.update({\"p_tost\": None, \"ci90_lo\": None, \"ci90_hi\": None,\n                    \"equivalent\": None})\n        return out\n    m = float(d.mean())\n    se = float(d.std(ddof=1) / math.sqrt(d.size))\n    df = d.size - 1\n    if se <= 0:\n        p_lo = p_hi = 0.0\n    else:\n        p_lo = float(stats.t.sf((m + margin) / se, df))       # H0: mu <= -margin\n        p_hi = float(stats.t.cdf((m - margin) / se, df))      # H0: mu >= +margin\n    lo90, hi90 = bootstrap_ci_level(d, level=0.90)\n    out.update({\n        \"mean\": m, \"se\": se, \"df\": int(df),\n        \"p_tost\": float(max(p_lo, p_hi)), \"p_lower\": p_lo, \"p_upper\": p_hi,\n        \"ci90_lo\": lo90, \"ci90_hi\": hi90,\n        \"equivalent\": bool(lo90 is not None and lo90 > -margin and hi90 < margin),\n    })\n    return out\n\n\ndef tost_sample_size(sd: float, margin: float, *, alpha: float = 0.05,\n                     power: float = 0.80) -> int | None:\n    \"\"\"n per (paired) sample for a TOST at `margin` with true effect 0.\"\"\"\n    if not np.isfinite(sd) or sd <= 0 or margin <= 0:\n        return None\n    z_a = stats.norm.ppf(1 - alpha)\n    z_b = stats.norm.ppf(1 - (1 - power) / 2)\n    return int(math.ceil(((z_a + z_b) ** 2) * (sd ** 2) / (margin ** 2)))\n\n\ndef holm(pvals: dict[str, float]) -> dict[str, float]:\n    \"\"\"Holm-Bonferroni step-down adjusted p-values.\"\"\"\n    items = [(k, v) for k, v in pvals.items() if v is not None and np.isfinite(v)]\n    m = len(items)\n    items.sort(key=lambda kv: kv[1])\n    adj: dict[str, float] = {}\n    running = 0.0\n    for i, (k, p) in enumerate(items):\n        val = min(1.0, (m - i) * p)\n        running = max(running, val)\n        adj[k] = float(running)\n    for k, v in pvals.items():\n        if k not in adj:\n            adj[k] = float(\"nan\")\n    return adj\n\n\n# --------------------------------------------------------------------------- #\n# AUROC\n# --------------------------------------------------------------------------- #\n\ndef auroc_mannwhitney(pos: Sequence[float], neg: Sequence[float]) -> dict[str, Any]:\n    a = np.asarray([v for v in pos if np.isfinite(v)], dtype=np.float64)\n    b = np.asarray([v for v in neg if np.isfinite(v)], dtype=np.float64)\n    if a.size == 0 or b.size == 0:\n        return {\"auroc\": None, \"n_pos\": int(a.size), \"n_neg\": int(b.size),\n                \"ci_lo\": None, \"ci_hi\": None, \"p\": None}\n    u, p = stats.mannwhitneyu(a, b, alternative=\"two-sided\")\n    auc = float(u / (a.size * b.size))\n    ci = auroc_hanley_ci(auc, a.size, b.size)\n    return {\"auroc\": auc, \"n_pos\": int(a.size), \"n_neg\": int(b.size),\n            \"ci_lo\": ci[\"lo\"], \"ci_hi\": ci[\"hi\"], \"se\": ci[\"se\"], \"p\": float(p)}\n\n\ndef auroc_hanley_ci(auc: float, n_pos: int, n_neg: int, z: float = 1.96) -> dict[str, float]:\n    \"\"\"Hanley & McNeil (1982) standard error and normal CI for an AUROC.\"\"\"\n    if not np.isfinite(auc) or n_pos <= 0 or n_neg <= 0:\n        return {\"se\": float(\"nan\"), \"lo\": float(\"nan\"), \"hi\": float(\"nan\")}\n    q1 = auc / (2 - auc)\n    q2 = 2 * auc ** 2 / (1 + auc)\n    var = (auc * (1 - auc)\n           + (n_pos - 1) * (q1 - auc ** 2)\n           + (n_neg - 1) * (q2 - auc ** 2)) / (n_pos * n_neg)\n    se = float(math.sqrt(max(var, 0.0)))\n    return {\"se\": se, \"lo\": float(max(0.0, auc - z * se)),\n            \"hi\": float(min(1.0, auc + z * se))}\n\n\n# --------------------------------------------------------------------------- #\n# exact permutation Spearman for tiny n\n# --------------------------------------------------------------------------- #\n\ndef exact_spearman_permutation(x: Sequence[float], y: Sequence[float]) -> dict[str, Any]:\n    \"\"\"Enumerate every assignment of the x-ranks to the y-ranks (n! of them) and\n    return the exact null distribution of Spearman rho, plus exact p-values.\n\n    Tie-aware: ranks are computed with 'average' tie handling, and DISTINCT\n    attainable rho values are enumerated (with their multiplicities) rather\n    than assuming n! distinct values.\"\"\"\n    xr = stats.rankdata(np.asarray(x, dtype=np.float64), method=\"average\")\n    yr = stats.rankdata(np.asarray(y, dtype=np.float64), method=\"average\")\n    n = len(xr)\n    obs = float(stats.spearmanr(xr, yr).statistic)\n    rhos: list[float] = []\n    for perm in itertools.permutations(range(n)):\n        rhos.append(float(stats.spearmanr(xr[list(perm)], yr).statistic))\n    arr = np.asarray(rhos, dtype=np.float64)\n    n_perm = arr.size\n    tol = 1e-9\n    p_greater = float((arr >= obs - tol).mean())\n    p_less = float((arr <= obs + tol).mean())\n    p_two = float(min(1.0, (np.abs(arr) >= abs(obs) - tol).mean()))\n    uniq = sorted({round(v, 10) for v in arr if np.isfinite(v)})\n    finite = arr[np.isfinite(arr)]\n    return {\n        \"rho_observed\": obs,\n        \"n_permutations\": int(n_perm),\n        \"n_distinct_rho\": int(len(uniq)),\n        \"p_one_sided_greater\": p_greater,\n        \"p_one_sided_less\": p_less,\n        \"p_two_sided\": p_two,\n        \"min_attainable_one_sided_p\": float(1.0 / n_perm),\n        \"min_attainable_two_sided_p\": float(\n            (np.abs(finite) >= np.abs(finite).max() - tol).mean()) if finite.size else None,\n        \"max_attainable_abs_rho\": float(np.abs(finite).max()) if finite.size else None,\n        \"null_rho_values\": [float(v) for v in uniq],\n    }\n\n\ndef n_resolvable_levels(rates: dict[str, dict[str, float]]) -> dict[str, Any]:\n    \"\"\"Greedy chain-count of ground-truth levels whose Wilson CIs do not overlap.\n    `rates` maps model -> {'p':..., 'lo':..., 'hi':...}.\"\"\"\n    items = sorted(rates.items(), key=lambda kv: kv[1][\"p\"])\n    groups: list[list[str]] = []\n    for name, r in items:\n        placed = False\n        for g in groups:\n            if all(not (rates[o][\"hi\"] < r[\"lo\"] or r[\"hi\"] < rates[o][\"lo\"]) for o in g):\n                g.append(name)\n                placed = True\n                break\n        if not placed:\n            groups.append([name])\n    return {\"n_levels\": len(groups), \"groups\": groups,\n            \"detail\": {k: dict(v) for k, v in rates.items()}}\n", "numLines": 279, "startLine": 1, "totalLines": 279}}
```

### [33] TOOL CALL — Bash · 2026-08-13 05:52:36 UTC

```
Build mini demo data:
cat > build_mini.py <<'EOF'
import json
SRC="/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/out/tier0_raw.json"
t=json.load(open(SRC))
KEEP={"qwen3-0.6b/instruct","qwen3-0.6b/abliterated"}
DIRS={"toward_refuse","random_direction"}
rows=[]
for r in t["lambda"]:
    if r["model"] not in KEEP or r["direction"] not in DIRS: continue
    if r["eps_c"]!=0.1 or r["p"]!=16 or not r["teacher_forced"]: continue
    out={k:r[k] for k in ("model","member","lineage","prompt_id","direction","eps_c","p",
                          "teacher_forced","n_roll","T","fit_len","identifiable","identifiable_reason")}
    for rd in ("layerL","final"):
        blk=r.get(rd) or {}
        est=blk.get("estimates") or {}
        out[rd]={
          "decay_ratio_16": blk.get("decay_ratio_16"),
          "estimates":{"auc_substitute":{"auc_norm":((est.get("auc_substitute") or {}).get("auc_norm"))},
                       "est1_nls":{"r2":((est.get("est1_nls") or {}).get("r2")),
                                   "at_bound":((est.get("est1_nls") or {}).get("at_bound"))}},
        }
    rows.append(out)
print(len(rows))
mini={
 "source":"tier0_raw.json:lambda (iteration-1 experiment 1 archive)",
 "subset":"primary cell eps_c=0.1, p=16, teacher_forced=True; models {qwen3-0.6b/instruct, qwen3-0.6b/abliterated}; directions {toward_refuse, random_direction}",
 "note":"Curated demo subset of the archived lambda table. Each row is one (model, prompt, steering direction) rollout cell with the two assumption-free dynamics statistics at both readouts.",
 "primary_pair":["qwen3-0.6b/instruct","qwen3-0.6b/abliterated"],
 "reference_results":{
   "primary_did_mean_log_units": None,
 },
 "lambda_rows":rows,
}
ev=json.load(open("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/full_eval_out.json"))
ma=ev["metrics_agg"]
mini["reference_results"]={k:ma[k] for k in ("primary_did_mean_log_units","primary_did_ci_lo","primary_did_ci_hi","primary_did_tost_p","n_did_tests","n_did_ci_excludes_zero","n_did_inconclusive") if k in ma}
json.dump(mini, open("mini_demo_data.json","w"), indent=1)
import os; print(os.path.getsize("mini_demo_data.json"))
print(json.dumps(mini["reference_results"],indent=1))
EOF
python3 build_mini.py
```

### [34] TOOL RESULT — Bash · 2026-08-13 05:52:36 UTC

```
{"stdout": "80\n67007\n{\n \"primary_did_mean_log_units\": -2.3338372643058096,\n \"primary_did_ci_lo\": -3.572734989281885,\n \"primary_did_ci_hi\": -1.0365288846483625,\n \"primary_did_tost_p\": 0.997750343241054,\n \"n_did_tests\": 48.0,\n \"n_did_ci_excludes_zero\": 8.0,\n \"n_did_inconclusive\": 40.0\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Bash · 2026-08-13 05:52:42 UTC

```
Verify mini data:
pwd && ls && python3 -c "
import json,numpy as np
d=json.load(open('mini_demo_data.json'))
r=d['lambda_rows'][0]; print(json.dumps(r,indent=1))
print(len(d['lambda_rows']))
"
```

### [36] TOOL RESULT — Bash · 2026-08-13 05:52:42 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9\nbuild_mini.py\nmini_demo_data.json\n{\n \"model\": \"qwen3-0.6b/instruct\",\n \"member\": \"instruct\",\n \"lineage\": \"qwen3-0.6b\",\n \"prompt_id\": \"fact_01\",\n \"direction\": \"toward_refuse\",\n \"eps_c\": 0.1,\n \"p\": 16,\n \"teacher_forced\": true,\n \"n_roll\": 20,\n \"T\": 192,\n \"fit_len\": 64,\n \"identifiable\": false,\n \"identifiable_reason\": \"geometry_below_prereg_rule\",\n \"layerL\": {\n  \"decay_ratio_16\": 0.4064473509788513,\n  \"estimates\": {\n   \"auc_substitute\": {\n    \"auc_norm\": 14.559110449100949\n   },\n   \"est1_nls\": {\n    \"r2\": 0.5352521331338453,\n    \"at_bound\": false\n   }\n  }\n },\n \"final\": {\n  \"decay_ratio_16\": 0.18857243657112122,\n  \"estimates\": {\n   \"auc_substitute\": {\n    \"auc_norm\": 48.716696575143985\n   },\n   \"est1_nls\": {\n    \"r2\": 0.22871511639728126,\n    \"at_bound\": false\n   }\n  }\n }\n}\n80", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] TOOL CALL — Write · 2026-08-13 05:54:44 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py

#!/usr/bin/env python3
"""Assemble code_demo.ipynb from cell sources (keeps the .ipynb JSON tidy)."""
import json

C = []


def md(s):
    C.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n").splitlines(keepends=True)})


def code(s):
    C.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
... [truncated, 26328 chars total]
```

### [38] TOOL RESULT — Write · 2026-08-13 05:54:44 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py", "content": "#!/usr/bin/env python3\n\"\"\"Assemble code_demo.ipynb from cell sources (keeps the .ipynb JSON tidy).\"\"\"\nimport json\n\nC = []\n\n\ndef md(s):\n    C.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\").splitlines(keepends=True)})\n\n\ndef code(s):\n    C.append({\... [truncated, 28056 chars total]
```

### [39] TOOL CALL — Edit · 2026-08-13 05:54:52 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py
OLD: def code(s):
    C.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
              "source": s.strip("\n").splitlines(keepends=True)})
NEW: def code(s):
    s = s.replace('\\"', '"')          # un-escape triple-quoted docstrings inside r-strings
    C.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
              "source": s.strip("\n").splitlines(keepends=True)})
```

### [40] TOOL RESULT — Edit · 2026-08-13 05:54:52 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py", "oldString": "def code(s):\n    C.append({\"cell_type\": \"code\", \"execution_count\": None, \"metadata\": {}, \"outputs\": [],\n              \"source\": s.strip(\"\\n\").splitlines(keepends=True)})", "newString": "def code(s):\n    s = s.replace('\\\\\"', '\"')          # un-escape triple-quoted docstrings inside r-strings\n    C.append({\"cell_type\": \"code\", \"execution_count\": None, \"metadata\": {}, \"outputs\": [],\n              \"source\": s.strip(\"\\n\").splitlines(keepends=True)})", "originalFile": null, "structuredPatch": [{"oldStart": 10, "oldLines": 6, "newStart": 10, "newLines": 7, "lines": [" ", " ", " def code(s):", "+    s = s.replace('\\\\\"', '\"')          # un-escape triple-quoted docstrings inside r-strings", "     C.append({\"cell_type\": \"code\", \"execution_count\": None, \"metadata\": {}, \"outputs\": [],", "               \"source\": s.strip(\"\\n\").splitlines(keepends=True)})", " "]}], "userModified": false, "replaceAll": false}
```

### [41] TOOL CALL — Edit · 2026-08-13 05:54:56 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py
OLD: lab = [f"{r.member if hasattr(r,'member') else ''}" for r in []]  # placeholder removed below
labels
NEW: labels
```

### [42] TOOL RESULT — Edit · 2026-08-13 05:54:56 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py", "oldString": "lab = [f\"{r.member if hasattr(r,'member') else ''}\" for r in []]  # placeholder removed below\nlabels", "newString": "labels", "originalFile": null, "structuredPatch": [{"oldStart": 563, "oldLines": 7, "newStart": 563, "newLines": 6, "lines": [" fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))", " ", " ax = axes[0]", "-lab = [f\"{r.member if hasattr(r,'member') else ''}\" for r in []]  # placeholder removed below", " labels = [f\"{r['model'].split('/')[-1]}\\n{r['statistic'][:2]} | {r['readout']}\"", "           for _, r in CON.iterrows()]", " y = np.arange(len(CON))"]}], "userModified": false, "replaceAll": false}
```

### [43] TOOL CALL — Bash · 2026-08-13 05:55:00 UTC

```
Build notebook:
python3 build_nb.py && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print(len(nb['cells']))
print(''.join(nb['cells'][6]['source'])[:300])
"
```

### [44] TOOL RESULT — Bash · 2026-08-13 05:55:00 UTC

```
{"stdout": "wrote code_demo.ipynb with 23 cells\n23\ndata = load_data()\n\nprint(\"source :\", data[\"source\"])\nprint(\"subset :\", data[\"subset\"])\nprint(\"rows   :\", len(data[\"lambda_rows\"]))\nprint(\"archived reference numbers (from the full artifact run):\")\nfor k, v in data[\"reference_results\"].items():\n    print(f\"   {k:32s} {v}\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] ASSISTANT · 2026-08-13 05:55:04 UTC

```
Now test-run in a clean environment.
```

### [46] TOOL CALL — Bash · 2026-08-13 05:55:04 UTC

```
Test-run notebook in clean venv:
/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -3 && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [47] TOOL RESULT — Bash · 2026-08-13 06:04:02 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/.nb_env/lib/python3.12/site-packages/nbformat/validator.py:434: MissingIDFieldWarning: Cell is missing an id field, this will become a hard error in future nbformat versions. You may want to use `normalize()` on your notebooks before validations (available since nbformat 5.1.4). Previous versions of nbformat are fixing this issue transparently, and will stop doing so in the future.\n  _validate(nbdict, ref, version, version_minor, relax_add_props)\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 46002 bytes to code_demo.ipynb\n\nreal\t4m3.240s\nuser\t0m14.362s\nsys\t0m1.784s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] TOOL CALL — Bash · 2026-08-13 06:04:10 UTC

```
Check notebook outputs:
python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c.get('outputs',[]):
        if o.get('output_type')=='error':
            print('ERROR cell',i,o['ename'],o['evalue'])
        t=''.join(o.get('text',''))
        if t.strip(): print(f'--- cell {i} ---'); print(t[:2500])
EOF
```

### [49] TOOL RESULT — Bash · 2026-08-13 06:04:10 UTC

```
{"stdout": "--- cell 1 ---\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n--- cell 6 ---\nsource : tier0_raw.json:lambda (iteration-1 experiment 1 archive)\nsubset : primary cell eps_c=0.1, p=16, teacher_forced=True; models {qwen3-0.6b/instruct, qwen3-0.6b/abliterated}; directions {toward_refuse, random_direction}\nrows   : 80\narchived reference numbers (from the full artifact run):\n   primary_did_mean_log_units       -2.3338372643058096\n   primary_did_ci_lo                -3.572734989281885\n   primary_did_ci_hi                -1.0365288846483625\n   primary_did_tost_p               0.997750343241054\n   n_did_tests                      48.0\n   n_did_ci_excludes_zero           8.0\n   n_did_inconclusive               40.0\n\n--- cell 8 ---\n10000 bootstrap reps | 20 prompts | margin +/-0.2 log units\nmodels  : ['qwen3-0.6b/instruct', 'qwen3-0.6b/abliterated']\nstats   : ['S1_decay_ratio_16', 'S2_auc_norm']\nreadouts: ['layerL', 'final']\n\n--- cell 10 ---\nestimator library loaded\n\n--- cell 12 ---\nLAM frame: (160, 18)\nprompts  : 20 ['creat_01', 'creat_02', 'creat_03', 'creat_04', 'creat_05'] ...\n\nmodel                   direction         readout\nqwen3-0.6b/abliterated  random_direction  final      20\n                                          layerL     20\n                        toward_refuse     final      20\n                                          layerL     20\nqwen3-0.6b/instruct     random_direction  final      20\n                                          layerL     20\n                        toward_refuse     final      20\n                                          layerL     20\n\nlambda identifiable=false on 80/80 rows in this subset (geometry_below_prereg_rule) -> lambda cannot carry the direction control\n\n--- cell 14 ---\n                 model         statistic readout  mean_log_diff     ci_lo     ci_hi  ci_excludes_zero  wilcoxon_p  cliffs_delta_paired\n   qwen3-0.6b/instruct S1_decay_ratio_16  layerL       1.208013  0.303669  2.207915              True    0.029575                  0.3\nqwen3-0.6b/abliterated S1_decay_ratio_16  layerL      -1.125824 -2.246119  0.026980             False    0.089695                 -0.3\n   qwen3-0.6b/instruct S1_decay_ratio_16   final       0.635480 -0.154489  1.460446             False    0.261099                  0.1\nqwen3-0.6b/abliterated S1_decay_ratio_16   final       0.425104 -0.145549  0.981289             False    0.142906                  0.5\n   qwen3-0.6b/instruct       S2_auc_norm  layerL       0.715358  0.134480  1.381852              True    0.058258                  0.3\nqwen3-0.6b/abliterated       S2_auc_norm  layerL      -0.926300 -1.759825 -0.141326              True    0.026642                 -0.4\n   qwen3-0.6b/instruct       S2_auc_norm   final       0.482651  0.050074  0.916595              True    0.069580                  0.3\nqwen3-0.6b/abliterated       S2_auc_norm   final       0.236061 -0.231548  0.681648             False    0.430433                  0.1\n\n--- cell 16 ---\n        statistic readout  did_mean     ci_lo     ci_hi   tost_p            verdict  n_prompts_for_pm020_margin_80pct_power\nS1_decay_ratio_16  layerL -2.333837 -3.572735 -1.036529 0.997750 DIRECTION_SPECIFIC                                    1880\nS1_decay_ratio_16   final -0.210376 -1.299738  0.902924 0.507073       INCONCLUSIVE                                    1429\n      S2_auc_norm  layerL -1.641658 -2.445109 -0.857555 0.998779 DIRECTION_SPECIFIC                                     731\n      S2_auc_norm   final -0.246590 -0.925430  0.408214 0.552064       INCONCLUSIVE                                     529\n\n--- cell 18 ---\nfamily size in this subset: 4  (published family size: 48)\n\n        statistic readout  wilcoxon_p  wilcoxon_p_holm            verdict\nS1_decay_ratio_16  layerL    0.004860         0.014580 DIRECTION_SPECIFIC\nS1_decay_ratio_16   final    0.869488         1.000000       INCONCLUSIVE\n      S2_auc_norm  layerL    0.001017         0.004066 DIRECTION_SPECIFIC\n      S2_auc_norm   final    0.570597         1.000000       INCONCLUSIVE\n\n--- cell 20 ---\nPRIMARY DiD  (instruct vs abliterated | S1_decay_ratio_16 | layerL | teacher-forced)\n  recomputed here : -2.334 [-3.573, -1.037]\n  archived run    : -2.334 [-3.573, -1.037]\n  delta vs archive: +0.00e+00\n\n  verdict         : DIRECTION_SPECIFIC\n  TOST p at +/-0.2: 0.9978  (archived 0.9978) -> equivalence NOT established\n  n_pairs         : 20 prompts\n  prompts needed for an equivalence verdict at +/-0.2: 1880\n\nReading: the direction effect is NOT the same in the safety-tuned instruct model as in its\nabliterated sibling -> the iteration-1 'generic mixing' null does not hold. But the test is\nbadly underpowered: no cell is equivalent at +/-0.20, and the sizing says ~2 orders of\nmagnitude more prompts would be needed to make a negative call.\n\n--- cell 22 ---\n====================================================================================================\n1.1  DIRECTION CONTRAST   log S(random) - log S(toward_refuse), paired over prompts\n====================================================================================================\n                 model         statistic readout  n_pairs  mean_log_diff   ci_lo   ci_hi  ratio_natural_scale  wilcoxon_p  cliffs_delta_paired  ci_excludes_zero\n   qwen3-0.6b/instruct S1_decay_ratio_16  layerL       20         1.2080  0.3037  2.2079               3.3468      0.0296                  0.3              True\nqwen3-0.6b/abliterated S1_decay_ratio_16  layerL       20        -1.1258 -2.2461  0.0270               0.3244      0.0897                 -0.3             False\n   qwen3-0.6b/instruct S1_decay_ratio_16   final       20         0.6355 -0.1545  1.4604               1.8879      0.2611                  0.1             False\nqwen3-0.6b/abliterated S1_decay_ratio_16   final       20         0.4251 -0.1455  0.9813               1.5297      0.1429                  0.5             False\n   qwen3-0.6b/instruct       S2_auc_norm  layerL       20         0.7154  0.1345  1.3819               2.0449      0.0583                  0.3              True\nqwen3-0.6b/abliterated       S2_auc_norm  layerL       20        -0.9263 -1.7598 -0.1413               0.3960      0.0266                 -0.4              True\n   qwen3-0.6b/instruct       S2_auc_norm   final       20         0.4827  0.0501  0.9166               1.6204      0.0696                  0.3              True\nqwen3-0.6b/abliterated       S2_auc_norm   final       20         0.2361 -0.2315  0.6816               1.2663      0.4304                  0.1             False\n\n====================================================================================================\n1.2  DIFFERENCE-IN-DIFFERENCES   instruct vs abliterated\n====================================================================================================\n        statistic readout  n_pairs  did_mean   ci_lo   ci_hi  tost_p  wilcoxon_p  wilcoxon_p_holm            verdict\nS1_decay_ratio_16  layerL       20   -2.3338 -3.5727 -1.0365  0.9978      0.0049           0.0146 DIRECTION_SPECIFIC\nS1_decay_ratio_16   final       20   -0.2104 -1.2997  0.9029  0.5071      0.8695           1.0000       INCONCLUSIVE\n      S2_auc_norm  layerL       20   -1.6417 -2.4451 -0.8576  0.9988      0.0010           0.0041 DIRECTION_SPECIFIC\n      S2_auc_norm   final       20", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] TOOL CALL — Bash · 2026-08-13 06:04:22 UTC

```
Cleanup, verify, write struct out:
rm -rf .nb_env && grep -c "raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-2/evaluation-1/demo/mini_demo_data.json" code_demo.ipynb && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
print('img cells:',[i for i,c in enumerate(nb['cells']) if any(o.get('output_type')=='display_data' for o in c.get('outputs',[]))])
print('errors:',[i for i,c in enumerate(nb['cells']) if any(o.get('output_type')=='error' for o in c.get('outputs',[]))])
" && ls -la && cat > .terminal_claude_agent_struct_out.json <<'EOF'
{
  "out_expected_files": {
    "notebook": "code_demo.ipynb",
    "mini_data_file": "mini_demo_data.json"
  }
}
EOF
echo done
```

### [51] TOOL RESULT — Bash · 2026-08-13 06:05:02 UTC

```
{"stdout": "1\nimg cells: []\nerrors: []\ntotal 3815\ndrwxr-xr-x 2 root root 1080146 Aug 13 06:05 .\ndrwxr-xr-x 6 root root 2003919 Aug 13 05:50 ..\n-rw-r--r-- 1 root root  679271 Aug 13 06:05 .repl_agent.ptylog\n-rw-r--r-- 1 root root    2251 Aug 13 05:52 build_mini.py\n-rw-r--r-- 1 root root   26213 Aug 13 05:54 build_nb.py\n-rw-r--r-- 1 root root   46040 Aug 13 06:04 code_demo.ipynb\n-rw-r--r-- 1 root root   67007 Aug 13 05:52 mini_demo_data.json\ndone", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [52] TOOL CALL — Edit · 2026-08-13 06:05:10 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py
OLD: import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
NEW: import matplotlib.pyplot as plt
```

### [53] TOOL RESULT — Edit · 2026-08-13 06:05:10 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_lYnzVulUmeG9/build_nb.py", "oldString": "import matplotlib\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt", "newString": "import matplotlib.pyplot as plt", "originalFile": null, "structuredPatch": [{"oldStart": 78, "oldLines": 8, "newStart": 78, "newLines": 6, "lines": [" import pandas as pd", " from scipy import stats", " ", "-import matplotlib", "-matplotlib.use(\"Agg\")", " import matplotlib.pyplot as plt", " \"\"\")", " "]}], "userModified": false, "replaceAll": false}
```

### [54] TOOL CALL — Bash · 2026-08-13 06:05:14 UTC

```
Rebuild and re-test notebook:
python3 build_nb.py && /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1|tail -1; time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [55] TOOL RESULT — Bash · 2026-08-13 06:13:58 UTC

```
{"stdout": "wrote code_demo.ipynb with 23 cells\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 121855 bytes to code_demo.ipynb\n\nreal\t3m56.428s\nuser\t0m12.760s\nsys\t0m1.590s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] TOOL CALL — Bash · 2026-08-13 06:14:05 UTC

```
Verify final notebook:
rm -rf .nb_env; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
print('img cells:',[i for i,c in enumerate(nb['cells']) if any(o.get('output_type')=='display_data' for o in c.get('outputs',[]))])
print('errors:',[i for i,c in enumerate(nb['cells']) if any(o.get('output_type')=='error' for o in c.get('outputs',[]))])
print('primary ok:', 'delta vs archive: +0.00e+00' in json.dumps(nb))
print('url ok:', 'round-2/evaluation-1/demo/mini_demo_data.json' in json.dumps(nb))
"; ls
```

### [57] TOOL RESULT — Bash · 2026-08-13 06:14:49 UTC

```
{"stdout": "img cells: [22]\nerrors: []\nprimary ok: True\nurl ok: True\nbuild_mini.py\nbuild_nb.py\ncode_demo.ipynb\nmini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [58] ASSISTANT · 2026-08-13 06:15:02 UTC

```
Done. All todos complete.

**Deliverables** (in the workspace):

- **`mini_demo_data.json`** (67 KB) — curated subset of ONE dataset: the archived `tier0_raw.json:lambda` table, restricted to the primary cell (`eps_c=0.1, p=16`, teacher-forced), the primary model pair (`qwen3-0.6b/instruct` vs `qwen3-0.6b/abliterated`), both steering directions × 20 prompts = **80 rows**, each carrying `decay_ratio_16` and `auc_norm` at both readouts, plus the artifact's published reference numbers for comparison.
- **`code_demo.ipynb`** (23 cells, executed, no errors) — reproduces **repair (1)**, the artifact's headline: the direction control recomputed on assumption-free statistics.
  - Cells: title → conditional install (numpy/pandas/scipy/matplotlib behind the `google.colab` guard) → imports → GitHub-URL loader with local fallback → `data = load_data()` → config → estimator library copied **verbatim** from `eval_lib.py` → `build_frames` → analysis 1.1 direction contrast → 1.2/1.3 DiD + TOST → 1.4 Holm → primary-number cell → tables + 2-panel figure.
  - Config runs at the **original** pre-registered values (`BOOT_REPS=10_000`, all 20 prompts, `EQ_MARGIN=0.20`) — no scaling-down was needed; notebook execution is seconds, ~4 min total wall clock dominated by pip installs, within the 600 s budget.
- Verified: the primary DiD reproduces the archived value **exactly** — `-2.334 [-3.573, -1.037]`, delta `+0.00e+00`, verdict `DIRECTION_SPECIFIC`, TOST p 0.9978, sizing 1,880 prompts.

One scoping note: the notebook's Holm family is 4 tests (this subset is one model pair, one channel), not the published 48 — the markdown states this explicitly and quotes the published adjusted p (0.214) so the demo can't be misread as showing the primary test surviving multiplicity.

`./.terminal_claude_agent_struct_out.json` written with `notebook: code_demo.ipynb`, `mini_data_file: mini_demo_data.json`.
```
