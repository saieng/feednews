#!/usr/bin/env python3
"""
启动脚本 - 用于本地开发
"""

import uvicorn
import logging

# 设置详细的日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        raise