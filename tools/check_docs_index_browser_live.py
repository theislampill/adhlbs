#!/usr/bin/env python3
"""Live local browser smoke for docs/index.html using Chrome DevTools Protocol.

This avoids adding Playwright as a project dependency while still exercising
the generated single-file artifact in a real browser when Chrome/Chromium is
available locally or in CI.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from build_docs_index import DOCS_INDEX


ROOT = Path(__file__).resolve().parents[1]
CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    shutil.which("google-chrome") or "",
    shutil.which("google-chrome-stable") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("chrome") or "",
]


class CdpError(RuntimeError):
    pass


def find_chrome() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_json(url: str, timeout: float = 10.0) -> dict[str, object]:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic path
            last_error = exc
            time.sleep(0.15)
    raise CdpError(f"timed out waiting for {url}: {last_error}")


def read_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise CdpError("websocket connection closed")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


class WebSocket:
    def __init__(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "ws":
            raise CdpError(f"unsupported websocket scheme: {parsed.scheme}")
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 80
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        self.sock = socket.create_connection((host, port), timeout=8)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode("ascii"))
        response = b""
        while b"\r\n\r\n" not in response:
            response += self.sock.recv(4096)
        if b" 101 " not in response.split(b"\r\n", 1)[0]:
            raise CdpError(f"websocket upgrade failed: {response[:120]!r}")
        accept = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest())
        if accept not in response:
            raise CdpError("websocket accept header mismatch")

    def send_text(self, text: str) -> None:
        payload = text.encode("utf-8")
        header = bytearray([0x81])
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[idx % 4] for idx, byte in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def recv_text(self) -> str:
        while True:
            first, second = read_exact(self.sock, 2)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", read_exact(self.sock, 2))[0]
            elif length == 127:
                length = struct.unpack("!Q", read_exact(self.sock, 8))[0]
            mask = read_exact(self.sock, 4) if masked else b""
            payload = read_exact(self.sock, length)
            if masked:
                payload = bytes(byte ^ mask[idx % 4] for idx, byte in enumerate(payload))
            if opcode == 0x8:
                raise CdpError("websocket closed by browser")
            if opcode == 0x9:
                self.sock.sendall(b"\x8a\x00")
                continue
            if opcode in {0x1, 0x0}:
                return payload.decode("utf-8")

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass


class CdpClient:
    def __init__(self, websocket_url: str) -> None:
        self.ws = WebSocket(websocket_url)
        self.next_id = 1

    def call(self, method: str, params: dict[str, object] | None = None) -> dict[str, object]:
        cid = self.next_id
        self.next_id += 1
        self.ws.send_text(json.dumps({"id": cid, "method": method, "params": params or {}}, separators=(",", ":")))
        while True:
            message = json.loads(self.ws.recv_text())
            if message.get("id") != cid:
                continue
            if "error" in message:
                raise CdpError(f"{method} failed: {message['error']}")
            return message.get("result", {})

    def evaluate(self, expression: str) -> object:
        result = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "awaitPromise": True,
                "returnByValue": True,
                "timeout": 10000,
            },
        )
        if "exceptionDetails" in result:
            raise CdpError(f"Runtime.evaluate exception: {result['exceptionDetails']}")
        remote = result.get("result", {})
        if isinstance(remote, dict) and "value" in remote:
            return remote["value"]
        return remote

    def key(self, key: str, code: str, vk: int) -> None:
        payload = {"key": key, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
        self.call("Input.dispatchKeyEvent", {"type": "keyDown", **payload})
        self.call("Input.dispatchKeyEvent", {"type": "keyUp", **payload})

    def close(self) -> None:
        self.ws.close()


PAGE_SMOKE_JS = r"""
(async () => {
  const checks = [];
  const fail = msg => { throw new Error(msg); };
  const assert = (cond, msg) => { if (!cond) fail(msg); checks.push(msg); };
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
  const q = sel => document.querySelector(sel);
  const qa = sel => Array.from(document.querySelectorAll(sel));
  const shown = el => {
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === 'none' || style.visibility === 'hidden') return false;
    }
    return true;
  };
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: { writeText: async text => { window.__lastCopied = String(text || ''); return true; } }
  });
  const dispatch = (el, type) => el.dispatchEvent(new Event(type, { bubbles: true }));
  await sleep(100);
  const cards = qa('article.card');
  const stacks = qa('#stacksTable tbody tr');
  const packs = qa('article.promptbox');
  const sources = qa('#sourcesTable tbody tr');
  const common = qa('[data-common-task-id]');
  assert(cards.length === 166, 'directive card count is 166');
  assert(stacks.length === 25, 'stack row count is 25');
  assert(packs.length === 20, 'prompt pack count is 20');
  assert(sources.length === 62, 'source row count is 62');
  assert(common.length === 5, 'common task count is 5');
  assert(!!q('meta[http-equiv="Content-Security-Policy"]'), 'CSP meta is present');
  assert(location.protocol === 'file:', 'local file protocol opens');
  const remote = performance.getEntriesByType('resource').filter(entry => /^https?:/.test(entry.name));
  assert(remote.length === 0, 'no active remote resources loaded');

  q('#search').value = 'Trust Boundary';
  dispatch(q('#search'), 'input');
  await sleep(30);
  let visibleCards = cards.filter(shown);
  assert(visibleCards.length > 0 && visibleCards.length < cards.length, 'search filters directive cards');
  assert(visibleCards.some(card => card.dataset.cardId === 'SEC-TRUST-BOUNDARY'), 'search surfaces trust-boundary card');
  assert(q('#resultSummary').textContent.includes('cards'), 'result summary updates after search');

  q('#search').value = '';
  dispatch(q('#search'), 'input');
  q('#kind').value = 'Security';
  dispatch(q('#kind'), 'change');
  await sleep(30);
  visibleCards = cards.filter(shown);
  assert(visibleCards.length > 0 && visibleCards.every(card => card.dataset.kind === 'Security'), 'category filter limits cards to Security');

  q('#resetBtn').click();
  await sleep(30);
  q('#stackTag').value = 'security';
  dispatch(q('#stackTag'), 'change');
  await sleep(30);
  let visibleStacks = stacks.filter(shown);
  assert(visibleStacks.length > 0 && visibleStacks.every(row => row.dataset.tag === 'security'), 'stack workstream filter limits rows');

  q('#resetBtn').click();
  await sleep(30);
  q('#sortRisk').click();
  await sleep(30);
  let ranks = qa('#stacksTable tbody tr').filter(shown).map(row => Number(row.dataset.riskRank || 0));
  assert(ranks.every((rank, idx) => idx === 0 || ranks[idx - 1] >= rank), 'stack risk sort is descending');
  q('#sortStackId').click();
  await sleep(30);
  let ids = qa('#stacksTable tbody tr').filter(shown).map(row => row.dataset.stackId || '');
  assert(ids.every((id, idx) => idx === 0 || ids[idx - 1].localeCompare(id) <= 0), 'stack ID sort is ascending');

  q('#toggleDensity').click();
  await sleep(20);
  assert(document.body.classList.contains('compact-mode'), 'compact mode toggles on');
  q('#toggleDensity').click();
  await sleep(20);
  assert(!document.body.classList.contains('compact-mode'), 'compact mode toggles off');

  q('#expandAll').click();
  await sleep(20);
  assert(qa('article.card details').some(detail => detail.open), 'card details expand');
  q('#collapseAll').click();
  await sleep(20);
  assert(qa('article.card details').every(detail => !detail.open), 'card details collapse');

  q('#packs details').open = true;
  q('#collapsePackDetails').click();
  await sleep(20);
  assert(qa('#packs details').every(detail => !detail.open), 'prompt pack details collapse');

  q('#copyAllPacks').click();
  await sleep(60);
  const allPackCopy = window.__lastCopied || '';
  assert(allPackCopy.includes('PACK-REPO-STRICT') && allPackCopy.includes('Codex agent variant'), 'copy all packs includes agent variants');
  q('#search').value = 'Security-Sensitive Agent Pack';
  dispatch(q('#search'), 'input');
  await sleep(30);
  q('#copyVisiblePacks').click();
  await sleep(60);
  assert((window.__lastCopied || '').includes('PACK-SEC-HIGH'), 'copy filtered packs follows search filter');
  assert((window.__lastCopied || '').length < allPackCopy.length, 'copy filtered packs is smaller than all packs');

  const firstSourceButton = q('#sourcesTable button[data-copy]');
  firstSourceButton.click();
  await sleep(60);
  assert(/^https?:\/\//.test(window.__lastCopied || ''), 'source URL copy uses inert data-copy text');

  window.__printed = false;
  window.print = () => { window.__printed = true; };
  q('#printBtn').click();
  await sleep(20);
  assert(window.__printed === true, 'print button invokes window.print');

  q('#search').value = 'escape check';
  q('#search').focus();
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  await sleep(20);
  assert(q('#search').value === '', 'Escape clears focused search');

  const positiveTabIndex = qa('[tabindex]').filter(el => Number(el.getAttribute('tabindex')) > 0);
  assert(positiveTabIndex.length === 0, 'no positive tabindex values');
  assert(!!q('.skip-link[href="#main"]') && !!q('main#main[tabindex="-1"]'), 'skip link and main target are present');
  assert(qa('details').every(detail => !!detail.querySelector('summary')), 'all details have summaries');
  return { ok: true, checks, resultSummary: q('#resultSummary').textContent };
})()
"""


def create_target(port: int, file_url: str) -> str:
    target_url = f"http://127.0.0.1:{port}/json/new?{quote(file_url, safe=':/%')}"
    request = Request(target_url, method="PUT")
    with urlopen(request, timeout=5) as response:
        payload = json.loads(response.read().decode("utf-8"))
    ws = payload.get("webSocketDebuggerUrl")
    if not isinstance(ws, str):
        raise CdpError(f"target websocket URL missing from {payload}")
    return ws


def keyboard_focus_smoke(cdp: CdpClient) -> dict[str, object]:
    cdp.evaluate("document.querySelector('#search').focus(); window.__focusTrace=[]; true")
    trace: list[str] = []
    for _ in range(14):
        cdp.key("Tab", "Tab", 9)
        active = cdp.evaluate(
            "(() => { const el = document.activeElement; "
            "return (el.id || el.getAttribute('aria-label') || el.textContent || el.tagName).trim().slice(0, 80); })()"
        )
        trace.append(str(active))
    unique = [item for idx, item in enumerate(trace) if item and item not in trace[:idx]]
    if len(unique) < 4:
        raise CdpError(f"keyboard focus did not move through enough controls: {trace}")
    cdp.evaluate("document.querySelector('#search').value='escape'; document.querySelector('#search').focus(); true")
    cdp.key("Escape", "Escape", 27)
    search_value = cdp.evaluate("document.querySelector('#search').value")
    if search_value:
        raise CdpError("Escape key did not clear focused search in live browser")
    return {"tab_steps": len(trace), "unique_focus_targets": len(unique)}


def run_live_smoke() -> tuple[str, dict[str, object]]:
    chrome = find_chrome()
    if not chrome:
        return "not-run", {"reason": "chrome-not-found"}
    port = free_port()
    with tempfile.TemporaryDirectory(prefix="adhlbs-chrome-") as tmpdir:
        args = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-extensions",
            "--allow-file-access-from-files",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={tmpdir}",
            "about:blank",
        ]
        flags = 0
        if os.name == "nt":
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
        try:
            wait_json(f"http://127.0.0.1:{port}/json/version")
            file_url = DOCS_INDEX.resolve().as_uri()
            ws_url = create_target(port, file_url)
            cdp = CdpClient(ws_url)
            try:
                cdp.call("Runtime.enable")
                for _ in range(60):
                    ready = cdp.evaluate("document.readyState")
                    if ready == "complete":
                        break
                    time.sleep(0.1)
                page_result = cdp.evaluate(PAGE_SMOKE_JS)
                focus_result = keyboard_focus_smoke(cdp)
                if not isinstance(page_result, dict) or not page_result.get("ok"):
                    raise CdpError(f"unexpected page smoke result: {page_result!r}")
                page_result.update(focus_result)
                page_result["chrome"] = chrome
                return "ok", page_result
            finally:
                cdp.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def main() -> int:
    try:
        status, payload = run_live_smoke()
    except Exception as exc:
        print("BROWSER_LIVE_CHECK_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    if status == "not-run":
        print(f"BROWSER_LIVE_NOT_RUN reason={payload['reason']} mode=not-run")
        return 0
    print(
        "BROWSER_LIVE_CHECK_OK "
        f"checks={len(payload.get('checks', []))} "
        f"tab_steps={payload.get('tab_steps')} "
        f"unique_focus_targets={payload.get('unique_focus_targets')} "
        "clipboard=checked keyboard=checked print=checked protocol=file mode=chrome-cdp-local"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
