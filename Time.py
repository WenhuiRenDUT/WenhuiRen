import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_file_capture_time(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()

        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':  # 拍摄时间
                    value = str(value)
                    value = value.replace(':', '.')
                    value = value.replace(' ', '.')
                    return value
            mod_time = os.path.getmtime(file_path)
            mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y.%m.%d.%H.%M.%S')
        return mod_time_str
    except Exception as e:
        mod_time = os.path.getmtime(file_path)
        mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y.%m.%d.%H.%M.%S')
        return mod_time_str

def rename_files_recursively(folder_path):
    # 确保路径存在
    if not os.path.exists(folder_path):
        print("指定的文件夹不存在")
        return

    # 遍历所有子文件夹和文件
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[-1]

            # 获取文件的修改时间
            mod_time_str = get_file_capture_time(file_path)

            # 生成新文件名
            new_name = f"{mod_time_str}{file_ext}"
            new_path = os.path.join(root, new_name)

            # 重命名文件
            os.rename(file_path, new_path)
            print(f"重命名: {file_path} -> {new_path}")

# 指定要操作的文件夹路径
folder = "D:\\2025.02.08\\video"
rename_files_recursively(folder)
