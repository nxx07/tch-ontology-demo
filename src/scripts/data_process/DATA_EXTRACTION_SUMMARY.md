# TCM多源数据提取总结

## 📊 提取结果概览

### ✅ 所有数据类型提取完成

| 数据类型 | 数据源1 | 记录数1 | 数据源2 | 记录数2 | 总记录数 | 文件大小 |
|---------|---------|---------|---------|---------|----------|----------|
| **Pattern (证候)** | symap.SymMap_v2_0__SMSY_file | 233 | - | - | **2,294** (含原有2,061) | 1,078 KB |
| **Symptom (症状)** | symap.SymMap_v2_0__SMTS_file | 2,364 | - | - | **2,364** | 625 KB |
| **Herb (中药)** | herb2_0.HERB_herb_info_v2 | 6,892 | etcm2_0.chinese_medical_materials | 2,079 | **8,971** | 2,391 KB |
| **Formula (方剂)** | herb2_0.HERB_formula_info_v2 | 6,743 | etcm2_0.tcm_formulas_cn | 46,140 | **52,883** | 8,996 KB |

**总计：66,512 条新提取的术语记录**

## 📁 输出文件位置

所有数据文件保存在：
```
/Users/cailingxi/课题组工作/tch-ontology-demo/target/tch/data/data_temp_ids/
├── pattern_data_temp_ids.csv   (2,294 条记录)
├── symptom_data_temp_ids.csv   (2,364 条记录)
├── herb_data_temp_ids.csv      (8,971 条记录)
└── formula_data_temp_ids.csv   (52,883 条记录)
```

## 🔧 技术实现要点

### 1. 字段映射配置
- 使用 `field_mapping.csv` 定义数据库字段到模板字段的映射关系
- 支持复杂字段表达式：
  - 字符串常量：`"SymMap2.0 SMSY"`
  - 字段拼接：`"SymMap2.0 SMSY"+Syndrome_id`
  - 多字段组合：`Herb_id;SymMap_id;"TCMID: "+TCMID_id`

### 2. SQL保留字处理
- 自动用反引号包裹字段名（如 `Function`、`Properties`）
- 避免SQL语法错误

### 3. 临时ID管理
- Pattern: TmpTCH:PATTERN_10000-12293 (新增从12061开始)
- Symptom: TmpTCH:SYMPTOM_20000-22363
- Herb: TmpTCH:HERB_100000-108970
- Formula: TmpTCH:FORMULA_400000-452882

### 4. 分批查询机制
- 每批2,000条记录，避免大数据集超时
- 自动重连机制处理连接断开
- 实时显示提取进度

### 5. 数据追加功能
- 自动识别现有数据的最大ID
- 新数据追加时保持ID唯一性和连续性
- Pattern数据成功追加了233条新记录

## 🔍 字段映射修正

### 修正的字段名
1. **Formula功效字段**：
   - 原配置：`formula_function`
   - 修正为：`Type`
   - 数据库：herb2_0.HERB_formula_info_v2

## 🚀 使用方法

### 单独提取某个数据类型
```bash
cd /Users/cailingxi/课题组工作/tch-ontology-demo/target/tch/src/scripts/data_process
python3 TCM_multi_source_data_process.py pattern
python3 TCM_multi_source_data_process.py symptom
python3 TCM_multi_source_data_process.py herb
python3 TCM_multi_source_data_process.py formula
```

### 提取多个数据类型
```bash
python3 TCM_multi_source_data_process.py pattern symptom
```

### 提取所有数据类型
```bash
python3 TCM_multi_source_data_process.py
```

## 📝 数据源信息

### MySQL数据库配置
- **symap** (SymMap 2.0)
  - Host: eggabc.site:3306
  - Database: symap
  - Tables: SymMap_v2_0__SMSY_file, SymMap_v2_0__SMTS_file

- **herb2_0** (HERB 2.0)
  - Host: eggabc.site:3306
  - Database: herb2_0
  - Tables: HERB_herb_info_v2, HERB_formula_info_v2

- **etcm2_0** (ETCM 2.0)
  - Host: eggabc.site:3306
  - Database: etcm2_0
  - Tables: chinese_medical_materials, tcm_formulas_cn

## ✨ 脚本特性

1. ✅ 支持多数据源提取
2. ✅ 复杂字段表达式解析
3. ✅ SQL保留字自动处理
4. ✅ 临时ID自动分配和管理
5. ✅ 数据追加而非覆盖
6. ✅ 分批查询避免超时
7. ✅ 自动重连机制
8. ✅ 详细的进度显示

## 📊 数据统计

### 按数据源统计
- **SymMap 2.0**: 2,597条 (233 pattern + 2,364 symptom)
- **HERB 2.0**: 13,635条 (6,892 herb + 6,743 formula)
- **ETCM 2.0**: 48,219条 (2,079 herb + 46,140 formula)

### 按数据类型统计
- **证候 (Pattern)**: 233条新增 (总2,294)
- **症状 (Symptom)**: 2,364条
- **中药 (Herb)**: 8,971条
- **方剂 (Formula)**: 52,883条 (最大数据集)

## 📅 提取时间

- Pattern: 2025-11-12 21:52
- Symptom: 2025-11-12 21:52
- Herb: 2025-11-12 21:59
- Formula: 2025-11-12 22:38-22:44

## 🎯 下一步工作建议

1. **数据验证**
   - 验证提取数据的完整性
   - 检查字段映射的正确性
   - 确认临时ID的唯一性

2. **数据清洗**
   - 处理空值和重复值
   - 标准化格式（如日期、名称等）
   - 验证交叉引用的有效性

3. **数据导入**
   - 使用 `import_terms.py` 导入到本体
   - 生成OWL格式文件
   - 验证本体一致性

4. **持续更新**
   - 定期从数据源更新数据
   - 追踪数据版本变化
   - 记录数据变更日志

---

**创建时间**: 2025-11-12 22:45  
**版本**: 1.0  
**脚本**: TCM_multi_source_data_process.py
