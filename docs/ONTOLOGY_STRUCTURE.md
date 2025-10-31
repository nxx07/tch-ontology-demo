# Traditional Chinese Medicine Cold-Heat Pattern Ontology (TCH)

## 寒热证本体结构说明

### 概述 / Overview

本本体（TCH Ontology）是一个用于表示传统中医寒热证候及相关概念的形式化知识表示系统。基于 BFO（Basic Formal Ontology）、RO（Relation Ontology）、IAO（Information Artifact Ontology）和 PATO（Phenotypic Quality Ontology）等上层本体构建。

This ontology (TCH Ontology) is a formal knowledge representation system for Traditional Chinese Medicine cold-heat patterns and related concepts, built on top of BFO (Basic Formal Ontology), RO (Relation Ontology), IAO (Information Artifact Ontology), and PATO (Phenotypic Quality Ontology).

---

## 本体类别结构 / Ontology Class Structure

### 1. 证候类 (Pattern/Syndrome) - TCH_0001000 系列
**BFO 范畴**: Disposition (倾向性)  
**ID 范围**: TCH_0001000 - TCH_0099999 (容量: 99,000)

- **TCH_0001000** - Pattern (证候/证)
  - **TCH_0001001** - Cold pattern (寒证)
  - **TCH_0001002** - Heat pattern (热证)
  - **TCH_0001003** - Cold-Heat complex pattern (寒热错杂证)

**定义**: 在一定病因病机作用下由相互联系的症状与体征构成的总体倾向。  
**外部映射**: ICD-11 TM (Traditional Medicine), OGMS

**关键关系**:
- `has part` (BFO:0000051) → Symptom/Sign
- `causally downstream of` (RO:0002404) → Pathomechanism

---

### 2. 中医疾病类 (TCM Disease) - TCH_0100000 系列
**BFO 范畴**: Disposition (倾向性)  
**ID 范围**: TCH_0100000 - TCH_0199999 (容量: 100,000)

- **TCH_0100000** - TCM disease (中医疾病)

**定义**: 以病名与病机为核心、可跨多个证候阶段的疾病性倾向。  
**外部映射**: MONDO, DOID, ICD-11 MMS, OGMS

**关键关系**:
- `has symptom` (RO:0002452) → Symptom
- `has part` (BFO:0000051) → Sign
- `realized in` (BFO:0000054) → Pathomechanism
- `inheres in` (RO:0000052) → Pattern/Organ

---

### 3. 症状与征象类 (Symptom & Sign) - TCH_0200000 & TCH_0500000 系列
**BFO 范畴**: Quality (性质)  
**ID 范围**: 
- Symptom: TCH_0200000 - TCH_0499999 (容量: 300,000)
- Sign: TCH_0500000 - TCH_0799999 (容量: 300,000)

- **TCH_0200000** - Symptom (症状)
- **TCH_0500000** - Sign (征象)

**定义**:
- 症状: 患者主观感受到的异常体验
- 征象: 医者客观观察或测得的异常征象

**外部映射**: HPO, PATO, ISO 23961 (舌脉诊)

**关键关系**:
- `inheres in` (RO:0000052) → Organ
- `located in` (RO:0001025) → Organ (征象)
- `depends on` (RO:0002502) → Environment

---

### 4. 器官与脏腑系统类 (Organ & Viscera) - TCH_0800000 系列
**BFO 范畴**: Material Entity (物质实体)  
**ID 范围**: TCH_0800000 - TCH_0899999 (容量: 100,000)

- **TCH_0800000** - Organ (器官)
- **TCH_0800001** - Viscera system (脏腑系统)

**定义**:
- 器官: 中医语境下的人体器官结构
- 脏腑系统: 中医理论中的功能性脏腑系统

**外部映射**: UBERON

**关键关系**:
- Organ `part of` (BFO:0000050) → Viscera system
- Viscera system `has part` (BFO:0000051) → Organ

---

### 5. 经络与腧穴类 (Meridian & Acupoint) - TCH_0900000 系列
**BFO 范畴**: Immaterial Entity - Site (非物质实体 - 位点)  
**ID 范围**: TCH_0900000 - TCH_0999999 (容量: 100,000)

- **TCH_0900000** - Meridian (经络)
- **TCH_0900001** - Acupoint (腧穴)

**定义**:
- 经络: 中医理论中气血运行的通路
- 腧穴: 经络上用于针灸的特定穴位点

**外部映射**: ADO (Acupuncture & Moxibustion Ontology), WHO

