# 方案量产测试策略 Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | WR | beta | 2025-05-10 |

- **日期**: 2023/04/24
- **编制**: \< Leader\>

## 目的 (Objectives)

为量产测试策略评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for software development.

## 适用范围 (Scope)

适用于公司内部量产测试策略评审。
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
| 4.0 | Requirement Normalization Check （测试分析检查） | YES |
| 5.0 | Requirement Classification Check （测试设计分类检查） | YES |

### 1.0 Configuration Items Check（需求过程域配置项检查）

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
| BIC2 | 产品特性分析、可测试性分析、测试流程、测试设计章节是否有为空？ | No | Mandatory | OK |
| BIC3 | 测试分析字段是否按要求填写？ | No | Mandatory | OK |
| BIC4 | 如有特殊需求是否已标注出来？ | No | Mandatory | OK |

### 3.0 Requirement Traceability Check （测试项目识别检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RTC1 | 每条测试设计是否都按要求填写？ | No | Mandatory | OK |
| RTC2 | 针对产品特性，测试项目是否有遗漏？ | No | Mandatory | OK |
| RTC3 | 测试项目与测试设计是否对应？ | No | Mandatory | OK |

### 4.0 Requirement Normalization Check （测试分析检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RNC1 | 测试分析字段是否按要求填写？ | Yes | Mandatory | OK |
| RNC2 | 测试分析是否包含主要接口特性？ | Yes | Mandatory | OK |
| RNC3 | 测试分析是否包含主要功能特性？ | Yes | Mandatory | OK |
| RNC4 | 测试分析是否包含主要性能特性？ | Yes | Mandatory | OK |

### 5.0 Requirement Classification Check （测试设计分类检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RCC1 | 测试设计与测试分析是否对应？ | Yes | Mandatory | OK |
| RCC2 | 测试设计是否可操作？ | Yes | Mandatory | OK |

