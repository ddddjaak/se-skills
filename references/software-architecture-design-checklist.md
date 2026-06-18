# Software Development Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | DJ | 初版 | 2023-04-24 |
| A02 | Liuyb | 增加FOSS检查项 | 2024-01-29 |

- **版本**: A02
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
| 3.0 | Architecture Chart Check（架构视图检查） | NO |
| 4.0 | Interface Design Check（接口设计检查） | NO |
| 5.0 | Static/Dynamic Design Check（静态动态设计检查） | NO |

### 1.0 Configuration Items Check（需求过程域配置项检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CIC1 | 是否有沟通记录 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC2 | 是否有接口需求规范 (Optional ，如不需要请备注 ) | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC3 | 是否有架构设计输出 ( 在线系统承载或线下文档 ) | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CIC4 | 是否有FOSS评估报告 (Optional ，若涉及，需提供 ) | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Basic Information Check（基本的信息检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| BIC1 | 架构文档需要包含软件描述，静态视图，物理视图，数据视图，开发视图，设计约束，接口设计，动态视图，资源消耗目标，模块说明等主要章节描述。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC2 | 需要描述软件概要信息，包含主要功能，性能，主要接口等 （相当于软件简介） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| BIC3 | 概要设计输出物的版本是否记录清晰？ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 3.0 Architecture Chart Check（架构视图检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| ACC1 | 静态视图设计的检查： - 需要包含软件架构图（包含架构层次和架构元素） - 针对框图进行描述，包含信息有，哪些软件模块为 COTS （ Commercial Off the Shelf ） , 哪些是复用组件，包含复用来源及版本 , 复用百分度， 哪些为开源组件及包含开源代码（Optional），哪些为新模块 ? | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| ACC2 | 物理视图设计的检查： -物理视图需要从系统或产品层面分析，包括MCU，外设，内存信息等。 -物理视图必须标明硬件的接口的电气性。最大速率，内存大小，工作电流等关键指标。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| ACC3 | 数据视图设计的检查： -必须准确描述数据持久化和存储设计，以及如何的保障数据存储层面的性能，考虑可靠性，恢复性。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| ACC4 | 开发视图设计的检查： - 需要包括开发语言约束，开源使用情况约束以及定义，包规则，编译环境以及构建规则约束（Optional）。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 4.0 Interface Design Check（接口设计检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| IDC1 | 设计约束的检查： -需要考虑基于软件的需求限制在软件架构中的过程分解或者软件设计涉及行业应用，过程分解对初始化，输入信号，输出信号，硬件约束限制应用，通信相关设计约束，诊断设计相关约束设计，等其他维度的设计约束： | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| IDC2 | 过程设计约束的检查： -需要包含watchdog，EEPROM（flash）的设计。 -需要包含芯片复位，初始化，中断，堆栈，OS shut off等相关设计内容或者约束设计。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| IDC3 | 接口设计检查： -需要描述软件内部元素之间的接口（一般包含数据接口和函数接口）数据接口包括全局，公共变量，对外函数参数等定义，包括定义数据类型，值，范围，发送接受方，格式，大小，分辨率，频率等。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| IDC4 | 接口设计检查： -需要描述软件外部接口 -函数接口可按模块罗列。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 5.0 Static/Dynamic Design Check（静态动态设计检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| SDC1 | 静态模块设计需要包含文件层级结构。必须和软件静态视图保持一致，文件的存储位置，用途必须准确描述。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| SDC2 | -动态视图需要描述软件元素之间的动态行为，包含而不限于运行模式（如启动、关机、正常模式、标定、诊断等）、进程及进程间相互通信、任务、线程、时间片、中断等。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| SDC3 | -动态视图的描述形式包括不限于状态转换图、顺序图、消息序列图、用例图等。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| SDC4 | 资源的消耗目标设计的检查： -消耗目标需要基于实时架构的设计，从Cyclic task，Event-triggered task，Static task scheduling，Interrupts，Alarm configuration，Shared resources protection等方面进行设计。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| SDC5 | 资源的消耗目标设计的检查： -消耗目标需要包含内存(RoM, Ram, EEPROM, 数据闪存)设计。 -消耗目标需要包含CPU负载设计。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| SDC6 | 双向可追溯性和一致性设计检查(由工具承载)： -软件需求和软件概要设计要素之间必须具有双向可追溯性。双向可追溯性必须覆盖软件需求向软件概要设计的要素的分配。同时， 软件需求和软件概要设计要素之间必须具有一致性。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

