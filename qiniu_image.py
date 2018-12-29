import os

# 七牛管理控制台 https://portal.qiniu.com/bucket/lmm333/index
# 工具下载地址 https://developer.qiniu.com/kodo/tools/1300/qrsctl

User = "a@b.c"
Passwd = "abc"
Bucket = "lmm333"
FileNamePrefix = "qiniu"

JSON_FILE_PATH = "output/qiniu.json"
JSON_FILE_PATH2 = "output/qiniu2.json"
POST_FILE_PATH = "../slices/southeastasia/"

WIDTH = 600


def get_file_list(str, start, end):
    for index in range(start, end + 1):
        index_str = '%02d' % index
        yield str.format(index_str=index_str)


# 应人而异，返回文件名列表
def prepare_filenames():
    filenames = []

    filenames.extend(list(get_file_list("trail/151205hangzhou/{index_str}.JPG", 0, 25)))
    filenames.extend(list(get_file_list("travel/091005nanping/{index_str}.jpg", 1, 40)))

    filenames.extend(list(get_file_list("travel/180719slices/Brunei{index_str}.JPG", 0, 15)))
    filenames.extend(list(get_file_list("travel/180719slices/Cambodia{index_str}.JPG", 0, 15)))
    filenames.extend(list(get_file_list("travel/180719slices/Malaysia{index_str}.JPG", 0, 17)))
    filenames.extend(list(get_file_list("travel/180719slices/Myanmar{index_str}.JPG", 0, 29)))
    filenames.extend(list(get_file_list("travel/180719slices/Philippines{index_str}.JPG", 0, 5)))
    filenames.extend(list(get_file_list("travel/180719slices/Singarpore{index_str}.JPG", 0, 32)))
    filenames.extend(list(get_file_list("travel/180719slices/Thailand15-{index_str}.JPG", 0, 7)))
    filenames.extend(list(get_file_list("travel/180719slices/Thailand17-{index_str}.JPG", 0, 7)))
    filenames.extend(list(get_file_list("travel/180719slices/Vietnam{index_str}.JPG", 0, 7)))

    li_chenghu = ["travel/150419ChenghuLake/0-map1.PNG",
                  "travel/150419ChenghuLake/0-map2.PNG",
                  "travel/150419ChenghuLake/1-1SIP.JPG",
                  "travel/150419ChenghuLake/1-2road.JPG",
                  "travel/150419ChenghuLake/1-3road.JPG",
                  "travel/150419ChenghuLake/2-1village.JPG",
                  "travel/150419ChenghuLake/2-2village.JPG",
                  "travel/150419ChenghuLake/2-3duck.JPG",
                  "travel/150419ChenghuLake/2-4flower.JPG",
                  "travel/150419ChenghuLake/2-5road.JPG",
                  "travel/150419ChenghuLake/2-6village.JPG",
                  "travel/150419ChenghuLake/2-7boat.JPG",
                  "travel/150419ChenghuLake/2-8boat.JPG",
                  "travel/150419ChenghuLake/2-91road.JPG",
                  "travel/150419ChenghuLake/2-9boat.JPG",
                  "travel/150419ChenghuLake/3-01countryRoad.JPG",
                  "travel/150419ChenghuLake/3-02rise.JPG",
                  "travel/150419ChenghuLake/3-03rise.JPG",
                  "travel/150419ChenghuLake/3-04farmYard.JPG",
                  "travel/150419ChenghuLake/3-05purpleFlower.JPG",
                  "travel/150419ChenghuLake/3-06purpleFlower.JPG",
                  "travel/150419ChenghuLake/3-07chengLake.JPG",
                  "travel/150419ChenghuLake/3-08fishing.jpg",
                  "travel/150419ChenghuLake/3-09lmm.JPG",
                  "travel/150419ChenghuLake/3-09lmm2.jpg",
                  "travel/150419ChenghuLake/3-10lmm.JPG",
                  "travel/150419ChenghuLake/3-11bike.jpg",
                  "travel/150419ChenghuLake/3-12bike.JPG",
                  "travel/150419ChenghuLake/3-13Highway.JPG",
                  "travel/150419ChenghuLake/3-14.JPG",
                  "travel/150419ChenghuLake/3-15.JPG",
                  "travel/150419ChenghuLake/3-16.JPG",
                  "travel/150419ChenghuLake/4-1wetland.jpg",
                  "travel/150419ChenghuLake/4-2road.JPG",
                  "travel/150419ChenghuLake/4-3village.jpg",
                  "travel/150419ChenghuLake/5-1road.jpg",
                  "travel/150419ChenghuLake/5-2chefang.JPG",
                  "travel/150419ChenghuLake/5-3wusongRiver.JPG",
                  "travel/150419ChenghuLake/5-4pintanSchool.JPG",
                  "travel/150419ChenghuLake/5-5road.JPG"]

    filenames.extend(li_chenghu)

    return filenames


# doc for qrsctl [link]( https://developer.qiniu.com/kodo/tools/1300/qrsctl )
def login():
    os.system("./qrsctl login {User} {Passwd}".format(User=User, Passwd=Passwd))


