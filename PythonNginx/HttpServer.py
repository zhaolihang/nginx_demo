import requests # 如果没有requests,使用命令 'pip install requests' 安装
from wsgiref.simple_server import make_server# 从wsgiref模块导入

# 1. 配置规则
# 2. 接受客户端请求
# 3. 解析规则查找真正请求
# 4. 访问真正请求
# 5. 将结果传回客户端


path_rules = {} # 1. 配置规则
path_rules['/baidu'] = "https://www.baidu.com"
path_rules['/tm'] = "https://www.tmall.com/"


def parseRule(environ):
    # http://localhost:8000/baidu
    # path_info = /baidu
    path_info = environ['PATH_INFO']
    if path_info:
        if path_info in path_rules:
            url = path_rules[path_info]
            return url


def application(environ, start_response):# 2. 接受客户端请求
    # print(environ['REQUEST_METHOD'])
    # print(environ['HTTP_HOST'])
    # print(environ['PATH_INFO'])
    # print(environ['QUERY_STRING'])

    url = parseRule(environ)# 3. 解析规则查找真正请求

    if url:
        res = requests.get(url)# 4. 访问真正请求
        res.encoding = "utf-8"
        bs = bytes(res.text, 'utf-8')
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [bs] # 5. 将结果传回客户端
    else:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<h1>Hello, web!</h1>'] # 5. 没有匹配项 返回默认结果


httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
httpd.serve_forever()