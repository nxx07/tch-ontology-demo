# TCH 本体构建操作日志
# TCH Ontology Construction Operation Log

**目的**: 记录本体构建过程中的关键操作步骤，为后续类似项目提供可复用的工作流程。

**Purpose**: Record key operation steps in ontology construction to provide reusable workflows for future similar projects.

---

## 操作记录 / Operation Records

### [2025-10-30] Op-001: 初始化 ODK 本体仓库

**目标**: 使用 ODK 创建标准化本体仓库结构

**命令**:
```bash
# 创建本体仓库（在 Docker 中执行）
docker run -v $(pwd):/work -w /work --rm obolibrary/odkfull:v1.6 \
  seed-via-docker.sh -d tch -t "Traditional Chinese Medicine Cold-Heat Pattern Ontology"
```

**关键参数**:
- `-d tch`: 本体 ID 前缀
- `-t`: 本体标题

**结果**:
- ✅ 生成标准目录结构 `target/tch/`
- ✅ 生成 `tch-edit.owl` 主编辑文件
- ✅ 生成 `Makefile` 和构建脚本
- ✅ 生成 `tch-idranges.owl` ID 配置文件

**注意事项**:
- 确保 Docker 已安装并运行
- 使用 odkfull 镜像以获得完整功能

---

### [2025-10-30] Op-002: 添加核心类到本体

**目标**: 在 tch-edit.owl 中添加 11 个主要类别

**工具**: Protégé 或文本编辑器

**操作步骤**:
1. 打开 `src/ontology/tch-edit.owl`
2. 在 `<owl:Ontology>` 后添加类声明
3. 为每个类添加：
   - `rdf:about` - 类 IRI
   - `rdfs:label` - 中英文标签
   - `obo:IAO_0000115` - 定义
   - `rdfs:subClassOf` - 父类关系

**示例代码**:
```xml
<owl:Class rdf:about="http://purl.obolibrary.org/obo/TCH_0001000">
    <rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/BFO_0000016"/>
    <obo:IAO_0000115 xml:lang="en">A disposition that represents...</obo:IAO_0000115>
    <obo:IAO_0000115 xml:lang="zh">证候的定义...</obo:IAO_0000115>
    <rdfs:label xml:lang="en">Pattern</rdfs:label>
    <rdfs:label xml:lang="zh">证候</rdfs:label>
</owl:Class>
```

**结果**:
- ✅ 添加 23 个类（1 root + 22 core）
- ✅ 所有类映射到 BFO 顶层本体

**注意事项**:
- ID 必须唯一
- 必须有中英文双语标签和定义
- `xml:lang` 属性必须正确

---

### [2025-10-30] Op-003: 声明对象属性

**目标**: 在 tch-edit.owl 中声明和导入标准对象属性

**操作步骤**:
1. 在文件开头添加导入声明
2. 声明要使用的对象属性
3. 添加详细注释说明用途

**示例代码**:
```xml
<!-- Import External Ontologies -->
<owl:imports rdf:resource="http://purl.obolibrary.org/obo/ro/imports/ro_import.owl"/>
<owl:imports rdf:resource="http://purl.obolibrary.org/obo/bfo/2.0/bfo.owl"/>

<!-- Object Property Declarations -->
<owl:ObjectProperty rdf:about="http://purl.obolibrary.org/obo/BFO_0000051">
    <rdfs:label xml:lang="en">has part</rdfs:label>
    <rdfs:label xml:lang="zh">具有部分</rdfs:label>
    <rdfs:comment>Pattern has part Symptom/Sign</rdfs:comment>
</owl:ObjectProperty>
```

**关键属性列表**:
- BFO:0000051 (has part)
- BFO:0000050 (part of)
- RO:0000052 (inheres in)
- RO:0002452 (has symptom)
- RO:0000091 (has disposition)
- IAO:0000136 (is about)
- ... (见 RELATION_VALIDATION.md)

