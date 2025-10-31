# TCH 本体文件组织分析报告
# TCH Ontology File Organization Analysis Report

**分析日期**: 2025-10-31  
**分析范围**: `/target/tch/` 完整目录结构  
**目标**: 识别重复、冗余、未完成的文件，并提出整理建议

---

## 一、文件重复问题 / Duplicate Files

### 1.1 根目录与 docs/ 目录的重复文件

发现 **5 个文件完全重复**（通过 `diff` 验证，内容 100% 相同）：

| 文件名 | 根目录 | docs/ 目录 | 状态 | 建议 |
|--------|--------|-----------|------|------|
| CONTRIBUTING.md | ✅ | ✅ | 完全重复 | ❌ 删除根目录版本 |
| ONTOLOGY_STRUCTURE.md | ✅ | ✅ | 完全重复 | ❌ 删除根目录版本 |
| RELATION_VALIDATION.md | ✅ | ✅ | 完全重复 | ❌ 删除根目录版本 |
| ID_ALLOCATION_STRATEGY.md | ✅ | ✅ | 完全重复 | ❌ 删除根目录版本 |
| CORRECTION_SUMMARY.md | ✅ | ✅ | 完全重复 | ❌ 删除根目录版本 |

**原因分析**:
- `docs/` 目录是 MkDocs 文档系统的源文件目录
- 根目录的版本可能是早期手动创建的副本
- GitHub 自动同步时创建了重复

**整理建议**:
1. **保留**: `docs/` 目录中的版本（MkDocs 文档源）
2. **删除**: 根目录中的 5 个重复文件
3. **原因**: MkDocs 会自动构建 `docs/` 下的文档，无需根目录副本

### 1.2 README.md vs docs/index.md

| 文件 | 行数 | 用途 | 状态 |
|------|------|------|------|
| README.md | 431 | GitHub 项目主页 | ✅ 保留 |
| docs/index.md | 431 | MkDocs 文档首页 | ✅ 保留 |

**内容**: 完全相同（通过 `diff` 验证）

**建议**: ✅ **两个都保留**
- `README.md` - GitHub 仓库首页，用户第一眼看到的内容
- `docs/index.md` - MkDocs 文档网站首页
- 虽然内容相同，但用途不同，应保持同步

**维护策略**: 修改时同步更新两个文件

---

## 二、未完成的模板文件 / Incomplete Template Files

### 2.1 src/metadata/tch.md - 元数据模板 ⚠️

**问题**:
```yaml
contact:
  email:           # ❌ 空白
  label:           # ❌ 空白
  github:          # ❌ 空白
description: tch-ontology-demo is an ontology...  # ❌ 占位符
domain: stuff      # ❌ 通用占位符，应为 "Traditional Chinese Medicine"
license:
  url: http://creativecommons.org/licenses/by/3.0/  # ⚠️ 需确认
  label: CC-BY
```

**用途**: 
- 提交到 OBO Foundry 时使用
- OLS (Ontology Lookup Service) 展示
- AberOWL 索引

**待完善**:
1. **联系人信息** (`contact`):
   - `email`: 项目维护者邮箱
   - `label`: 联系人姓名
   - `github`: GitHub 用户名

2. **描述** (`description`):
   - 当前: "tch-ontology-demo is an ontology..."（占位符）
   - 应改为: 完整的项目描述（可参考 README.md 的概述部分）

3. **领域** (`domain`):
   - 当前: "stuff"（通用占位符）
   - 应改为: "Traditional Chinese Medicine" 或 "health"

4. **许可证** (`license`):
   - 当前: CC-BY 3.0
   - 需确认: 是否符合项目需求

### 2.2 issue_template.md - Issue 模板 ⚠️

**问题**: 当前是 **通用 OBO 术语请求模板**，不适合 TCM 领域

**现有字段**:
```markdown
## Preferred term label
## Synonyms
## Textual definition
## Suggested parent term
## Attribution
```

