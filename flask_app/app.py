from time import sleep
import prometheus_client
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import threading

app = Flask(__name__)

registry = prometheus_client.CollectorRegistry()

OFIR_COUNTER = prometheus_client.Counter('ofir_metric', 'A description for ofir metric',['label1','label2'], registry=registry)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def run():
    while True:
        sleep(15)
        OFIR_COUNTER.labels(label1="value1", label2="value1").inc()
        OFIR_COUNTER.labels(label1="value1", label2="value2").inc()

t = threading.Thread(target=run)
t.start()

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app(registry)
})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)