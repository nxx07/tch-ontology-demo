
![Build Status](https://github.com/nxx07/tch-ontology-demo/actions/workflows/qc.yml/badge.svg)
# Traditional Chinese Medicine Cold-Heat Pattern Ontology (TCH)

**寒热证本体**

## Description

An ontology for Traditional Chinese Medicine focusing on Cold-Heat patterns (寒热证), syndromes, symptoms, signs, and therapeutic principles. This ontology provides a formal representation of TCM concepts based on the Basic Formal Ontology (BFO) and other upper-level ontologies.

本本体用于表示传统中医寒热证候及相关概念，包括证候、症状、体征、治则治法等，基于 BFO 等上层本体构建的形式化知识表示系统。

### Key Features | 主要特点

- ✅ **Multi-language support** (Chinese/English) | 中英文双语支持
- ✅ **BFO-compliant** structure | 符合 BFO 标准结构
- ✅ **External ontology mappings** (MONDO, HPO, UBERON, etc.) | 外部本体映射
- ✅ **Rich semantic relations** | 丰富的语义关系
- ✅ **Coverage of TCM core concepts** | 涵盖中医核心概念

## Documentation | 文档

📖 **[Detailed Ontology Structure Guide](ONTOLOGY_STRUCTURE.md)** - Complete documentation of classes, properties, and relationships.

查看 **[详细本体结构文档](ONTOLOGY_STRUCTURE.md)** 了解完整的类、属性和关系说明。

## Main Content | 主要内容

The ontology includes the following major categories:

本体包含以下主要类别:

1. **Pattern/Syndrome** (证候) - Cold, Heat, and Complex patterns
2. **TCM Disease** (中医疾病) - Traditional disease concepts
3. **Symptom & Sign** (症状与征象) - Clinical manifestations
4. **Organ & Viscera** (器官与脏腑) - Anatomical structures
5. **Meridian & Acupoint** (经络与腧穴) - Channel systems
6. **Herb & Properties** (中草药及药性) - Medicinal materials
7. **Formula** (方剂) - Herbal prescriptions
8. **Therapeutic Principles & Methods** (治则与治法) - Treatment strategies
9. **Diagnostic & Pattern Differentiation** (诊断与辨证) - Diagnostic processes
10. **Pathomechanism** (病机) - Disease mechanisms
11. **Environment** (环境) - Environmental factors

More information can be found at http://obofoundry.org/ontology/tch

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