**关键关系**:
- Meridian `has part` (BFO:0000051) → Acupoint
- Meridian `connected to` (RO:0002170) → Viscera system
- Acupoint `part of` (BFO:0000050) → Meridian

---

### 6. 中草药及药性类 (Herb & Properties) - TCH_1000000 & TCH_3000000 系列
**ID 范围**: 
- Herb: TCH_1000000 - TCH_2999999 (容量: 2,000,000)
- Properties: TCH_3000000 - TCH_3999999 (容量: 1,000,000)

#### 6.1 中草药 (Herb) - TCH_1000000
**BFO 范畴**: Material Entity (物质实体)

**定义**: 源于自然的中医药用材料  
**外部映射**: TCDO, CHEBI

#### 6.2 药性 (TCM Nature) - TCH_3000000
**BFO 范畴**: Disposition (倾向性)

**定义**: 药物的温热寒凉属性倾向（温/热/凉/寒）  
**外部映射**: TCDO

#### 6.3 药味 (TCM Flavor) - TCH_3000001
**BFO 范畴**: Quality (性质)

**定义**: 药物的辛甘苦酸咸等味道属性  
**外部映射**: TCDO

#### 6.4 归经 (Channel Tropism) - TCH_3000002
**BFO 范畴**: Disposition (倾向性)

**定义**: 药物作用于特定经络的倾向  
**外部映射**: TCDO

**关键关系**:
- Herb `has disposition` (RO:0000091) → TCM Nature
- Herb `has quality` (RO:0000086) → TCM Flavor
- Herb `has disposition` (RO:0000091) → Channel Tropism

---

### 7. 方剂类 (Formula) - TCH_4000000 系列
**BFO 范畴**: Information Content Entity - Plan Specification  
**ID 范围**: TCH_4000000 - TCH_5999999 (容量: 2,000,000)

- **TCH_4000000** - Formula (方剂)

**定义**: 多味中药配伍组成的处方  
**外部映射**: DRON

**关键关系**:
- `realized in` (BFO:0000054) → Herb

---

### 8. 治则与治法类 (Therapeutic Principles & Methods) - TCH_6000000 系列
**BFO 范畴**: Information Content Entity - Plan Specification  
**ID 范围**: TCH_6000000 - TCH_6999999 (容量: 1,000,000)

- **TCH_6000000** - Therapeutic principle (治则)
- **TCH_6000001** - Therapeutic method (治法)

**定义**:
- 治则: 治疗的总体指导原则
- 治法: 由治则派生的具体治疗方法

**外部映射**: IAO, OBI, MAxO

**关键关系**:
- Principle `is concretized by` (BFO:0000165) → Method
- Principle `has input` (RO:0002233) → Pattern
- Principle `occurs in` (BFO:0000066) → TCM Disease
- Method `is about` (IAO:0000136) → Pattern/Disease

---

### 9. 诊断与辨证类 (Diagnostic & Pattern Differentiation) - TCH_7000000 系列
**ID 范围**: TCH_7000000 - TCH_7999999 (容量: 1,000,000)

#### 9.1 辨证 (Pattern Differentiation) - TCH_7000000
**BFO 范畴**: Process (过程)

**定义**: 分析症状体征以识别证候的过程  
**外部映射**: OBI, OGMS

#### 9.2 诊断 (Diagnostic Assertion) - TCH_7000001
**BFO 范畴**: Information Content Entity

**定义**: 关于患者证候或疾病的结论性陈述  
**外部映射**: OGMS, IAO, PROV, ECO

**关键关系**:
- Pattern Differentiation `causally related to` (RO:0002410) → Pattern
- Diagnostic `is about` (IAO:0000136) → Pattern/Disease

---

### 10. 病机类 (Pathomechanism) - TCH_8000000 系列
**BFO 范畴**: Process (过程)  
**ID 范围**: TCH_8000000 - TCH_8999999 (容量: 1,000,000)

- **TCH_8000000** - Pathomechanism (病机)

**定义**: 疾病发生、发展的病理机制  

**关键关系**:
- `causally related to` (RO:0002410) → TCM Disease
- `causally related to` (RO:0002410) → Pattern
- Pattern `causally downstream of` (RO:0002404) → Pathomechanism

---

### 11. 环境类 (Environment) - TCH_9000000 系列
**BFO 范畴**: Material Entity (物质实体)  
**ID 范围**: TCH_9000000 - TCH_9999999 (容量: 1,000,000)

