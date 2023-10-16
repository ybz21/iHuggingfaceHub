import os
from util import get_file_md5, generate_commit_id

from flask import Flask, request, make_response, send_file

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/health')
def health():
    return 'ok', 200


@app.route('/<path:repo_id>/resolve/<string:revision>/<path:filename>', methods=['GET', 'POST', 'HEAD'])
def resolve(repo_id, revision, filename):
    print(f"repo_id: {repo_id}, revision: {revision}, filename: {filename}")
    path = os.path.join(current_dir, 'files', repo_id, filename)
    if not os.path.exists(path):
        headers = {
            'Content-Type': 'text/plain; charset=utf-8',
            'X-Error-Code': 'EntryNotFound',
            'X-Error-Message': 'EntryNotFound',
        }
        return make_response('Entry not found', 404, headers)
    if request.method == 'HEAD':
        return head_file(repo_id, revision, filename)
    else:
        return get_file(repo_id, revision, filename)


def get_file(repo_id, revision, filename):
    path = os.path.join(current_dir, 'files', repo_id, filename)

    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range', None)

    if not range_header:
        # 不支持断点续传下载
        return send_file(path, as_attachment=True)

    # 支持断点续传下载
    byte_range = range_header.strip().split('=')[1]
    start, end = map(int, byte_range.split('-'))
    length = end - start + 1

    headers = {
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Content-Length': str(length),
        'Accept-Ranges': 'bytes',
    }

    return send_file(
        path,
        as_attachment=True,
        attachment_filename=filename,
        mimetype='application/octet-stream',
        add_etags=True, conditional=True,
        headers=headers,
        response_class=PartialFileResponse
    )


class PartialFileResponse:
    def __init__(self, *args, **kwargs):
        self.response = send_file(*args, **kwargs)

    def __call__(self, environ, start_response):
        range_header = environ.get('HTTP_RANGE', None)

        if range_header:
            start, end = self.get_range(range_header)
            self.response.headers.add('Content-Range', f'bytes {start}-{end}/{self.response.content_length}')
            self.response.status_code = 206

        return self.response(environ, start_response)

    def get_range(self, range_header):
        range_header = range_header.strip().split('=')[1]
        start, end = map(int, range_header.split('-'))
        if end == -1:
            end = self.response.content_length - 1
        return start, end


def head_file(repo_id, revision, filename):
    file_path = os.path.join(current_dir, 'files', repo_id, filename)
    # {
    #     'Content-Type': 'text/plain; charset=utf-8',
    #     'Content-Length': '910',
    #     'Connection': 'keep-alive',
    #     'Date': 'Fri, 13 Oct 2023 07:37:37 GMT',
    #     'X-Powered-By': 'huggingface-moon',
    #     'X-Request-Id': 'Root=1-6528f3c1-000c56961b74ede3096aac33',
    #     'Access-Control-Allow-Origin': 'https://huggingface.co',
    #     'Vary': 'Origin',
    #     'Access-Control-Expose-Headers': 'X-Repo-Commit,X-Request-Id,X-Error-Code,X-Error-Message,ETag,Link,Accept-Ranges,Content-Range',
    #     'X-Repo-Commit': 'c9bdb955021a80ae26fa6978891996dbe4951d8d',
    #     'Accept-Ranges': 'bytes',
    #     'Content-Security-Policy': 'default-src none; sandbox',
    #     'ETag': '"81b03286cdb93c249cd95cc61822083a7649a2d4"',
    #     'X-Cache': 'Miss from cloudfront',
    #     'Via': '1.1 729399d6290e74ddd43cb2da1cab5266.cloudfront.net (CloudFront)',
    #     'X-Amz-Cf-Pop': 'SIN2-P1',
    #     'X-Amz-Cf-Id': 'x1est6j39po_jU1V7TQh74R832g48nZiB4jYRX_HLyDIvRfETBChQg=='
    # }
    file_size = os.path.getsize(file_path)
    file_md5 = get_file_md5(file_path)
    headers = {
        'Content-Length': file_size,
        # must match commit hash pattern. REGEX_COMMIT_HASH = re.compile(r"^[0-9a-f]{40}$")
        # todo: get commit id from repo git files
        'X-Repo-Commit': generate_commit_id(repo_id),
        'X-Linked-Etag': file_md5,
        'ETag': file_md5,
        'X-Linked-Size': file_size,
    }
    return make_response('', 200, headers)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
