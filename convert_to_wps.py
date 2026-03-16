#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time

def convert_html_to_docx():
    """使用WPS将HTML转换为DOCX"""
    try:
        # 尝试导入win32com
        import win32com.client
        
        html_path = r"C:\Users\Administrator\Desktop\openclaw应用.html"
        docx_path = r"C:\Users\Administrator\Desktop\openclaw应用.docx"
        
        # 创建WPS应用对象
        wps = win32com.client.Dispatch("Kwps.Application")
        wps.Visible = False
        
        # 打开HTML文件
        doc = wps.Documents.Open(html_path)
        
        # 另存为DOCX格式 (16 = wdFormatDocumentDefault)
        doc.SaveAs2(docx_path, 16)
        
        # 关闭文档
        doc.Close()
        wps.Quit()
        
        print(f"转换成功！文件已保存到: {docx_path}")
        return True
        
    except ImportError:
        print("错误: 需要安装 pywin32")
        print("请运行: pip install pywin32")
        return False
    except Exception as e:
        print(f"转换失败: {e}")
        return False

if __name__ == "__main__":
    convert_html_to_docx()
