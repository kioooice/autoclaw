# 批量转换 Agency Agents 到 OpenClaw Skills
# 高优先级代理列表 (20个)

$agents = @(
    # Engineering (4个)
    @{category="engineering"; file="engineering-security-engineer.md"; name="Security Engineer"; desc="安全工程师 - 威胁建模、漏洞评估、安全架构"; emoji="🔒"},
    @{category="engineering"; file="engineering-mobile-app-builder.md"; name="Mobile App Builder"; desc="移动应用开发 - iOS/Android、React Native、Flutter"; emoji="📱"},
    @{category="engineering"; file="engineering-rapid-prototyper.md"; name="Rapid Prototyper"; desc="快速原型开发 - POC、MVP、快速迭代"; emoji="🚀"},
    @{category="engineering"; file="engineering-senior-developer.md"; name="Senior Developer"; desc="高级开发者 - 代码质量、架构决策、最佳实践"; emoji="👨‍💻"},
    
    # Marketing (3个新增)
    @{category="marketing"; file="marketing-seo-specialist.md"; name="SEO Specialist"; desc="SEO专家 - 技术SEO、内容优化、链接建设"; emoji="🔍"},
    @{category="marketing"; file="marketing-linkedin-content-creator.md"; name="LinkedIn Content Creator"; desc="LinkedIn内容创作 - 思想领导力、B2B营销"; emoji="💼"},
    @{category="marketing"; file="marketing-reddit-community-builder.md"; name="Reddit Community Builder"; desc="Reddit社区建设 - 真实互动、价值驱动"; emoji="🔴"},
    
    # Design (2个新增)
    @{category="design"; file="design-brand-guardian.md"; name="Brand Guardian"; desc="品牌守护 - 品牌识别、一致性、定位"; emoji="🎯"},
    @{category="design"; file="design-ux-researcher.md"; name="UX Researcher"; desc="UX研究员 - 用户测试、行为分析、洞察提炼"; emoji="🔬"},
    
    # Paid Media (3个)
    @{category="paid-media"; file="paid-media-ppc-strategist.md"; name="PPC Strategist"; desc="PPC策略师 - Google/Microsoft/Amazon Ads"; emoji="💰"},
    @{category="paid-media"; file="paid-media-paid-social-strategist.md"; name="Paid Social Strategist"; desc="付费社交策略师 - Meta/LinkedIn/TikTok广告"; emoji="📢"},
    @{category="paid-media"; file="paid-media-auditor.md"; name="Paid Media Auditor"; desc="付费媒体审计师 - 200+检查点审计"; emoji="📊"},
    
    # Sales (2个)
    @{category="sales"; file="sales-deal-strategist.md"; name="Deal Strategist"; desc="成交策略师 - 谈判、成交、大客户"; emoji="🤝"},
    @{category="sales"; file="sales-outbound-strategist.md"; name="Outbound Strategist"; desc="外呼策略师 - 冷启动、拓客、序列"; emoji="📧"},
    
    # Product (1个新增)
    @{category="product"; file="product-feedback-synthesizer.md"; name="Feedback Synthesizer"; desc="反馈整合 - 用户声音、优先级、洞察"; emoji="👂"},
    
    # Testing (2个)
    @{category="testing"; file="testing-accessibility-auditor.md"; name="Accessibility Auditor"; desc="无障碍审计 - WCAG合规、A11y测试"; emoji="♿"},
    @{category="testing"; file="testing-performance-benchmarker.md"; name="Performance Benchmarker"; desc="性能基准测试 - 响应时间、吞吐量、优化"; emoji="⚡"},
    
    # Support (1个)
    @{category="support"; file="support-support-responder.md"; name="Support Responder"; desc="客服响应 - 工单处理、客户满意度"; emoji="🎧"},
    
    # Specialized (2个)
    @{category="specialized"; file="specialized-developer-advocate.md"; name="Developer Advocate"; desc="开发者布道 - 技术传播、社区建设、内容"; emoji="🎤"},
    @{category="specialized"; file="compliance-auditor.md"; name="Compliance Auditor"; desc="合规审计 - GDPR、SOC2、ISO27001"; emoji="📋"}
)

$sourceRoot = "C:\Users\Administrator\.openclaw-autoclaw\workspace\agency-agents-repo"
$targetRoot = "C:\Users\Administrator\.openclaw-autoclaw\workspace\skills"

$converted = 0
$skipped = 0

foreach ($agent in $agents) {
    $sourcePath = Join-Path $sourceRoot "$($agent.category)\$($agent.file)"
    
    # 处理 specialized 目录下的特殊文件
    if ($agent.category -eq "specialized" -and $agent.file -eq "compliance-auditor.md") {
        $sourcePath = Join-Path $sourceRoot "specialized\specialized-compliance-auditor.md"
    }
    
    $skillName = "agency-" + ($agent.name -replace ' ', '-').ToLower()
    $targetDir = Join-Path $targetRoot $skillName
    $targetPath = Join-Path $targetDir "SKILL.md"
    
    # 检查源文件是否存在
    if (-not (Test-Path $sourcePath)) {
        Write-Host "❌ 源文件不存在: $sourcePath" -ForegroundColor Red
        $skipped++
        continue
    }
    
    # 检查目标是否已存在
    if (Test-Path $targetPath) {
        Write-Host "⏭️ 已存在: $skillName" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    # 创建目标目录
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    
    # 读取源文件
    $content = Get-Content $sourcePath -Raw -Encoding UTF8
    
    # 创建 SKILL.md 内容
    $skillContent = @"
---
name: $skillName
description: Expert $($agent.desc). From Agency Agents.
version: 1.0.0
author: msitarzewski/agency-agents (converted to OpenClaw skill)
emoji: $($agent.emoji)
color: cyan
---

# Agency $($agent.name)

> **$($agent.desc)**

从 [Agency Agents](https://github.com/msitarzewski/agency-agents) 项目转换而来的 OpenClaw Skill。

---

## 🎯 何时使用此技能

当你需要：
$($content -replace '(?s)^---.*?---\s*', '' -replace '(?m)^# .*\n', '')

---

## 📚 原始来源

- **原始项目**: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
- **原始文件**: `$($agent.category)/$($agent.file)`
- **转换日期**: $(Get-Date -Format "yyyy-MM-dd")
"@

    # 写入文件
    $skillContent | Out-File -FilePath $targetPath -Encoding UTF8 -NoNewline
    
    Write-Host "✅ 转换成功: $skillName" -ForegroundColor Green
    $converted++
}

Write-Host "`n========== 转换完成 ==========" -ForegroundColor Cyan
Write-Host "✅ 成功转换: $converted" -ForegroundColor Green
Write-Host "⏭️ 跳过: $skipped" -ForegroundColor Yellow