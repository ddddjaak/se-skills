# 方案软件发布评审Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | Pangxj | beta | 2019-04-20 |
| A02 | DJ | 1.增加表格外框，对齐行列内容，使模版外观更整齐； 2.针对方案开发完善检查内容； | 2025-05-06 |

## 目的 (Objectives)

为方案发布评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for software development.

## 适用范围 (Scope)

适用于公司内部方案软件发布评审。
This document is only for internal use.

## 参考文件 (Reference)

https://www.nasa.gov/seh/appendix-c-how-to-write-a-good-requirement

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 | 评估 |
|------|--------|------|
| 1.0 | 需求实现覆盖率检查 | NO |
| 2.0 | 测试覆盖率检查 | NO |
| 3.0 | 软件问题项检查 | NO |
| 4.0 | 软件发布内容检查 | NO |

### 1.0 需求实现覆盖率检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 是否列出清晰的设计目标 | No | Mandatory | OK |
| 是否列出清晰的功能 / 性能需求 | No | Mandatory | OK |
| 是否列出DFX需求、约束假定、运行环境、组件间关系 | No | Optional | OK |
| 需求实现覆盖率是否达到 100% | No | Mandatory | OK |
| 未实现项是否跟相关方达成一致 | No | Mandatory | OK |

### 2.0 测试覆盖率检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 代码开发是否符合方案软件开发规范（包括编码规则） | No | Mandatory | OK |
| 是否按自测用例完成了开发自测（覆盖率100%） | No | Mandatory | OK |
| 是否按方案转测用例完成了方案测试（覆盖率100%） | No | Mandatory | OK |

### 3.0 软件问题项检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 如果有同类项目的历史缺陷，是否已规避 | No | Mandatory | OK |
| 软件问题清单中致命和严重缺陷是否已全部close | No | Mandatory | OK |

### 4.0 软件发布内容检查

**评估**: NO

| 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|
| 源代码工程是否OK | No | Optional | OK |
| HEX等可执行文件是否OK | No | Mandatory | OK |
| 版本修改说明是否清晰 | No | Mandatory | OK |
| 版本测试报告是否完整清晰 | No | Mandatory | OK |
| 软件使用说明是否完整清晰 | No | Optional | OK |
| 测试工具及使用说明是否完整清晰 | No | Optional | OK |