**建议增加 TCM 特定字段**:
```markdown
## 中文术语名 / Chinese Term Name

## 英文术语名 / English Term Name

## BFO 范畴 / BFO Category
(Disposition, Quality, Process, Material Entity, etc.)

## 定义 / Definition
### 中文定义
### English Definition

## 同义词 / Synonyms
### 中文同义词
### English Synonyms

## 父类 / Parent Class
请在本体层次结构中查找: [OLS](http://www.ebi.ac.uk/ols/ontologies/tch)

## 关系属性 / Object Properties
与其他类的关系 (如: has part, inheres in, etc.)

## 外部映射 / External Mappings
- ICD-11 TM: 
- SNOMED CT:
- HPO:
- 其他:

## 参考文献 / References
请提供 PubMed ID 或其他学术引用

## ORCID (可选)
```

---

## 三、文件结构整理建议 / File Organization Recommendations

### 3.1 当前目录结构

```
target/tch/
├── .git/                          # Git 仓库
├── .github/                       # GitHub Actions 配置
├── .gitignore                     # Git 忽略规则
├── README.md                      # ✅ GitHub 项目主页
├── CONTRIBUTING.md                # ❌ 重复，应删除
├── ONTOLOGY_STRUCTURE.md          # ❌ 重复，应删除
├── RELATION_VALIDATION.md         # ❌ 重复，应删除
├── ID_ALLOCATION_STRATEGY.md      # ❌ 重复，应删除
├── CORRECTION_SUMMARY.md          # ❌ 重复，应删除
├── OPERATION_LOG.md               # ⚠️ 未提交到 git
├── PROJECT_PROGRESS_REPORT.md     # ⚠️ 可能未提交
├── issue_template.md              # ⚠️ 需完善为 TCM 模板
├── mkdocs.yaml                    # ✅ MkDocs 配置
├── docs/                          # ✅ MkDocs 文档源目录
│   ├── index.md                   # ✅ 文档首页
│   ├── CONTRIBUTING.md            # ✅ 保留
│   ├── ONTOLOGY_STRUCTURE.md      # ✅ 保留
│   ├── RELATION_VALIDATION.md     # ✅ 保留
│   ├── ID_ALLOCATION_STRATEGY.md  # ✅ 保留
│   └── CORRECTION_SUMMARY.md      # ✅ 保留
├── src/                           # ✅ 源代码目录
│   ├── metadata/                  # 元数据
│   │   ├── README.md              # ✅ 元数据说明
│   │   ├── tch.md                 # ⚠️ 需完善
│   │   └── tch.yml                # ✅ PURL 配置
│   ├── ontology/                  # 本体文件
│   │   ├── README-editors.md      # ✅ 编辑者指南
│   │   ├── tch-edit.owl           # ✅ 主编辑文件
│   │   ├── tch-idranges.owl       # ✅ ID 配置
│   │   ├── Makefile               # ✅ 构建配置
│   │   ├── imports/               # ✅ 导入的外部本体
│   │   ├── mirror/                # ✅ 本体镜像（自动生成）
│   │   ├── reports/               # ✅ 验证报告（自动生成）
│   │   └── tmp/                   # ✅ 临时文件
│   ├── scripts/                   # ✅ 脚本文件
│   └── sparql/                    # ✅ SPARQL 查询
└── [发布文件]                      # ✅ 自动生成
    ├── tch.owl
    ├── tch.obo
    ├── tch-base.owl
    └── tch-full.owl
```

### 3.2 建议的清理后结构

