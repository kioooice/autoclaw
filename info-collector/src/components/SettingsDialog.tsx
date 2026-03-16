"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { getSettings, saveSettings } from "@/lib/db"
import { AppSettings } from "@/lib/types"
import { Key, Save, Check } from "lucide-react"

interface SettingsDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onApiKeyChange?: (key: string) => void
}

export function SettingsDialog({ open, onOpenChange, onApiKeyChange }: SettingsDialogProps) {
  const [apiKey, setApiKey] = useState("")
  const [shortcut, setShortcut] = useState("Ctrl+Q")
  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (open) {
      loadSettings()
    }
  }, [open])

  const loadSettings = async () => {
    try {
      const settings = await getSettings()
      setApiKey(settings.aiConfig?.apiKey || "")
      setShortcut(settings.shortcut || "Ctrl+Q")
    } catch (error) {
      console.error("加载设置失败:", error)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      await saveSettings({
        aiConfig: {
          provider: 'deepseek',
          apiKey,
        },
        shortcut,
      })
      onApiKeyChange?.(apiKey)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (error) {
      console.error("保存设置失败:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[400px]">
        <DialogHeader>
          <DialogTitle>设置</DialogTitle>
          <DialogDescription>
            配置 API Key 和快捷键
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* API Key */}
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <Key className="h-4 w-4" />
              DeepSeek API Key
            </label>
            <Input
              type="password"
              placeholder="sk-..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <p className="text-xs text-muted-foreground">
              获取 API Key: <a 
                href="https://platform.deepseek.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                platform.deepseek.com
              </a>
            </p>
          </div>

          {/* 快捷键 */}
          <div className="space-y-2">
            <label className="text-sm font-medium">快捷键</label>
            <Input
              value={shortcut}
              onChange={(e) => setShortcut(e.target.value)}
              placeholder="Ctrl+Shift+C"
            />
            <p className="text-xs text-muted-foreground">
              用于快速唤起收集窗口
            </p>
          </div>

          <div className="flex justify-end">
            <Button onClick={handleSave} disabled={loading}>
              {saved ? (
                <>
                  <Check className="h-4 w-4 mr-2" />
                  已保存
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  保存
                </>
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}