"use client"

import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ItemCard } from "./ItemCard"
import { CollectionItem } from "@/lib/types"
import { getAllItems, searchItems } from "@/lib/db"
import { Search, Settings, Camera, Loader2, Image } from "lucide-react"

interface ItemListProps {
  onOpenSettings: () => void
  onCapture: () => void
}

export function ItemList({ onOpenSettings, onCapture }: ItemListProps) {
  const [items, setItems] = useState<CollectionItem[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    loadItems()
  }, [])

  const loadItems = async () => {
    try {
      const data = await getAllItems()
      setItems(data.sort((a, b) => 
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      ))
    } catch (error) {
      console.error("加载失败:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadItems()
      return
    }

    setSearching(true)
    try {
      const results = await searchItems(searchQuery)
      setItems(results)
    } catch (error) {
      console.error("搜索失败:", error)
    } finally {
      setSearching(false)
    }
  }

  const handleItemDeleted = () => {
    loadItems()
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* 顶部工具栏 */}
      <div className="flex items-center gap-2 p-4 border-b">
        <div className="flex-1 flex gap-2">
          <Input
            placeholder="搜索..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            className="max-w-sm"
          />
          <Button variant="outline" size="icon" onClick={handleSearch} disabled={searching}>
            <Search className="h-4 w-4" />
          </Button>
        </div>
        <Button onClick={onCapture} className="gap-1">
          <Camera className="h-4 w-4" />
          截图
        </Button>
        <Button variant="outline" size="icon" onClick={onOpenSettings}>
          <Settings className="h-4 w-4" />
        </Button>
      </div>

      {/* 快捷提示 */}
      <div className="px-4 py-2 bg-muted/50 border-b text-xs text-muted-foreground flex items-center gap-2">
        <kbd className="px-1.5 py-0.5 bg-muted rounded text-[10px]">Ctrl+Q</kbd>
        <span>快速截图收集</span>
      </div>

      {/* 列表 */}
      <ScrollArea className="flex-1">
        <div className="p-4">
          {items.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <Image className="h-16 w-16 text-muted-foreground/50 mb-4" />
              <p className="text-muted-foreground mb-2">还没有收集任何内容</p>
              <p className="text-sm text-muted-foreground mb-4">
                按 <kbd className="px-1.5 py-0.5 bg-muted rounded text-xs">Ctrl+Q</kbd> 截图收集
              </p>
              <Button variant="outline" onClick={onCapture}>
                <Camera className="h-4 w-4 mr-2" />
                开始截图
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {items.map((item) => (
                <ItemCard 
                  key={item.id} 
                  item={item} 
                  onDelete={handleItemDeleted}
                />
              ))}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  )
}