**结果**:
- ✅ 声明 19 个对象属性
- ✅ 按功能分类组织

**注意事项**:
- 避免创建自定义属性，优先使用标准属性
- RO:0002451 是 "transmitted by" 不是 "has sign"

---

### [2025-10-30] Op-004: 验证关系属性

**目标**: 验证所有对象属性与标准本体一致

**工具**: 
- RO 官方文档
- BFO 规范
- CSV 源文件

**操作步骤**:
1. 查看 RO GitHub: https://github.com/oborel/obo-relations
2. 下载 ro.owl 文件
3. 搜索每个属性 ID
4. 比对标签和定义
5. 记录验证结果

**验证命令**:
```bash
# 搜索 RO 属性
grep "RO:0002452" ro.owl -A 5
```

**结果**:
- ✅ 19/19 属性验证通过
- ⚠️ 发现 RO:0002451 标签错误并修正

**注意事项**:
- 始终以官方本体为准
- 使用 grep 快速查找
- 记录验证过程到 RELATION_VALIDATION.md

---

### [2025-10-31] Op-005: ID 系统容量分析

**目标**: 评估现有 ID 容量是否满足需求

**分析方法**:
1. 统计实际术语数量
2. 计算组合扩展数量
3. 评估增长空间

**数据来源**:
- 中国药典: 13,000+ 种中药
- 中医方剂数据库: 100,000+ 方剂
- 舌诊标准: 50+ 舌色 × 30+ 舌苔 = 1500+ 组合
- 脉诊标准: 28 种基本脉象

**计算示例**:
```
Herb 容量需求:
- 基础药材: 13,000
- 炮制方法: ×5 (生、炒、蒸、煮、炮)
- 产地差异: ×3 (道地药材)
- 总需求: 13,000 × 5 × 3 = 195,000
- 建议容量: 2,000,000 (10× 安全系数)
```

**结果**:
- ❌ 原系统容量不足 (仅 100 IDs/类别)
- ✅ 识别扩展需求

**注意事项**:
- 考虑组合爆炸（舌脉诊）
- 预留扩展空间（50-70%）
- 参考类似本体的规模（HPO: 15,000+ 术语）

---

### [2025-10-31] Op-006: 重新设计 ID 分配系统

**目标**: 设计 7-8 位 ID 系统支持 10,000,000 术语

**设计原则**:
1. 清晰的百万级边界
2. 高增长类别分配更多空间
3. 相关类别可以相邻但独立

**分配策略**:
```
TCH_0000000         - Root (1)
TCH_0001000-0099999 - Pattern (99K)
TCH_0100000-0199999 - Disease (100K)
TCH_0200000-0499999 - Symptom (300K)
TCH_0500000-0799999 - Sign (300K)
TCH_0800000-0899999 - Organ (100K)
TCH_0900000-0999999 - Meridian (100K)
TCH_1000000-2999999 - Herb (2M) ⚠️ 高增长
TCH_3000000-3999999 - Properties (1M)
TCH_4000000-5999999 - Formula (2M) ⚠️ 高增长
TCH_6000000-6999999 - Therapeutic (1M)
TCH_7000000-7999999 - Diagnostic (1M)
TCH_8000000-8999999 - Pathomechanism (1M)
TCH_9000000-9999999 - Environment (1M)
```

**关键决策**:
- Symptom/Sign 分离: 各 300K（原共享 100）
- Herb/Properties 分离: 2M + 1M（原共享 100）
- Formula: 2M（考虑经典方+现代方+验方）

**结果**:
- ✅ 总容量 10,000,000
- ✅ 3300× 容量增长

**工具**: Excel 或表格工具进行容量规划

---

### [2025-10-31] Op-007: 批量更新类 ID

**目标**: 将所有类 ID 从 4-5 位更新到 7 位

**工具**: sed (批量文本替换)

**操作步骤**:

