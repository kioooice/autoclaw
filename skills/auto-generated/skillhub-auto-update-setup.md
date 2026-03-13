# skillhub-auto-update-setup

自动创建。从 2026-03-13 配置自动更新任务中提炼。

## 触发条件

- 用户要求"配置自动更新"、"设置定时更新技能"
- 需要为 Skillhub 技能设置 cron 任务

## 前置条件

- Skillhub CLI 已安装 (`~/.local/bin/skillhub`)
- OpenClaw Gateway 需要运行才能执行 cron 任务

## 步骤

1. **确认 Skillhub 可用**：`skillhub --version`
2. **创建 cron 任务配置**：
   - 时间：默认每周一 10:00（可调整）
   - 时区：Asia/Shanghai
   - 命令：`skillhub upgrade`
3. **写入 jobs.json**：`~/.openclaw/cron/jobs.json`
4. **创建 Windows 任务计划**：双重保障（即使 Gateway 不运行也能执行）
5. **更新 memory/world/facts.md** 记录 cron 配置

## 配置格式

```json
{
  "jobs": [
    {
      "name": "Weekly skills auto-update",
      "schedule": {
        "kind": "cron",
        "expr": "0 10 * * 1",
        "tz": "Asia/Shanghai"
      },
      "sessionTarget": "isolated",
      "payload": {
        "kind": "agentTurn",
        "message": "Run skillhub upgrade to update all installed skills. Report what was updated.",
        "lightContext": true
      },
      "delivery": {
        "mode": "announce",
        "channel": "webchat",
        "bestEffort": true
      },
      "enabled": true
    }
  ]
}
```

## Windows 任务计划

```powershell
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "10:00 AM"
Register-ScheduledTask -TaskName "Skillhub-Weekly-Upgrade" ...
```

## 注意事项

- Gateway 必须运行才能触发 cron 任务
- Windows 任务计划在用户登录时执行，无需 Gateway
- `delivery.channel` 根据用户实际使用的频道调整

## 改进记录

- 2026-03-13：初始创建
- 2026-03-13：改为每周运行，添加 Windows 任务计划支持