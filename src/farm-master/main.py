from flask import Flask
import os

app = Flask(__name__, template_folder='views')

from controllers.client import client
from controllers.file_entry import file_entry
from controllers.index import index
from controllers.workers import worker


app.register_blueprint(client, url_prefix='/api')
app.register_blueprint(file_entry)
app.register_blueprint(worker, url_prefix='/api')
app.register_blueprint(index)


# 使用Flask服务器作为中心节点master的主进程
def main():
    ''''''
    # if os.path.abspath(os.curdir) == 
    # chdir()
    print('Server on!')
    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    main() 