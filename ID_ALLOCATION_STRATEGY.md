# TCH 本体 ID 分配策略
# TCH Ontology ID Allocation Strategy

## 概述 / Overview

TCH 本体采用 **7 位数字编码系统**（TCH_0000000 - TCH_9999999），总容量为 **1000 万个 ID**，为各类术语预留充足的扩展空间。

The TCH ontology uses a **7-digit numeric coding system** (TCH_0000000 - TCH_9999999) with a total capacity of **10 million IDs**, providing ample expansion space for各 term categories.

---

## ID 范围分配原则 / ID Range Allocation Principles

### 1. 容量评估 / Capacity Assessment

基于以下因素确定各类别的 ID 容量需求：

Capacity requirements for each category are determined based on the following factors:

- **现有术语数量** / Existing term count
  - 参考现有中医术语数据库（如 TCDO、ISO 23961、ICD-11 TM）
  - Reference existing TCM terminology databases (e.g., TCDO, ISO 23961, ICD-11 TM)

- **增长潜力** / Growth potential
  - 历史文献挖掘空间
  - Space for historical literature mining
  - 地方性证候、药材、方剂的收录
  - Inclusion of regional patterns, herbs, and formulas
  - 现代中医临床新发现
  - Modern TCM clinical discoveries

- **多样性因素** / Diversity factors
  - 中草药：植物药、动物药、矿物药（约 1.3 万种基础药材）
  - Herbs: Plant, animal, mineral medicines (~13,000 base materials)
  - 方剂：经典方剂、地方方、院内制剂（数十万种）
  - Formulas: Classic formulas, regional formulas, hospital preparations (hundreds of thousands)
  - 症状与征象：主观症状 + 客观体征（舌诊、脉诊、望诊等细分）
  - Symptoms & Signs: Subjective symptoms + objective signs (tongue, pulse, inspection subdivisions)

### 2. 预留空间策略 / Reserved Space Strategy

采用"**宁多勿少**"的原则，为高增长类别预留 10-20 倍的扩展空间：

Follow the principle of "**better too much than too little**", reserving 10-20 times expansion space for high-growth categories:

- **中草药** (TCH_1000000-2999999): 200 万容量
  - 当前约 13,000 种基础药材
  - 预留空间供不同产地、炮制方法、药用部位的细分
  
- **方剂** (TCH_4000000-5999999): 200 万容量
  - 经典方剂约 10 万首
  - 预留空间供现代方剂、院内制剂、复方颗粒等

- **症状** (TCH_0200000-0499999): 30 万容量
- **征象** (TCH_0500000-0799999): 30 万容量
  - 分离症状与征象，便于语义区分
  - 舌诊、脉诊、面诊等可细分出数千种体征

### 3. 类别边界清晰性 / Category Boundary Clarity

使用"百万级"或"十万级"边界，便于人工识别和管理：

Use "million-level" or "hundred-thousand-level" boundaries for easy human recognition and management:

- ✅ **推荐** / Recommended: TCH_1000000 (Herb), TCH_3000000 (Properties), TCH_4000000 (Formula)
- ❌ **不推荐** / Not recommended: TCH_1234567, TCH_2345678 (不规则边界 / Irregular boundaries)

---

## 详细分配表 / Detailed Allocation Table

| 范围 | 类别 (中文) | 类别 (English) | 容量 | 当前使用 | 使用率 | 设计理由 |
|------|------------|----------------|------|---------|--------|---------|
| **TCH_0000001-0000999** | 根类与元数据 | Root & Metadata | 999 | 1 | 0.1% | 保留给本体基础设施 |
| **TCH_0001000-0099999** | 证候 | Pattern/Syndrome | 99,000 | 4 | 0.004% | 证候类型多样，含八纲辨证、脏腑辨证、六经辨证、卫气营血等各体系 |
| **TCH_0100000-0199999** | 中医疾病 | TCM Disease | 100,000 | 1 | 0.001% | 中医病名数千种，预留空间供现代疾病中医命名 |
| **TCH_0200000-0499999** | 症状 | Symptom | 300,000 | 1 | 0.0003% | 主观症状种类繁多，含部位、性质、程度等维度组合 |
| **TCH_0500000-0799999** | 征象 | Sign | 300,000 | 1 | 0.0003% | 客观体征，重点是舌诊（数千种）、脉诊（数百种）及其组合 |
| **TCH_0800000-0899999** | 器官与脏腑 | Organ & Viscera | 100,000 | 2 | 0.002% | 解剖学器官 + 中医脏腑系统（五脏六腑及经络连属） |
| **TCH_0900000-0999999** | 经络与腧穴 | Meridian & Acupoint | 100,000 | 2 | 0.002% | 361 个经穴 + 奇穴 + 阿是穴 + 新穴，预留空间供现代发现 |
| **TCH_1000000-2999999** | 中草药 | Herb | 2,000,000 | 1 | 0.00005% | 基础药材 1.3 万种，含不同产地、炮制方法、药用部位的细分 |
| **TCH_3000000-3999999** | 药性属性 | Herb Properties | 1,000,000 | 3 | 0.0003% | 药性（四气）、药味（五味）、归经、升降浮沉、毒性等多维属性 |
| **TCH_4000000-5999999** | 方剂 | Formula | 2,000,000 | 1 | 0.00005% | 经典方剂 10 万首，现代方剂、院内制剂数十万种 |
| **TCH_6000000-6999999** | 治则与治法 | Therapeutic | 1,000,000 | 2 | 0.0002% | 治则（总体原则）、治法（具体方法）分层表示 |
| **TCH_7000000-7999999** | 诊断与辨证 | Diagnostic | 1,000,000 | 2 | 0.0002% | 辨证过程、诊断结论、四诊方法（望闻问切） |
| **TCH_8000000-8999999** | 病机 | Pathomechanism | 1,000,000 | 1 | 0.0001% | 病因病机理论，含六淫、七情、饮食劳倦等 |
| **TCH_9000000-9999999** | 环境 | Environment | 1,000,000 | 1 | 0.0001% | 气候、节气、地理环境对证候的影响 |