# qrsctl get <Bucket> <Key> <DestFile>
def download_item(Bucket, Key, DestFile):
    output = os.popen("./qrsctl get {Bucket} {Key} {DestFile}".format(Bucket=Bucket, Key=Key, DestFile=DestFile))
    return output.readlines()


def download_files(filenames):
    result = []

    for filename in filenames:
        output_file_name = "{Prefix}-{Filename}".format(Prefix=FileNamePrefix,
                                                        Filename=filename.replace("/", "-").lower())
        output_file_path = "output/{output_file_name}".format(output_file_name=output_file_name)

        r = download_item(Bucket, filename, output_file_path)

        result.append({
            'filename': filename,
            'output_file_name': output_file_name,
            'output_file_path': output_file_path,
            'result': r,
        })

    return result


def check_file_status(result):
    result2 = []
    for item in result:
        if os.path.exists(item['output_file_path']):
            item['result2'] = True
        else:
            item['result2'] = False
        result2.append(item)

    return result2


def save_result(result, filepath):
    import json
    j = json.dumps(result)

    with open(filepath, "w") as f:
        f.write(j)


def read_result(filepath):
    import json

    with open(filepath) as f:
        data = json.load(f)

    return data


# make sure small folder existed
def resize_images(result):
    from PIL import Image  # pip3 install Pillow

    result2 = []

    # files = os.listdir("output")

    for item in result:
        if os.path.exists(item['output_file_path']):
            filename = item['output_file_name']
        else:
            continue

        try:
            in_path = "output/{filename}".format(filename=filename)
            out_path = "output/small2/{filename}".format(filename=filename)
            with Image.open(in_path) as im:
                # lenght2/length = WIDTH/width
                length, width = im.size

                if width > WIDTH:
                    size_new = (int(length * WIDTH / width), WIDTH)
                else:
                    size_new = im.size

                print(in_path, im.format, "%d %d" % im.size, "%d %d" % size_new, im.mode)

                im.thumbnail(size_new, Image.ANTIALIAS)
                exif = im.info.get('exif', None)
                if exif:
                    im.save(out_path, exif=exif)
                else:
                    im.save(out_path)

                # out = im.resize((length2, WIDTH))
                # out.save(out_path)

                item['size_old'] = "%d x %d" % (length, width)  # im is replaced
                item['size_new'] = "%d x %d" % size_new
                item['mode'] = im.mode

                result2.append(item)
        except IOError:
            result2.append(item)

    return result2


def replace_image_url_in_posts(result, post_file_path):
    import re

    # prepare valid urls

    valid_urls = []
    for i in result:
        if i['result2'] == True:
            valid_urls.append({
                'old_file_name': i['filename'],  # "travel/180719slices/Brunei15.PNG",
                'new_file_name': i['output_file_name'],  # "qiniu-travel-180719slices-brunei15.png"
                'new_link': "/images/{filename}".format(filename=i['output_file_name'])
            })

    files = os.listdir(post_file_path)
    print(files)
    print(len(files))

    for file_name in files:
        file_path = "{folder}/{filename}".format(folder=post_file_path, filename=file_name)

        # read file
        input_lines = []
        output_lines = []
        try:
            with open(file_path) as read_file:
                input_lines = read_file.readlines()
        except Exception:
            print("File read error: {file_path}".format(file_path=file_path))

        # replace urls

        #  src="/images/netease-025.jpg"
        # ![越野](/images/1-head-trail.png)

        for line in input_lines:
            for u in valid_urls:
                if line.find(u['old_file_name']) >= 0:
                    print("line: " + line)
                    # 经过观察，发现所有链接都是md格式的 ![xx](xxx)，这就好办了，直接用正则提取信息，然后构造新链接
                    g = re.match(r'.*?!\[(.*?)\]\((.*?)\)', line)

                    if g:
                        print("res.group() : ", g.group())
                        print("res.group(1) : ", g.group(1))
                        print("res.group(2) : ", g.group(2))

                        # for replace line in jekyll
                        # line = "![{info}]({url})\n".format(info=g.group(1), url=u['new_link'])

                        # for replace line in markdown slices
                        line = line.replace(g.group(2), u['new_link'])
                        print("new line: " + line)
            output_lines.append(line)

        # write file
        with open(file_path, "w") as write_file:
            write_file.writelines([line for line in output_lines])


def main():
    login()

    # step1: download_item photo from qiniu
    names = prepare_filenames()
    result = download_files(names)
    save_result(result, JSON_FILE_PATH)

    # step2 检查文件是否成功下载
    result = read_result(JSON_FILE_PATH)
    result2 = check_file_status(result)
    save_result(result2, JSON_FILE_PATH)

    # step3 compress images 压缩图片
    result2 = read_result(JSON_FILE_PATH)
    result3 = resize_images(result2)
    save_result(result3, JSON_FILE_PATH2)

    # step4: replace image urls from posts
    result3 = read_result(JSON_FILE_PATH2)
    replace_image_url_in_posts(result3, POST_FILE_PATH)


if __name__ == "__main__":
    main()
