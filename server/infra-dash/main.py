from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import docker
import os
import subprocess

app = FastAPI(title="Infra-Dash API")
client = docker.from_env()

# 静态文件映射
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/api/services")
async def get_services():
    try:
        containers = client.containers.list(all=True)
        services = []
        for container in containers:
            # 只显示属于本项目或相关的容器
            # 简单起见，显示所有容器
            services.append({
                "id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "none",
                "ports": container.ports
            })
        return services
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/services/{name}/{action}")
async def service_action(name: str, action: str):
    try:
        container = client.containers.get(name)
        if action == "start":
            container.start()
        elif action == "stop":
            container.stop()
        elif action == "restart":
            container.restart()
        elif action == "rebuild":
            # 重建逻辑：这里简单通过 shell 调用 docker compose
            # 注意：这需要容器内能访问 docker compose 并能找到对应的路径
            # 初始版本我们先实现重启，后续优化
            container.restart()
        return {"status": "success", "message": f"Action {action} performed on {name}"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=44, detail="Container not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/system/update")
async def system_update():
    try:
        # 运行 shell 脚本
        result = subprocess.run(["sh", "/app/scripts/update.sh"], capture_output=True, text=True)
        return {"status": "success", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/system/shutdown-all")
async def shutdown_all():
    try:
        # 在容器内调用宿主机的 docker compose stop
        # 因为我们挂载了 docker socket 且安装了 docker cli，这是可行的
        # 但要注意我们在容器里，路径可能需要调整，或者直接操作 docker client
        
        # 方案A：使用 docker sdk 停止所有容器
        containers = client.containers.list()
        for container in containers:
            container.stop()
            
        return {"status": "success", "message": "All containers stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
