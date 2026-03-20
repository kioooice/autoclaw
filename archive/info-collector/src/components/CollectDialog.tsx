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
import { detectContentType, extractSource, summarizeContent } from "@/lib/ai"
import { saveItem } from "@/lib/db"
import { CollectionItem } from "@/lib/types"
import { Loader2, Sparkles, ClipboardPaste } from "lucide-react"

interface CollectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: (item: CollectionItem) => void
  apiKey?: string
  initialContent?: string
}

export function CollectDialog({ open, onOpenChange, onSuccess, apiKey, initialContent }: CollectDialogProps) {
  const [content, setContent] = useState("")
  const [note, setNote] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  // 当打开或初始内容变化时更新
  useEffect(() => {
    if (open && initialContent) {
      setContent(initialContent)
    }
  }, [open, initialContent])

  const handleSubmit = async () => {
    if (!content.trim()) {
      setError("请输入内容")
      return
    }

    if (!apiKey) {
      setError("请先配置 API Key")
      return
    }

    setLoading(true)
    setError("")

    try {
      const type = detectContentType(content)
      const source = extractSource(content)

      // 调用 AI 总结
      const aiResult = await summarizeContent(content, {
        provider: 'deepseek',
        apiKey,
      })

      // 保存到数据库
      const item = await saveItem({
        type,
        content: content.trim(),
        title: source ? `来自 ${source}` : undefined,
        summary: aiResult.summary,
        tags: aiResult.tags,
        category: aiResult.category,
        source,
        note: note.trim() || undefined,
      })

      // 重置表单
      setContent("")
      setNote("")
      onOpenChange(false)
      onSuccess?.(item)
    } catch (err) {
      setError(err instanceof Error ? err.message : "保存失败")
    } finally {
      setLoading(false)
    }
  }

  const handlePaste = async () => {
    try {
      const { readText } = await import('@tauri-apps/plugin-clipboard-manager')
      const text = await readText()
      if (text) {
        setContent(text)
      }
    } catch (error) {
      console.error("读取剪贴板失败:", error)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            收集信息
          </DialogTitle>
          <DialogDescription>
            粘贴链接或文本，AI 将自动总结并分类
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="space-y-2">
            <div className="flex gap-2">
              <Input
                placeholder="粘贴链接或文本..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="flex-1"
                autoFocus
              />
              <Button variant="outline" onClick={handlePaste} title="从剪贴板粘贴">
                <ClipboardPaste className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <Input
              placeholder="添加笔记（可选）"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </div>

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              取消
            </Button>
            <Button onClick={handleSubmit} disabled={loading}>
              {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {loading ? "处理中..." : "收集"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}