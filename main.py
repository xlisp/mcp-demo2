#!/usr/bin/env python3
"""
MCP多功能应用
功能包括：文件访问、网络爬虫、数据库查询
"""

import asyncio
import json
import sqlite3
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import aiohttp
from bs4 import BeautifulSoup
import requests
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# 创建MCP服务器实例
server = Server("multi-function-mcp")

# 数据库初始化
def init_database():
    """初始化SQLite数据库"""
    conn = sqlite3.connect("mcp_data.db")
    cursor = conn.cursor()
    
    # 创建示例表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# 工具函数
def get_file_info(filepath: str) -> Dict[str, Any]:
    """获取文件信息"""
    try:
        path = Path(filepath)
        if not path.exists():
            return {"error": f"文件不存在: {filepath}"}
        
        stat = path.stat()
        return {
            "filename": path.name,
            "filepath": str(path.absolute()),
            "size": stat.st_size,
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "created_time": stat.st_ctime,
            "modified_time": stat.st_mtime
        }
    except Exception as e:
        return {"error": f"获取文件信息失败: {str(e)}"}

def read_file_content(filepath: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """读取文件内容"""
    try:
        path = Path(filepath)
        if not path.exists():
            return {"error": f"文件不存在: {filepath}"}
        
        if not path.is_file():
            return {"error": f"不是文件: {filepath}"}
        
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        
        return {
            "filepath": str(path.absolute()),
            "content": content,
            "size": len(content)
        }
    except Exception as e:
        return {"error": f"读取文件失败: {str(e)}"}

def list_directory(dirpath: str) -> Dict[str, Any]:
    """列出目录内容"""
    try:
        path = Path(dirpath)
        if not path.exists():
            return {"error": f"目录不存在: {dirpath}"}
        
        if not path.is_dir():
            return {"error": f"不是目录: {dirpath}"}
        
        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "path": str(item.absolute()),
                "is_file": item.is_file(),
                "is_directory": item.is_dir()
            })
        
        return {
            "directory": str(path.absolute()),
            "items": items,
            "count": len(items)
        }
    except Exception as e:
        return {"error": f"列出目录失败: {str(e)}"}

async def scrape_webpage(url: str) -> Dict[str, Any]:
    """爬取网页内容"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return {"error": f"HTTP错误: {response.status}"}
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # 提取基本信息
                title = soup.title.string if soup.title else "无标题"
                
                # 移除脚本和样式
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # 提取文本内容
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                content = '\n'.join(chunk for chunk in chunks if chunk)
                
                return {
                    "url": url,
                    "title": title,
                    "content": content[:5000],  # 限制长度
                    "status": "success"
                }
    except Exception as e:
        return {"error": f"爬取失败: {str(e)}"}

def database_query(query: str) -> Dict[str, Any]:
    """执行数据库查询"""
    try:
        conn = sqlite3.connect("mcp_data.db")
        cursor = conn.cursor()
        
        # 安全检查 - 只允许SELECT查询
        if not query.strip().upper().startswith('SELECT'):
            return {"error": "只允许SELECT查询"}
        
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))
        
        conn.close()
        return {
            "query": query,
            "columns": columns,
            "rows": result,
            "count": len(result)
        }
    except Exception as e:
        return {"error": f"数据库查询失败: {str(e)}"}

def save_file_to_db(filepath: str) -> Dict[str, Any]:
    """保存文件信息到数据库"""
    try:
        file_info = get_file_info(filepath)
        if "error" in file_info:
            return file_info
        
        conn = sqlite3.connect("mcp_data.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO files_info (filename, filepath, size)
            VALUES (?, ?, ?)
        """, (file_info["filename"], file_info["filepath"], file_info["size"]))
        
        conn.commit()
        conn.close()
        
        return {"message": "文件信息已保存到数据库", "file_info": file_info}
    except Exception as e:
        return {"error": f"保存失败: {str(e)}"}

async def save_scraped_data(url: str) -> Dict[str, Any]:
    """爬取并保存数据到数据库"""
    try:
        scraped = await scrape_webpage(url)
        if "error" in scraped:
            return scraped
        
        conn = sqlite3.connect("mcp_data.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO scraped_data (url, title, content)
            VALUES (?, ?, ?)
        """, (scraped["url"], scraped["title"], scraped["content"]))
        
        conn.commit()
        conn.close()
        
        return {"message": "爬取数据已保存到数据库", "scraped_data": scraped}
    except Exception as e:
        return {"error": f"保存爬取数据失败: {str(e)}"}

# MCP工具定义
@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """返回可用工具列表"""
    return [
        types.Tool(
            name="get_file_info",
            description="获取文件或目录的详细信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "文件或目录路径"
                    }
                },
                "required": ["filepath"]
            }
        ),
        types.Tool(
            name="read_file",
            description="读取文件内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "文件路径"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "文件编码，默认utf-8",
                        "default": "utf-8"
                    }
                },
                "required": ["filepath"]
            }
        ),
        types.Tool(
            name="list_directory",
            description="列出目录内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "目录路径"
                    }
                },
                "required": ["dirpath"]
            }
        ),
        types.Tool(
            name="scrape_webpage",
            description="爬取网页内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要爬取的网页URL"
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="database_query",
            description="执行数据库查询（仅支持SELECT）",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL查询语句"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="save_file_to_db",
            description="保存文件信息到数据库",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "文件路径"
                    }
                },
                "required": ["filepath"]
            }
        ),
        types.Tool(
            name="save_scraped_data",
            description="爬取网页并保存到数据库",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要爬取的网页URL"
                    }
                },
                "required": ["url"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """处理工具调用"""
    try:
        if name == "get_file_info":
            result = get_file_info(arguments["filepath"])
        elif name == "read_file":
            encoding = arguments.get("encoding", "utf-8")
            result = read_file_content(arguments["filepath"], encoding)
        elif name == "list_directory":
            result = list_directory(arguments["dirpath"])
        elif name == "scrape_webpage":
            result = await scrape_webpage(arguments["url"])
        elif name == "database_query":
            result = database_query(arguments["query"])
        elif name == "save_file_to_db":
            result = save_file_to_db(arguments["filepath"])
        elif name == "save_scraped_data":
            result = await save_scraped_data(arguments["url"])
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"工具执行失败: {str(e)}"}, ensure_ascii=False)
        )]

async def main():
    """主函数"""
    # 初始化数据库
    init_database()
    
    # 运行MCP服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="multi-function-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())

