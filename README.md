# MCP多功能应用使用指南

## 功能概述

这个MCP应用提供了三大核心功能：
1. **文件系统访问** - 读取、查看文件和目录信息
2. **网络爬虫** - 爬取网页内容并解析
3. **数据库操作** - SQLite数据库查询和数据存储

## 安装步骤

### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv mcp_env
source mcp_env/bin/activate  # Linux/Mac
# 或
mcp_env\Scripts\activate  # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行应用
```bash
python main.py
```

## 可用工具

### 文件操作工具

#### 1. get_file_info
获取文件或目录的详细信息
```json
{
  "name": "get_file_info",
  "arguments": {
    "filepath": "/path/to/file.txt"
  }
}
```

#### 2. read_file
读取文件内容
```json
{
  "name": "read_file",
  "arguments": {
    "filepath": "/path/to/file.txt",
    "encoding": "utf-8"
  }
}
```

#### 3. list_directory
列出目录内容
```json
{
  "name": "list_directory",
  "arguments": {
    "dirpath": "/path/to/directory"
  }
}
```

#### 4. save_file_to_db
保存文件信息到数据库
```json
{
  "name": "save_file_to_db",
  "arguments": {
    "filepath": "/path/to/file.txt"
  }
}
```

### 网络爬虫工具

#### 5. scrape_webpage
爬取网页内容
```json
{
  "name": "scrape_webpage",
  "arguments": {
    "url": "https://example.com"
  }
}
```

#### 6. save_scraped_data
爬取网页并保存到数据库
```json
{
  "name": "save_scraped_data",
  "arguments": {
    "url": "https://example.com"
  }
}
```

### 数据库工具

#### 7. database_query
执行数据库查询（仅支持SELECT）
```json
{
  "name": "database_query",
  "arguments": {
    "query": "SELECT * FROM files_info LIMIT 10"
  }
}
```

## 数据库结构

### files_info表
存储文件信息
```sql
CREATE TABLE files_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### scraped_data表
存储爬取的网页数据
```sql
CREATE TABLE scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    title TEXT,
    content TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 使用示例

### 示例1：文件系统操作
```bash
# 查看当前目录内容
list_directory(".")

# 读取配置文件
read_file("config.json")

# 获取文件信息并保存到数据库
get_file_info("README.md")
save_file_to_db("README.md")
```

### 示例2：网络爬虫
```bash
# 爬取网页
scrape_webpage("https://httpbin.org/json")

# 爬取并保存到数据库
save_scraped_data("https://httpbin.org/json")
```

### 示例3：数据库查询
```bash
# 查询所有文件信息
database_query("SELECT * FROM files_info")

# 查询最近爬取的数据
database_query("SELECT url, title, scraped_at FROM scraped_data ORDER BY scraped_at DESC LIMIT 5")

# 统计数据
database_query("SELECT COUNT(*) as total_files FROM files_info")
```

## 安全特性

1. **文件访问限制** - 可配置允许访问的文件类型和路径
2. **数据库安全** - 仅允许SELECT查询，防止数据被恶意修改
3. **内容长度限制** - 爬取内容限制在5000字符以内
4. **错误处理** - 完善的异常处理机制

## 配置选项

编辑 `config.json` 文件可以自定义：
- 数据库设置
- 爬虫超时时间
- 允许的文件扩展名
- 安全限制

## 扩展功能

可以轻松添加新的工具：
1. 在主文件中定义新的工具函数
2. 在 `handle_list_tools()` 中添加工具描述
3. 在 `handle_call_tool()` 中添加工具调用逻辑

## 故障排除

### 常见问题
1. **文件不存在** - 检查文件路径是否正确
2. **网络连接失败** - 检查URL是否有效和网络连接
3. **数据库错误** - 确保数据库文件权限正确
4. **编码问题** - 尝试不同的编码参数

### 日志调试
应用会在控制台输出详细的错误信息，便于调试。

## 许可证

MIT License - 自由使用和修改

---

## 更多说明: 可以直接与支持MCP协议的客户端（如Claude Desktop）集成使用

一个完整的MCP应用，它将包含文件访问、网络爬虫和数据库查询功能。现在让我为你创建依赖文件和配置文件：我已经为你创建了一个完整的MCP多功能应用！这个应用包含了你要求的所有功能：

## 🎯 主要功能

### 1. **文件系统访问**
- `get_file_info` - 获取文件/目录详细信息
- `read_file` - 读取文件内容（支持不同编码）
- `list_directory` - 列出目录内容
- `save_file_to_db` - 保存文件信息到数据库

### 2. **网络爬虫**
- `scrape_webpage` - 爬取网页内容并解析
- `save_scraped_data` - 爬取网页并保存到数据库
- 使用BeautifulSoup解析HTML，提取标题和文本内容

### 3. **数据库操作**
- `database_query` - 执行SQL查询（仅支持SELECT保证安全）
- 自动创建SQLite数据库和表结构
- 存储文件信息和爬取数据

## 🔧 技术特性

- **异步支持** - 使用async/await提高性能
- **安全设计** - 限制数据库操作，防止恶意查询
- **错误处理** - 完善的异常处理和错误反馈
- **可配置** - 通过config.json自定义行为
- **扩展性** - 易于添加新工具和功能

## 📦 安装使用

1. **安装依赖**：
```bash
pip install -r requirements.txt
```

2. **运行应用**：
```bash
python main.py
```

3. **使用工具**：
应用会自动创建数据库表，然后你可以通过MCP协议调用各种工具。

## 🛡️ 安全特性

- 文件访问限制和路径验证
- 数据库仅允许SELECT查询
- 网络请求超时和内容长度限制
- 完善的输入验证和错误处理

这个应用已经是一个完整的MCP服务器，可以直接与支持MCP协议的客户端（如Claude Desktop）集成使用。你可以根据需要进一步扩展功能或调整配置。

---
### 高级用法: https://github.com/modelcontextprotocol/python-sdk

```python
"""
Run from the repository root:
uv run examples/snippets/servers/lowlevel/basic.py
"""

import asyncio

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Create a server instance
server = Server("example-server")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="example-prompt",
            description="An example prompt template",
            arguments=[types.PromptArgument(name="arg1", description="Example argument", required=True)],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Get a specific prompt by name."""
    if name != "example-prompt":
        raise ValueError(f"Unknown prompt: {name}")

    arg1_value = (arguments or {}).get("arg1", "default")

    return types.GetPromptResult(
        description="Example prompt",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=f"Example prompt text with argument: {arg1_value}"),
            )
        ],
    )


async def run():
    """Run the basic low-level server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
```

### FastMCP 

```python
"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

```

### 其他资料参考：

https://github.com/liaokongVFX/MCP-Chinese-Getting-Started-Guide

https://zhuanlan.zhihu.com/p/29001189476

