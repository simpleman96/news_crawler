import re


def check_content(in_string):
    regex = re.compile('[0-9a-zàáảãạăắằẵặẳâầấậẫẩđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ .,!;]+')
    if regex.sub('', in_string) < 30:
        return True
    else:
        return False
