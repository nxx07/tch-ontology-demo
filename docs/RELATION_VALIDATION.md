# TCH 本体关系属性验证文档
# TCH Ontology Object Property Validation

本文档验证 tch-edit.owl 中声明的所有对象属性（Object Properties），确保其 IRI 和标签与源 CSV 文件以及 RO/BFO 本体定义一致。

This document validates all object properties declared in tch-edit.owl, ensuring their IRIs and labels match the source CSV file and RO/BFO ontology definitions.

---

## 验证结果总结 / Validation Summary

✅ **所有关系属性已验证正确** / All object properties validated as correct

❌ **已修正错误** / Errors corrected:
- 移除了不存在的 "has sign" (RO:0002451) 关系
- 澄清了 Sign（征象）使用 `has part` (BFO:0000051) 关系

---

## 组成关系 / Compositional Relations

### BFO:0000051 - has part
- **RO 官方标签**: has part
- **CSV 中用法**:
  - Pattern has part Symptom（证候具有症状部分）
  - Pattern has part Sign（证候具有征象部分）
  - TCM Disease has part Sign（中医疾病具有征象部分）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "湿热伤阴证" has part "口渴"

### BFO:0000050 - part of
- **RO 官方标签**: part of
- **CSV 中用法**: 作为 has part 的逆关系
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "口渴" part of "湿热伤阴证"

---

## 依存关系 / Inherence Relations

### RO:0000052 - inheres in
- **RO 官方标签**: inheres in
- **CSV 中用法**: Symptom inheres in Organ（症状依存于器官）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "咽痛" inheres in "咽"

### RO:0000053 - bearer of
- **RO 官方标签**: bearer of
- **关系说明**: inheres in 的逆关系
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "咽" bearer of "咽痛"

---

## 定位关系 / Location Relations

### RO:0001025 - located in
- **RO 官方标签**: located in
- **CSV 中用法**: Sign located in Organ（征象位于器官）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "舌苔" located in "舌"

### BFO:0000066 - occurs in
- **RO 官方标签**: occurs in
- **CSV 中用法**: Principles occurs in TCM Disease（治则应用于疾病）
- **tch-edit.owl 声明**: ✅ 已正确声明

---

## 因果关系 / Causal Relations

### RO:0002404 - causally downstream of
- **RO 官方标签**: causally downstream of
- **CSV 中用法**: Pattern causally downstream of Pathomechanism（证候是病机的下游结果）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "湿热伤阴证" causally downstream of "湿热病机"

### RO:0002410 - causally related to
- **RO 官方标签**: causally related to
- **CSV 中用法**: 
  - Diagnostic causally related to Pattern
  - Pattern differentiation causally related to Pattern
  - Pathomechanism causally related to Disease/Pattern
- **tch-edit.owl 声明**: ✅ 已正确声明

---

## 功能关系 / Functional Relations

### RO:0000091 - has disposition
- **RO 官方标签**: has disposition
- **CSV 中用法**: Herb has disposition（中药具有倾向性/性味）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "黄连" has disposition "寒性"

### RO:0000086 - has quality
- **RO 官方标签**: has quality
- **CSV 中用法**: Herb has quality（中药具有性质）
- **tch-edit.owl 声明**: ✅ 已正确声明

### BFO:0000054 - realized in
- **RO 官方标签**: realized in
- **CSV 中用法**: 功能实现关系
- **tch-edit.owl 声明**: ✅ 已正确声明

### RO:0000087 - has role
- **RO 官方标签**: has role
- **CSV 中用法**: 角色关系
- **tch-edit.owl 声明**: ✅ 已正确声明

---

## 信息关系 / Information Relations

### RO:0002233 - has input
- **RO 官方标签**: has input
- **CSV 中用法**: Principles has input Pattern（治则以证候为输入）
- **tch-edit.owl 声明**: ✅ 已正确声明

### RO:0002234 - has output
- **RO 官方标签**: has output
- **关系说明**: has input 的逆关系
- **tch-edit.owl 声明**: ✅ 已正确声明

### IAO:0000136 - is about
- **IAO 官方标签**: is about
- **CSV 中用法**:
  - Therapeutic method is about Pattern
  - Therapeutic method is about Disease
  - Diagnostic is about Disease
- **tch-edit.owl 声明**: ✅ 已正确声明