- **TCH_9000000** - Environment (环境)

**定义**: 影响证候的季节、气候等环境因素  
**外部映射**: ENVO

**关键关系**:
- Symptom/Sign `depends on` (RO:0002502) → Environment

---

## 核心对象属性 / Core Object Properties

### 组成关系 (Compositional Relations)
- `has part` (BFO:0000051) - 具有部分
- `part of` (BFO:0000050) - 部分属于
- `has component` - 具有组成成分

### 依存关系 (Inherence Relations)
- `inheres in` (RO:0000052) - 依存于
- `bearer of` (RO:0000053) - 承载

### 定位关系 (Location Relations)
- `located in` (RO:0001025) - 位于
- `occurs in` (BFO:0000066) - 发生于

### 因果关系 (Causal Relations)
- `causally related to` (RO:0002410) - 因果相关
- `causally downstream of` (RO:0002404) - 因果下游

### 功能关系 (Functional Relations)
- `has disposition` (RO:0000091) - 具有倾向性
- `has quality` (RO:0000086) - 具有性质
- `realized in` (BFO:0000054) - 实现于
- `has role` (RO:0000087) - 具有角色

### 信息关系 (Information Relations)
- `is about` (IAO:0000136) - 关于
- `has input` (RO:0002233) - 具有输入
- `has output` (RO:0002234) - 具有输出
- `is concretized by` (BFO:0000165) - 具体化为

### 表现关系 (Manifestation Relations)
- `has symptom` (RO:0002452) - 具有症状
- `has part` (BFO:0000051) - 具有部分（用于 Sign）

### 连接关系 (Connection Relations)
- `connected to` (RO:0002170) - 连接到
- `depends on` (RO:0002502) - 依赖于

---

## ID 范围分配 / ID Range Allocation

本体采用 7 位数字编码系统，总容量 10,000,000 个 ID，为各类别预留充足的扩展空间。

The ontology uses a 7-digit numeric coding system with a total capacity of 10,000,000 IDs, providing ample expansion space for each category.

| 范围 | 类别 | 预计容量 | 说明 |
|------|------|---------|------|
| TCH_0000001-TCH_0000999 | Root & Metadata | 999 | 根类及元数据 |
| TCH_0001000-TCH_0099999 | Pattern/Syndrome | 99,000 | 证候类（含寒热虚实等各类证型） |
| TCH_0100000-TCH_0199999 | TCM Disease | 100,000 | 中医疾病类 |
| TCH_0200000-TCH_0499999 | Symptom | 300,000 | 症状类（主观感受） |
| TCH_0500000-TCH_0799999 | Sign | 300,000 | 征象类（客观体征，含舌脉诊） |
| TCH_0800000-TCH_0899999 | Organ & Viscera | 100,000 | 器官与脏腑系统类 |
| TCH_0900000-TCH_0999999 | Meridian & Acupoint | 100,000 | 经络与腧穴类 |
| TCH_1000000-TCH_2999999 | Herb | 2,000,000 | 中草药类（含植物、动物、矿物药） |
| TCH_3000000-TCH_3999999 | Herb Properties | 1,000,000 | 药性、药味、归经等属性类 |
| TCH_4000000-TCH_5999999 | Formula | 2,000,000 | 方剂类（经典方、现代方） |
| TCH_6000000-TCH_6999999 | Therapeutic | 1,000,000 | 治则与治法类 |
| TCH_7000000-TCH_7999999 | Diagnostic | 1,000,000 | 诊断与辨证类 |
| TCH_8000000-TCH_8999999 | Pathomechanism | 1,000,000 | 病机类 |
| TCH_9000000-TCH_9999999 | Environment & Others | 1,000,000 | 环境因素及其他类 |

### 当前已分配 ID / Currently Allocated IDs

