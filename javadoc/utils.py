import re


def is_summary(s):
    regex = r'^\w+_summary$'
    pattern = re.compile(regex)
    if pattern.match(s):
        return True
    else:
        return False


def is_new_page(new_url, current_url):
    regex = r'^%s#.*' % current_url
    pattern = re.compile(regex)
    if pattern.match(new_url):
        return False
    else:
        return True


def get_summary_type(header):
    # Todo : Use regex
    words = header.split()
    return " ".join(words[:len(words) - 1])


def get_class_type(text, cls_name):
    m = text.find(cls_name)
    assert m != -1
    return text[:m].rstrip().lstrip()
