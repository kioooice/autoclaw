import { CollectionItem, AIConfig, AppSettings } from './types';

// 数据库操作（通过 Tauri 命令）

// 初始化数据库
export async function initDatabase(): Promise<void> {
  const { invoke } = await import('@tauri-apps/api/core');
  await invoke('init_database');
}

// 截图
export async function captureScreenshot(): Promise<string> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('capture_screenshot');
}

// 保存图片
export async function saveImage(imageData: string): Promise<string> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('save_image', { imageData });
}

// 保存收集项
export async function saveItem(item: Omit<CollectionItem, 'id' | 'createdAt' | 'updatedAt'>): Promise<CollectionItem> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('save_item', { item });
}

// 获取所有收集项
export async function getAllItems(): Promise<CollectionItem[]> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('get_all_items');
}

// 搜索收集项
export async function searchItems(query: string): Promise<CollectionItem[]> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('search_items', { query });
}

// 删除收集项
export async function deleteItem(id: string): Promise<void> {
  const { invoke } = await import('@tauri-apps/api/core');
  await invoke('delete_item', { id });
}

// 更新收集项
export async function updateItem(id: string, updates: Partial<CollectionItem>): Promise<CollectionItem> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('update_item', { id, updates });
}

// 获取设置
export async function getSettings(): Promise<AppSettings> {
  const { invoke } = await import('@tauri-apps/api/core');
  return await invoke('get_settings');
}

// 保存设置
export async function saveSettings(settings: Partial<AppSettings>): Promise<void> {
  const { invoke } = await import('@tauri-apps/api/core');
  await invoke('save_settings', { settings });
}