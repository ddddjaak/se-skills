# 方案测试策略 Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | WR | beta | 2025-05-10 |

- **日期**: 2023/04/24
- **编制**: \< Leader\>

## 目的 (Objectives)

为方案测试策略评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for software development.

## 适用范围 (Scope)

适用于公司内部发难测试策略评审。
This document is only for internal use.

## 参考文件 (Reference)

https://www.nasa.gov/seh/appendix-c-how-to-write-a-good-requirement

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 | 评估 |
|------|--------|------|
| 1.0 | Configuration Items Check （测试过程域配置项检查） | NO |
| 2.0 | Basic Information Check（基本的信息检查） | NO |
| 3.0 | Requirement Traceability Check （测试项目识别检查） | NO |
| 4.0 | Requirement Normalization Check （测试策略检查） | NO |
| 5.0 | Requirement Classification Check （测试特性分类检查） | NO |

### 1.0 Configuration Items Check （测试过程域配置项检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | No | Optional | OK |
| CIC2 | 是否有软硬件技术要求或规格 | No | Optional | OK |
| CIC3 | 是否有软硬件详设或规范 | No | Mandatory | OK |

### 2.0 Basic Information Check（基本的信息检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| BIC1 | 引用文档的版本、发布日期是否记录清晰？ | No | Mandatory | OK |
| BIC2 | 产品特性分析、测试分析、测试策略、测试设计章节是否有为空？ | No | Mandatory | OK |
| BIC3 | 测试设计字段是否按要求填写？ | No | Mandatory | OK |
| BIC4 | 如有特殊需求是否已标注出来？ | No | Mandatory | OK |

### 3.0 Requirement Traceability Check （测试项目识别检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RTC1 | 每条测试设计是否都按要求填写？ | No | Mandatory | OK |
| RTC2 | 针对产品特性，测试项目是否有遗漏？ | No | Mandatory | OK |
| RTC3 | 测试项目与测试设计是否对应？ | No | Mandatory | OK |

### 4.0 Requirement Normalization Check （测试策略检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RNC1 | 测试业务分层模块化是否有遗漏？ | No | Mandatory | OK |
| RNC2 | 测试设计字段是否按要求填写？ | No | Mandatory | OK |
| RNC3 | 测试策略中对测试的重点、难点和优先级是否有明确描述？ | No | Mandatory | OK |
| RNC4 | 针对测试验收标准模糊的测试点，测试策略是否有风险预警？ | No | Mandatory | OK |
| RNC5 | 测试使用的量具、设备是否有清楚的记录名称、数量、型号、有效期？ | No | Mandatory | OK |
| RNC6 | 测试策略中对测试的重点、难点和优先级是否有明确描述？ | No | Mandatory | OK |
| RNC7 | 测试的准入、准出规则是否有遗漏？ | No | Mandatory | OK |
| RNC8 | 测试人员及进度完成节点是否有遗漏？ | No | Mandatory | OK |

### 5.0 Requirement Classification Check （测试特性分类检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RCC1 | 测试特性分解是否包含对外接口特性？ | Yes | Mandatory | OK |
| RCC2 | 测试特性分解是否包含容限特性？ | Yes | Mandatory | OK |
| RCC3 | 测试特性分解是否包含容错特性？ | Yes | Mandatory | OK |
| RCC4 | 测试特性分解是否包含一致性特性？ | Yes | Mandatory | OK |
| RCC5 | 测试特性分解是否包含可靠性特性？ | Yes | Mandatory | OK |

