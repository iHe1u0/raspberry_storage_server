import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse

app = FastAPI()


@app.get("/")
def index():
    return "It works!"


@app.get("/files/{directory_path:path}")
async def get_files(directory_path: str):
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        return {"error": "目录不存在"}

    # 获取目录下所有文件和文件夹
    files_and_folders = os.listdir(directory_path)

    # 检查每个文件/文件夹的类型并生成结果列表
    file_info = []
    for item in files_and_folders:
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            file_info.append({"name": item, "type": "file", "path": item_path})
        elif os.path.isdir(item_path):
            file_info.append({"name": item, "type": "folder"})
        else:
            file_info.append({"name": item, "type": "unknown"})

    return {"files": file_info}


@app.get("/download/")
async def download_file(file_path: str):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return {"error": "文件不存在"}

    # 返回文件下载
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11109)
