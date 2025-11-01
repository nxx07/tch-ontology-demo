#!/bin/bash
# 批量验证所有类别的 CSV 模板
# Batch Validate All Category Templates

echo "==================================================================="
echo "TCH 术语导入系统 - 模板验证测试"
echo "TCH Term Import System - Template Validation Test"
echo "==================================================================="
echo ""

cd "$(dirname "$0")/../ontology" || exit 1

CATEGORIES=("pattern" "disease" "symptom" "sign" "herb" "formula" "principle" "method" "differentiation" "pathomechanism")

PASSED=0
FAILED=0
TOTAL=${#CATEGORIES[@]}

for category in "${CATEGORIES[@]}"; do
    echo "-------------------------------------------------------------------"
    echo "测试类别 / Testing Category: $category"
    echo "-------------------------------------------------------------------"
    
    template_file="../scripts/templates/${category}_template.csv"
    
    if [ ! -f "$template_file" ]; then
        echo "❌ 模板文件不存在 / Template file not found: $template_file"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    # 执行验证
    python ../scripts/import_terms.py \
        --category "$category" \
        --input "$template_file" \
        --validate-only
    
    if [ $? -eq 0 ]; then
        echo "✅ $category 模板验证通过 / Template validation passed"
        PASSED=$((PASSED + 1))
    else
        echo "❌ $category 模板验证失败 / Template validation failed"
        FAILED=$((FAILED + 1))
    fi
    
    echo ""
done

echo "==================================================================="
echo "验证汇总 / Validation Summary"
echo "==================================================================="
echo "总计 / Total: $TOTAL"
echo "通过 / Passed: $PASSED"
echo "失败 / Failed: $FAILED"
echo "==================================================================="

if [ $FAILED -eq 0 ]; then
    echo "✅ 所有模板验证通过！"
    echo "✅ All templates validated successfully!"
    exit 0
else
    echo "❌ 有 $FAILED 个模板验证失败"
    echo "❌ $FAILED template(s) failed validation"
    exit 1
fi