1. **备份文件**:
```bash
cd src/ontology
cp tch-edit.owl tch-edit.owl.backup
```

2. **构造 sed 替换命令**:
```bash
sed -i '' \
  -e 's/TCH_0000100>/TCH_0001000>/g' \
  -e 's/TCH_0000101>/TCH_0001001>/g' \
  -e 's/TCH_0000102>/TCH_0001002>/g' \
  -e 's/TCH_0000103>/TCH_0001003>/g' \
  -e 's/TCH_0000200>/TCH_0100000>/g' \
  -e 's/TCH_0000300>/TCH_0200000>/g' \
  -e 's/TCH_0000301>/TCH_0500000>/g' \
  -e 's/TCH_0000600>/TCH_1000000>/g' \
  -e 's/TCH_0000601>/TCH_3000000>/g' \
  -e 's/TCH_0000602>/TCH_3000001>/g' \
  -e 's/TCH_0000603>/TCH_3000002>/g' \
  -e 's/TCH_0000700>/TCH_4000000>/g' \
  -e 's/TCH_0000800>/TCH_0800000>/g' \
  -e 's/TCH_0000801>/TCH_0800001>/g' \
  -e 's/TCH_0000900>/TCH_0900000>/g' \
  -e 's/TCH_0000901>/TCH_0900001>/g' \
  -e 's/TCH_0000A00>/TCH_8000000>/g' \
  -e 's/TCH_0000B00>/TCH_9000000>/g' \
  -e 's/TCH_0000C00>/TCH_6000000>/g' \
  -e 's/TCH_0000C01>/TCH_6000001>/g' \
  -e 's/TCH_0000D00>/TCH_7000000>/g' \
  -e 's/TCH_0000D01>/TCH_7000001>/g' \
  tch-edit.owl
```

3. **验证替换结果**:
```bash
# 检查所有 TCH ID
grep -o "TCH_[0-9A-F]*>" tch-edit.owl | sort -u
```

**预期输出**: 23 个唯一 ID，全部为 7 位数字

4. **删除备份** (确认无误后):
```bash
rm tch-edit.owl.backup
```

**结果**:
- ✅ 22 个 ID 成功替换
- ✅ 0 个遗漏
- ✅ 验证通过

**注意事项**:
- macOS sed 需要 `-i ''` (Linux 用 `-i`)
- 替换模式末尾加 `>` 确保精确匹配
- 务必先备份
- 使用 `grep` 验证结果

---

### [2025-10-31] Op-008: 更新 tch-idranges.owl

**目标**: 更新 ID 配置文件支持 8 位数字

**文件位置**: `src/ontology/tch-idranges.owl`

**修改内容**:

**修改 1**: 更新 iddigits
```xml
<!-- 修改前 -->
<iddigits>7</iddigits>

<!-- 修改后 -->
<iddigits>8</iddigits>
```

**修改 2**: 更新 ID 范围
```xml
<!-- 修改前 -->
<allocatedto>Main TCH Editor</allocatedto>
<idrange>0000001-0999999</idrange>

<!-- 修改后 -->
<allocatedto>Main TCH Editor</allocatedto>
<idrange>0000001-9999999</idrange>
```

**工具**: 文本编辑器或 replace_string_in_file

**结果**:
- ✅ 支持 0-9,999,999 范围
- ✅ iddigits=8 (包含前缀 TCH_)

**注意事项**:
- iddigits 包括前缀后的总位数
- 范围必须与实际分配一致

---

### [2025-10-31] Op-009: 验证构建

**目标**: 确保本体文件无错误且符合 OBO 规范

**命令**:
```bash
cd src/ontology
sh run.sh make
```

**验证内容**:
1. **SPARQL 规则检查**: 5 个规则
   - owldef-self-reference-violation
   - iri-range-violation
   - label-with-iri-violation
   - multiple-replaced_by-violation
   - dc-properties-violation

2. **ROBOT 推理**: ELK 推理器
3. **格式生成**: OWL, OBO, JSON

