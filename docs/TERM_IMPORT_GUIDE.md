# TCH 本体术语导入指南
# TCH Ontology Term Import Guide

**版本**: v1.0  
**日期**: 2025-10-31  
**维护**: TCH Ontology Team

---

## 目录 / Table of Contents

1. [概述](#概述)
2. [环境准备](#环境准备)
3. [数据准备](#数据准备)
4. [字段说明](#字段说明)
5. [导入流程](#导入流程)
6. [验证规则](#验证规则)
7. [常见问题](#常见问题)
8. [示例](#示例)

---

## 概述 / Overview

TCH 本体术语导入工具支持从 CSV/Excel 表格批量导入术语到 `tch-edit.owl` 本体文件。

### 支持的术语类别

| 类别 | 英文 | ID范围 | 模板文件 |
|------|------|--------|----------|
| Pattern | 证候 | TCH_0001000-0099999 | pattern_template.csv |
| Disease | 中医疾病 | TCH_0100000-0199999 | disease_template.csv |
| Symptom | 症状 | TCH_0200000-0499999 | symptom_template.csv |
| Sign | 征象 | TCH_0500000-0799999 | sign_template.csv |
| Herb | 中草药 | TCH_1000000-2999999 | herb_template.csv |
| Formula | 方剂 | TCH_4000000-5999999 | formula_template.csv |
| Principle | 治则 | TCH_6000000-6999999 | principle_template.csv |
| Method | 治法 | TCH_6000000-6999999 | method_template.csv |
| Differentiation | 辨证 | TCH_7000000-7999999 | differentiation_template.csv |
| Pathomechanism | 病机 | TCH_8000000-8999999 | pathomechanism_template.csv |

---

## 环境准备 / Environment Setup

### 1. 安装 Python 依赖

```bash
cd src/scripts
pip install -r requirements.txt
```

### 2. 验证安装

```bash
python -c "import pandas; import yaml; import owlready2; print('OK')"
```

---

## 数据准备 / Data Preparation

### 1. 选择术语类别

确定您要导入的术语属于哪个类别（如 Pattern、Herb 等）。

### 2. 使用模板文件

复制对应类别的模板文件：

```bash
cp src/scripts/templates/pattern_template.csv my_pattern_data.csv
```

### 3. 填写术语数据

在 Excel 或文本编辑器中打开 CSV 文件，按照字段说明填写数据。

#### CSV 文件要求

- **编码**: UTF-8
- **分隔符**: 逗号 (,)
- **换行符**: LF 或 CRLF
- **引号**: 字段值包含逗号时使用双引号包裹

#### Excel 文件要求

- **格式**: .xlsx 或 .xls
- **工作表**: 仅使用第一个工作表
- **表头**: 第一行必须是字段名

---

## 字段说明 / Field Descriptions

### 通用字段 (所有类别必填)

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **tch_id** | ID | ✅ | 本体术语唯一标识符，格式: TCH_XXXXXXX | TCH_0001001 |
| **label_zh** | 文本 | ✅ | 中文术语名称 | 寒证 |
| **label_en** | 文本 | ✅ | 英文术语名称 | Cold pattern |
| **definition_zh** | 文本 | ✅ | 中文定义 | 以恶寒、肢冷... |
| **definition_en** | 文本 | ✅ | 英文定义 | A pattern characterized by... |
| **has_exact_synonym_zh** | 列表 | ❌ | 中文精确同义词（\|分隔） | 虚寒证\|阳虚寒证 |
| **has_related_synonym_zh** | 列表 | ❌ | 中文相关同义词（\|分隔） | 表寒证\|里寒证 |
| **has_exact_synonym_en** | 列表 | ❌ | 英文精确同义词（\|分隔） | Yang deficiency pattern |
| **has_related_synonym_en** | 列表 | ❌ | 英文相关同义词（\|分隔） | Exterior cold\|Interior cold |
| **parents** | ID列表 | ❌ | 上位类术语ID（\|分隔） | TCH_0001000 |
| **sources** | 列表 | ❌ | 来源文献或数据库（\|分隔） | 《中医诊断学》\|《中医基础理论》 |
| **evidence_ECO** | 代码 | ❌ | 证据代码（ECO本体） | ECO:0000033 |
| **date_accessed** | 日期 | ❌ | 检索/创建日期 (YYYY-MM-DD) | 2025-10-31 |
| **notes** | 文本 | ❌ | 备注信息 | 示例数据 |

### Pattern (证候) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **has_sign** | ID列表 | ❌ | 具有的征象术语ID（\|分隔） | TCH_0500001\|TCH_0500002 |
| **has_symptom** | ID列表 | ❌ | 具有的症状术语ID（\|分隔） | TCH_0200001\|TCH_0200002 |
| **reflect_pathomechanism** | ID列表 | ❌ | 反映的病机术语ID（\|分隔） | TCH_8000001 |
| **xrefs** | 列表 | ❌ | 外部数据库交叉引用（\|分隔） | ICD11:TM1.01 |

### Disease (中医疾病) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **icd11_mms** | 代码 | ❌ | ICD-11 MMS编码 | ICD11:CA40 |
| **has_sign** | ID列表 | ❌ | 具有的征象术语ID | TCH_0500010 |
| **has_symptom** | ID列表 | ❌ | 具有的症状术语ID | TCH_0200010 |
| **anatomical_site_uberon** | ID列表 | ❌ | 解剖定位（UBERON） | UBERON:0001004 |
| **etiologic_agent** | 列表 | ❌ | 病因/病原 | Wind pathogen |
| **typical_tcm_patterns** | ID列表 | ❌ | 常见对应证候 | TCH_0001010 |

### Symptom (症状) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **related_MMsymptom** | ID列表 | ❌ | 相关西医症状（HPO） | HPO:0001234 |
| **inheresIn_UBERON** | ID列表 | ❌ | 依附的解剖载体 | UBERON:0001004 |
| **iso_id** | 代码 | ❌ | ISO术语编号 | ISO23961:12345 |

### Sign (征象) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **sign_category** | 文本 | ❌ | 征象类别 | 舌诊 / 脉诊 / 其他 |
| **iso_id** | 代码 | ❌ | ISO术语编号 | ISO23961:12345 |

### Herb (中草药) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **tcdo_id** | 代码 | ❌ | TCDO编号 | TCDO:12345 |
| **has_nature** | ID列表 | ❌ | 药性术语ID | TCH_3000000 |
| **has_flavor** | ID列表 | ❌ | 药味术语ID | TCH_3000001 |
| **has_channel_tropism** | ID列表 | ❌ | 归经术语ID | TCH_3000002 |
| **active_ingredient_chebi** | ID列表 | ❌ | 活性成分（CHEBI） | CHEBI:12345 |

### Formula (方剂) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **has_herb** | ID列表 | ❌ | 药味组成术语ID | TCH_1000001\|TCH_1000002 |
| **treats_dispositions** | ID列表 | ❌ | 对应证候术语ID | TCH_0001001 |

### Principle (治则) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **treats_dispositions** | ID列表 | ❌ | 针对证候术语ID | TCH_0001001 |
| **treats_diseases** | ID列表 | ❌ | 针对疾病术语ID | TCH_0100001 |
| **realizedBy_process** | ID列表 | ❌ | 由……实现（治法）术语ID | TCH_6000001 |

### Method (治法) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **treats_dispositions** | ID列表 | ❌ | 针对证候术语ID | TCH_0001001 |
| **treats_diseases** | ID列表 | ❌ | 针对疾病术语ID | TCH_0100001 |

### Pathomechanism (病机) 特有字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| **explains_disease** | ID列表 | ❌ | 解释疾病术语ID | TCH_0100001 |
| **causes_pattern** | ID列表 | ❌ | 导致证候术语ID | TCH_0001001 |

---

## 导入流程 / Import Process

### 1. 仅验证数据（推荐先执行）

在正式导入前，建议先验证数据格式和完整性：

```bash
cd src/ontology
python ../scripts/import_terms.py \
  --category pattern \
  --input ../../data/pattern_terms.csv \
  --validate-only
```

### 2. 正式导入

验证通过后，执行正式导入：

```bash
python ../scripts/import_terms.py \
  --category pattern \
  --input ../../data/pattern_terms.csv
```

### 3. 检查导入结果

- 查看控制台输出和日志文件 `term_import.log`
- 查看导入报告文件 `term_import_report_*.txt`
- 使用 Protégé 打开 `tch-edit.owl` 检查术语

### 4. 验证本体

```bash
sh run.sh make
```

### 5. 提交更改

```bash
git add tch-edit.owl
git commit -m "添加XXX类术语 XX 条"
git push origin main
```

---

## 验证规则 / Validation Rules

### ID 格式验证

- **格式**: `TCH_XXXXXXX` (7位数字)
- **示例**: `TCH_0001001` ✅
- **错误**: `TCH_001` ❌, `TCH_A001001` ❌

### ID 范围验证

每个类别的ID必须在指定范围内：

| 类别 | ID范围 |
|------|--------|
| Pattern | 0001000-0099999 |
| Disease | 0100000-0199999 |
| Symptom | 0200000-0499999 |
| Sign | 0500000-0799999 |
| Herb | 1000000-2999999 |
| Formula | 4000000-5999999 |
| ... | ... |

### 必填字段验证

以下字段必须填写，不能为空：

- `tch_id`
- `label_zh`
- `label_en`
- `definition_zh`
- `definition_en`

### 引用完整性验证

关系字段中引用的术语ID必须存在于本体中，或在同批次导入数据中。

### 重复ID检查

不允许导入已存在的术语ID。

---

## 常见问题 / FAQ

### Q1: CSV 文件中文乱码怎么办？

**A**: 确保使用 UTF-8 编码保存 CSV 文件。在 Excel 中另存为 CSV 时选择"UTF-8 CSV"。

### Q2: 多个值如何分隔？

**A**: 使用竖线符号 `|` 分隔多个值，例如：`TCH_0001001|TCH_0001002|TCH_0001003`

### Q3: 术语ID范围错误怎么办？

**A**: 检查术语ID是否在该类别的有效范围内。参考上文"ID范围验证"部分。

### Q4: 导入失败如何回滚？

**A**: 工具会自动备份本体文件，备份文件位于 `tch-edit.owl.backup.YYYYMMDD_HHMMSS`

### Q5: 如何批量导入多个类别？

**A**: 编写 shell 脚本循环调用导入命令：

```bash
#!/bin/bash
for category in pattern disease symptom; do
  python import_terms.py --category $category --input data/${category}_terms.csv
done
```

### Q6: Excel 文件支持多个工作表吗？

**A**: 仅支持读取第一个工作表。如有多个工作表，请分别保存为独立文件。

### Q7: 如何更新已有术语？

**A**: 目前工具不支持更新，重复ID会被跳过。如需更新，请先在 Protégé 中手动删除旧术语。

### Q8: 关系字段引用的术语不存在怎么办？

**A**: 
- 选项1: 先导入被引用的术语，再导入当前术语
- 选项2: 在同一批次中同时导入（工具会处理引用关系）
- 选项3: 暂时留空，后续手动添加关系

---

## 示例 / Examples

### 示例 1: 导入 Pattern 类术语

**数据文件**: `pattern_terms.csv`

```csv
tch_id,label_zh,label_en,definition_zh,definition_en,has_symptom,has_sign
TCH_0001001,寒证,Cold pattern,以恶寒、肢冷为主征...,A pattern characterized by...,TCH_0200001|TCH_0200002,TCH_0500001
```

**导入命令**:

```bash
python import_terms.py --category pattern --input pattern_terms.csv
```

### 示例 2: 导入 Herb 类术语

**数据文件**: `herb_terms.xlsx`

| tch_id | label_zh | label_en | definition_zh | definition_en | has_nature | has_flavor |
|--------|----------|----------|---------------|---------------|------------|------------|
| TCH_1000001 | 人参 | Ginseng | 人参为五加科植物... | Ginseng is... | TCH_3000000 | TCH_3000001 |

**导入命令**:

```bash
python import_terms.py --category herb --input herb_terms.xlsx
```

### 示例 3: 仅验证 Disease 数据

```bash
python import_terms.py \
  --category disease \
  --input disease_terms.csv \
  --validate-only
```

---

## 进阶配置 / Advanced Configuration

### 自定义配置文件

复制并编辑配置文件：

```bash
cp term-import-config.yaml my-config.yaml
# 编辑 my-config.yaml
python import_terms.py --config my-config.yaml --category pattern --input data.csv
```

### 配置项说明

参见 `term-import-config.yaml` 文件中的详细注释。

---

## 技术支持 / Technical Support

- **GitHub Issues**: https://github.com/nxx07/tch-ontology-demo/issues
- **文档**: https://github.com/nxx07/tch-ontology-demo/blob/main/docs/

---

## 更新日志 / Changelog

### v1.0 (2025-10-31)

- ✅ 初始版本
- ✅ 支持 10 个术语类别
- ✅ CSV/Excel 文件导入
- ✅ 数据验证
- ✅ 导入报告生成

---

**最后更新**: 2025-10-31  
**维护**: TCH Ontology Team
