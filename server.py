from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import webbrowser


ROOT = Path(__file__).resolve().parent
# 8000번은 INBODY가 사용하므로 충돌하지 않는 포트를 기본값으로 사용
PORT = int(os.environ.get("INBODY_PORT", "8078"))
URL = f"http://127.0.0.1:{PORT}/inbody-manager.html"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


class Server(ThreadingHTTPServer):
    # Windows에서 reuse_address가 켜져 있으면 같은 포트에 서버가 중복 실행되어
    # 요청이 엉뚱한 서버로 가는 문제가 생긴다 — 반드시 끈다
    allow_reuse_address = False


def main():
    try:
        server = Server(("127.0.0.1", PORT), Handler)
    except OSError:
        # 이미 실행 중인 서버가 있음 — 새로 띄우지 않고 브라우저만 연다
        print(f"Server already running. Opening {URL}")
        webbrowser.open(URL)
        return

    print(f"Serving {ROOT} at {URL}")
    webbrowser.open(URL)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
