<!--
Sync Impact Report

- Version change: unversioned/template -> 1.0.0
- Modified principles: [PRINCIPLE_1_NAME] -> Code Quality and Maintainability
- Modified principles: [PRINCIPLE_2_NAME] -> Test-First & Coverage Standards
- Modified principles: [PRINCIPLE_3_NAME] -> User Experience Consistency
- Modified principles: [PRINCIPLE_4_NAME] -> Performance & Resource Requirements
- Modified principles: [PRINCIPLE_5_NAME] -> Observability, Versioning & Release Discipline
- Added sections: Standards & Constraints; Development Workflow
- Removed sections: none
- Templates requiring updates:
	- [.specify/templates/tasks-template.md](.specify/templates/tasks-template.md): ✅ updated
	- [.specify/templates/plan-template.md](.specify/templates/plan-template.md): ✅ checked
	- [.specify/templates/spec-template.md](.specify/templates/spec-template.md): ✅ checked
	- [.specify/templates/commands/](.specify/templates/commands/) : ⚠ pending (directory missing)
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): original ratification date unknown; please record when available
	- Verify any agent-specific command docs under `.specify/templates/commands/` and update names if present
-->

# HBR-AutoBeat Constitution

## Core Principles

### Code Quality and Maintainability
All production code MUST be clear, well-structured, and maintainable. Specific rules:
- Use automated linters and formatters on every PR (e.g., `black`/`prettier`, `flake8`, or equivalent). Linting failures MUST block merges.
- Prefer explicit types where the language supports them (e.g., `mypy` in Python). Type-checking SHOULD run in CI and any critical type errors MUST be resolved before merge.
- Code reviews are REQUIRED for all non-trivial changes; at least one approver other than the author is required. Large changes MUST include a design note and incremental plan.
- Keep functions and modules small and single-purpose; aim for low cyclomatic complexity and clear interfaces.
- 部署与分发：最终产物应提供单个 Windows 可执行文件（`.exe`）作为首选分发形式。为了保证最终文件体积可接受并在低配置机器上可用，开发时务必：
	- 优先选择无原生依赖或体积小的库；避免引入大型运行时或非必要的二进制依赖。
	- 在保证功能的前提下优先实现轻量化实现，并在发布说明中记录最终二进制大小与已知运行时约束。

- 开发环境与脚本约定：所有针对本仓库的本地开发与构建说明应优先支持 Windows PowerShell（兼容 PowerShell Core / pwsh）。PowerShell 命令与脚本示例应在文档中明确给出，且 CI 中的 Windows 步骤应复现相同的 PowerShell 命令语义。


### Test-First & Coverage Standards
Testing is non-negotiable. Rules:
- Tests MUST be authored before or alongside implementation (Test-First / TDD). Tests MUST fail before feature code is added, then pass after implementation.
- Include unit tests, integration tests, and contract tests as applicable. CI pipelines MUST run the full test suite on every PR.
- Minimum code coverage target: 80% for new code; coverage requirements MAY be stricter for critical modules (security, payments, data integrity).
- Test data and test harnesses MUST be deterministic and isolated; flaky tests are NOT acceptable and MUST be fixed promptly.

### User Experience Consistency
The product's UX (CLI, GUI, APIs) MUST be consistent and accessible:
- Error messages MUST be actionable, localized where applicable, and include telemetry-friendly identifiers for debugging.
- Public APIs and CLI interfaces MUST be stable across minor releases; breaking changes MUST follow the release discipline in Governance.
- Accessibility and internationalization considerations MUST be included in designs for user-facing features.
- Design patterns (naming, layout, interaction) MUST follow project-wide style guides; deviations MUST be justified.

### Performance & Resource Requirements
Performance goals and resource constraints MUST be explicit and measurable:
- Define and document performance targets (e.g., latency p95/p99, throughput, memory usage) in feature plans.
- Benchmarks and profiling MUST be included for performance-sensitive changes; regressions MUST be prevented by CI gates where feasible.
- Resource limits (memory, disk, CPU) for deployed components MUST be declared; components MUST degrade gracefully when limits are approached.

### Observability, Versioning & Release Discipline
Operational discipline is required to ensure reliability and safe evolution:
- Structured logging, metrics, and distributed tracing MUST be present for services and long-running processes.
- Follow semantic versioning for published artifacts: MAJOR.MINOR.PATCH. Definitions:
	- MAJOR: incompatible API or governance changes that break consumers.
	- MINOR: new, backward-compatible functionality or material expansion of guidance.
	- PATCH: non-functional changes, clarifications, typo fixes.
- Breaking changes (MAJOR) MUST be announced, documented with migration guidance, and have an explicit rollout plan.
- Release notes and changelogs MUST be maintained for every release; changelogs MUST reference related spec and plan documents.

## Standards & Constraints
This section captures mandatory cross-cutting constraints:
- Supported runtime for core project: Python 3.11+ (or explicit alternative documented in feature plan). If another runtime is chosen, it MUST be documented in the plan.
- CI MUST run linters, type checks, unit tests, integration tests, and packaging checks on every PR.
- Security-sensitive code (auth, crypto, data export) MUST be threat-modeled and reviewed by a security-aware reviewer.
- Dependency updates MUST be audited; critical security updates MUST be applied within 7 days of disclosure unless a documented exception exists.

## Development Workflow
Processes that enforce the principles above:
- Every feature MUST have a plan and spec: use the templates in `.specify/templates` and include a Constitution Check section.
- Branching: use short-lived feature branches; PR titles MUST reference the spec or plan (e.g., `spec: add XYZ` or `feat(US1): ...`).
- PR Gates: passing CI, successful linters/typechecks, and at least one approving reviewer are REQUIRED before merge.
- Rollbacks and emergency fixes MUST include a postmortem and an update to the relevant spec/plan documenting the cause and mitigation.

## Governance
Amendment procedure and compliance expectations:
- Amendments are proposed as a pull request against `.specify/memory/constitution.md` with rationale and migration notes.
- Amendment review: 7-day minimum public review period; approval requires at least two core maintainers or a simple majority of the active maintainers team when the core team is larger.
- Versioning policy: apply semantic versioning to the constitution per the MAJOR/MINOR/PATCH rules described above. This document is now `1.0.0` on adoption.
- Compliance: All feature plans MUST include a Constitution Check section; CI and reviewers MUST verify constitution compliance for each PR. Non-compliant PRs MUST include a documented exception approved by maintainers.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2025-12-19
