#!/usr/bin/env python3
"""
安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="multi-function-mcp",
    version="1.0.0",
    description="MCP多功能应用：文件访问、网络爬虫、数据库查询",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.11.0",
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "multi-function-mcp=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
