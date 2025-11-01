# tch-edit.owl 文件被清空问题 - 诊断报告
# tch-edit.owl File Cleared Issue - Diagnostic Report

**问题发现时间**: 2025-11-01 19:59  
**问题状态**: ✅ 已解决  
**数据损失**: ❌ 无（已从备份恢复）

---

## 🔍 问题描述

`tch-edit.owl` 文件在术语导入测试后被清空，仅保留 XML 头部和空的本体声明（620字节），丢失了所有23个类的定义和内容。

---

## 🐛 根本原因分析

### 问题根源：owlready2 保存机制

在 `import_terms.py` 的 `import_terms()` 方法中，使用了以下代码：

```python
# 保存本体
if not validate_only:
    try:
        self.ontology.save(file=str(self.ontology_path))
        logger.info(f"本体文件保存成功: {self.ontology_path}")
    except Exception as e:
        logger.error(f"本体文件保存失败: {e}")
```

**问题**：
1. 在测试导入时，本体文件以 OFN 格式加载：`load(format="ofn")`
2. 由于测试时基类不存在（TCH:0001000等），创建术语失败
3. owlready2 的 `save()` 方法保存了一个空的本体对象到 RDF/XML 格式
4. 原有的 OFN 格式内容被覆盖为空的 RDF/XML

### 时间线

| 时间 | 事件 |
|------|------|
| 19:34:39 | 导入测试开始，创建备份 `tch-edit.owl.backup.20251101_193439` |
| 19:34:39 | 本体加载成功 (OFN 格式，26KB，363行) |
| 19:34:39 | 尝试创建术语，因基类不存在而失败 |
| 19:34:39 | `ontology.save()` 执行，将空本体保存为 RDF/XML 格式 |
| 19:34:39 | `tch-edit.owl` 被覆盖为 620字节的空文件 |
| 19:59:00 | 问题被发现 |
| 19:59:30 | 从备份恢复文件 |

---

## ✅ 解决方案

### 立即恢复

```bash
cd src/ontology
cp tch-edit.owl.backup.20251101_193439 tch-edit.owl
```

**恢复结果**:
- ✅ 文件大小：620B → 26KB
- ✅ 行数：13行 → 363行
- ✅ 类数量：0个 → 23个
- ✅ 格式：RDF/XML → OWL Functional Syntax

### 验证恢复

```bash
# 统计类数量
grep -c "^Declaration(Class" tch-edit.owl
# 输出: 23 ✅

# 查看文件大小
ls -lh tch-edit.owl
# 输出: 26K ✅
```

---

## 🛡️ 预防措施

### 1. 修复导入脚本

需要修改 `import_terms.py`，在保存前检查是否有实际内容：

```python
# 保存本体（仅在成功创建术语时保存）
if not validate_only and self.stats['success'] > 0:
    try:
        self.ontology.save(file=str(self.ontology_path), format="ofn")
        logger.info(f"本体文件保存成功: {self.ontology_path}")
    except Exception as e:
        logger.error(f"本体文件保存失败: {e}")
        logger.warning(f"可以从备份恢复: {self.ontology_path}.backup.*")
else:
    logger.info("未保存本体文件（无成功导入的术语）")
```

**关键改进**:
1. 添加条件：`self.stats['success'] > 0` - 仅在有成功导入时保存
2. 指定格式：`format="ofn"` - 保持原格式
3. 添加警告：提示备份文件位置

### 2. 增强备份机制

在配置文件中已经有备份选项，但可以改进：

```yaml
import_options:
  backup_before_import: true
  backup_after_import: true  # 新增：导入后也备份
  keep_backup_count: 5       # 新增：保留最近5个备份
```

### 3. 添加文件锁

防止并发导入破坏文件：

```python
import fcntl

def load_ontology(self):
    # 获取文件锁
    with open(f"{self.ontology_path}.lock", "w") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        # 加载本体...
```

### 4. 添加回滚机制

