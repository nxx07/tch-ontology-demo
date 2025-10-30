
![Build Status](https://github.com/nxx07/tch-ontology-demo/actions/workflows/qc.yml/badge.svg)
# Traditional Chinese Medicine Cold-Heat Pattern Ontology (TCH)

**寒热证本体 (中医寒热证候形式化知识表示系统)**

---

## 📋 Table of Contents | 目录

- [Description | 项目描述](#description--项目描述)
- [Key Features | 主要特点](#key-features--主要特点)
- [Documentation | 文档](#documentation--文档)
- [Main Content | 主要内容](#main-content--主要内容)
- [Repository Structure | 仓库结构](#repository-structure--仓库结构)
- [Ontology Files | 本体文件](#ontology-files--本体文件)
- [Imported Ontologies | 导入的本体](#imported-ontologies--导入的本体)
- [Usage | 使用方法](#usage--使用方法)
- [Development | 开发指南](#development--开发指南)
- [Contact | 联系方式](#contact--联系方式)

---

## Description | 项目描述

An ontology for Traditional Chinese Medicine focusing on Cold-Heat patterns (寒热证), syndromes, symptoms, signs, and therapeutic principles. This ontology provides a formal representation of TCM concepts based on the Basic Formal Ontology (BFO) and other upper-level ontologies.

本本体用于表示传统中医寒热证候及相关概念，包括证候、症状、体征、治则治法等，是基于 BFO（基础形式本体）等上层本体构建的形式化知识表示系统。

---

## Key Features | 主要特点

- ✅ **Multi-language support** (Chinese/English) | 中英文双语支持
- ✅ **BFO-compliant** structure | 符合 BFO 标准结构
- ✅ **External ontology mappings** (MONDO, HPO, UBERON, TCDO, etc.) | 外部本体映射
- ✅ **Rich semantic relations** (compositional, causal, functional) | 丰富的语义关系
- ✅ **Coverage of TCM core concepts** | 涵盖中医核心概念
- ✅ **ODK-based development workflow** | 基于 ODK 的开发流程
- ✅ **Continuous Integration with GitHub Actions** | GitHub Actions 持续集成

---

## Documentation | 文档

### Core Documentation | 核心文档

- 📖 **[Detailed Ontology Structure Guide](ONTOLOGY_STRUCTURE.md)** | **[详细本体结构指南](ONTOLOGY_STRUCTURE.md)**
  - Complete class hierarchy | 完整类层级结构
  - Object properties and relations | 对象属性和关系
  - BFO category mappings | BFO 范畴映射
  - External ontology cross-references | 外部本体交叉引用
  - Usage examples | 使用示例

- 📝 **[Editor's Guide](src/ontology/README-editors.md)** | **[编辑者指南](src/ontology/README-editors.md)**
  - How to edit the ontology | 如何编辑本体
  - Build and release workflows | 构建和发布流程
  - Best practices | 最佳实践

- 🤝 **[Contributing Guidelines](CONTRIBUTING.md)** | **[贡献指南](CONTRIBUTING.md)**
  - How to contribute | 如何贡献
  - Issue reporting | 问题报告
  - Pull request process | 拉取请求流程

---

## Main Content | 主要内容

The ontology includes **11 major categories** organized hierarchically with a **7-digit ID system** providing capacity for **10 million terms**:

本体包含 **11 个主要类别**，采用 **7 位数字 ID 系统**，可容纳 **1000 万条术语**，按层级组织：

| ID Range | Category (EN) | 类别 (ZH) | Capacity | BFO Category | Current Count |
|----------|---------------|-----------|----------|--------------|---------------|
| TCH_0001000-0099999 | Pattern/Syndrome | 证候/证 | 99,000 | Disposition | 4 |
| TCH_0100000-0199999 | TCM Disease | 中医疾病 | 100,000 | Disposition | 1 |
| TCH_0200000-0499999 | Symptom | 症状 | 300,000 | Quality | 1 |
| TCH_0500000-0799999 | Sign | 征象 | 300,000 | Quality | 1 |
| TCH_0800000-0899999 | Organ & Viscera | 器官与脏腑系统 | 100,000 | Material Entity | 2 |
| TCH_0900000-0999999 | Meridian & Acupoint | 经络与腧穴 | 100,000 | Immaterial Entity | 2 |
| TCH_1000000-2999999 | Herb | 中草药 | 2,000,000 | Material Entity | 1 |
| TCH_3000000-3999999 | Herb Properties | 药性属性 | 1,000,000 | Disposition / Quality | 3 |
| TCH_4000000-5999999 | Formula | 方剂 | 2,000,000 | ICE | 1 |
| TCH_6000000-6999999 | Therapeutic | 治则与治法 | 1,000,000 | Plan Specification | 2 |
| TCH_7000000-7999999 | Diagnostic | 诊断与辨证 | 1,000,000 | Process / ICE | 2 |
| TCH_8000000-8999999 | Pathomechanism | 病机 | 1,000,000 | Process | 1 |
| TCH_9000000-9999999 | Environment | 环境 | 1,000,000 | Material Entity | 1 |

**Total Capacity | 总容量**: 10,000,000 IDs  
**Total Classes | 类总数**: 22 core classes + 1 root class

---

## Repository Structure | 仓库结构

```
tch-ontology-demo/
├── README.md                          # This file | 本文件
├── ONTOLOGY_STRUCTURE.md              # Detailed structure documentation | 详细结构文档
├── CONTRIBUTING.md                    # Contribution guidelines | 贡献指南
├── issue_template.md                  # Issue template | 问题模板
│
├── tch.owl                            # Main release (OWL) | 主要发布版本（OWL格式）
├── tch.obo                            # Main release (OBO) | 主要发布版本（OBO格式）
├── tch-base.owl                       # Base version (OWL) | 基础版本（OWL格式）
├── tch-base.obo                       # Base version (OBO) | 基础版本（OBO格式）
├── tch-full.owl                       # Full version with reasoning (OWL) | 完整版本含推理（OWL格式）
├── tch-full.obo                       # Full version (OBO) | 完整版本（OBO格式）
│
├── src/
│   ├── ontology/                      # Ontology source files | 本体源文件
│   │   ├── tch-edit.owl              # ⭐ MAIN EDIT FILE | 主编辑文件
│   │   ├── tch-odk.yaml              # ODK configuration | ODK配置
│   │   ├── tch-idranges.owl          # ID ranges | ID范围定义
│   │   ├── Makefile                   # Build automation | 构建自动化
│   │   ├── README-editors.md          # Editor's guide | 编辑者指南
│   │   │
│   │   ├── imports/                   # Imported ontology modules | 导入的本体模块
│   │   │   ├── bfo_import.owl        # BFO import module | BFO导入模块
│   │   │   ├── ro_import.owl         # RO import module | RO导入模块
│   │   │   ├── iao_import.owl        # IAO import module | IAO导入模块
│   │   │   ├── pato_import.owl       # PATO import module | PATO导入模块
│   │   │   └── *_terms.txt           # Term lists for imports | 导入术语列表
│   │   │
│   │   ├── mirror/                    # Mirrored source ontologies | 镜像源本体
│   │   │   ├── bfo.owl               # BFO mirror | BFO镜像
│   │   │   ├── ro.owl                # RO mirror | RO镜像
│   │   │   ├── iao.owl               # IAO mirror | IAO镜像
│   │   │   └── pato.owl              # PATO mirror | PATO镜像
│   │   │
│   │   ├── reports/                   # Quality control reports | 质量控制报告
│   │   │   └── *.tsv, *.txt          # Various QC reports | 各类QC报告
│   │   │
│   │   └── tmp/                       # Temporary build files | 临时构建文件
│   │
│   ├── metadata/                      # Project metadata | 项目元数据
│   │   ├── tch.yml                   # PURL configuration | PURL配置
│   │   └── tch.md                    # Ontology metadata | 本体元数据
│   │
│   ├── sparql/                        # SPARQL queries | SPARQL查询
│   │   ├── README.md                 # SPARQL documentation | SPARQL文档
│   │   └── *.sparql                  # Query files | 查询文件
│   │
│   └── scripts/                       # Utility scripts | 实用脚本
│
└── .github/
    └── workflows/                     # CI/CD workflows | CI/CD工作流
        ├── qc.yml                    # Quality control | 质量控制
        └── docs.yml                  # Documentation | 文档生成
```

---

## Ontology Files | 本体文件

### Release Files | 发布文件

These are the main files for users to download and use:

这些是用户下载和使用的主要文件：

| File | Format | Description (EN) | 描述 (ZH) |
|------|--------|------------------|-----------|
| **[tch.owl](tch.owl)** | OWL (RDF/XML) | Main release version | 主要发布版本 |
| **[tch.obo](tch.obo)** | OBO | Main release in OBO format | OBO格式主要版本 |
| **[tch-base.owl](tch-base.owl)** | OWL | Base version (TCH terms only) | 基础版本（仅TCH术语） |
| **[tch-base.obo](tch-base.obo)** | OBO | Base version in OBO format | OBO格式基础版本 |
| **[tch-full.owl](tch-full.owl)** | OWL | Full version with inferred axioms | 包含推理公理的完整版本 |
| **[tch-full.obo](tch-full.obo)** | OBO | Full version in OBO format | OBO格式完整版本 |

### Source Files | 源文件

For ontology developers and editors:

供本体开发者和编辑者使用：

| File | Description (EN) | 描述 (ZH) |
|------|------------------|-----------|
| **[src/ontology/tch-edit.owl](src/ontology/tch-edit.owl)** | ⭐ Main edit file - edit this! | ⭐ 主编辑文件 - 在此编辑！ |
| **[src/ontology/tch-odk.yaml](src/ontology/tch-odk.yaml)** | ODK configuration | ODK配置文件 |
| **[src/ontology/tch-idranges.owl](src/ontology/tch-idranges.owl)** | ID range definitions | ID范围定义 |
| **[src/ontology/Makefile](src/ontology/Makefile)** | Build automation script | 构建自动化脚本 |

---

## Imported Ontologies | 导入的本体

TCH ontology is built on top of several well-established upper-level and domain ontologies:

TCH 本体建立在几个完善的上层和领域本体之上：

### Upper-Level Ontologies | 上层本体

| Ontology | Full Name | Version | Purpose | 用途 |
|----------|-----------|---------|---------|------|
| **[BFO](http://purl.obolibrary.org/obo/bfo.owl)** | Basic Formal Ontology | 2.0 | Top-level categories (entity, continuant, occurrent) | 顶层范畴（实体、延续体、发生体） |
| **[RO](http://purl.obolibrary.org/obo/ro.owl)** | Relation Ontology | Latest | Relations (part of, has part, inheres in, etc.) | 关系（部分、具有部分、依存于等） |
| **[IAO](http://purl.obolibrary.org/obo/iao.owl)** | Information Artifact Ontology | Latest | Information entities (documents, datasets) | 信息实体（文档、数据集） |
| **[PATO](http://purl.obolibrary.org/obo/pato.owl)** | Phenotypic Quality Ontology | Latest | Quality attributes | 性质属性 |

### Import Modules | 导入模块

Located in `src/ontology/imports/`:

位于 `src/ontology/imports/` 目录：

- **[bfo_import.owl](src/ontology/imports/bfo_import.owl)** - BFO terms used in TCH | TCH使用的BFO术语
- **[ro_import.owl](src/ontology/imports/ro_import.owl)** - RO relations used in TCH | TCH使用的RO关系
- **[iao_import.owl](src/ontology/imports/iao_import.owl)** - IAO terms used in TCH | TCH使用的IAO术语
- **[pato_import.owl](src/ontology/imports/pato_import.owl)** - PATO terms used in TCH | TCH使用的PATO术语

### External Mappings | 外部映射

TCH includes cross-references to:

TCH 包含对以下本体的交叉引用：

- **MONDO** / **DOID** - Disease ontologies | 疾病本体
- **HPO** - Human Phenotype Ontology | 人类表型本体
- **UBERON** - Anatomy ontology | 解剖学本体
- **TCDO** - Traditional Chinese Drug Ontology | 中药本体
- **ADO** - Acupuncture & Moxibustion Ontology | 针灸本体
- **CHEBI** - Chemical Entities of Biological Interest | 生物学化学实体
- **ENVO** - Environment Ontology | 环境本体
- **ICD-11** - International Classification of Diseases | 国际疾病分类
- **ISO 23961** - Traditional Chinese Medicine terminology | 中医术语标准
- **WHO** - World Health Organization standards | 世界卫生组织标准

---

## Versions | 版本信息

### Stable Release Versions | 稳定发布版本

The latest version of the ontology can always be found at:

最新版本的本体可以在以下位置找到：

- **OWL format**: http://purl.obolibrary.org/obo/tch.owl
- **OBO format**: http://purl.obolibrary.org/obo/tch.obo

### Editors' Version | 编辑者版本

Editors of this ontology should use the edit version:

本体编辑者应使用编辑版本：

- **[src/ontology/tch-edit.owl](src/ontology/tch-edit.owl)**

### Browse Online | 在线浏览

- **OntoBee**: http://www.ontobee.org/ontology/TCH
- **BioPortal**: (Coming soon | 即将推出)

---

## Usage | 使用方法

### For Users | 用户使用

1. **Download the ontology** | 下载本体
   ```bash
   # OWL format
   wget http://purl.obolibrary.org/obo/tch.owl
   
   # OBO format
   wget http://purl.obolibrary.org/obo/tch.obo
   ```

2. **Open in Protégé** | 在 Protégé 中打开
   - Download Protégé: https://protege.stanford.edu/
   - Open `tch.owl` file
   - Browse classes, properties, and axioms

3. **Query with SPARQL** | 使用 SPARQL 查询
   - Example queries in `src/sparql/` directory
   - Use tools like Apache Jena or RDFLib

### For Developers | 开发者使用

See **[Development](#development--开发指南)** section below.

---

## Development | 开发指南

### Prerequisites | 前置要求

1. **Docker** - For running ODK (Ontology Development Kit)
   ```bash
   docker pull obolibrary/odkfull
   ```

2. **Git** - Version control
   ```bash
   git clone https://github.com/nxx07/tch-ontology-demo.git
   cd tch-ontology-demo/target/tch
   ```

3. **(Optional) Protégé** - For visual editing
   - Download: https://protege.stanford.edu/

### Editing Workflow | 编辑工作流

1. **Edit the source file** | 编辑源文件
   ```bash
   # Open in your preferred editor
   protege src/ontology/tch-edit.owl
   # Or use any text editor for Manchester syntax
   ```

2. **Build the ontology** | 构建本体
   ```bash
   cd src/ontology
   sh run.sh make
   ```

3. **Check quality reports** | 检查质量报告
   ```bash
   cat reports/tch-edit.owl-obo-report.tsv
   ```

4. **Commit and push** | 提交并推送
   ```bash
   git add -A
   git commit -m "Description of changes"
   git push origin main
   ```

### Build Commands | 构建命令

```bash
cd src/ontology

# Full build (recommended)
sh run.sh make

# Build specific targets
sh run.sh make tch.owl          # Main release
sh run.sh make tch-base.owl     # Base version
sh run.sh make imports          # Update imports
sh run.sh make reports          # Generate QC reports

# Clean build artifacts
sh run.sh make clean
```

### Testing | 测试

The ontology is automatically tested on every commit via GitHub Actions:

每次提交时通过 GitHub Actions 自动测试本体：

- ✅ OWL 2 DL profile validation | OWL 2 DL 配置验证
- ✅ SPARQL query tests | SPARQL 查询测试
- ✅ Custom validation rules | 自定义验证规则
- ✅ Reasoning consistency check | 推理一致性检查

---

## Contact | 联系方式

### Report Issues | 报告问题

Please use this GitHub repository's **[Issue tracker](https://github.com/nxx07/tch-ontology-demo/issues)** to:

请使用本 GitHub 仓库的 **[问题跟踪器](https://github.com/nxx07/tch-ontology-demo/issues)** 来：

- Request new terms/classes | 请求新术语/类
- Report errors or inconsistencies | 报告错误或不一致
- Suggest improvements | 建议改进
- Ask questions | 提问

### Repository | 仓库

- **GitHub**: https://github.com/nxx07/tch-ontology-demo
- **Organization**: nxx07

---

## Acknowledgements | 致谢

This ontology repository was created using the **[Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit)**.

本本体仓库使用 **[本体开发工具包 (ODK)](https://github.com/INCATools/ontology-development-kit)** 创建。

We acknowledge the following ontology projects that TCH builds upon:

我们感谢以下本体项目，TCH 建立在它们之上：

- **BFO** (Basic Formal Ontology) - https://basic-formal-ontology.org/
- **RO** (Relation Ontology) - http://obofoundry.org/ontology/ro.html
- **IAO** (Information Artifact Ontology) - http://obofoundry.org/ontology/iao.html
- **PATO** (Phenotypic Quality Ontology) - http://obofoundry.org/ontology/pato.html

---

## License | 许可证

[![License](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

This ontology is released under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**.

本本体在 **CC0 1.0 通用 (CC0 1.0) 公共领域贡献** 许可证下发布。

---

*Last updated: 2025-10-30 | 最后更新: 2025-10-30*

*Version: 1.0.0 | 版本: 1.0.0*

## Versions

### Stable release versions

The latest version of the ontology can always be found at:

http://purl.obolibrary.org/obo/tch.owl

(note this will not show up until the request has been approved by obofoundry.org)

### Editors' version

Editors of this ontology should use the edit version, [src/ontology/tch-edit.owl](src/ontology/tch-edit.owl)

## Contact

Please use this GitHub repository's [Issue tracker](https://github.com/nxx07/tch/issues) to request new terms/classes or report errors or specific concerns related to the ontology.

## Acknowledgements

This ontology repository was created using the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit).