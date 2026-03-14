# 热度评估脚本

## 触发条件
- Heartbeat 中定期执行（每 2-3 天）
- 用户明确要求"反思"
- episodic/warm/ 文件超过 20 个

## 评估流程

1. 读取 `episodic/heat.json`
2. 遍历 episodic/ 下所有 .md 文件
3. 计算热度评分：
   ```
   heat_score = access_count × 0.3
              + importance × 0.4
              + recency × 0.2
              + user_explicit × 0.1
   ```
4. 根据评分执行晋升/降级：
   - `warm → hot`: heat_score > 0.6 且 7 天内有访问
   - `hot → profile`: heat_score > 0.8 且用户明确标记
   - `hot → warm`: 7 天无访问
   - `warm → archive`: 30 天无访问
5. 更新 heat.json
6. 输出变更报告

## PowerShell 实现

```powershell
# scripts/evaluate-heat.ps1

$heatFile = "memory/episodic/heat.json"
$heat = Get-Content $heatFile | ConvertFrom-Json

foreach ($item in $heat.items) {
    # 计算时间衰减
    $daysSinceAccess = (Get-Date) - [datetime]$item.last_access
    $recency = [math]::Max(0, 1 - ($daysSinceAccess.Days / 30))

    # 计算热度
    $heatScore = $item.access_count * 0.3 +
                 $item.importance * 0.4 +
                 $recency * 0.2 +
                 ($item.user_explicit ? 0.1 : 0)

    $item.heat_score = [math]::Round($heatScore, 2)
}

$heat | ConvertTo-Json -Depth 10 | Set-Content $heatFile
```

## 输出格式

```
📊 热度评估报告 (2026-03-14)

晋升:
  - cli-anything.md → hot/ (heat: 0.72)

降级:
  - old-project.md → archive/ (heat: 0.15)

保留:
  - current-work.md → warm/ (heat: 0.45)
```

---

*此文件为脚本说明，实际执行时由 Agent 完成*