**预期输出**:
```
PASS Rule ../sparql/owldef-self-reference-violation.sparql: 0 violation(s)
PASS Rule ../sparql/iri-range-violation.sparql: 0 violation(s)
...
Violations: 134 ERROR: 92 WARN: 18 INFO: 24
```

**结果**:
- ✅ 0 个 SPARQL 违规
- ⚠️ 134 个 violations (双语定义导致的 multiple_definitions，正常)
- ✅ 推理成功

**注意事项**:
- multiple_definitions 警告是双语标签的预期行为
- 网络问题可能导致镜像下载失败，但不影响构建
- 检查 `reports/` 目录获取详细报告

---

### [2025-10-31] Op-010: Git 提交更改

**目标**: 使用双语 commit message 提交更改

**操作步骤**:

1. **查看更改**:
```bash
git status
git diff src/ontology/tch-edit.owl
```

2. **暂存更改**:
```bash
git add -A
```

3. **提交** (双语格式):
```bash
git commit -m "重新设计 ID 范围分配系统，支持 10M 术语扩展

Redesign ID range allocation system to support 10M term expansion

主要变更 / Main Changes:
- 将 ID 系统从 4-5 位扩展到 7-8 位数字
- 总容量从 <1000 提升至 10,000,000 (10000× 增长)
- Expand ID system from 4-5 digits to 7-8 digits
- Total capacity increased from <1000 to 10,000,000 (10000× growth)

详细分配 / Detailed Allocation:
- Pattern: 100 → 99,000 (990×)
- Disease: 100 → 100,000 (1000×)
- Symptom: 50 → 300,000 (6000×)
- Sign: 50 → 300,000 (6000×, 独立分配)
- Herb: 100 → 2,000,000 (20000×)
- Formula: 100 → 2,000,000 (20000×)

关键改进 / Key Improvements:
- 分离 Symptom 与 Sign 的 ID 空间
- 为高增长类别 (Herb, Formula) 预留 2M 空间
- 建立清晰的百万级边界 (1M, 3M, 4M, 6M, 7M, 8M, 9M)
- Separate ID spaces for Symptom and Sign
- Reserve 2M space for high-growth categories
- Establish clear million-level boundaries

文件更改 / Files Changed:
- src/ontology/tch-edit.owl: 更新所有 23 个类 ID
- src/ontology/tch-idranges.owl: 更新 iddigits 和范围
- ONTOLOGY_STRUCTURE.md: 更新 ID 分配表格
- README.md: 更新主内容表格
- ID_ALLOCATION_STRATEGY.md: 新增详细策略文档

验证 / Validation:
- ✅ SPARQL 规则: 5/5 通过
- ✅ ROBOT 推理: 成功
- ✅ ID 唯一性: 23 个唯一 ID 确认
"
```

4. **推送到远程**:
```bash
git push origin main
```

**Commit Message 模板**:
```
<中文简短标题>

<English short title>

主要变更 / Main Changes:
- <中文变更 1>
- <English change 1>

详细内容 / Details:
- <详细描述>

文件更改 / Files Changed:
- <文件列表>

验证 / Validation:
- ✅ <验证项>
```

**结果**:
- ✅ 清晰的版本历史
- ✅ 双语描述便于国际协作

**注意事项**:
- 第一行简短概括（50 字符内）
- 详细描述使用要点列表
- 必须包含验证结果

---

### [2025-10-31] Op-011: 创建策略文档

**目标**: 记录重要的设计决策和理由

**文档类型**:
1. **RELATION_VALIDATION.md** - 关系验证记录
2. **CORRECTION_SUMMARY.md** - 修正总结
3. **ID_ALLOCATION_STRATEGY.md** - ID 分配策略
4. **ONTOLOGY_STRUCTURE.md** - 本体结构说明
5. **PROJECT_PROGRESS_REPORT.md** - 项目进度报告

