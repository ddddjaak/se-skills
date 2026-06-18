# Software Development Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | Dingzx | beta | 2023-12-06 |
| A02 | DJ | 1.增加表格外框，对齐行列内容，使模版外观更整齐； 2.针对汽车软件开发完善检查内容； | 2023-04-24 |
| A03 | Liuyb | 增加FOSS检查项 | 2024-01-29 |

- **版本**: A03
- **日期**: 2024/01/29
- **编制**: Liuyb

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
| 3.0 | Architecture Chart Check （需求概述检查） | NO |
| 4.0 | Interface Design Check （接口设计检查） | NO |
| 5.0 | Design Check（设计检查） | NO |

### 1.0 Configuration Items Check（需求过程域配置项检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC2 | 是否有接口需求规范(Optional，如不需要请备注) | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC3 | 是否有概要设计输出(在线系统承载或线下文档) | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC4 | 是否有FOSS评估报告 (Optional ，若涉及，需提供 ) | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Basic Information Check（基本的信息检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| BIC1 | 概要设计文档需要包含模块需求概述、模块架构设计、软件静态设计、软件动态设计、接口设计、设计约束等主要章节描述。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC2 | 需要描述软件概要信息，包含主要功能，性能，主要接口等 （相当于软件简介） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC3 | 概要设计输出物的版本是否记录清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC4 | 对于使用的到开源组件，是否有明确的说明 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 3.0 Requirements Overview Check （需求概述检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| ROC1 | 承接的需求是否描述完备 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 4.0 Interface Design Check（接口设计检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| IDC1 | 接口设计检查： - 需要描述软件外部接口 - 函数接口可按模块罗列。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| IDC2 | 接口描述检查：要素是否完备 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| IDC3 | 接口时序图检查： - 需要包含主要的功能 -从时序图判断设计是否存在冲突、冗余等问题 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 5.0 Design Check （设计检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| DC1 | 架构设计是否合理，是否清晰展示软硬件架构关系 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DC2 | 源文件描述是否清晰，完备 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DC3 | 头文件引用关系图是否表达准确无误 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DC4 | 动态设计： - 有展示软硬件功能流转图 -清楚描述运行模式、进程通信、中断等关系 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| DC5 | 设计约束检查： - 硬件约束 - 时间约束设计 -性能约束设计 -内存使用设计 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

