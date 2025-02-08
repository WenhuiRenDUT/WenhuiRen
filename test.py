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

def rename_files_in_photo(photo_dir):
    if not os.path.exists(photo_dir):
        print("指定的 Photo 目录不存在")
        return

    # 遍历所有子文件夹和文件
    for root, _, files in os.walk(photo_dir):
        path_parts = root.split(os.sep)
        print(path_parts)
        if len(path_parts) < 6:  # 确保目录至少包含 "Photo\A\22.23\子分类"
            continue

        if len(path_parts) == 6:
            parent_category = path_parts[-3]  # A, B, C, D
            category_number = path_parts[-2]  # 19.22, 22.23, 23.24, 24.25
            sub_category = path_parts[-1]  # 子分类（直接上级文件夹）

        if len(path_parts) == 7:
            parent_category = path_parts[-4]  # A, B, C, D
            category_number = path_parts[-3]  # 19.22, 22.23, 23.24, 24.25
            sub_category = path_parts[-2]  # 子分类（直接上级文件夹）
            sub_sub_category = path_parts[-1]

        # 用于保存已处理文件的名字，避免重复
        file_names_seen = {}

        for file in files:
            file_path = os.path.join(root, file)
            mod_time_str = get_file_capture_time(file_path)
            file_ext = os.path.splitext(file)[-1]
            file_ext = str(file_ext)
            file_ext = file_ext.lower()

            # 处理子子分类情况
            if len(path_parts) > 6:  # 存在子子分类
                new_name = f"{category_number}-{mod_time_str}-{parent_category}-{sub_category}_{sub_sub_category}{file_ext}"
            else:
                new_name = f"{category_number}-{mod_time_str}-{parent_category}-{sub_category}{file_ext}"

            # 处理重名文件，添加 (1), (2), ... 后缀
            base_name = os.path.splitext(new_name)[0]  # 去除扩展名，得到基础文件名
            if new_name in file_names_seen:
                file_names_seen[new_name] += 1
                new_name = f"{base_name}({file_names_seen[new_name]}){file_ext}"
            else:
                file_names_seen[new_name] = 0

            new_path = os.path.join(root, new_name)
            os.rename(file_path, new_path)
            print(f"重命名: {file_path} -> {new_path}")

# 指定 Photo 目录路径
photo_dir = r"D:\\Test"  # 你的 Photo 目录路径
rename_files_in_photo(photo_dir)

