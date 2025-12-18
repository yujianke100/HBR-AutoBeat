---
description: "Implementation tasks for feature 001-auto-song-play"
---

# Tasks: 自动打歌 - 选难度、自动切歌与自动打歌

**Feature**: `001-auto-song-play`  
**Spec**: [spec.md](spec.md)  
**Checklist**: [checklists/requirements.md](checklists/requirements.md)

## Phase 1: Developer UX & Code Hygiene (P0)

- [X] T001-1 Configure formatting & linting: update `pyproject.toml` to include `black`, `isort`, `flake8`, `mypy` (if desired) and add pre-commit hooks. (files: `pyproject.toml`, `.pre-commit-config.yaml`)
- [X] T001-2 Run formatter across repo and fix issues; add CI lint/check job. (commands: `black .`, `flake8`)

## Phase 2: Localization & Code Organization (P0)

 - [X] T002-1 Create `i18n/` directory with `zh-CN.yml` and `en-US.yml` and extract all UI strings into these files. (files: `i18n/*.yml`)
 - [X] T002-2 Add small `i18n` loader module (`src/i18n.py` or `i18n/__init__.py`) to select language at runtime and provide `t(key)` helper.

## Phase 3: UI Refactor - Main/Feature Screens (P0)

- [ ] T003-1 Create `ui/` package and move existing UI code into `ui/main_window.py` and `ui/auto_song.py`. (files: `ui/*.py`)
- [ ] T003-2 Implement main window layout: first row contains `识别游戏窗口` + `语言切换` buttons; below is list of feature entry buttons (first entry: 自动打歌)。
- [ ] T003-3 Implement logic to load `ui/auto_song.py` as secondary view when entry clicked (keep back/navigation control).
- [ ] T003-4 Add persistent config storage (`config.json`) and small helper module `src/config.py` for reading/writing settings.

## Phase 4: Documentation & Release Artefacts (P0)

- [ ] T004-1 Create `README.md` (English) and `README_zh-CN.md` (Chinese) using `./icon` images; add quickstart, usage, configuration and troubleshooting sections.
- [ ] T004-2 Add `LICENSE` (suggest MIT unless otherwise requested) and `RELEASE.md` template with changelog guidance.
- [ ] T004-3 Add `docs/` short HOWTO for contributors: running formatters, tests, and creating releases.

## Phase 5: Continuous Play UI (P1)

- [ ] T005-1 Add `连续打歌` button to `ui/auto_song.py` secondary view; default state: disabled/greyed-out when preconditions not satisfied.
- [ ] T005-2 Add hover tooltip for disabled state: "请先识别游戏窗口并进入选歌界面" (localized via `i18n`).
- [ ] T005-3 Implement enabling/disabling rules: enabled only when `GameWindow` recognized and UI reports in '选歌界面' state.

## Phase 6: Continuous Play Settings Dialog (P1)

- [ ] T006-1 Implement settings dialog UI that appears when `连续打歌` clicked: top hint line, two large toggles, a small divider, difficulty dropdown, and repeat-count numeric input with spinner/wheel support.
- [ ] T006-2 Toggle A: "打新曲子（单曲，依次刷EASY, NORMAL, HARD，然后再打两次EASY）"; Toggle B: "连续刷歌（每首当新歌）". When either large toggle is ON, subsequent detailed settings should be disabled (greyed).
- [ ] T006-3 Difficulty selector: choices `EASY, NORMAL, HARD, EXPERT` (default maintain current config). Repeat count: integer >=1, default 1.
- [ ] T006-4 Validate inputs and persist settings to `config.json` upon OK; cancel should not persist.

## Phase 7: Song Completion Detection & External Cut-Song Logic (P1)

- [ ] T007-1 Design detection heuristics: detect '结算页面' vs '失败页面' vs '选歌页面' using screen templates / pixel checks. Add modular detectors under `src/detectors.py`.
- [ ] T007-2 Implement robust completion detection: only treat play as 'completed' when settlement screen pattern observed; treat failure when failure pattern observed; fallback: timeouts and conservative stop.
- [ ] T007-3 Implement external cut-song flow: record current selected song identifier, send `Down` (or mapped) key, confirm selection via reading selected element, then choose difficulty and start song. Retry logic if confirmation fails.
- [ ] T007-4 Add telemetry/logging hooks to record decisions for diagnostics (`logs/sessions/*.log`).

## Phase 8: Tests, CI & QA (P1)

- [ ] T008-1 Add unit tests for `i18n` loader, `config` persistence, detectors (mocked), and scheduling logic. (tests in `tests/unit/`)
- [ ] T008-2 Add integration tests for UI flows using a lightweight UI test harness or mocked window state. (tests in `tests/integration/`)
- [ ] T008-3 Add CI pipeline job to run linters, type checks, and tests on PRs.

## Phase 9: Finalize & Review (P1)

- [ ] T009-1 Manual QA checklist run: basic scenarios for P1/P2/P3. Record results in `specs/001-auto-song-play/checklists/manual_qa.md`.
- [ ] T009-2 Prepare PR: include description, link to spec, and reviewer checklist.

## Notes and Constraints

- Keep UI logic OS-agnostic as much as possible; window detection is platform-specific (currently Windows). Encapsulate platform calls behind a small adapter.
- Avoid implementing anti-cheat evasion; record and stop on detection per spec.
- Use `Press Time` parameter from existing `main.py` for timing calibration rather than hard-coded delays.
