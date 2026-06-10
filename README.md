# SE Skills

**面向芯片原厂 SE（系统工程师 / 应用架构师）的工作流技能。**

Skills 将资深系统工程师在芯片应用项目中所遵循的工作流、质量门禁和最佳实践进行编码封装，使 AI 助手能够在 SE 工作流的每个阶段 — 从原始需求分解、架构设计、规格撰写、跨部门评审到可追溯性验证 — 一致地遵循这些规范。

---

## 命令

提供 5 个斜杠命令，映射到 SE 工作流的各个阶段。每个命令会自动激活相应的技能。

| 你在做什么 | 命令 | 核心原则 |
|-------------------|---------|---------------|
| 分解原始需求 | `/se-requirements` | 每个需求可追溯、可测试、有归属 |
| 设计系统架构 | `/se-architecture` | 每个接口精确定义，每个决策有据可查 |
| 撰写正式规格 | `/se-spec` | 架构 + 需求 → SOD、HW-SW IF Spec、测试方案 |
| 跨部门评审 | `/se-review` | 四视角对抗式审查（HW/SW/Test/System） |
| 验证可追溯性 | `/se-traceability` | 跨产物差距分析，覆盖率报告 |

技能也会根据你正在做的事情自动激活 — 设计架构会触发 `architecture-design`，需求存在矛盾会触发 `requirements-decompose`，以此类推。

---

## 快速开始

<details>
<summary><b>Claude Code（推荐）</b></summary>

**通过 Marketplace 安装：**

```
/plugin marketplace add ddddjaak/se-skills
/plugin install se-skills@se-skills
```

> **遇到 SSH 错误？** Marketplace 通过 SSH 克隆仓库。如果你没有在 GitHub 上设置 SSH 密钥，请先[添加 SSH 密钥](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)，或使用完整的 HTTPS URL 强制走 HTTPS 克隆：
> ```bash
> /plugin marketplace add https://github.com/ddddjaak/se-skills.git
> /plugin install se-skills@se-skills
> ```

**本地 / 开发环境：**

```bash
git clone https://github.com/ddddjaak/se-skills.git
claude --plugin-dir /path/to/se-skills
```

</details>

<details>
<summary><b>Cursor</b></summary>

将任意 `SKILL.md` 复制到 `.cursor/rules/` 目录下，或引用整个 `skills/` 目录。技能是纯 Markdown 格式，可与任何支持规则文件的 AI 编码工具配合使用。

</details>

<details>
<summary><b>Gemini CLI</b></summary>

以原生技能方式安装，实现自动发现；或添加到 `GEMINI.md` 中以获得持久上下文。

**从仓库安装：**

```bash
gemini skills install https://github.com/ddddjaak/se-skills.git --path skills
```

**从本地克隆安装：**

```bash
gemini skills install ./se-skills/skills/
```

</details>

<details>
<summary><b>Windsurf</b></summary>

将技能内容添加到你的 Windsurf 规则配置中。技能是结构化的工作流，可直接作为规则文件使用。

</details>

<details>
<summary><b>OpenCode</b></summary>

通过 AGENTS.md 和 `skill` 工具使用基于 agent 驱动的技能执行模式。将技能目录引入即可自动发现。

</details>

<details>
<summary><b>GitHub Copilot</b></summary>

将技能内容放入 `.github/copilot-instructions.md` 作为持久上下文。每个 SKILL.md 都是独立的工作流，可单独或组合使用。

</details>

<details>
<summary><b>Codex / 其他 Agent</b></summary>

技能是纯 Markdown 格式 — 可以与任何接受系统提示或指令文件的 agent 配合使用。每个 SKILL.md 都是自包含的工作流：概览 → 触发条件 → 分步流程 → 常见合理化借口 → 红旗信号 → 验证检查清单。

</details>

---

## 全部 5 个技能

上述命令是入口点。本包包含 5 个 SE 工作流技能加 1 个 `using-se-skills` 元技能。每个技能都是一个结构化的工作流，包含步骤、验证门禁和反合理化表。你也可以直接引用任何技能。

### 元技能 — 发现该用哪个技能

| 技能 | 功能 | 使用场景 |
|-------|-------------|----------|
| [using-se-skills](skills/using-se-skills/SKILL.md) | 将任务映射到正确的 SE 技能工作流，并定义共享操作规则（9 项核心行为、10 个失败模式、5 条技能规则） | 开始一个 SE 会话，或不确定该用哪个技能时 |

