import os
from datetime import datetime

from starlette.responses import FileResponse

from files import file_api
from files.helper import check_safe_dir, get_files, json_msg
from utils.token_utils import get_token, users

root_directory = "c:/users"


@file_api.get("/")
def index():
    return "It works!"


@file_api.post("/list")
# async def get_files_with_token(directory_path: str, token: str = Depends(get_token)):
async def get_files_with_token(path: str):
    if check_safe_dir(root_directory, path):
        return get_files(path, None)
    else:
        return json_msg(403, "Not authorized")


@file_api.get("/download")
async def download_file(file_path: str):
    if not check_safe_dir(root_directory, file_path):
        return json_msg(403, "Not authorized")
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return json_msg(404, "File not found")
    # 返回文件下载
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))


@file_api.post("/get_token")
async def generate_token(user: str, password: str):
    # 检查用户和密码是否匹配
    if user not in users or users[user] != password:
        raise json_msg(-100, "user or password incorrect")

    # 获取当前时间戳
    timestamp = datetime.utcnow().timestamp()

    # 生成 token
    token = get_token(user, password, int(timestamp))
    return json_msg(0, "success", {"token": token})
