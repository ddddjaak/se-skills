# 方案架构设计 Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | TJ | beta | 2025-04-28 |

- **日期**: 2025/04/28
- **编制**: \< 应用SE \>

## 目的 (Objectives)

为方案架构设计文档评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for software development.

## 适用范围 (Scope)

适用于公司内部方案架构设计文档的评审。
This document is only for internal use.

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 | 评估 |
|------|--------|------|
| 1.0 | 文档基础信息 | NO |
| 2.0 | 需求来源检查 | NO |
| 3.0 | 系统概述检查 | NO |
| 4.0 | 系统架构设计检查 | NO |

### 1.0 文档基础信息

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| 1.1 | 标题与版本号：是否明确标注文档标题、版本号、发布日期？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | 应用 SE | SW Lead |
| 1.2 | 方案版本变更：是否记录清晰？修订记录是否有？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 1.3 | 方案承接需求：是否条目化？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 1.4 | 术语表：是否定义专业术语、缩写和符号？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 1.5 | 如有特殊需求是否已标注出来？ |  |  |  |  |  |  |  |

### 2.0 需求来源检查

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| 2.1 | 方案承接的每条需求是否都清晰标注来源？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 3.0 系统概述检查

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| 3.1 | 项目背景：是否说明项目的背景、需求和目标？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 3.2 | 功能需求：是否列出系统核心功能（与需求文档一致）？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 3.3 | 非功能需求：是否涵盖性能、功耗、实时性、安全性、可靠性等要求？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 3.4 | 系统边界：是否明确系统与外部设备/环境的交互关系？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 4.0 系统架构设计检查

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| 4.1 | 总架构图：是否有清晰的架构框图？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.2 | 硬件架构图：是否有且清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.3 | 软件架构图：是否有且清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.4 | 模块划分：是否划分核心模块（如传感器、通信、存储、处理单元等）？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.5 | 模块职责：是否定义每个模块的功能和职责？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.6 | 关键子场景：是否描述清楚了关键子场景逻辑？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.7 | 关键子场景：是否描述清楚了关键子场景的数据交互方式？输入输出要求？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.8 | 关键子场景：如果有核心算法设计，是否描述清楚了核心算法？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.9 | 协议设计：是否描述清楚了协议内容，包括帧格式、时序要求，以及数据ID定义是否清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.1 | 协议设计：如果由单独文件承载协议详情，是否提供相关协议文件？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| 4.11 | 工具：是否有且清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