**总计 / Total**: 10,000,000 IDs | 当前使用 / Currently used: 23 | 使用率 / Usage rate: 0.00023%

---

## ID 分配决策依据 / ID Allocation Decision Basis

### 高容量类别 (200 万) / High-Capacity Categories (2M)

#### 中草药 (Herb) - 2,000,000 IDs
**理由 / Rationale:**
- **基础药材约 1.3 万种**（《中华本草》收录 8,980 种，加上地方药材、民族药）
- **炮制方法多样化**：同一药材可有生用、蜜炙、醋炙、盐炙、姜炙等数十种炮制品
  - 例如：甘草 → 生甘草、炙甘草、蜜炙甘草
- **产地差异**：道地药材，如四川黄连、云南三七、东北人参
- **药用部位**：同一植物的根、茎、叶、花、果实、种子可能是不同的药材
  - 例如：桑树 → 桑叶、桑枝、桑葚、桑白皮

**实际示例 / Real Examples:**
- 麻黄: TCH_1000001 (基础)
- 蜜麻黄: TCH_1000002 (炮制变体)
- 麻黄根: TCH_1000003 (不同药用部位)

#### 方剂 (Formula) - 2,000,000 IDs
**理由 / Rationale:**
- **经典方剂**：《伤寒论》《金匮要略》《千金方》等古籍收录约 10 万首
- **现代方剂**：中成药、院内制剂、现代临床经验方
- **地方方剂**：各地民间验方、少数民族方剂
- **剂型变化**：同一方剂可能有汤剂、丸剂、散剂、颗粒剂等形式

**实际示例 / Real Examples:**
- 麻黄汤: TCH_4000001 (原方)
- 麻黄加术汤: TCH_4000002 (加味方)
- 小青龙汤: TCH_4000003 (类方)

### 中高容量类别 (100 万) / Medium-High Capacity (1M)

#### 药性属性 (Herb Properties) - 1,000,000 IDs
- 四气（寒、热、温、凉）+ 平性
- 五味（辛、甘、苦、酸、咸）+ 淡、涩
- 归经（十二经络）
- 升降浮沉
- 有毒无毒（大毒、有毒、小毒、无毒）
- 属性组合形成大量复合概念

#### 治则与治法 / 病机 / 诊断 (各 100 万) / Each 1M
- 治疗理论体系完善，含八法（汗、吐、下、和、温、清、消、补）及各种子类
- 病机理论涵盖六淫、七情、饮食劳倦、痰饮、瘀血等多维度
- 四诊方法（望、闻、问、切）及各细分技术

### 中容量类别 (10 万) / Medium Capacity (100K)

#### 证候 / 疾病 / 器官与脏腑 / 经络与腧穴 (各 10 万) / Each 100K
- **证候**：八纲辨证、脏腑辨证、六经辨证、卫气营血辨证、三焦辨证等体系
- **疾病**：中医病名数千种，预留空间供与现代医学对接
- **器官脏腑**：解剖学器官 + 五脏六腑系统 + 经络连属
- **经络腧穴**：361 经穴 + 约 1,500 奇穴 + 阿是穴 + 现代新穴

### 高容量类别 (30 万) / High Capacity for Signs (300K)

