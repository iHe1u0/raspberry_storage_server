import mimetypes
import os
# from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse


# from utils.token_utils import tokens


def get_files(directory_path: str, token: Optional[str] = None):
    # # 检查是否提供了 token
    # if not token:
    #     return {"error": "未提供访问权限"}
    # # 检查 token 是否有效
    # if token not in tokens or datetime.utcnow() > tokens[token]:
    #     raise HTTPException(status_code=401, detail="Token 已过期或无效")
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    # 获取目录下所有文件和文件夹
    files_and_folders = os.listdir(directory_path)

    # 检查每个文件/文件夹的类型并生成结果列表
    file_info = []
    for item in files_and_folders:
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            file_type, _ = mimetypes.guess_type(item_path)
            file_size = os.path.getsize(item_path)
            modified_time = os.path.getmtime(item_path)
            file_info.append({
                "name": item,
                "type": file_type if file_type else 'Unknown',
                "path": item_path,
                "size": file_size,
                "modified_time": modified_time
            })
        elif os.path.isdir(item_path):
            modified_time = os.path.getmtime(item_path)
            file_info.append({
                "name": item,
                "type": "folder",
                "modified_time": modified_time,
                "path": item_path,
            })
        else:
            file_info.append({"name": item, "type": "Unknown"})
    return json_msg(0, "success", file_info)


def check_safe_dir(root_dir, path):
    # 将路径和根目录都转换为小写（或大写）来忽略大小写
    root_dir_lower = root_dir.lower()
    path_lower = path.lower()
    # 确保路径在指定的根目录下（忽略大小写）
    if path_lower.startswith("."):
        return False
    return True


def json_msg(code, msg, data=""):
    message = {"code": code, "message": msg, "data": data}
    return JSONResponse(message)


def get_directory_size(folder):
    total_size = 0
    for path, _, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size
