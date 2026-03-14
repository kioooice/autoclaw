"use client"

import { useState, useEffect } from "react"
import { ItemList } from "@/components/ItemList"
import { ScreenshotCollector } from "@/components/ScreenshotCollector"
import { SettingsDialog } from "@/components/SettingsDialog"
import { CollectionItem } from "@/lib/types"
import { getSettings, captureScreenshot } from "@/lib/db"
import { Sparkles, Loader2, Camera } from "lucide-react"
import { toast } from "@/components/Toast"

export default function Home() {
  const [collectOpen, setCollectOpen] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [apiKey, setApiKey] = useState<string>()
  const [initializing, setInitializing] = useState(true)
  const [screenshotData, setScreenshotData] = useState<string>("")

  // 初始化
  useEffect(() => {
    const init = async () => {
      try {
        const { invoke } = await import('@tauri-apps/api/core')
        await invoke('init_database')
        
        const settings = await getSettings()
        setApiKey(settings.aiConfig?.apiKey)
      } catch (error) {
        console.error("初始化失败:", error)
      } finally {
        setInitializing(false)
      }
    }
    init()
  }, [])

  // 注册全局快捷键
  useEffect(() => {
    const registerShortcut = async () => {
      if (initializing) return
      
      try {
        const { register, unregister } = await import('@tauri-apps/plugin-global-shortcut')
        const { getCurrentWindow } = await import('@tauri-apps/api/window')
        
        try {
          await unregister('Ctrl+Q')
        } catch {}
        
        await register('Ctrl+Q', async (event) => {
          if (event.state === 'Pressed') {
            // 截图
            try {
              const imageData = await captureScreenshot()
              setScreenshotData(imageData)
              
              // 显示窗口
              const mainWindow = getCurrentWindow()
              await mainWindow.show()
              await mainWindow.setFocus()
              setCollectOpen(true)
            } catch (error) {
              console.error("截图失败:", error)
              toast.error("截图失败: " + (error instanceof Error ? error.message : String(error)))
            }
          }
        })
        console.log("全局快捷键注册成功: Ctrl+Q")
      } catch (error) {
        console.error("注册快捷键失败:", error)
      }
    }
    registerShortcut()
  }, [initializing])

  const handleCollectSuccess = (item: CollectionItem) => {
    toast.success("收集成功！")
    setScreenshotData("")
  }

  const handleApiKeyChange = (key: string) => {
    setApiKey(key)
  }

  // 手动触发截图
  const handleManualCapture = async () => {
    try {
      const imageData = await captureScreenshot()
      setScreenshotData(imageData)
      setCollectOpen(true)
    } catch (error) {
      console.error("截图失败:", error)
      toast.error("截图失败")
    }
  }

  if (initializing) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b bg-card">
        <div className="flex items-center gap-2">
          <Sparkles className="h-6 w-6 text-primary" />
          <h1 className="text-lg font-semibold">InfoCollector</h1>
          <span className="text-xs text-muted-foreground ml-2 hidden sm:inline">
            按 Ctrl+Q 截图收集
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button 
            onClick={handleManualCapture}
            className="flex items-center gap-1 px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
          >
            <Camera className="h-4 w-4" />
            截图收集
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <ItemList 
          onOpenSettings={() => setSettingsOpen(true)}
          onCapture={handleManualCapture}
        />
      </main>

      {/* Dialogs */}
      <ScreenshotCollector 
        open={collectOpen} 
        onOpenChange={(open) => {
          setCollectOpen(open)
          if (!open) setScreenshotData("")
        }}
        onSuccess={handleCollectSuccess}
        apiKey={apiKey}
        screenshotData={screenshotData}
      />
      <SettingsDialog 
        open={settingsOpen} 
        onOpenChange={setSettingsOpen}
        onApiKeyChange={handleApiKeyChange}
      />
    </div>
  )
}