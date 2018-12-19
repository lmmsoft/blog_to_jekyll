# from xml.dom.minidom import parse
import xml.dom.minidom
import os
import datetime


def parse_xml(inputFile):
    domtree = xml.dom.minidom.parse(inputFile)
    root = domtree.documentElement
    blog_elements = root.getElementsByTagName("blog")
    blogs = []

    for blogItem in blog_elements:
        id = blogItem.getElementsByTagName("id")[0].childNodes[0].data.strip()
        userId = blogItem.getElementsByTagName("userId")[0].childNodes[0].data.strip()
        userName = blogItem.getElementsByTagName("userName")[0].childNodes[0].data.strip()
        userNickname = blogItem.getElementsByTagName("userNickname")[0].childNodes[0].data.strip()
        title = blogItem.getElementsByTagName("title")[0].childNodes[0].data.strip().strip()
        publishTime = blogItem.getElementsByTagName("publishTime")[0].childNodes[0].data.strip()
        ispublished = blogItem.getElementsByTagName("ispublished")[0].childNodes[0].data.strip()
        classId = blogItem.getElementsByTagName("classId")[0].childNodes[0].data.strip()
        className = blogItem.getElementsByTagName("className")[0].childNodes[0].data.strip()
        allowView = blogItem.getElementsByTagName("allowView")[0].childNodes[0].data.strip()
        content = blogItem.getElementsByTagName("content")[0].childNodes[0].data.strip()
        valid = blogItem.getElementsByTagName("valid")[0].childNodes[0].data.strip()
        moveForm = blogItem.getElementsByTagName("moveForm")[0].childNodes[0].data.strip()

        print("blog title {title}\tclassName {className}".format(title=title, className=className))

        title = parse_title(title).strip()
        date_string, file_name_date = parse_timestamp(publishTime)
        if moveForm is None or moveForm is '' or moveForm == 'NONE':
            moveForm = "blog.163.com"


        blog = {
            'title': title,
            'date': date_string,
            'layout': "post",
            'published': "true",
            'comments': "true",
            'permalink': "",  # todo
            'id': id,  # todo
            'category': className,
            'tags': "",  # 导出的xml没有tag
            'content': parse_content(content),

            'fileName': "{date}{title}.html".format(date=file_name_date, title=title),
            'moveForm': moveForm
        }
        blogs.append(blog)

    return blogs


def parse_title(input):
    # 有些标题里含义html的转义符号，类似于 &#60;草稿&#62;  需要转成正常的符号
    import html
    output = html.unescape(input)

    # 文件名里不能含有[]符号，否则jekyll引擎不能生成文章，转换成汉字的【】符号
    output = output.replace("[", "【")
    output = output.replace("]", "】")

    # 文件名里不能含有<>符号，否则jekyll引擎生成的首页链接有问题，转换成汉字的【】符号
    output = output.replace("<", "【")
    output = output.replace(">", "】")

    return output


def parse_content(input):
    # jekyll引擎不能处理 {{ 需要改成{ { ，因为 {{会被识别成代码的开始
    return input.replace("{{", "{ {")


# date: 2014-05-04T12:36:23+00:00
# YYYY-MM-DD HH:MM:SS +/-TTTT
def parse_timestamp(timestamp_string):
    timestamp_int = int(timestamp_string) / 1000  # convert from millisecond to second

    datetime_obj = datetime.datetime.utcfromtimestamp(timestamp_int)
    date_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S +0800")
    file_name_date = datetime_obj.strftime("%Y-%m-%d-")
    return date_string, file_name_date


def generate_files(blog_dict, folder_name):
    import os

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for title, blog in blog_dict.items():
        lines = []

        try:
            lines.append("---")
            lines.append("title: {title}".format(title=title))
            lines.append("date: {date}".format(date=blog['date']))
            lines.append("layout: {layout}".format(layout=blog['layout']))
            lines.append("published: {published}".format(published=blog['published']))
            lines.append("comments: {comments}".format(comments=blog['comments']))
            lines.append("category: {category}".format(category=blog['category']))
            lines.append("moveForm: {moveForm}".format(moveForm=blog['moveForm']))
            lines.append("---")
            lines.append(blog['content'])

            # 写入多行
            file_name = folder_name + "/" + validate_file_name(blog['fileName'])

            file = open(file_name, 'w')
            file.writelines([line + "\n" for line in lines])
            file.close()
        except:
            raise


def validate_file_name(title):
    import re
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def remove_duplicated_blogs(blog_list):
    blog_dict = {}
    for blog in blog_list:
        title = blog['title']
        if title in blog_dict:
            # 我的重复博客都是百度导入的
            # moveForm 为 baidu 或 baidu_qing
            # baidu_qing 的html相对更简洁，所以重复的用baidu_qing替代baidu的
            if blog['moveForm'] == "baidu_qing":
                blog_dict[title] = blog
        else:
            blog_dict[title] = blog

    return blog_dict


def main():
    blog_list = parse_xml("blog.xml")
    blog_dict = remove_duplicated_blogs(blog_list)
    generate_files(blog_dict, "output")


if __name__ == "__main__":
    main()
