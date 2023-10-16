import hashlib


def get_file_md5(file_path):
    with open(file_path, 'rb') as fp:
        data = fp.read()
        file_md5 = hashlib.md5(data).hexdigest()
        return file_md5


def generate_commit_id(content):
    sha1 = hashlib.sha1()
    sha1.update(content.encode())
    commit_id = sha1.hexdigest()
    return commit_id
