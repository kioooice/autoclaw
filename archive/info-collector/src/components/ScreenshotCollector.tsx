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
import { summarizeContent } from "@/lib/ai"
import { saveItem, saveImage } from "@/lib/db"
import { CollectionItem } from "@/lib/types"
import { Loader2, Sparkles, Crop, Check, X } from "lucide-react"

interface ScreenshotCollectorProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: (item: CollectionItem) => void
  apiKey?: string
  screenshotData?: string
}

export function ScreenshotCollector({ 
  open, 
  onOpenChange, 
  onSuccess, 
  apiKey,
  screenshotData 
}: ScreenshotCollectorProps) {
  const [note, setNote] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [saving, setSaving] = useState(false)

  const handleSave = async () => {
    if (!screenshotData) {
      setError("没有截图数据")
      return
    }

    setSaving(true)
    setLoading(true)
    setError("")

    try {
      // 保存图片文件
      const imagePath = await saveImage(screenshotData)
      
      let summary = ""
      let tags: string[] = []
      let category = "其他"
      
      // AI 总结（如果有 API Key）
      if (apiKey) {
        try {
          const aiResult = await summarizeContent(
            "请分析这张截图的内容，总结主要信息", 
            { provider: 'deepseek', apiKey }
          )
          summary = aiResult.summary
          tags = aiResult.tags
          category = aiResult.category
        } catch (e) {
          console.error("AI 总结失败:", e)
        }
      }

      // 保存收集项
      const item = await saveItem({
        type: 'text',
        content: summary || "截图收集",
        title: note ? `笔记: ${note.slice(0, 30)}` : "截图收集",
        summary,
        tags,
        category,
        note: note.trim() || undefined,
        image_path: imagePath,
      })

      setNote("")
      onOpenChange(false)
      onSuccess?.(item)
    } catch (err) {
      setError(err instanceof Error ? err.message : "保存失败")
    } finally {
      setLoading(false)
      setSaving(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Crop className="h-5 w-5 text-primary" />
            收集截图
          </DialogTitle>
          <DialogDescription>
            截图已捕获，添加笔记后保存
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-auto space-y-4">
          {/* 截图预览 */}
          {screenshotData && (
            <div className="border rounded-lg overflow-hidden bg-muted/50">
              <img 
                src={`data:image/png;base64,${screenshotData}`}
                alt="Screenshot"
                className="w-full h-auto max-h-[400px] object-contain"
              />
            </div>
          )}

          {/* 笔记输入 */}
          <div className="space-y-2">
            <Input
              placeholder="添加笔记说明（可选）..."
              value={note}
              onChange={(e) => setNote(e.target.value)}
              disabled={loading}
            />
          </div>

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}
        </div>

        <div className="flex justify-end gap-2 pt-4 border-t">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
            <X className="h-4 w-4 mr-2" />
            取消
          </Button>
          <Button onClick={handleSave} disabled={loading || !screenshotData}>
            {loading ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Check className="h-4 w-4 mr-2" />
            )}
            {loading ? "保存中..." : "保存截图"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}