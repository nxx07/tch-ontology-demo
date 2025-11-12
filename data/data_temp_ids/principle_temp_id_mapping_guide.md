# Principle临时ID映射指南

**生成时间**: 2025-11-12 01:29:32
**数据来源**: clinical_diagnosis_and_treatment.clinical_treatment (code 2开头)
**临时ID范围**: TmpTCH:PRINCIPLE_60000 - TmpTCH:PRINCIPLE_60034
**总术语数**: 35

## 1. 映射关系概览

| 临时ID | 原始Code | 中文术语 | 父级临时ID |
|--------|----------|----------|------------|
| TmpTCH:PRINCIPLE_60001 | 2 | 治则类术语 | TmpTCH:PRINCIPLE_60000 |
| TmpTCH:PRINCIPLE_60002 | 2.1 | 治未病法 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60007 | 2.1.1 | 未病先防 | TmpTCH:PRINCIPLE_60002 |
| TmpTCH:PRINCIPLE_60008 | 2.1.2 | 已病防变 | TmpTCH:PRINCIPLE_60002 |
| TmpTCH:PRINCIPLE_60009 | 2.1.3 | 瘥后防复 | TmpTCH:PRINCIPLE_60002 |
| TmpTCH:PRINCIPLE_60010 | 2.10 | 祛邪扶正 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60003 | 2.11 | 攻补兼施 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60011 | 2.11.1 | 先攻后补 | TmpTCH:PRINCIPLE_60003 |
| TmpTCH:PRINCIPLE_60012 | 2.11.2 | 先补后攻 | TmpTCH:PRINCIPLE_60003 |
| TmpTCH:PRINCIPLE_60013 | 2.11.3 | 寓攻于补 | TmpTCH:PRINCIPLE_60003 |
| TmpTCH:PRINCIPLE_60014 | 2.11.4 | 寓补于攻 | TmpTCH:PRINCIPLE_60003 |
| TmpTCH:PRINCIPLE_60004 | 2.12 | 正治法 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60015 | 2.12.1 | 寒者热之 | TmpTCH:PRINCIPLE_60004 |
| TmpTCH:PRINCIPLE_60016 | 2.12.2 | 热者寒之 | TmpTCH:PRINCIPLE_60004 |
| TmpTCH:PRINCIPLE_60017 | 2.12.3 | 虚则补之 | TmpTCH:PRINCIPLE_60004 |
| TmpTCH:PRINCIPLE_60018 | 2.12.4 | 实则泻之 | TmpTCH:PRINCIPLE_60004 |
| TmpTCH:PRINCIPLE_60005 | 2.13 | 反治法 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60019 | 2.13.1 | 寒因寒用 | TmpTCH:PRINCIPLE_60005 |
| TmpTCH:PRINCIPLE_60020 | 2.13.2 | 热因热用 | TmpTCH:PRINCIPLE_60005 |
| TmpTCH:PRINCIPLE_60021 | 2.13.3 | 塞因塞用 | TmpTCH:PRINCIPLE_60005 |
| TmpTCH:PRINCIPLE_60022 | 2.13.4 | 通因通用 | TmpTCH:PRINCIPLE_60005 |
| TmpTCH:PRINCIPLE_60006 | 2.14 | 调理阴阳 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60023 | 2.14.1 | 从阴引阳 | TmpTCH:PRINCIPLE_60006 |
| TmpTCH:PRINCIPLE_60024 | 2.14.2 | 从阳引阴 | TmpTCH:PRINCIPLE_60006 |
| TmpTCH:PRINCIPLE_60025 | 2.15 | 虚者补其母 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60026 | 2.16 | 实者泻其子 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60027 | 2.2 | 急则治标 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60028 | 2.3 | 缓则治本 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60029 | 2.4 | 标本兼治 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60030 | 2.5 | 因时制宜 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60031 | 2.6 | 因地制宜 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60032 | 2.7 | 因人制宜 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60033 | 2.8 | 扶正祛邪 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60034 | 2.9 | 扶正固本 | TmpTCH:PRINCIPLE_60001 |
| TmpTCH:PRINCIPLE_60000 | ROOT | 治则(根类别) |  |


## 2. 层级结构示例

以下是典型的层级关系示例:

- **2** → TmpTCH:PRINCIPLE_60001 (治则类术语)
  - 父级: TmpTCH:PRINCIPLE_60000
- **2.1** → TmpTCH:PRINCIPLE_60002 (治未病法)
  - 父级: TmpTCH:PRINCIPLE_60001
- **2.1.1** → TmpTCH:PRINCIPLE_60007 (未病先防)
  - 父级: TmpTCH:PRINCIPLE_60002


## 3. 后续处理步骤

### 3.1 人工审核阶段
1. 审核 `principle_data_temp_ids.csv` 文件中的术语
2. 删除不需要的术语行
3. 修正术语信息(如有需要)
4. 补充关系字段(applied_to_pattern, applied_to_disease, realized_by_method等)

### 3.2 最终ID分配阶段
1. 确定保留的术语列表
2. 按照TCH ID分配策略分配正式ID(TCH:6000000-6099999)
3. 更新parents字段为正式ID
4. 生成最终的principle_data_processed.csv

### 3.3 关系字段说明
- **applied_to_pattern**: 该治则适用的证候(TCH ID,分号分隔)
- **applied_to_disease**: 该治则适用的疾病(TCH ID,分号分隔)
- **realized_by_method**: 实现该治则的治法(TCH ID,分号分隔)
- **constrains_formula**: 该治则约束的方剂(TCH ID,分号分隔)

## 4. 注意事项

⚠️ **重要提醒**:
- 临时ID仅用于审核阶段,不应用于生产环境
- 删除术语时注意检查是否有子术语依赖
- 最终ID分配时需保持层级关系的一致性
- 关系字段需要与pattern、disease、method、formula数据交叉引用
- 建议在ID重分配前备份数据

---
*本文档由 TCM_principle_data_process.py 自动生成*