#### 症状 & 征象 (各 30 万) / Symptom & Sign (Each 300K)
**分离设计理由 / Separation Design Rationale:**
- **语义清晰性**：症状（主观）vs 征象（客观）在临床和研究中需严格区分
- **数量对等性**：症状和征象在中医诊断中同等重要，各需独立大容量空间
- **舌脉诊特殊性**：
  - 舌诊：舌质（颜色、形态）× 舌苔（颜色、厚薄、润燥）= 数千种组合
    - 例如：淡红舌、红舌、绛舌、紫舌、青舌
    - 薄白苔、厚黄苔、白腻苔、黄燥苔...
  - 脉诊：28 种基本脉象 × 部位（寸关尺、左右手）× 强度 = 数百种组合
  - 组合舌象脉象：红舌黄苔 + 数脉 = 数万种临床体征组合

---

## 扩展策略 / Expansion Strategy

### 1. 垂直扩展 (Vertical Expansion)
在现有类别内增加子类，例如：
- TCH_1000001: 人参
  - TCH_1000002: 野山参
  - TCH_1000003: 园参
  - TCH_1000004: 红参
  - TCH_1000005: 白参
  - TCH_1000006: 西洋参

### 2. 水平扩展 (Horizontal Expansion)
未来如需新增一级类别，可使用预留的"10000000 以上"范围（见 `tch-idranges.owl`）：
- TCH_10000000-19999999: 预留给未来扩展类别
- TCH_20000000-99999999: 更长远的预留空间

### 3. 版本管理 (Version Management)
- 使用 `owl:deprecated` 标记过时术语
- 使用 `IAO:0100001` (term replaced by) 指向替代术语
- 不回收已分配的 ID，避免语义混淆

---

## 最佳实践 / Best Practices

### ID 分配流程 / ID Allocation Process

1. **确定类别** / Determine category
   - 根据术语的 BFO 范畴和语义确定所属类别
   
2. **检查现有术语** / Check existing terms
   - 使用 SPARQL 或 grep 搜索避免重复
   
3. **顺序分配** / Sequential allocation
   - 在相应类别的当前最大 ID 基础上 +1
   - 例如：Pattern 类最后一个是 TCH_0001003，新增为 TCH_0001004
   
4. **记录元数据** / Record metadata
   - 添加 rdfs:label (中英文)
   - 添加 IAO:0000115 (定义)
   - 添加 oboInOwl:hasDbXref (外部映射)

### ID 使用注意事项 / ID Usage Notes

✅ **应该做** / Do:
- 使用 7 位数字，前导零不可省略: `TCH_0001000`
- 为同一概念的不同方面使用连续 ID（便于管理）
- 定期更新 ID 使用统计

❌ **不应该做** / Don't:
- 跨类别"跳号"分配 ID
- 回收已废弃术语的 ID
- 使用非数字字符（如 TCH_00A1000）

---

## 统计与监控 / Statistics and Monitoring

### 当前使用情况 / Current Usage (as of 2025)

- **总容量** / Total Capacity: 10,000,000
- **已分配** / Allocated: 23
- **使用率** / Usage Rate: 0.00023%
- **剩余容量** / Remaining: 9,999,977 (99.99977%)

### 容量预警阈值 / Capacity Warning Thresholds

| 类别 | 容量 | 50% 警告阈值 | 80% 警告阈值 | 90% 紧急阈值 |
|------|------|------------|------------|------------|
| Pattern | 99,000 | 49,500 | 79,200 | 89,100 |
| Herb | 2,000,000 | 1,000,000 | 1,600,000 | 1,800,000 |
| Formula | 2,000,000 | 1,000,000 | 1,600,000 | 1,800,000 |
| Symptom | 300,000 | 150,000 | 240,000 | 270,000 |
| Sign | 300,000 | 150,000 | 240,000 | 270,000 |

**建议** / Recommendations:
- 当某类别达到 50% 容量时，评估是否需要调整分配
- 达到 80% 时，考虑启用预留的扩展空间
- 达到 90% 时，紧急重新规划 ID 范围

---

## 参考文献 / References

1. **OBO Foundry ID Policy**  
   - http://obofoundry.org/id-policy.html

2. **中华本草**  
   - 收录约 8,980 种中药材
   
3. **方剂学**（第 9 版）  
   - 常用经典方剂约 10 万首
   
4. **ISO 23961:2022**  
   - 中医舌诊与脉诊标准化术语
   
5. **ICD-11 Traditional Medicine (TM)**  
   - 世界卫生组织传统医学分类

---

## 版本历史 / Version History

- **v2.0** (2025-10-30): 重新设计 ID 范围，采用 7 位系统，总容量扩展到 1000 万
- **v1.0** (2025-10-29): 初始 ID 范围设计，采用 4-5 位系统

---

## 联系方式 / Contact

如有 ID 分配相关问题，请通过 GitHub Issue 联系：  
For ID allocation questions, please contact via GitHub Issue:

📧 GitHub: https://github.com/nxx07/tch-ontology-demo/issues
