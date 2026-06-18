# Software Development Checklist

**CHIPSEA CONFIDENTIAL**

## 修订记录 (Revision History)

| 版本 | 作者 | 变更内容 | 日期 |
|------|------|----------|------|
| A01 | DJ | 初版 | 2023-04-24 |

- **版本**: A01
- **日期**: 2024/01/29
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
| 0.0 | Code Hierarchy Check（代码层次和文件结构检查） | NO |
| 1.0 | Code Layout Check（排版与代码表达检查） | NO |
| 2.0 | Code Annotation Check（代码注释检查） | NO |
| 3.0 | Code Naming Check（命名规则检查） | NO |
| 4.0 | Code Design Check（代码设计检查） | NO |

### 0.0 Code Hierarchy Check（代码层次和文件结构检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CHC1 | 模块软件结构符合软件开发规范要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CHC2 | 模块文件引用关系符合软件开发规范要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CHC3 | 开源软件代码需独立形成一个或者多个文件（若涉及），不能和自研混淆 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 1.0 Code Layout Check（排版与代码表达检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CLC1 | 一行不超过120字符，新行需要缩进 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC2 | 缩进统一为4个空格，每一级代码需比上一级缩进4空格 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC3 | 一行代码只做一件事 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC4 | 复杂表达式必须使用括号来明确逻辑，减少歧义；宏定义必须用括号 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC5 | 相等判断表达式中常量放左边 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC6 | 避免直接使用数字 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC7 | 满足if语句格式要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC8 | 满足switch语句格式要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC9 | 满足for、while语句格式要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC10 | 满足条件编译语句格式要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC11 | 避免直接使用编译器和平台/模块特定关键字 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC12 | 满足空格处理格式要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC13 | 满足花括号格式要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC14 | 所有数字加大写U | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC15 | 表达式中数的检测应该明确给出判断，不能默认0为假，非0为真 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC16 | .c.h文件有统一的模板，明确了文件头、符号定义、类型声明等摆放的位置。见eclipse模板《Chipsea_C_Templates.xml》 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CLC17 | 变量定义和代码之间要空行，函数、类型的定义、声明，相互之间要空行 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 2.0 Code Annotation Check（代码注释检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CAC1 | 代码的注释说明等，均使用/\\/，不能使用// | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CAC2 | 无用代码的注释，使用#if 0，不要用/\\/ | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CAC3 | 全局变量定义，结构体、联合体、枚举类型定义，应注释描述其作用、功能、取值范围等。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CAC4 | 条件执行体或循环体的花括号内为空时，应添加注释说明。 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CAC5 | 函数定义的前面必须加注释 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 3.0 Code Naming Check（命名规则检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CNC1 | 所有的符号命名要遵循见名知意原则，看到命名知道其含义 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC2 | 满足宏定义与枚举的命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC3 | 满足全局变量命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC4 | 满足成员变量/局部变量/形参命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC5 | 满足指针变量命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC6 | 满足数据类型命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC7 | 满足函数命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CNC8 | 满足文件命名要求 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 4.0 Code Design Check（代码设计检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| CDC1 | 模块应提供初始化函数，并记录模块初始化状态，如果使用模块功能前未进行初始化，应报错。 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC2 | 对服务层接口，用户传入的所有参数必须进行合法检查 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC3 | 每个模块对外的唯一头文件\<Module\>.h需定义版本宏信息 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC4 | 模块的可选功能应能够在编译前进行配置（开 / 关） | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC5 | 满足inline函数使用要求 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC6 | 每个模块应该有一个该模块的初始化函数，按照用户配置来初始化模块功能 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC7 | 不能在代码中定义变量，每个函数的所有局部变量需在函数开头明确定义 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC8 | 自研接口若关联开源组件功能，只允许通过接口调用，禁止复制开源组件的源代码到接口内部 | No | Optional | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| CDC9 | 提交代码0错误，0警告，若存在无法修改的警告，需备注原因 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

### 5.0 Register Define Check（寄存器定义检查）

**评估**: NO

| 编号 | 检查内容 | 评估 | 类别 | 状态 | 备注/参考 | 检查要求人 | 检查人 | 批准要求人 |
|------|------|------|------|------|------|------|------|------|
| RDC1 | 寄存器定义时需使用Csx_RegTypes.h定义的别名 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RDC2 | 寄存器中预留位：reserved\_\<该预留位的起始地址，十进制表示\> 模块寄存器预留空间：reserved\_\<该预留空间的起始地址，十六进制表示\> | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RDC3 | 寄存器定义包括两层，第一层为联合体定义，第二层为位域定义。且命名规则符合：Csx\_\<全大写的模块名\>\_\<全大写的寄存器名\> | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RDC4 | 每个模块的寄存器在内存上是放在一块的，有一个共同的基地址，每个寄存器相对基地址有固定的偏移 | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |
| RDC5 | 基于模块寄存器汇总结构体的类型，修饰该模块寄存器的基地址，以此为实例进行读写访问。该符号命名规则：MODULE\_\<全大写的模块名\>\<实例ID\> | No | Mandatory | OK | Peer SW Eng | Peer SW Eng | SW Lead | SW Lead |

