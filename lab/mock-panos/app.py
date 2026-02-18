#!/usr/bin/env python3
from __future__ import annotations

import io
import tarfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

MOCK_USER = "admin"
MOCK_PASSWORD = "admin"
MOCK_KEY = "mock-api-key"


class MockPanosHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/healthz":
            self._respond_text(200, "ok")
            return

        if parsed.path != "/api/":
            self._respond_xml(404, _xml_error("not found"))
            return

        args = parse_qs(parsed.query)
        req_type = _first(args, "type")

        if req_type == "keygen":
            self._handle_keygen(args)
            return

        if req_type == "export":
            self._handle_export(args)
            return

        self._respond_xml(400, _xml_error("unsupported request type"))

    def _handle_keygen(self, args: dict[str, list[str]]) -> None:
        user = _first(args, "user")
        password = _first(args, "password")

        if user != MOCK_USER or password != MOCK_PASSWORD:
            self._respond_xml(403, _xml_error("invalid credentials"))
            return

        body = (
            "<response status=\"success\">"
            f"<result><key>{MOCK_KEY}</key></result>"
            "</response>"
        )
        self._respond_xml(200, body)

    def _handle_export(self, args: dict[str, list[str]]) -> None:
        key = _first(args, "key")
        category = _first(args, "category")

        if key != MOCK_KEY:
            self._respond_xml(403, _xml_error("invalid API key"))
            return

        if category == "configuration":
            xml_body = (
                "<config>"
                f"<generated>{datetime.now(timezone.utc).isoformat()}</generated>"
                "<device><hostname>mock-fw01</hostname></device>"
                "</config>"
            ).encode("utf-8")
            self._respond_binary(
                200,
                xml_body,
                "application/xml",
                'attachment; filename="running-config.xml"',
            )
            return

        if category == "device-state":
            tar_bytes = _build_mock_device_state_tar()
            self._respond_binary(
                200,
                tar_bytes,
                "application/gzip",
                'attachment; filename="device-state.tgz"',
            )
            return

        self._respond_xml(400, _xml_error("unsupported export category"))

    def _respond_text(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _respond_xml(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/xml")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _respond_binary(
        self,
        status: int,
        payload: bytes,
        content_type: str,
        content_disposition: str,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition", content_disposition)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


def _first(args: dict[str, list[str]], key: str) -> str | None:
    values = args.get(key, [])
    return values[0] if values else None


def _build_mock_device_state_tar() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        payload = (
            "mock device-state archive\n"
            f"generated={datetime.now(timezone.utc).isoformat()}\n"
        ).encode("utf-8")

        tarinfo = tarfile.TarInfo(name="state.txt")
        tarinfo.size = len(payload)
        tar.addfile(tarinfo, io.BytesIO(payload))

    return buf.getvalue()


def _xml_error(message: str) -> str:
    return (
        "<response status=\"error\">"
        f"<msg><line>{message}</line></msg>"
        "</response>"
    )


def run() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8080), MockPanosHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