```
target/tch/
├── .git/
├── .github/
├── .gitignore
├── README.md                      # ✅ 项目主页
├── OPERATION_LOG.md               # 🆕 添加或忽略
├── PROJECT_PROGRESS_REPORT.md     # 🆕 添加或删除
├── issue_template.md              # 🔄 完善模板
├── mkdocs.yaml
├── docs/                          # 所有文档在这里
│   ├── index.md
│   ├── CONTRIBUTING.md
│   ├── ONTOLOGY_STRUCTURE.md
│   ├── RELATION_VALIDATION.md
│   ├── ID_ALLOCATION_STRATEGY.md
│   ├── CORRECTION_SUMMARY.md
│   └── FILE_ORGANIZATION.md       # 🆕 本文档
├── src/
│   ├── metadata/
│   │   ├── tch.md                 # 🔄 需完善
│   │   └── tch.yml
│   ├── ontology/
│   └── ...
└── [发布文件]
```

---

## 四、具体整理操作清单 / Action Items

### 步骤 1: 删除重复文件 ❌

```bash
cd /Users/cailingxi/课题组工作/tch-ontology-demo/target/tch

# 删除根目录的重复文件（保留 docs/ 版本）
rm CONTRIBUTING.md
rm ONTOLOGY_STRUCTURE.md
rm RELATION_VALIDATION.md
rm ID_ALLOCATION_STRATEGY.md
rm CORRECTION_SUMMARY.md

# 验证删除
git status
```

**影响**: 无负面影响，docs/ 中的版本会被 MkDocs 使用

### 步骤 2: 处理 OPERATION_LOG.md 和 PROJECT_PROGRESS_REPORT.md

**选项 A**: 添加到 git 并移动到 docs/
```bash
git add OPERATION_LOG.md PROJECT_PROGRESS_REPORT.md
git mv OPERATION_LOG.md docs/
git mv PROJECT_PROGRESS_REPORT.md docs/
```

**选项 B**: 添加到 .gitignore（如果是个人笔记）
```bash
echo "OPERATION_LOG.md" >> .gitignore
echo "PROJECT_PROGRESS_REPORT.md" >> .gitignore
```

**建议**: 选项 A - 这些文档对项目有价值

### 步骤 3: 完善 src/metadata/tch.md

需要填写的字段：
1. `contact.email` - 维护者邮箱
2. `contact.label` - 维护者姓名
3. `contact.github` - GitHub 用户名
4. `description` - 完整项目描述
5. `domain` - "Traditional Chinese Medicine"

### 步骤 4: 完善 issue_template.md

创建 TCM 特定的术语请求模板（见上文 2.2 节）

### 步骤 5: 创建 FILE_ORGANIZATION.md

将本分析报告的主要内容整理为永久文档

### 步骤 6: 提交更改

```bash
git add -A
git commit -m "文件结构整理：删除重复文件，完善模板

File structure cleanup: remove duplicates, improve templates

主要变更 / Main Changes:
- 删除根目录的 5 个重复文档（保留 docs/ 版本）
- 移动 OPERATION_LOG.md 和 PROJECT_PROGRESS_REPORT.md 到 docs/
- 完善 src/metadata/tch.md 元数据
- 更新 issue_template.md 为 TCM 特定模板
- 添加 FILE_ORGANIZATION.md 文档结构说明

删除文件 / Removed Files (duplicates):
- CONTRIBUTING.md
- ONTOLOGY_STRUCTURE.md
- RELATION_VALIDATION.md
- ID_ALLOCATION_STRATEGY.md
- CORRECTION_SUMMARY.md

移动文件 / Moved Files:
- OPERATION_LOG.md → docs/
- PROJECT_PROGRESS_REPORT.md → docs/

完善文件 / Enhanced Files:
- src/metadata/tch.md
- issue_template.md

新增文件 / New Files:
- docs/FILE_ORGANIZATION.md
"
```

---

## 五、文件分类说明 / File Classification

### 5.1 手动维护的文件 ✍️

需要人工编辑和维护：

**文档类**:
- `README.md` / `docs/index.md`
- `docs/CONTRIBUTING.md`
- `docs/ONTOLOGY_STRUCTURE.md`
- `docs/RELATION_VALIDATION.md`
- `docs/ID_ALLOCATION_STRATEGY.md`
- `docs/CORRECTION_SUMMARY.md`
- `docs/OPERATION_LOG.md`
- `issue_template.md`

