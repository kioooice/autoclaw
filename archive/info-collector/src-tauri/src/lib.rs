use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use tauri::Manager;
use tauri_plugin_store::StoreExt;
use uuid::Uuid;
use chrono::Utc;
use base64::{engine::general_purpose::STANDARD, Engine};

// 收集项
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CollectionItem {
    pub id: String,
    #[serde(rename = "type")]
    pub item_type: String,
    pub content: String,
    pub title: Option<String>,
    pub summary: Option<String>,
    pub tags: Vec<String>,
    pub category: Option<String>,
    pub source: Option<String>,
    pub note: Option<String>,
    pub image_path: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

// AI 配置
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct AIConfig {
    pub provider: String,
    pub api_key: Option<String>,
    pub base_url: Option<String>,
    pub model: Option<String>,
}

// 应用设置
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct AppSettings {
    #[serde(rename = "aiConfig")]
    pub ai_config: AIConfig,
    pub shortcut: String,
    pub theme: String,
}

// 全局状态
pub struct AppState {
    pub settings: Mutex<AppSettings>,
}

// 截图功能 (Windows)
#[cfg(target_os = "windows")]
pub fn capture_screen() -> Result<String, String> {
    use std::io::Cursor;
    use image::{ImageBuffer, RgbaImage};
    use windows::Win32::Graphics::Gdi::*;
    use windows::Win32::UI::WindowsAndMessaging::*;

    unsafe {
        // 获取屏幕尺寸
        let width = GetSystemMetrics(SM_CXSCREEN);
        let height = GetSystemMetrics(SM_CYSCREEN);

        // 创建设备上下文
        let hdc_screen = GetDC(None);
        let hdc_mem = CreateCompatibleDC(Some(hdc_screen));
        let hbitmap = CreateCompatibleBitmap(hdc_screen, width, height);
        
        SelectObject(hdc_mem, hbitmap.into());
        
        // 截图
        BitBlt(hdc_mem, 0, 0, width, height, Some(hdc_screen), 0, 0, SRCCOPY);

        // 创建图像缓冲区
        let mut buffer: Vec<u8> = vec![0u8; (width * height * 4) as usize];
        let mut bmi = BITMAPINFO {
            bmiHeader: BITMAPINFOHEADER {
                biSize: std::mem::size_of::<BITMAPINFOHEADER>() as u32,
                biWidth: width,
                biHeight: -height, // top-down
                biPlanes: 1,
                biBitCount: 32,
                biCompression: BI_RGB.0,
                biSizeImage: 0,
                biXPelsPerMeter: 0,
                biYPelsPerMeter: 0,
                biClrUsed: 0,
                biClrImportant: 0,
            },
            bmiColors: [Default::default()],
        };

        GetDIBits(
            hdc_mem,
            hbitmap,
            0,
            height as u32,
            Some(buffer.as_mut_ptr() as *mut _),
            &mut bmi as *mut _ as *mut BITMAPINFO,
            DIB_RGB_COLORS,
        );

        // 清理资源
        DeleteObject(hbitmap.into());
        DeleteDC(hdc_mem);
        ReleaseDC(None, hdc_screen);

        // BGRA -> RGBA
        for chunk in buffer.chunks_exact_mut(4) {
            let b = chunk[0];
            chunk[0] = chunk[2]; // R
            chunk[2] = b;        // B
            chunk[3] = 255;      // A
        }

        // 创建图像并转换为 PNG
        let img: RgbaImage = ImageBuffer::from_raw(width as u32, height as u32, buffer).unwrap();
        let mut png_data = Vec::new();
        img.write_to(&mut Cursor::new(&mut png_data), image::ImageFormat::Png)
            .map_err(|e| e.to_string())?;

        // 转换为 base64
        Ok(STANDARD.encode(&png_data))
    }
}

// 初始化
#[tauri::command]
async fn init_database(_app: tauri::AppHandle) -> Result<(), String> {
    Ok(())
}

// 截图命令
#[tauri::command]
async fn capture_screenshot() -> Result<String, String> {
    #[cfg(target_os = "windows")]
    {
        capture_screen()
    }
    #[cfg(not(target_os = "windows"))]
    {
        Err("Screenshot not supported on this platform".to_string())
    }
}

// 保存收集项
#[tauri::command]
async fn save_item(app: tauri::AppHandle, item: CollectionItem) -> Result<CollectionItem, String> {
    let store = app.store("data.json").map_err(|e| e.to_string())?;
    
    let id = Uuid::new_v4().to_string();
    let now = Utc::now().to_rfc3339();
    
    let new_item = CollectionItem {
        id: id.clone(),
        item_type: item.item_type,
        content: item.content,
        title: item.title,
        summary: item.summary,
        tags: item.tags,
        category: item.category,
        source: item.source,
        note: item.note,
        image_path: item.image_path,
        created_at: now.clone(),
        updated_at: now,
    };

    // 获取现有列表
    let mut items: Vec<CollectionItem> = store
        .get("items")
        .and_then(|v| serde_json::from_value(v.clone()).ok())
        .unwrap_or_default();
    
    items.push(new_item.clone());
    
    store.set("items", serde_json::to_value(&items).map_err(|e| e.to_string())?);
    store.save().map_err(|e| e.to_string())?;

    Ok(new_item)
}

// 保存图片
#[tauri::command]
async fn save_image(app: tauri::AppHandle, image_data: String) -> Result<String, String> {
    // 解码 base64
    let bytes = STANDARD.decode(&image_data).map_err(|e| format!("Base64 decode error: {}", e))?;
    
    // 生成文件名
    let filename = format!("screenshot_{}.png", Utc::now().format("%Y%m%d_%H%M%S"));
    
    // 获取应用数据目录
    let app_dir = app.path().app_data_dir()
        .map_err(|e| format!("Get app_data_dir error: {:?}", e))?;
    
    let images_dir = app_dir.join("images");
    
    // 创建目录
    std::fs::create_dir_all(&images_dir)
        .map_err(|e| format!("Create dir error: {} (path: {:?})", e, images_dir))?;
    
    // 保存文件
    let file_path = images_dir.join(&filename);
    std::fs::write(&file_path, &bytes)
        .map_err(|e| format!("Write file error: {} (path: {:?})", e, file_path))?;
    
    log::info!("Image saved to: {:?}", file_path);
    Ok(file_path.to_string_lossy().to_string())
}

// 获取所有收集项
#[tauri::command]
async fn get_all_items(app: tauri::AppHandle) -> Result<Vec<CollectionItem>, String> {
    let store = app.store("data.json").map_err(|e| e.to_string())?;
    
    let items: Vec<CollectionItem> = store
        .get("items")
        .and_then(|v| serde_json::from_value(v.clone()).ok())
        .unwrap_or_default();

    let mut sorted = items;
    sorted.sort_by(|a, b| b.created_at.cmp(&a.created_at));

    Ok(sorted)
}

// 搜索收集项
#[tauri::command]
async fn search_items(app: tauri::AppHandle, query: String) -> Result<Vec<CollectionItem>, String> {
    let store = app.store("data.json").map_err(|e| e.to_string())?;
    
    let items: Vec<CollectionItem> = store
        .get("items")
        .and_then(|v| serde_json::from_value(v.clone()).ok())
        .unwrap_or_default();

    let query_lower = query.to_lowercase();
    let filtered: Vec<CollectionItem> = items
        .into_iter()
        .filter(|item| {
            item.content.to_lowercase().contains(&query_lower)
                || item.title.as_ref().map_or(false, |t| t.to_lowercase().contains(&query_lower))
                || item.summary.as_ref().map_or(false, |s| s.to_lowercase().contains(&query_lower))
                || item.note.as_ref().map_or(false, |n| n.to_lowercase().contains(&query_lower))
        })
        .collect();

    Ok(filtered)
}

// 删除收集项
#[tauri::command]
async fn delete_item(app: tauri::AppHandle, id: String) -> Result<(), String> {
    let store = app.store("data.json").map_err(|e| e.to_string())?;
    
    let mut items: Vec<CollectionItem> = store
        .get("items")
        .and_then(|v| serde_json::from_value(v.clone()).ok())
        .unwrap_or_default();
    
    items.retain(|item| item.id != id);
    
    store.set("items", serde_json::to_value(&items).map_err(|e| e.to_string())?);
    store.save().map_err(|e| e.to_string())?;

    Ok(())
}

// 更新收集项
#[tauri::command]
async fn update_item(
    app: tauri::AppHandle,
    id: String,
    updates: CollectionItem,
) -> Result<CollectionItem, String> {
    let store = app.store("data.json").map_err(|e| e.to_string())?;
    
    let mut items: Vec<CollectionItem> = store
        .get("items")
        .and_then(|v| serde_json::from_value(v.clone()).ok())
        .unwrap_or_default();

    let now = Utc::now().to_rfc3339();
    let updated_item = CollectionItem {
        id: id.clone(),
        item_type: updates.item_type,
        content: updates.content,
        title: updates.title,
        summary: updates.summary,
        tags: updates.tags,
        category: updates.category,
        source: updates.source,
        note: updates.note,
        image_path: updates.image_path,
        created_at: updates.created_at,
        updated_at: now,
    };

    if let Some(item) = items.iter_mut().find(|i| i.id == id) {
        *item = updated_item.clone();
    }

    store.set("items", serde_json::to_value(&items).map_err(|e| e.to_string())?);
    store.save().map_err(|e| e.to_string())?;

    Ok(updated_item)
}

// 获取设置
#[tauri::command]
async fn get_settings(app: tauri::AppHandle) -> Result<AppSettings, String> {
    let store = app.store("settings.json").map_err(|e| e.to_string())?;
    
    let settings: AppSettings = store
        .get("settings")
        .and_then(|v| serde_json::from_value(v.clone()).ok())
        .unwrap_or_default();

    Ok(settings)
}

// 保存设置
#[tauri::command]
async fn save_settings(app: tauri::AppHandle, settings: AppSettings) -> Result<(), String> {
    let store = app.store("settings.json").map_err(|e| e.to_string())?;
    
    store.set("settings", serde_json::to_value(&settings).map_err(|e| e.to_string())?);
    store.save().map_err(|e| e.to_string())?;

    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_clipboard_manager::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_store::Builder::default().build())
        .manage(AppState {
            settings: Mutex::new(AppSettings::default()),
        })
        .invoke_handler(tauri::generate_handler![
            init_database,
            capture_screenshot,
            save_item,
            save_image,
            get_all_items,
            search_items,
            delete_item,
            update_item,
            get_settings,
            save_settings,
        ])
        .setup(|app| {
            #[cfg(debug_assertions)]
            {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}