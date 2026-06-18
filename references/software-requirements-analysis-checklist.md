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
| 1.0 | Configuration Items Check（需求过程域配置项检查） | NO |
| 2.0 | Basic Information Check（基本的信息检查） | NO |
| 3.0 | Requirement Traceability Check（需求来源检查） | NO |
| 4.0 | Requirement Normalization Check（需求规范检查） | NO |
| 5.0 | Requirement Classification Check（需求分类检查） | NO |

### 1.0 Configuration Items Check（需求过程域配置项检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC2 | 是否有接口需求规范(Optional，如不需要请备注) | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC3 | 是否有需求分析输出(在线系统承载或线下文档) | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Basic Information Check（基本的信息检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| BIC1 | 需求是否条目化？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC2 | 需求字段是否按要求填写？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC3 | 需求分析输出物的版本是否记录清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC4 | 如有特殊需求是否已标注出来？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 3.0 Requirement Traceability Check（需求来源检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| RTC1 | 每条需求是否都清晰标注来源？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RTC2 | 来源是否超出之前识别的范围？(芯片手册，标杆产品分析，标准规范里的要求) | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 4.0 Requirement Normalization Check（需求规范检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| RNC1 | 需求的正确性，需求是不是定义的系统真正需要的功能？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC2 | 需求的明确性，需求是否描述清晰，易于理解，并且没有歧义。不同的人应该有同样的认识？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC3 | 需求的完整性，单个的需求是否包含所有必要的信息来理解需求本身？单个的需求是否覆盖了所需的输入数据，事件，或系统环境？需求里面提到的术语是否有预先定义？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC4 | 需求的可验证性，需求是否可被充分的测试？可以从需求出发，清晰地确立测试目标以验证需求是否被满足？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC5 | 需求的书写是否规范化、简洁易懂？如果是英文的，主谓宾句子结构需要完整，助动词使用Shall | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC6 | 需求的目的性是否明确，需求是用来描述要干什么事情？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC7 | 需求的易更改性，如果系统需要迭代，需求是否容易被更新，改变，或者剔除？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC8 | 需求的原子化，单个需求本身是否可以做到包含所需的限定，以及一些功能实现的细节？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC9 | 需求的系统性，所有的需求合起来是否能提供一个完整的系统定义，是否能提供所有功能所需的说明？ | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC10 | 需求的一致性，需求与需求之间是否重复，或者是否有冲突？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC11 | 需求的优先级，各个需求在实现上是否有轻重缓急之分，哪些是必须的，哪些是期望的，哪些是可选的？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC12 | 需求的可追溯性，需求本身是否被赋予唯一且在项目周期内不可更改的编号？需求与原始输入文档或者其他相关材料之间是否建立了合适的链接关系 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RNC13 | 需求的纯粹性，需求不应涉及项目计划，人力资源分配等相关的东西 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 5.0 Requirement Classification Check（需求分类检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| RCC1 | 功能类和非功能类需求是否分开？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RCC2 | 功能安全类需求是否单独列出？ | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

