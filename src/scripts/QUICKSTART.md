# TCH 术语导入快速开始
# Quick Start Guide for Term Import

## 🚀 5分钟快速开始

### 步骤 1: 安装依赖

```bash
cd /Users/cailingxi/课题组工作/tch-ontology-demo/target/tch/src/scripts
pip install -r requirements.txt
```

### 步骤 2: 准备数据

使用模板文件开始：

```bash
# 复制 Pattern 类模板
cp templates/pattern_template.csv my_data/pattern_terms.csv

# 在 Excel 中打开并编辑
open my_data/pattern_terms.csv
```

### 步骤 3: 验证数据

```bash
cd ../ontology
python ../scripts/import_terms.py \
  --category pattern \
  --input ../../my_data/pattern_terms.csv \
  --validate-only
```

### 步骤 4: 导入术语

```bash
python ../scripts/import_terms.py \
  --category pattern \
  --input ../../my_data/pattern_terms.csv
```

### 步骤 5: 验证本体

```bash
sh run.sh make
```

---

## 📁 文件结构

```
tch/
├── src/
│   ├── ontology/
│   │   ├── tch-edit.owl                    # 主本体文件
│   │   └── term-import-config.yaml         # 导入配置 🆕
│   └── scripts/
│       ├── import_terms.py                 # 导入脚本 🆕
│       ├── requirements.txt                # Python依赖 🆕
│       └── templates/                      # CSV模板 🆕
│           ├── pattern_template.csv
│           ├── disease_template.csv
│           └── ...
└── docs/
    └── TERM_IMPORT_GUIDE.md                # 详细指南 🆕
```

---

## 📋 支持的类别

| 类别 | 命令参数 | ID范围 | 模板文件 |
|------|---------|--------|----------|
| 证候 | `pattern` | 0001000-0099999 | pattern_template.csv |
| 疾病 | `disease` | 0100000-0199999 | disease_template.csv |
| 症状 | `symptom` | 0200000-0499999 | symptom_template.csv |
| 征象 | `sign` | 0500000-0799999 | sign_template.csv |
| 中草药 | `herb` | 1000000-2999999 | herb_template.csv |
| 方剂 | `formula` | 4000000-5999999 | formula_template.csv |
| 治则 | `principle` | 6000000-6999999 | principle_template.csv |
| 治法 | `method` | 6000000-6999999 | method_template.csv |
| 辨证 | `differentiation` | 7000000-7999999 | differentiation_template.csv |
| 病机 | `pathomechanism` | 8000000-8999999 | pathomechanism_template.csv |

---

## ⚙️ 核心功能

### 1. 字段映射配置 (YAML)

`term-import-config.yaml` 定义了：
- ✅ 通用字段（标签、定义、同义词等）
- ✅ 类别特定字段（关系属性）
- ✅ 外部本体前缀
- ✅ 验证规则

### 2. Python 导入脚本

`import_terms.py` 实现了：
- ✅ CSV/Excel 文件读取
- ✅ 数据验证（ID格式、必填字段、引用完整性）
- ✅ OWL 本体操作（创建类、添加注释、建立关系）
- ✅ 导入报告生成
- ✅ 自动备份

### 3. CSV 模板

每个类别提供示例模板：
- ✅ 包含所有字段列
- ✅ 示例数据行
- ✅ 字段说明注释

---

## 🔍 字段说明示例

### Pattern (证候) 字段

**必填字段**:
- `tch_id`: TCH_0001001
- `label_zh`: 寒证
- `label_en`: Cold pattern
- `definition_zh`: 以恶寒、肢冷...
- `definition_en`: A pattern characterized by...

**关系字段**:
- `has_sign`: TCH_0500001|TCH_0500002 (具有的征象)
- `has_symptom`: TCH_0200001|TCH_0200002 (具有的症状)
- `reflect_pathomechanism`: TCH_8000001 (反映的病机)

**元数据字段**:
- `sources`: 《中医诊断学》|《中医基础理论》
- `evidence_ECO`: ECO:0000033
- `date_accessed`: 2025-10-31

---

## 💡 使用技巧

### 技巧 1: 使用 Excel 编辑

CSV 文件可以用 Excel 打开编辑，但保存时选择"UTF-8 CSV"格式。

### 技巧 2: 多值分隔

使用 `|` 分隔多个值：
```
TCH_0001001|TCH_0001002|TCH_0001003
```

### 技巧 3: 先验证后导入

始终先使用 `--validate-only` 验证数据：
```bash
python import_terms.py --category pattern --input data.csv --validate-only
```

### 技巧 4: 批量导入

创建脚本批量导入多个类别：
```bash
#!/bin/bash
for cat in pattern disease symptom; do
  python import_terms.py --category $cat --input data/${cat}.csv
done
```

### 技巧 5: 查看日志

导入过程会生成详细日志：
- 控制台输出：实时查看
- `term_import.log`：完整日志
- `term_import_report_*.txt`：导入报告

---

## ❗ 常见问题

### Q: 中文乱码？
A: 使用 UTF-8 编码保存 CSV 文件

### Q: ID 范围错误？
A: 检查术语ID是否在类别范围内

### Q: 引用的术语不存在？
A: 先导入被引用的术语，或在同批次中一起导入

### Q: 导入失败如何回滚？
A: 使用自动备份文件 `tch-edit.owl.backup.*`

---

## 📚 完整文档

详细说明请查看：[docs/TERM_IMPORT_GUIDE.md](../docs/TERM_IMPORT_GUIDE.md)

---

## 🔗 相关资源

- **配置文件**: `src/ontology/term-import-config.yaml`
- **导入脚本**: `src/scripts/import_terms.py`
- **模板目录**: `src/scripts/templates/`
- **详细指南**: `docs/TERM_IMPORT_GUIDE.md`

---

**维护**: TCH Ontology Team  
**更新**: 2025-10-31
