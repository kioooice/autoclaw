// 收集项类型
export interface CollectionItem {
  id: string;
  type: 'link' | 'text' | 'video';
  content: string;           // 原始链接或文本
  title?: string;            // 标题
  summary?: string;          // AI 总结
  tags: string[];            // AI 生成的标签
  category?: string;         // AI 分类
  source?: string;           // 来源域名
  note?: string;             // 用户自己的笔记
  image_path?: string;       // 截图路径
  createdAt: string;
  updatedAt: string;
}

// AI 配置
export interface AIConfig {
  provider: 'deepseek' | 'openai' | 'ollama';
  apiKey?: string;
  baseUrl?: string;
  model?: string;
}

// 应用设置
export interface AppSettings {
  aiConfig: AIConfig;
  shortcut: string;
  theme: 'dark' | 'light' | 'system';
}

// 预设分类
export const PRESET_CATEGORIES = [
  '技术',
  '设计',
  '产品',
  '商业',
  '学习',
  '生活',
  '娱乐',
  '其他',
] as const;

export type Category = typeof PRESET_CATEGORIES[number];