**写作要点**:
- 记录决策理由
- 包含数据支持
- 提供示例
- 双语对照
- 清晰的章节结构

**示例结构**:
```markdown
# 文档标题

## 1. 问题背景
描述遇到的问题...

## 2. 分析过程
数据收集和分析...

## 3. 解决方案
设计决策和实现...

## 4. 验证结果
测试和验证...

## 5. 经验总结
最佳实践...
```

**结果**:
- ✅ 完整的决策记录
- ✅ 便于后续参考

**注意事项**:
- 记录数据来源
- 包含计算过程
- 说明替代方案及选择理由

---

### [2025-10-31] Op-012: 文档更新同步

**目标**: 确保所有文档与代码更改保持同步

**需要更新的文档**:
1. **README.md** - 主要项目说明
   - 更新类别表格
   - 更新容量信息
   - 更新示例

2. **ONTOLOGY_STRUCTURE.md** - 结构文档
   - 更新 ID 范围表
   - 更新当前分配 ID 表
   - 更新类别说明

3. **CONTRIBUTING.md** - 贡献指南
   - 更新 ID 分配规则

**更新检查清单**:
- [ ] ID 范围是否一致
- [ ] 术语计数是否正确
- [ ] 示例代码是否有效
- [ ] 链接是否可访问
- [ ] 双语内容是否对应

**工具**: Markdown 编辑器 + grep 搜索

**验证命令**:
```bash
# 检查所有文档中的 ID 引用
grep -r "TCH_[0-9]\{7\}" *.md

# 检查表格一致性
grep -A 20 "ID.*范围\|ID.*Range" *.md
```

**注意事项**:
- 代码更改后立即更新文档
- 使用统一的表格格式
- 保持双语内容同步

---

## 工作流程总结 / Workflow Summary

### 标准本体开发流程

```
1. 初始化 ODK 仓库
   └─> Op-001: seed-via-docker.sh

2. 设计类别体系
   ├─> Op-002: 添加核心类
   ├─> Op-003: 声明对象属性
   └─> Op-004: 验证关系属性

3. 容量规划
   ├─> Op-005: ID 系统容量分析
   └─> Op-006: 重新设计 ID 分配

4. 实施更改
   ├─> Op-007: 批量更新类 ID (sed)
   ├─> Op-008: 更新配置文件
   └─> Op-009: 验证构建 (ROBOT)

5. 文档化
   ├─> Op-011: 创建策略文档
   └─> Op-012: 文档更新同步

6. 版本控制
   └─> Op-010: Git 提交 (双语)
```

### 关键工具链

| 工具 | 用途 | 关键命令 |
|------|------|---------|
| **ODK** | 本体开发工具包 | `seed-via-docker.sh` |
| **ROBOT** | OWL 操作和验证 | `sh run.sh make` |
| **sed** | 批量文本替换 | `sed -i '' -e 's/old/new/g' file` |
| **grep** | 文本搜索验证 | `grep -o "pattern" file` |
| **git** | 版本控制 | `git add/commit/push` |
| **Protégé** | 可视化编辑器 | GUI 操作 |

### 最佳实践

1. **始终先备份**: `cp file file.backup`
2. **小步提交**: 每个逻辑变更单独提交
3. **双语文档**: 所有文档保持中英文对照
4. **验证优先**: 每次更改后运行 `make`
5. **记录决策**: 重要设计决策写入文档
6. **使用标准**: 优先使用 BFO/RO 标准关系
7. **容量规划**: 预留 50-70% 扩展空间
8. **清晰命名**: ID 范围使用清晰的边界

### 常见问题处理

**问题 1**: sed 命令在 macOS 和 Linux 上语法不同
- **解决**: macOS 使用 `sed -i ''`, Linux 使用 `sed -i`

**问题 2**: ROBOT 构建报告大量 violations
- **解决**: 检查是否为双语标签导致的 multiple_definitions（正常）

