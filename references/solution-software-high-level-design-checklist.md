# 方案软件概要设计 Checklist

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
| 4.0 | 重用性检查 | NO |
| 5.0 | DFX设计项检查 | NO |
| 6.0 | 设计难点与解决措施项检查 | NO |

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
| 模块设计是否跟前面接口设计一致 | No | Mandatory | OK |
| 模块设计是否高内聚低耦合 | No | Mandatory | OK |
| 模块功能描述和接口是否清晰 | No | Mandatory | OK |

### 3.0 需求追溯项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 模块设计与需求间的承接是否清晰明确 | No | Mandatory |  |

### 4.0 重用性检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 是否考虑对以往模块 / 组件的继承复用 | No | Mandatory | OK |
| 是否会使用到FOSS（开源免费软件） | No | Optional | OK |
| 如使用到FOSS（开源免费软件），是否评估过影响 | No | Optional | OK |

### 5.0 DFX 设计项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 对效率的考虑是否足够 | No | Optional | OK |
| 对兼容性的考虑是否足够 | No | Optional | OK |
| 对可移植性的考虑是否足够 | No | Optional | OK |
| 对可扩展的考虑是否足够 | No | Optional | OK |
| 对可靠性的考虑是否足够 | No | Mandatory | OK |
| 对可维护性的考虑是否足够 | No | Optional |  |
| 对可重用的考虑是否足够 | No | Optional |  |
| 对安全性的考虑是否足够 | No | Optional |  |
| 对集成与测试的考虑是否足够 | No | Mandatory |  |

### 6.0 设计难点与解决措施项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 是否评估过设计难点 | No | Optional | OK |
| 如果有设计难点，是否有妥善的解决措施 | No | Optional | OK |

