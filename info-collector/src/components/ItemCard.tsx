"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CollectionItem } from "@/lib/types"
import { 
  Trash2, 
  FileText, 
  Link, 
  Video,
  Calendar,
  Image as ImageIcon
} from "lucide-react"
import { deleteItem } from "@/lib/db"

interface ItemCardProps {
  item: CollectionItem
  onDelete?: () => void
}

const typeIcons = {
  link: Link,
  text: FileText,
  video: Video,
}

const typeColors = {
  link: "text-blue-400",
  text: "text-green-400",
  video: "text-purple-400",
}

export function ItemCard({ item, onDelete }: ItemCardProps) {
  const [isDeleting, setIsDeleting] = useState(false)
  const [showImage, setShowImage] = useState(false)

  const handleDelete = async () => {
    if (!confirm("确定删除？")) return
    setIsDeleting(true)
    try {
      await deleteItem(item.id)
      onDelete?.()
    } catch (error) {
      console.error("删除失败:", error)
    } finally {
      setIsDeleting(false)
    }
  }

  const TypeIcon = typeIcons[item.type] || FileText

  return (
    <>
      <Card className="group hover:border-primary/50 transition-colors overflow-hidden">
        {/* 截图预览 */}
        {item.image_path && (
          <div 
            className="h-32 bg-muted overflow-hidden cursor-pointer"
            onClick={() => setShowImage(true)}
          >
            <img 
              src={`file://${item.image_path}`}
              alt="Screenshot"
              className="w-full h-full object-cover hover:scale-105 transition-transform"
              onError={(e) => {
                e.currentTarget.style.display = 'none'
              }}
            />
          </div>
        )}
        
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-center gap-2 min-w-0">
              {item.image_path ? (
                <ImageIcon className="h-4 w-4 shrink-0 text-primary" />
              ) : (
                <TypeIcon className={`h-4 w-4 shrink-0 ${typeColors[item.type]}`} />
              )}
              <CardTitle className="text-sm font-medium truncate">
                {item.title || item.content.slice(0, 50)}
              </CardTitle>
            </div>
            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-7 w-7 text-destructive hover:text-destructive"
                onClick={handleDelete}
                disabled={isDeleting}
              >
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-3">
          {item.summary && (
            <p className="text-sm text-muted-foreground line-clamp-3">
              {item.summary}
            </p>
          )}
          
          {item.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {item.tags.map((tag) => (
                <Badge key={tag} variant="secondary" className="text-xs">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
          
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              {new Date(item.createdAt).toLocaleDateString('zh-CN')}
            </div>
            {item.category && (
              <Badge variant="outline" className="text-xs">
                {item.category}
              </Badge>
            )}
          </div>

          {item.note && (
            <div className="pt-2 border-t">
              <p className="text-xs text-muted-foreground italic">
                📝 {item.note}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* 图片预览弹窗 */}
      {showImage && item.image_path && (
        <div 
          className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4"
          onClick={() => setShowImage(false)}
        >
          <img 
            src={`file://${item.image_path}`}
            alt="Screenshot"
            className="max-w-full max-h-full object-contain"
          />
          <button 
            className="absolute top-4 right-4 text-white hover:text-white/80"
            onClick={() => setShowImage(false)}
          >
            ✕
          </button>
        </div>
      )}
    </>
  )
}