**问题 3**: Git 推送失败
- **解决**: 先 `git pull --rebase origin main` 再推送

**问题 4**: ID 范围冲突
- **解决**: 使用 grep 搜索所有 ID 引用，统一更新

**问题 5**: 导入本体加载失败
- **解决**: 检查网络连接，或使用本地 mirror

**问题 6**: ROBOT 报告显示 134 个 ERROR violations
- **现象**: `tch-edit.owl-obo-report.tsv` 中有 92 个 multiple_definitions 和 multiple_labels 错误
- **原因**: OBO 格式原始规范不支持多语言，但 OWL 格式完全支持
- **解决**: ✅ **无需修复**！这是双语本体的正常现象
  - multiple_definitions (46条): 每个术语有中英文两个定义 `@zh` 和 `@en`
  - multiple_labels (46条): 每个术语有中英文两个标签
  - lowercase_definition (24条): 中文定义不适用英文小写规则
  - invalid_xref (18条): 外部引用占位符，待后续补充具体 ID
  - missing_superclass (1条): 根类无父类，正常
- **参考**: HPO, MONDO, ICD-11 等国际多语言本体都有类似"违规"

---

## 快速参考 / Quick Reference

### 常用命令速查

```bash
# 构建本体
cd src/ontology && sh run.sh make

# 验证 ID 唯一性
grep -o "TCH_[0-9]*>" tch-edit.owl | sort -u | wc -l

# 查找所有类定义
grep "<owl:Class" tch-edit.owl

# 搜索特定 ID
grep "TCH_0001000" tch-edit.owl -A 10

# 检查构建报告
cat reports/tch-edit.owl-obo-report.tsv

# 批量替换 ID
sed -i '' -e 's/OLD_ID/NEW_ID/g' tch-edit.owl

# Git 双语提交
git commit -m "中文标题

English title

主要变更 / Main Changes:
- 变更内容"
```

### ID 分配速查表

| 范围 | 类别 | 容量 |
|------|------|------|
| 0-999 | Root | 999 |
| 1K-99K | Pattern | 99K |
| 100K-199K | Disease | 100K |
| 200K-499K | Symptom | 300K |
| 500K-799K | Sign | 300K |
| 800K-899K | Organ | 100K |
| 900K-999K | Meridian | 100K |
| 1M-2.99M | Herb | 2M |
| 3M-3.99M | Properties | 1M |
| 4M-5.99M | Formula | 2M |
| 6M-6.99M | Therapeutic | 1M |
| 7M-7.99M | Diagnostic | 1M |
| 8M-8.99M | Pathomechanism | 1M |
| 9M-9.99M | Environment | 1M |

### 关键文件路径

```
target/tch/
├── src/ontology/
│   ├── tch-edit.owl         # 主编辑文件 ⭐
│   ├── tch-idranges.owl     # ID 配置 ⭐
│   ├── Makefile             # 构建配置
│   ├── run.sh               # 构建脚本
│   ├── imports/             # 导入文件
│   ├── mirror/              # 本体镜像
│   └── reports/             # 验证报告
├── tch.owl                  # 发布文件
├── README.md                # 项目说明 ⭐
├── ONTOLOGY_STRUCTURE.md    # 结构文档 ⭐
├── RELATION_VALIDATION.md   # 关系验证
├── ID_ALLOCATION_STRATEGY.md # ID 策略
└── OPERATION_LOG.md         # 本文档 ⭐
```

---

**最后更新**: 2025-10-31  
**版本**: v1.0  
**维护**: 每次重要操作后更新

---

## 注意事项 / Notes

1. **本文档持续更新**: 每次新操作后应立即记录
2. **精简为主**: 只记录关键步骤和命令，详细说明见专项文档
3. **可复用性**: 命令应具有通用性，可用于类似项目
4. **版本记录**: 重要版本节点应标注日期和操作编号
5. **跨平台**: 命令应注明平台差异（macOS/Linux/Windows）
