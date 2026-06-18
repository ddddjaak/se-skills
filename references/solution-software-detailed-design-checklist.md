# 方案软件详细设计Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | Pangxj | beta | 2019-04-20 |
| A02 | DJ | 1.增加表格外框，对齐行列内容，使模版外观更整齐； 2.针对方案开发完善检查内容； | 2025-05-06 |

## 目的 (Objectives)

为方案开发评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for software development.

## 适用范围 (Scope)

适用于公司内部方案开发评审。
This document is only for internal use.

## 参考文件 (Reference)

https://www.nasa.gov/seh/appendix-c-how-to-write-a-good-requirement

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 | 评估 |
|------|--------|------|
| 1.0 | 设计需求概述项检查 | NO |
| 2.0 | 模块设计项检查 | NO |
| 3.0 | 需求追溯项检查 | NO |
| 4.0 | 设计难点与解决措施项检查 | NO |

### 1.0 设计需求概述项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 是否列出清晰的设计目标 | No | Mandatory | OK |
| 是否列出清晰的功能 / 性能需求 | No | Mandatory | OK |
| 是否列出DFX需求、约束假定、运行环境、组件间关系 | No | Optional | OK |

### 2.0 模块设计项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 代码开发是否符合方案软件开发规范（包括编码规则） | No | Mandatory | OK |
| 是否按自测用例完成了开发自测 | No | Mandatory | OK |
| 单元功能描述和接口是否清晰 | No | Mandatory | OK |
| 是否用状态转换图/顺序图/消息序列图/用例图等描述模块内部的软件单元之间的动态行为，如任务、线程、时间片、中断等 | No | Mandatory | OK |
| 函数详细设计是否清晰定义函数传入参数的名称、含义、数据类型、取值范围，以及返回值的类型、含义、取值范围。 | No | Mandatory | OK |
| 函数详细设计是否体现函数实现逻辑的流程图（逻辑简单的函数可忽略） | No | Mandatory | OK |

### 3.0 需求追溯项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 单元设计与需求间的承接是否清晰明确 | No | Mandatory | OK |
| 如果有同类项目的历史缺陷，是否已规避 | No | Mandatory |  |

### 6.0 设计难点与解决措施项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 是否评估过设计难点 | No | Optional | OK |
| 如果有设计难点，是否有妥善的解决措施 | No | Optional | OK |

