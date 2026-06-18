# 方案测试报告 Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | Pangxj | beta | 2019-04-20 |
| A02 | DJ | 1.增加表格外框，对齐行列内容，使模版外观更整齐； 2.针对方案开发完善检查内容； | 2025-05-06 |

- **日期**: 2023/04/24
- **编制**: \<Team Leader\>

## 目的 (Objectives)

为方案开发评审提供检查列表和报告。checklist侧重于检查内容，而非实现工具。
The objective of this document is to provide check list and report for solution development.

## 适用范围 (Scope)

适用于公司内部方案开发评审。
This document is only for internal use.

## 参考文件 (Reference)

https://www.nasa.gov/seh/appendix-c-how-to-write-a-good-requirement

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 | 评估 |
|------|--------|------|
| 1.0 | Configuration Items Check （测试过程域配置项检查） | YES |
| 2.0 | Basic Information Check（基本的信息检查） | YES |
| 3.0 | Requirement Traceability Check （测试项目检查） | YES |
| 4.0 | Requirement Normalization Check （测试执行规范检查） | YES |
| 5.0 | Requirement Classification Check （测试结果检查） | YES |

### 1.0 Configuration Items Check （测试过程域配置项检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | Yes | Optional | OK |
| CIC2 | 是否有软硬件技术要求或规格 | Yes | Optional | OK |
| CIC3 | 是否有软硬件详设或规范 | Yes | Mandatory | OK |

### 2.0 Basic Information Check（基本的信息检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| BIC1 | 测试项是否条目化？ | Yes | Mandatory | OK |
| BIC2 | 测试结果字段是否按要求填写？ | Yes | Mandatory | OK |
| BIC3 | 整体测试结论是否记录清晰？ | Yes | Mandatory | OK |
| BIC4 | 如有特殊需求是否已标注出来？ | Yes | Mandatory | OK |

### 3.0 Requirement Traceability Check （测试项目检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RTC1 | 每个测试项是否都清晰标注（已测/未测/部分测试）状态？ | Yes | Mandatory | OK |
| RTC2 | 每个测试项是否都清晰标注测试结论？ | Yes | Mandatory | OK |

### 4.0 Requirement Normalization Check （测试执行范检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RNC1 | 测试版本、时间、地点、人员信息是否记录清楚？ | Yes | Mandatory | OK |
| RNC2 | 测试环境说明是否包含业务组网说明？ | Yes | Mandatory | OK |
| RNC3 | 测试使用的量具、设备是否有清楚的记录名称、数量、型号、有效期？ | Yes | Mandatory | OK |
| RNC4 | 测试执行统计是否按字段记录清晰？ | Yes | Mandatory | OK |
| RNC5 | 详细测试结果是否按字段记录清晰？ | Yes | Mandatory | OK |
| RNC6 | 缺陷统计是否明确了TOP问题和缺陷闭环情况？ | Yes | Mandatory | OK |
| RNC7 | 遗留问题是否按字段记录清晰？ | Yes | Mandatory | OK |

### 5.0 Requirement Classification Check （测试结果检查）

**评估**: YES

| 编号 | 检查内容 | 评估 | 类别 | 状态 |
|------|------|------|------|------|
| RCC1 | 每一项的详细测试结果对应的测试结论是否正确？ | Yes | Mandatory | OK |
| RCC2 | 遗留问题是否与详细测试结果相对应？ | Yes | Optional | OK |

