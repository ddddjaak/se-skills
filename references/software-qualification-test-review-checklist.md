# Software Development Checklist

## 检查清单 (CheckList)

### 检查项概览

| 编号 | 检查项 |
|------|--------|
| 0.0 | Configuration Items Check （过程域配置项检查） |
| 1.0 | Basic Information Check （基本的信息检查） |
| 2.0 | Test Case Check （测试用例检查） |

### 0.0 Configuration Items Check （过程域配置项检查）

| 编号 | 检查内容 |
|------|------|
| CIC1 | 是否有沟通记录 |
| CIC2 | 是否有集成测试用例输出(在线系统承载或线下文档) |
| CIC3 | 是否有集成测试代码输出(Git或SVN存储) |

### 1.0 Basic Information Check （基本的信息检查）

| 编号 | 检查内容 |
|------|------|
| BIC1 | 测试用例是否覆盖对应模块需求的所有条目 |

### 2.0 Test case Check （测试用例检查）

| 编号 | 检查内容 |
|------|------|
| TCC1 | 是否明确测试用例优先级（优先级高为冒烟测试用例） |
| TCC2 | 是否存在基本功能测试用例，比如GPIO高/低电平输出，CAN通信 |
| TCC3 | 是否存在压力测试的测试用例 |
| TCC4 | 是否存在中断和DMA测试用例（仅支持中断和DMA的模块） |
