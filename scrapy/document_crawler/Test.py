import re

with open("tmp.txt", "r") as f:
    content = f.read()

a = content.replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "").replace("\\\"", "\"").replace("\\/", "/")

# pattent = re.compile("<h4\s+class=\"title_news_site\"><a\s+href=\"(https://e\.vnexpress\.net.+)\">.+</h4>")
#
# urls = pattent.findall(a)
#
# print(len(urls))
# print(urls)


print([1] + [2])