| ID | 类别 | 中文名 | 英文名 |
|------|------|--------|--------|
| TCH_0000000 | Root | 寒热证本体实体 | Cold-Heat pattern ontology entity |
| TCH_0001000 | Pattern | 证候/证 | Pattern / Syndrome |
| TCH_0001001 | Pattern | 寒证 | Cold pattern |
| TCH_0001002 | Pattern | 热证 | Heat pattern |
| TCH_0001003 | Pattern | 寒热错杂证 | Cold-Heat complex pattern |
| TCH_0100000 | Disease | 中医疾病 | TCM Disease |
| TCH_0200000 | Symptom | 症状 | Symptom |
| TCH_0500000 | Sign | 征象 | Sign |
| TCH_0800000 | Organ | 器官 | Organ |
| TCH_0800001 | Viscera | 脏腑系统 | Viscera system |
| TCH_0900000 | Meridian | 经络 | Meridian |
| TCH_0900001 | Acupoint | 腧穴 | Acupoint |
| TCH_1000000 | Herb | 中草药 | Herb |
| TCH_3000000 | Property | 药性 | TCM Nature |
| TCH_3000001 | Property | 药味 | TCM Flavor |
| TCH_3000002 | Property | 归经 | Channel Tropism |
| TCH_4000000 | Formula | 方剂 | Formula |
| TCH_6000000 | Therapeutic | 治则 | Therapeutic principle |
| TCH_6000001 | Therapeutic | 治法 | Therapeutic method |
| TCH_7000000 | Diagnostic | 辨证 | Pattern differentiation |
| TCH_7000001 | Diagnostic | 诊断 | Diagnostic assertion |
| TCH_8000000 | Pathomechanism | 病机 | Pathomechanism |
| TCH_9000000 | Environment | 环境 | Environment |

---

## 外部本体映射 / External Ontology Mappings

### 上层本体 (Upper Ontologies)
- **BFO** (Basic Formal Ontology) - 基础形式本体
- **RO** (Relation Ontology) - 关系本体
- **IAO** (Information Artifact Ontology) - 信息制品本体
- **PATO** (Phenotypic Quality Ontology) - 表型性质本体

### 领域本体 (Domain Ontologies)
- **MONDO** / **DOID** - 疾病本体
- **HPO** (Human Phenotype Ontology) - 人类表型本体
- **UBERON** - 解剖学本体
- **CHEBI** - 化学实体本体
- **ENVO** (Environment Ontology) - 环境本体
- **TCDO** (Traditional Chinese Drug Ontology) - 中药本体
- **ADO** (Acupuncture & Moxibustion Ontology) - 针灸本体

### 医学标准 (Medical Standards)
- **ICD-11** (International Classification of Diseases) - 国际疾病分类
  - TM (Traditional Medicine) - 传统医学模块
  - MMS (Mortality and Morbidity Statistics) - 死亡和发病统计
- **ISO 23961** - 舌诊脉诊国际标准
- **WHO** - 世界卫生组织标准 (腧穴命名)

### 其他相关 (Related)
- **OGMS** (Ontology for General Medical Science) - 通用医学科学本体
- **OBI** (Ontology for Biomedical Investigations) - 生物医学研究本体
- **MAxO** (Medical Action Ontology) - 医学行为本体
- **DRON** (Drug Ontology) - 药物本体
- **PROV** (Provenance Ontology) - 溯源本体
- **ECO** (Evidence & Conclusion Ontology) - 证据与结论本体

---

## 使用示例 / Usage Examples

### 示例 1: 寒证的定义
```
寒证 (Cold pattern)
  - 类型: Disposition
  - 父类: Pattern
  - has part: 恶寒 (Symptom), 肢冷 (Symptom), 舌淡 (Sign), 脉迟 (Sign)
  - causally downstream of: 阳虚病机 (Pathomechanism)
```

### 示例 2: 附子的属性
```
附子 (Aconite)
  - 类型: Herb (Material Entity)
  - has disposition: 热性 (Hot nature)
  - has quality: 辛味 (Pungent flavor)
  - has disposition: 归心经、归肾经 (Channel tropism)
```

### 示例 3: 治疗关系
```
辛温解表法 (Acrid-warm exterior-releasing method)
  - 类型: Therapeutic method
  - is about: 表寒证 (Exterior cold pattern)
  - realized in: 麻黄汤 (Ma Huang Tang formula)
```

---

## 开发工具 / Development Tools

- **ODK** (Ontology Development Kit) v1.6
- **ROBOT** (ROBOT is an OBO Tool) v1.9.8
- **Protégé** - 推荐用于可视化编辑

---

## 维护说明 / Maintenance Notes

### 编辑工作流
1. 编辑 `src/ontology/tch-edit.owl` 文件
2. 运行 `sh run.sh make` 构建本体
3. 检查 `reports/` 目录中的报告
4. 提交更改到 Git

### 发布流程
1. 更新版本号
2. 运行完整构建
3. 创建 GitHub release
4. 生成发布文件

---

## 许可证 / License

待定 (To be determined)

---

## 联系方式 / Contact

GitHub: https://github.com/nxx07/tch-ontology-demo

---

*最后更新: 2025-10-30*