```python
def import_terms(self, ...):
    backup_path = None
    try:
        # 创建备份
        backup_path = self._create_backup()
        
        # 执行导入
        ...
        
        # 验证导入结果
        if self.stats['success'] == 0:
            logger.warning("没有成功导入任何术语，不保存本体文件")
            return
        
        # 保存本体
        self.ontology.save(...)
        
    except Exception as e:
        if backup_path:
            logger.error(f"导入失败，从备份恢复: {backup_path}")
            shutil.copy(backup_path, self.ontology_path)
        raise
```

---

## 📊 影响评估

### 数据安全性

| 项目 | 状态 | 说明 |
|------|------|------|
| 数据丢失 | ❌ 无 | 自动备份机制保护了数据 |
| 恢复时间 | ✅ < 1分钟 | 简单的文件复制 |
| 工作影响 | ✅ 最小 | 问题在测试阶段发现 |

### 备份文件状态

```bash
$ ls -lh src/ontology/tch-edit.owl.backup.*

-rw-r--r--  26K  tch-edit.owl.backup.20251031_222829
-rw-r--r--  26K  tch-edit.owl.backup.20251031_222901
-rw-r--r--  26K  tch-edit.owl.backup.20251101_193439
```

**结论**: 自动备份功能正常工作，保留了3个时间点的完整备份。

---

## 🎓 经验教训

### 1. owlready2 的保存行为

- `save()` 默认使用 RDF/XML 格式
- 需要明确指定 `format="ofn"` 来保持 OWL Functional Syntax
- 空的本体对象会生成只有头部的文件

### 2. 测试环境隔离

当前问题：测试直接操作生产文件 `tch-edit.owl`

**改进方案**：
```python
# 在测试模式下使用临时文件
if validate_only or test_mode:
    test_onto_path = "tch-edit-test.owl"
    shutil.copy(self.ontology_path, test_onto_path)
    self.ontology_path = test_onto_path
```

### 3. 保存前验证

应该在保存前验证本体内容：

```python
def _validate_before_save(self):
    """保存前验证本体是否有有效内容"""
    class_count = len(list(self.ontology.classes()))
    if class_count == 0:
        logger.error("本体中没有任何类，拒绝保存以避免数据丢失")
        return False
    logger.info(f"本体验证通过，包含 {class_count} 个类")
    return True
```

### 4. 备份策略的重要性

这次事件证明了自动备份的价值：
- ✅ 备份文件自动生成，带时间戳
- ✅ 多个备份保留，增加安全性
- ✅ 恢复过程简单快速

---

## 📝 待办事项

### 高优先级

- [ ] 修复 `import_terms.py` 的保存逻辑
- [ ] 添加保存前内容验证
- [ ] 指定保存格式为 OFN

### 中优先级

- [ ] 实现测试环境隔离
- [ ] 添加回滚机制
- [ ] 改进备份管理（保留数量限制）

### 低优先级

- [ ] 添加文件锁机制
- [ ] 创建自动化测试用例
- [ ] 编写操作手册

---

## 🔗 相关文件

- **问题文件**: `src/ontology/tch-edit.owl`
- **备份文件**: `src/ontology/tch-edit.owl.backup.20251101_193439`
- **导入脚本**: `src/scripts/import_terms.py`
- **配置文件**: `src/ontology/term-import-config.yaml`

---

## ✅ 检查清单

其他文件状态检查：

| 文件 | 状态 | 大小 | 说明 |
|------|------|------|------|
| src/ontology/tch.owl | ✅ 正常 | 232K | 发布版本本体 |
| src/ontology/tch-base.owl | ✅ 正常 | 20K | 基础本体 |
| src/ontology/tch-full.owl | ✅ 正常 | 232K | 完整本体 |
| tch.owl (根目录) | ✅ 正常 | 176K | 发布副本 |
| tch-base.owl (根目录) | ✅ 正常 | 2.3K | 基础副本 |
| tch-full.owl (根目录) | ✅ 正常 | 176K | 完整副本 |

**结论**: 其他本体文件均正常，没有类似问题。

---

**报告生成时间**: 2025-11-01 20:00  
**问题状态**: ✅ 已解决，数据已恢复  
**后续行动**: 修复导入脚本，防止再次发生