### 定义 — 明确要构建什么

| 技能 | 功能 | 使用场景 |
|-------|-------------|----------|
| [requirements-decompose](skills/requirements-decompose/SKILL.md) | 六步流程（收集→分类→解决冲突→派生→分配归属→验证）：将原始异构输入（PRD、芯片数据手册、行业标准、客户规格）转化为结构化、可追溯的系统需求文档 | 新项目启动且需求分散在多个文档中；多个输入源存在矛盾；需要为每条需求分配归属（HW/SW/System） |

### 设计 — 架构方案与模块分解

| 技能 | 功能 | 使用场景 |
|-------|-------------|----------|
| [architecture-design](skills/architecture-design/SKILL.md) | 五步流程（分解→接口→约束→权衡→文档）：模块分解、精确接口定义（含时序/错误处理/并发模型）、跨域约束分析、设计决策记录（含被拒绝方案和接受的下行风险） | 系统需求已确认，需要设计模块划分；评估架构替代方案；下游规格撰写发现缺失的架构决策 |

### 文档 — 撰写正式规格

| 技能 | 功能 | 使用场景 |
|-------|-------------|----------|
| [spec-authoring](skills/spec-authoring/SKILL.md) | 从架构和需求生成三类正式规格文档：软件概要设计（SOD）、软硬件接口规格（HW-SW IF Spec）、测试方案（Test Plan） | 架构已确认，固件团队需要实现规格；软硬件边界需要明确定义；验证团队需要测试程序 |

### 验证 — 发布前的质量门禁

| 技能 | 功能 | 使用场景 |
|-------|-------------|----------|
| [design-review](skills/design-review/SKILL.md) | 四视角（HW/SW/Test/System）对抗式审查，每一位审查者独立考察同一份产物，交叉比对发现分歧。包含角色指派、逐章节审查、差异分类（问题/建议/观察）、评审报告生成 | 任何 SE 产物在分发前需要跨部门评审；审查同事的架构设计；里程碑前确认设计质量 |
| [traceability-matrix](skills/traceability-matrix/SKILL.md) | 跨产物可追溯性分析 — 需求→设计→测试的覆盖率缺口检测、孤立产物识别、追溯报告生成 | 里程碑评审前验证覆盖率；检测无测试覆盖的需求；发现无需求来源的设计元素 |

---

## Agent 角色

用于针对性审查的预配置专业角色，覆盖 SE 工作流的五个审查视角：

| Agent | 角色 | 视角 |
|-------|------|-------------|
| [system-architect](agents/system-architect.md) | 资深系统架构师 | 系统一致性、约束满足、跨域集成、风险暴露 |
| [hw-domain-expert](agents/hw-domain-expert.md) | 硬件域专家 | 引脚分配、电源域、时钟树、信号完整性、电气合规 |
| [fw-domain-expert](agents/fw-domain-expert.md) | 固件域专家 | 驱动接口、RTOS 集成、内存映射、启动流程、并发模型 |
| [verification-engineer](agents/verification-engineer.md) | 验证质量工程师 | 可测试性、测试覆盖率、追溯完整性、验证方法论 |
| [compliance-reviewer](agents/compliance-reviewer.md) | 合规安全审查员 | 法规合规、功能安全、安全控制、隐私、行业标准 |

五个角色可以通过 `/se-review` 并行扇出（parallel fan-out），对同一份 SE 产物进行五视角对抗式审查，合并生成分类问题报告。也可以单独调用任一角色进行针对性审查。

---

## 技能的工作原理

每个技能都遵循一致的结构：

```
┌─────────────────────────────────────────────────┐
│  SKILL.md                                       │
│                                                 │
│  ┌─ 前置元数据 ──────────────────────────────┐  │
│  │ name: 小写连字符命名                      │  │
│  │ description: 引导 agent 完成 [任务]。     │  │
│  │              使用场景：…                  │  │
│  └───────────────────────────────────────────┘  │
│  概览             → 这个技能做什么              │
│  使用场景         → 触发条件                    │
│  流程             → 逐步工作流                  │
│  常见合理化借口   → 借口 + 反驳                 │
│  红旗信号         → 出问题的迹象                │
│  验证             → 证据要求                    │
└─────────────────────────────────────────────────┘
```

**核心设计选择：**

