# SE Skills — 文档目录

本目录存放 SE 工作流产出的参考模板和指南。

## 目录结构

SE 技能会将产出物保存到以下子目录（由技能在工作流中自动创建）：

```
docs/
├── README.md                        # 本文件
├── requirements/                    # requirements-decompose 产出
│   └── [project]-system-requirements.md
├── architecture/                    # architecture-design 产出
│   └── [project]-architecture-design.md
├── specifications/                  # spec-authoring 产出
│   ├── [project]-software-outline-design.md
│   ├── [project]-hw-sw-interface-spec.md
│   └── [project]-test-plan.md
├── reviews/                         # design-review 产出
│   └── [project]-[artifact]-review-report.md
└── traceability/                    # traceability-matrix 产出
    └── [project]-traceability-matrix.md
```

## 技能产出物说明

### 系统需求文档

`docs/requirements/[project]-system-requirements.md`

由 `requirements-decompose` 生成。包含：需求表（ID、来源、域、类型、归属、验证者、状态）、派生需求、冲突解决日志、缺口日志、可追溯性种子。

### 架构设计文档

`docs/architecture/[project]-architecture-design.md`

由 `architecture-design` 生成。包含：系统框图、模块定义、接口规格、约束分析、设计决策记录、风险注册表、未决事项列表。

### 规格文档

由 `spec-authoring` 生成，包含三类：

- **软件概要设计 (SOD):** `docs/specifications/[project]-software-outline-design.md`
- **软硬件接口规格:** `docs/specifications/[project]-hw-sw-interface-spec.md`
- **测试方案:** `docs/specifications/[project]-test-plan.md`

### 评审报告

由 `design-review` 生成：`docs/reviews/[project]-[artifact]-review-report.md`

### 可追溯性矩阵

由 `traceability-matrix` 生成：`docs/traceability/[project]-traceability-matrix.md`

## 注意事项

- 所有产出物应在版本控制之下
- 文档名称中的 `[project]` 替换为实际项目名称
- 每个技能在执行过程中会自动提示用户确认保存路径
- 产出物格式详见各技能的 `## Output` 章节
