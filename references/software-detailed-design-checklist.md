# Software Development Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | DJ | 初版 | 2023-04-24 |

- **版本**: A01
- **日期**: 2023/04/24
- **编制**: DJ

## 目的 (Objectives)

为软件开发评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for software development.

## 适用范围 (Scope)

适用于公司内部软件模块评审。
This document is only for internal use.

## 参考文件 (Reference)

https://www.nasa.gov/seh/appendix-c-how-to-write-a-good-requirement

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 | 评估 |
|------|--------|------|
| 1.0 | Configuration Items Check（过程域配置项检查） | NO |
| 2.0 | Basic Information Check（基本的信息检查） | NO |
| 3.0 | Detail Design Rule Check（详细设计检查） | NO |

### 1.0 Configuration Items Check（需求过程域配置项检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC2 | 是否有详细设计输出 ( 在线系统承载或线下文档 ) 和模块单元 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Basic Information Check（基本的信息检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| BIC1 | 文档描述是否包含编写目的、项目背景、缩写词定义、专业术语定义、参考资料？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC2 | 架构设计输出物的版本是否记录清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 3.0 Detail Design Rule Check（详细设计检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| DRC1 | 是否使用图表的方式对模块内部结构进行定义，且分解到文件和函数级别，体现出函数的调用关系。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DRC2 | 模块设计是否满足如下设计原则：高内聚，低耦合，通用功能设计，服从命名规则。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DRC3 | 功能概要是否体现该软件模块所有的函数，包括函数名称，函数功能。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DRC4 | 功能概要是否体现如下全局信息：数据类型，全局变量，宏符号。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DRC5 | 函数详细设计是否清晰定义函数传入参数的名称、含义、数据类型、取值范围，以及返回值的类型、含义、取值范围。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DRC6 | 函数详细设计是否体现函数实现逻辑的流程图（逻辑简单的函数可忽略） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DRC7 | 如果软件单元之间有状态转换、顺序调用、消息序列等动态行为，是否有体现 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

