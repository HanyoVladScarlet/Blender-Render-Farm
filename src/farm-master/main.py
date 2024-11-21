from flask import Flask
import os

app = Flask(__name__, template_folder='views', static_folder='static')

from config import configure
from routes.client import client
from routes.file_entry import file_entry
from routes.index import index
from routes.workers import worker


app.register_blueprint(client, url_prefix='/api')
app.register_blueprint(file_entry)
app.register_blueprint(worker, url_prefix='/api')
app.register_blueprint(index)

# 使用Flask服务器作为中心节点master的主进程
def main():
    ''''''
    configure(app).run(debug=True, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    main() 