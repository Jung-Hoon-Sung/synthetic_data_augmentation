import os, datetime, exifread, shutil
import exiftool
import sqlite3
import json

from site import venv
from pickle import FALSE

from PIL import Image
from PIL.ExifTags import TAGS

## 정리할 사진, 동영상 디렉토리
dir_path = "/volume1/photo"

# 정리된 파일을 모을 디렉토리
go_path = "/volume2/backup_photo/Test"

target_date = ''


# exifread 사용 함수
def get_exif_info(file_path):
    print(file_path)
    tags = {}
    format_str1 = '%Y:%m:%d %H:%M:%S'
    format_str2 = '%d/%m/%Y %H:%M'
    exif_date_str = ''
    create_date = ''

    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)

        if len(tags) > 0:

            for tag in tags.keys():
                if tag in ('Image DateTime'):
                    # print("Key: %s, value %s" % (tag, tags[tag]))
                    exif_date_str = str(tags[tag])

            if (exif_date_str == ''):
                for tag in tags.keys():
                    print("Key: %s, value %s" % (tag, tags[tag]))
            else:
                try:
                    exix_date = datetime.datetime.strptime(exif_date_str, format_str1)
                    create_date = exix_date.strftime('%Y-%m-%d')
                except ValueError as ve:
                    exix_date = datetime.datetime.strptime(exif_date_str, format_str2)
                    create_date = exix_date.strftime('%Y-%m-%d')
                else:
                    create_date = ""

    return create_date


# exiftool 사용 함수
def get_exif_info2(file_path):
    # print("FILE LOCATION : " + file_path)
    create_date = ""
    metadata = {}
    format_str1 = '%Y:%m:%d %H:%M:%S'
    format_str2 = '%d/%m/%Y %H:%M'
    exif_date_str = ""
    file_date_str = ""

    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(file_path)

        # print(metadata)
        # print(len(metadata))

        if len(metadata) > 0:

            for tag in metadata.keys():
                # print("Key: %s, value %s" % (tag, metadata[tag]))
                if tag in ('EXIF:DateTimeOriginal'):  # 사진 촬영할 일자
                    # print("Key: %s, value %s" % (tag, metadata[tag]))
                    exif_date_str = str(metadata[tag])
                if tag in ('QuickTime:CreateDate'):  # 동영상 촬영 일자
                    # print("Key: %s, value %s" % (tag, metadata[tag]))
                    exif_date_str = str(metadata[tag])
                if tag in ('File:FileModifyDate'):  # 카톡 등으로 받은 사진들
                    # print("Key: %s, value %s" % (tag, metadata[tag]))
                    file_date_str = str(metadata[tag])

            if (exif_date_str == '') and (file_date_str == ''):
                for tag in metadata.keys():
                    print("Key: %s, value %s" % (tag, metadata[tag]))
            else:
                # print("exif_date_str" + exif_date_str)
                # print("exif_date_str" + exif_date_str)
                if ((exif_date_str == '') or (exif_date_str == '0000:00:00 00:00:00')) and (file_date_str != ''):
                    exif_date_str = file_date_str[0:19]
                    # print("exif_date_str : " + exif_date_str)

                try:
                    exix_date = datetime.datetime.strptime(exif_date_str, format_str1)
                    create_date = exix_date.strftime('%Y-%m-%d')
                    # print(create_date)
                except ValueError as ve:
                    exix_date = datetime.datetime.strptime(exif_date_str, format_str2)
                    create_date = exix_date.strftime('%Y-%m-%d')
                    # print(create_date)
                # else:
                # create_date = ""

    return create_date


conn = sqlite3.connect("all_photos.db", isolation_level=None)

c = conn.cursor()

# 디렉토리 구조 돌면서 처리
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)
    # print(d_path)

    for file in files:
        file_path = os.path.join(root, file)
        # print(file_path)

        if "@eaDir" not in file_path:
            file_dir, file_name = os.path.split(file_path)
            file_dir, file_ext = os.path.splitext(file_path)

            print("FILE LOCATION : " + file_path)

            param1 = (file_path,)
            c.execute(
                "SELECT idx, file_loc, file_name, copy_yn, copy_loc, reg_date, mod_date FROM photo WHERE file_loc = ?",
                param1)
            data1 = c.fetchone()

            copy_yn = 'N'

            # print(data1)
            if (data1 == None):
                now = datetime.datetime.now()
                nowStr = now.strftime('%Y-%m-%d %H:%M:%S')

                param2 = (file_path, file_name, 'N', '', nowStr, nowStr)
                c.execute(
                    "INSERT INTO photo (file_loc, file_name, copy_yn, copy_loc, reg_date, mod_date) VALUES (?, ?, ?, ?, ?, ?)",
                    param2)
                copy_yn = 'N'

            elif (data1[3] == 'Y'):
                now = datetime.datetime.now()
                nowStr = now.strftime('%Y-%m-%d %H:%M:%S')
                param3 = (nowStr, file_path,)
                c.execute("UPDATE photo SET mod_date = ? WHERE file_loc = ?", param3)

                copy_yn = 'Y'
                print(file_path + " Already Done!")
            elif (data1[3] == 'N'):
                copy_yn = 'N'

            # 파일 복사 대상이면 처리
            if (copy_yn == 'N'):
                # 정리할 파일 확장자 정의
                if (file_ext.upper() in (".JPG", ".PNG", ".NEF", ".HEIC", ".MOV", ".MP4", ".DNG")):
                    target_date = ''
                    # target_date = get_exif_info(file_path)
                    target_date = get_exif_info2(file_path)

                    # print("CREATE DATE : " + target_date)

                    if (len(target_date) == 10):
                        dest_path = go_path + "/" + target_date[0:4] + "/" + target_date + "/"
                        print(dest_path + " : " + str(len(target_date)))
                        if (os.path.isdir(dest_path) == False):
                            os.makedirs(dest_path)
                        shutil.copy2(file_path, dest_path + file_name)

                        now = datetime.datetime.now()
                        nowStr = now.strftime('%Y-%m-%d %H:%M:%S')
                        param4 = (dest_path + file_name, nowStr, file_path)
                        c.execute("UPDATE photo SET copy_yn = 'Y', copy_loc = ?, mod_date = ? WHERE file_loc = ?",
                                  param4)

conn.close
