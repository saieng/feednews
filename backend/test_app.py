#!/usr/bin/env python3
"""
测试应用程序导入
"""

try:
    print("正在导入应用程序...")
    from app.main import app
    print("应用程序导入成功")
    
    print("正在测试路由...")
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    print("测试根路径...")
    response = client.get("/")
    print(f"根路径状态码: {response.status_code}")
    print(f"根路径响应: {response.json()}")
    
    print("测试健康检查...")
    response = client.get("/health")
    print(f"健康检查状态码: {response.status_code}")
    print(f"健康检查响应: {response.json()}")
    
    print("测试 API 文档...")
    response = client.get("/docs")
    print(f"API 文档状态码: {response.status_code}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()