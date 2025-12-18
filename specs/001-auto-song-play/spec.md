```markdown
# Feature Specification: 自动打歌 - 选难度、自动切歌与自动打歌

**Feature Branch**: `001-auto-song-play`  
**Created**: 2025-12-19  
**Status**: Draft  
**Input**: User description: "可以手动选择一个打歌难度，然后开始自动切歌，然后自动打歌。完成这件事情之后，后续会增加“自动完成回合制战斗”的另一个该游戏玩法的基础功能"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 选择难度并开始自动打歌 (Priority: P1)

玩家在游戏界面打开后，手动在工具中选择当前歌曲的难度（例如 简单/普通/困难），点击“开始自动”后：工具自动执行切歌步骤（如需要切换到指定难度的谱面），并开始自动打歌（根据屏幕检测到的判定时点发送对应按键）。

**Why this priority**: 这是完成自动打歌的最小可行性功能，直接体现产品价值。

**Independent Test**: 在已知的测试歌曲上：手动选择难度→点击开始，观察工具是否在 5 秒内进入自动打歌状态并记录击中/未击中的统计数据；人工验证至少一个谱面能被自动完成一遍。

**Acceptance Scenarios**:

1. **Given** 游戏窗口已识别且按键映射已加载， **When** 用户选择难度并点击“开始自动”， **Then** 系统切换到指定难度（若游戏内可切）并开始自动打歌，输出实时命中统计。
2. **Given** 当前歌曲结束或失败， **When** 设置为“自动切歌”， **Then** 系统在 <= 3s 内切换到下一首并继续自动打歌（或在队列耗尽时停止）。

---

### User Story 2 - 自动切歌（队列与单首模式） (Priority: P2)

允许用户选择单曲自动播放或队列播放。队列播放时，工具应按顺序自动切换并继续自动打歌，提供暂停/跳过/停止控制。

**Why this priority**: 提高连贯体验，便于长时间练习或批量评估。

**Independent Test**: 配置 3 首测试歌曲到队列，启用队列播放并观察是否按顺序自动切换并继续打歌，记录切歌延迟与错误率。

**Acceptance Scenarios**:

1. **Given** 已配置队列， **When** 第一首结束， **Then** 系统在 <=3s 内加载并开始第二首的自动打歌。

---

### User Story 3 - 持续运行、暂停与中断 (Priority: P3)

提供可见的运行状态（运行/暂停/停止），并在暂停后能从暂停点恢复或从下一首重新开始。

**Why this priority**: 增强可控性，便于测试与故障恢复。

**Independent Test**: 在运行中点击暂停并等待 5 秒，再点击恢复，确认系统恢复到此前的自动状态或按预期行为继续。

**Acceptance Scenarios**:

1. **Given** 系统在自动打歌中， **When** 用户点击“暂停”， **Then** 系统应立即停止发送输入且保留当前状态以便恢复。

---

### Edge Cases

- 未能识别游戏窗口或窗口变化（最小化/遮挡）：应报告错误并进入安全停止状态。
- 输入映射缺失或按键冲突：提示用户并阻止进入自动模式。
- 判定延迟或帧数丢失导致长时间未击中：记录为失败并提供诊断日志。
 - 判定延迟或帧数丢失导致长时间未击中：记录为失败并提供诊断日志。
 - 游戏内防作弊检测或外部干预导致输入被阻止：仅记录事件并停止自动；不实现规避/反检测策略，向用户报告并安全退出自动模式。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统 MUST 提供手动选择当前歌曲难度的界面控件。
- **FR-002**: 系统 MUST 能检测并识别目标游戏窗口与当前播放歌曲的状态（开始/结束/失败/得分）。
- **FR-003**: 系统 MUST 在用户请求时执行“自动切歌”流程，并能在 <=3 秒内切换到下一首或目标难度的谱面（可测量的时延）。
- **FR-004**: 系统 MUST 提供自动打歌模块：基于屏幕判定在判定窗口内发送对应按键，支持可配置的时延补偿（latency compensation）。
- **FR-005**: 系统 MUST 提供运行状态控制（开始/暂停/停止/跳过）并持久保存用户的主要设置（如按键映射、难度偏好、队列）。
- **FR-006**: 系统 MUST 实时记录并展示命中统计（命中/错过/早按/晚按），并产出可导出的会话日志以供离线分析。
- **FR-007**: 系统 MUST 在遇到不可恢复的错误（窗口丢失、按键注入失败、检测异常）时，停止自动并记录错误原因。
- **FR-008**: 所有关键功能 MUST 带有自动化测试覆盖（单元、集成和验证用例），并在规范中定义每个用例的预期结果。
- **FR-009**: 输入注入方式：实现已在 `main.py` 中确定并实现，详见 `main.py` 的输入处理模块。无需在本规范中重新定义。

### Key Entities *(include if feature involves data)*

- **GameWindow**: 表示被识别的游戏窗口；属性：位置、尺寸、可见性、句柄/标识。
- **Song**: 表示单首曲目；属性：id、标题、难度列表、时长、队列位置。
- **Difficulty**: 难度级别枚举（例如：简单/普通/困难/专家），与曲目谱面关联。
- **AutoPlayer**: 自动打歌的执行器，负责判定检测、时序校准与输入发送。
- **InputMapper**: 管理按键映射与校准偏移。
- **Scheduler**: 管理队列、切歌时序与重试策略。
- **SessionMetrics**: 会话级统计与日志记录结构（命中率、平均偏移、错误计数）。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在典型测试环境中，用户选择难度并点击“开始自动”后，系统能在 <=5 秒内进入自动打歌状态（识别→切歌→开始发送输入）。
- **SC-002**: 自动切歌延迟（从上一首结束到下一首开始发送输入）应小于或等于 3 秒（在可达成情况下）。
- **SC-003**: 在受控测试曲目上，自动打歌的命中率会因用户的硬件与显示/延迟环境而异。工具提供可调参数 `Press Time` 以便用户在其设备上校准按键时序；默认参考值为 85%（仅作参考，不作为合并或发布门槛）。
- **SC-004**: 系统能连续运行 30 分钟以上而不崩溃，并在中途发生错误时安全停止且产生日志。
- **SC-005**: 所有功能点对应的自动化测试通过率为 100%（定义为：所有指定单元/集成/验收用例通过）。

## Assumptions

- 用户会在开始前手动选择目标游戏窗口或授权工具识别该窗口（存在可捕获的屏幕区域）。
- 按键映射和外设布局由用户配置并保存；工具提供校准界面以适配不同布局。
- 本规范不定义反作弊规避策略；若需要支持应作为单独需求讨论（参见上文 NEEDS CLARIFICATION）。

## Testing Notes

- 为每个用户故事编写可重复的验收测试用例，测试在真实游戏环境或模拟环境中运行并记录命中统计。
- 对自动打歌模块进行回归测试：一组代表性曲目 + 难度组合，记录命中率与延迟，验证目标阈值。

## Next Steps / Roadmap

- 实现 P1（选择难度 + 自动打歌）并验证核心成功标准。
- 在 P1 稳定后实现 P2（队列与自动切歌）与 P3（暂停/恢复），随后扩展到“自动完成回合制战斗”作为独立 feature 分支。

``` 
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
