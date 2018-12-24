import os
import xml.dom.minidom

INPUT_XML_FILE_PATH = "input/netease_blog_photo.xml"
JSON_FILE_PATH = "output/result.json"
POST_FILE_PATH = "_posts"


def parse_xml(inputFile):
    domtree = xml.dom.minidom.parse(inputFile)
    root = domtree.documentElement
    photos = root.getElementsByTagName("photo")

    for p in photos:
        yield p.firstChild.data


def download_photos(photos: list):
    import requests
    import requests.exceptions

    # 必须加header，否则人人等网站会返回403而不是200图片
    headers = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      + '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }

    result = list()

    index = 0

    for url in photos:
        try:
            r = requests.get(url, allow_redirects=False, headers=headers)
        except Exception as e:
            result.append({
                'url': url,
                'exception': e.__cause__,
                'succeed': False
            })
            continue

        if r.status_code == 200:
            file_format = r.headers['Content-Type']  # eg: "image/jpeg"
            file_format = file_format.split("/")[-1]

            file_format2 = url.split(".")[-1]

            index += 1
            index_str = '%03d' % index  # 大概400张图，所以文件名3位数，不足一百前面补0

            file_name = "netease-{index}.{file_format}".format(index=index_str, file_format=file_format2)
            file_path = "output/{filename}".format(filename=file_name)

            with open(file_path, 'wb') as f:
                f.write(r.content)
                f.close()

            result.append({
                'url': url,
                'file_name': file_name,
                'file_format': file_format,
                'file_format2': file_format2,
                'status_code': 200,
                'succeed': True
            })
            print("Succeed {url} ".format(url=url))
        else:
            status_code = r.status_code
            result.append({
                'url': url,
                'status_code': status_code,
                'succeed': False
            })
            print("Error {status_code} {url}".format(url=url, status_code=status_code))

        # if index == 20:
        #     break
    return result


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


def replace_image_url_in_posts(result):
    # prepare valid urls

    valid_urls = []
    for i in result:
        if i['succeed'] == True:
            valid_urls.append({
                'old_url': i['url'],
                'new_url': "/images/{file_name}".format(file_name=i['file_name'])
                # my image folder is like: /images/1-head-trail.png
            })

    files = os.listdir(POST_FILE_PATH)
    for file_name in files:
        file_path = "{folder}/{filename}".format(folder=POST_FILE_PATH, filename=file_name)

        # read file
        input_lines = []
        output_lines = []
        try:
            with open(file_path) as read_file:
                input_lines = read_file.readlines()
        except Exception:
            print("File read error: {file_path}".format(file_path=file_path))

        # replace urls

        for line in input_lines:
            for u in valid_urls:
                line = line.replace(u['old_url'], u['new_url'])
            output_lines.append(line)

        # write file
        with open(file_path, "w") as write_file:
            write_file.writelines([line for line in output_lines])


def main():
    # 以下两步可以分开做，进度会保存到json文件中

    # step1: parse photo xml
    photos = list(parse_xml(INPUT_XML_FILE_PATH))
    result = download_photos(photos)
    save_result(result, JSON_FILE_PATH)

    # step2: replace posts

    result = read_result(JSON_FILE_PATH)
    replace_image_url_in_posts(result)


if __name__ == "__main__":
    main()
