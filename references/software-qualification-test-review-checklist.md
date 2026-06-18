# Software Development Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | Wangliang | 初版 | 2025-07-07 |

- **版本**: A01
- **日期**: 2025/07/07
- **编制**: wangliang

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
| 0.0 | Configuration Items Check （过程域配置项检查） | NO |
| 1.0 | Basic Information Check （基本的信息检查） | NO |
| 2.0 | Test Case Check （测试用例检查） | NO |

### 0.0 Configuration Items Check （过程域配置项检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC2 | 是否有集成测试用例输出(在线系统承载或线下文档) | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC3 | 是否有集成测试代码输出(Git或SVN存储) | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 1.0 Basic Information Check （基本的信息检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| BIC1 | 测试用例是否覆盖对应模块需求的所有条目 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Test case Check （测试用例检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| TCC1 | 是否明确测试用例优先级（优先级高为冒烟测试用例） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC2 | 是否存在基本功能测试用例，比如GPIO高/低电平输出，CAN通信 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC3 | 是否存在压力测试的测试用例 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC4 | 是否存在中断和DMA测试用例（仅支持中断和DMA的模块） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

