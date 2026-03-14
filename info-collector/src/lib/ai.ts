import { AIConfig } from './types';

// DeepSeek API 调用
export async function summarizeContent(content: string, config: AIConfig): Promise<{ summary: string; tags: string[]; category: string }> {
  const baseUrl = config.baseUrl || 'https://api.deepseek.com';
  const model = config.model || 'deepseek-chat';
  
  const prompt = `请分析以下内容，提供：
1. 一段简洁的中文总结（50-100字）
2. 3-5个相关标签
3. 一个分类（技术/设计/产品/商业/学习/生活/娱乐/其他）

内容：
${content.slice(0, 4000)}

请以JSON格式返回：
{
  "summary": "总结内容",
  "tags": ["标签1", "标签2", "标签3"],
  "category": "分类"
}`;

  try {
    const response = await fetch(`${baseUrl}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7,
        max_tokens: 500,
      }),
    });

    if (!response.ok) {
      throw new Error(`AI API 错误: ${response.status}`);
    }

    const data = await response.json();
    const text = data.choices[0]?.message?.content || '';
    
    // 解析 JSON 响应
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const result = JSON.parse(jsonMatch[0]);
      return {
        summary: result.summary || '',
        tags: result.tags || [],
        category: result.category || '其他',
      };
    }
    
    // 如果解析失败，返回默认值
    return { summary: text.slice(0, 100), tags: [], category: '其他' };
  } catch (error) {
    console.error('AI 总结失败:', error);
    throw error;
  }
}

// 检测内容类型
export function detectContentType(content: string): 'link' | 'text' | 'video' {
  // 视频链接
  if (content.includes('bilibili.com') || 
      content.includes('youtube.com') || 
      content.includes('youtu.be')) {
    return 'video';
  }
  
  // 链接
  if (content.match(/^https?:\/\//)) {
    return 'link';
  }
  
  // 文本
  return 'text';
}

// 提取来源域名
export function extractSource(content: string): string | undefined {
  const match = content.match(/^https?:\/\/([^\/]+)/);
  return match ? match[1].replace('www.', '') : undefined;
}