- **是流程，不是散文。** 技能是 agent 遵循的工作流，不是让他们阅读的参考文档。每个技能都有步骤、检查点和退出标准。
- **反合理化。** 每个技能都包含一个常见借口表，列出 agent 用来跳过步骤的借口（例如 "需求大概清楚了，直接开始设计吧"），并附有文档化的反驳。
- **验证不容妥协。** 每个技能都以证据要求结尾 — 冲突解决日志、接口完整性检查清单、人类确认门禁。"看起来没问题" 永远不够。
- **渐进式披露。** `SKILL.md` 是入口点。每个技能控制在 500 行以内，深入细节在流程步骤中展开，不依赖外部参考文件。
- **独立可组合。** 五个技能可以端到端串联（需求→架构→规格→评审→追溯），也可以独立使用 — 单跑 `design-review` 审查同事的产物，或单跑 `traceability-matrix` 做里程碑前的覆盖率检查。

---

## 项目结构

```
se-skills/
├── skills/                            # 5 个 SE 工作流技能 + 1 个元技能
│   ├── using-se-skills/               #   元技能：如何使用本包
│   ├── requirements-decompose/        #   定义：原始输入 → 结构化需求
│   ├── architecture-design/           #   设计：需求 → 架构方案
│   ├── spec-authoring/                #   文档：架构 → 正式规格
│   ├── design-review/                 #   验证：四视角对抗式评审
│   └── traceability-matrix/           #   验证：跨产物可追溯性分析
├── agents/                            # 5 个专业审查角色
├── .github/                           # Issue/PR 模板
├── .claude-plugin/                    # 插件清单
│   ├── plugin.json
│   └── marketplace.json
├── .claude/commands/                  # 5 个斜杠命令（Claude Code）
│   ├── se-requirements.md
│   ├── se-architecture.md
│   ├── se-spec.md
│   ├── se-review.md
│   └── se-traceability.md
├── docs/                              # 产出物模板和参考文档
├── AGENTS.md                          # AI Agent 指令文件
├── CLAUDE.md                          # 仓库结构指南
├── CONTRIBUTING.md                    # 贡献指南
├── CHANGELOG.md                       # 变更日志
└── LICENSE                            # MIT
```

---

## 为什么需要 SE Skills？

AI 编程助手默认走最短路径 — 在系统工程师的工作中，这往往意味着跳过需求分解直接开始"设计"、用 "I2C" 三个字母代替完整的接口规格、默默解决需求矛盾而不追问、或者生成充满空章节的规格文档。

芯片应用项目中的错误发现越晚，修复成本越高 — 需求阶段的歧义用一次对话就能澄清，集成阶段才发现架构假设错误则需要数周返工。

每个技能都编码了资深 SE 来之不易的工程判断：

- **需求分解** — 每个需求必须可量化、可测试、有归属。模糊需求用 GUESS 模式（提出量化解释 + 推理 → 让干系人确认/纠正），比开放式提问更快更有效。
- **架构设计** — 每个接口必须定义数据格式、时序边界、错误处理和并发模型。每个非平凡决策必须记录被拒绝的替代方案和接受的下行风险。
- **规格撰写** — 遵循 "Numbers, Not Adjectives"（数字，而非形容词）原则。SOD 中的每个模块描述都追溯到架构接口 ID。测试方案中的每个测试用例都追溯到需求 ID。
- **设计评审** — 一人评审自己的产物会看到自己期望看到的东西。四视角对抗式评审（HW/SW/Test/System）确保每个视角发现其他视角的盲区。
- **可追溯性矩阵** — 在全链条上运行，而不只是在最后。每个产物产出后立即检查覆盖率，晚期发现的缺口修复成本呈指数增长。

这些不是泛泛的提示词 — 它们是那种有见地的、以流程为导向的工作流，能够区分经过工程验证的系统设计和拍脑袋的原型方案。

---

## 贡献

技能应该 **具体**（可操作的步骤，而非模糊的建议）、**可验证**（明确的退出标准和证据要求）、**经过实战检验**（基于真实 SE 工作流）以及 **精简**（只包含引导 agent 所需的内容）。

每个技能遵循标准格式：YAML 前置元数据（name, description）→ 概览 → 使用场景 → 分步流程 → 与其他技能的交互 → 常见合理化借口 → 红旗信号 → 验证检查清单。

详见 [CONTRIBUTING.md](CONTRIBUTING.md) 了解完整的贡献指南、技能格式规范和 PR 流程。

---

## 许可证

MIT — 在你的项目、团队和工具中自由使用这些技能。
