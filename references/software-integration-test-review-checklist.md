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
| BIC1 | 测试用例是否覆盖架构设计所有条目 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Test case Check （测试用例检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| TCC1 | 是否明确测试用例优先级（优先级高为冒烟测试用例） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC2 | 是否存在软硬件约束相关的测试用例 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC3 | 是否存在软件架构检查的测试用例 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC4 | 是否存在接口设计的测试用例，包括入参检查、DET检查 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC5 | 是否存在静态设计的测试用例，包括数据类型、文件结构设计 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC6 | 是否存在动态设计的测试用例，包括模块状态，启动流程、内存映射 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC7 | 是否存在模块基础功能的测试用例，如DIO端口读写、ADC采样精度、PWM占空比精度 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| TCC8 | 是否存在性能相关测试用例，包括内存使用、CPU负载测试、中断执行时间、临界区执行时间 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