**配置类**:
- `src/metadata/tch.md`
- `src/metadata/tch.yml`
- `src/ontology/tch-idranges.owl`
- `mkdocs.yaml`

**本体编辑文件**:
- `src/ontology/tch-edit.owl` ⭐ 核心文件

**导入配置**:
- `src/ontology/imports/*_terms.txt`

### 5.2 自动生成的文件 🤖

通过 `sh run.sh make` 自动生成，**不应手动编辑**：

**发布文件**:
- `tch.owl`
- `tch.obo`
- `tch-base.owl`
- `tch-base.obo`
- `tch-full.owl`
- `tch-full.obo`

**报告文件**:
- `src/ontology/reports/*.tsv`

**镜像文件**:
- `src/ontology/mirror/*.owl`

**临时文件**:
- `src/ontology/tmp/*`

### 5.3 系统文件 ⚙️

由工具自动管理：

- `.git/` - Git 版本控制
- `.github/` - GitHub Actions
- `.gitignore` - Git 忽略规则
- `.DS_Store` - macOS 系统文件（应忽略）

---

## 六、维护最佳实践 / Maintenance Best Practices

### 6.1 文档同步策略

**README.md 与 docs/index.md 同步**:
```bash
# 每次修改 README.md 后
cp README.md docs/index.md
```

**或使用符号链接** (推荐):
```bash
cd docs
rm index.md
ln -s ../README.md index.md
```

### 6.2 文件命名规范

- **文档**: 大写字母开头，下划线分隔 (`OPERATION_LOG.md`)
- **配置**: 小写字母，连字符分隔 (`tch-edit.owl`)
- **临时**: `.tmp` 后缀 (`temp.tmp.owl`)

### 6.3 目录职责

| 目录 | 职责 | 可编辑 |
|------|------|--------|
| `/` | 项目根目录，存放关键文档 | ✅ |
| `/docs/` | MkDocs 文档源 | ✅ |
| `/src/ontology/` | 本体源文件 | ✅ |
| `/src/metadata/` | OBO 元数据 | ✅ |
| `/src/scripts/` | 辅助脚本 | ✅ |
| `/src/sparql/` | SPARQL 查询 | ✅ |
| `/src/ontology/imports/` | 导入配置 | ✅ |
| `/src/ontology/mirror/` | 自动生成 | ❌ |
| `/src/ontology/reports/` | 自动生成 | ❌ |
| `/src/ontology/tmp/` | 临时文件 | ❌ |

---

## 七、.gitignore 优化建议

当前 `.gitignore` 已经很完善，建议增加：

```bash
# 个人笔记（如果不想提交）
OPERATION_LOG.md
PROJECT_PROGRESS_REPORT.md

# macOS
.DS_Store
.AppleDouble
.LSOverride

# MkDocs
site/

# 编辑器
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.py[cod]
```

---

## 八、总结 / Summary

### 问题统计

| 问题类型 | 数量 | 严重程度 |
|---------|------|---------|
| 重复文件 | 5 | 🟡 中 |
| 未完成模板 | 2 | 🟡 中 |
| 未跟踪文件 | 2 | 🟢 低 |
| 文档不同步风险 | 1 | 🟡 中 |

### 优先级操作

**高优先级** 🔴:
1. 删除 5 个重复文件（CONTRIBUTING.md 等）
2. 完善 `src/metadata/tch.md` 元数据

**中优先级** 🟡:
3. 完善 `issue_template.md` 为 TCM 模板
4. 决定 OPERATION_LOG.md 和 PROJECT_PROGRESS_REPORT.md 去向
5. 创建 FILE_ORGANIZATION.md 文档

**低优先级** 🟢:
6. 优化 .gitignore
7. 建立 README.md 和 docs/index.md 同步机制

---

**创建时间**: 2025-10-31  
**版本**: v1.0  
**维护**: 定期检查文件组织状况