### BFO:0000165 - is concretized by
- **RO 官方标签**: is concretized by
- **CSV 中用法**: 抽象概念的具体化关系
- **tch-edit.owl 声明**: ✅ 已正确声明

---

## 表现关系 / Manifestation Relations

### RO:0002452 - has symptom
- **RO 官方标签**: has symptom
- **CSV 中用法**: TCM Disease has symptom Symptom（中医疾病具有症状）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "感冒" has symptom "发热"

### ❌ RO:0002451 - 错误标记为 "has sign"
- **RO 官方标签**: **transmitted by**（传播途径，与医学征象无关！）
- **重要说明**: 此属性在 RO 中表示"通过某种方式传播"，不是 "has sign"
- **正确做法**: Sign（征象）应使用 `has part` (BFO:0000051) 关系
  - Pattern has part Sign
  - TCM Disease has part Sign
- **CSV 中验证**: ✅ CSV 正确使用 BFO:0000051 for Sign
- **tch-edit.owl 状态**: ✅ 未错误声明此属性
- **ONTOLOGY_STRUCTURE.md 状态**: ✅ 已修正错误描述

### ❌ RO:0002556 - "has manifestation" 未使用
- **说明**: 此属性在 CSV 和 tch-edit.owl 中均未使用
- **状态**: ✅ 已从文档中移除

---

## 连接关系 / Connection Relations

### RO:0002170 - connected to
- **RO 官方标签**: connected to
- **CSV 中用法**: Meridian connected to Viscera（经络连接脏腑）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "肺经" connected to "肺"

### RO:0002502 - depends on
- **RO 官方标签**: depends on
- **CSV 中用法**: 
  - Sign depends on Environment（征象依赖环境）
  - Symptom depends on Environment（症状依赖环境）
- **tch-edit.owl 声明**: ✅ 已正确声明
- **使用示例**: "遇寒则痛" depends on "寒冷环境"

---

## 验证方法 / Validation Method

1. ✅ 对照 CSV 源文件检查所有关系用法
2. ✅ 验证 RO/BFO IRI 与官方定义一致
3. ✅ 检查 tch-edit.owl 中的声明完整性
4. ✅ 更新 ONTOLOGY_STRUCTURE.md 中的错误描述
5. ✅ 添加注释说明特殊情况（如 Sign 使用 has part）

---

## 修正总结 / Correction Summary

### 已修正的错误文件：
1. **ONTOLOGY_STRUCTURE.md**
   - 移除错误的 "has sign (RO:0002451)" 描述
   - 添加说明：Sign 使用 `has part` (BFO:0000051)
   - 澄清 RO:0002451 实际是 "transmitted by"

2. **tch-edit.owl**
   - 重新组织对象属性声明，按功能分组
   - 添加详细注释说明每个关系的用途
   - 添加警告注释：RO:0002451 不是 "has sign"

### 未修改的文件（验证为正确）：
- ✅ tch-edit.owl 中的类定义（Classes）
- ✅ CSV 源文件中的关系定义
- ✅ imports 文件夹中的导入本体

---

## 关键发现 / Key Findings

1. **Sign vs Symptom 的关系区别**：
   - Symptom: 使用 `has symptom` (RO:0002452)
   - Sign: 使用 `has part` (BFO:0000051)
   - 原因：在本体中，Sign 被建模为 Pattern/Disease 的组成部分，而非独立的症状关系

2. **RO:0002451 的真实含义**：
   - 官方标签：transmitted by
   - 用途：表示疾病传播途径（如"通过接触传播"）
   - **绝不应用于**表示临床征象关系

3. **CSV 文件是权威来源**：
   - 所有关系映射应以 CSV 为准
   - CSV 中正确使用了 BFO:0000051 for Sign
   - 本次修正使文档与 CSV 保持一致

---

## 后续建议 / Future Recommendations

1. ✅ **定期验证**：每次添加新关系时，对照 CSV 和 RO/BFO 官方定义验证
2. ✅ **文档同步**：确保 tch-edit.owl 注释、ONTOLOGY_STRUCTURE.md 和 CSV 保持一致
3. ✅ **使用标准工具**：使用 ROBOT 工具验证关系属性的正确性
4. 📝 **建立检查清单**：创建 pre-commit 检查，自动验证新增关系的 IRI

---

**验证完成时间**: 2025
**验证者**: GitHub Copilot
**状态**: ✅ 所有关系属性已验证并修正
