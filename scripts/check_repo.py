#!/usr/bin/env python3
"""离线检查仓库：Markdown 本地链接、敏感文件/内容及大文件。

只读取 Git 已跟踪和未忽略的新文件，不执行仓库中的任何脚本。
默认根目录由本脚本位置决定，因此从任意当前目录运行均可。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import unescape
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

MIB = 1024 * 1024
WARNING_SIZE = 20 * MIB
ERROR_SIZE = 100 * MIB
TOKEN_RE = re.compile(
    rb"(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9]{36}|"
    rb"github_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59})(?![A-Za-z0-9_])"
)
PEM_RE = re.compile(
    rb"-----BEGIN (?P<kind>(?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY)-----"
    rb"[\r\n]+(?:Proc-Type: 4,ENCRYPTED\r?\n"
    rb"DEK-Info: [A-Z0-9-]+,[A-Fa-f0-9]+\r?\n\r?\n)?"
    rb"(?:[A-Za-z0-9+/=\r\n]|[ \t]){32,}?"
    rb"-----END (?P=kind)-----"
)
PRIVATE_NAMES = {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "identity"}


@dataclass(frozen=True)
class Issue:
    """一条不包含秘密值的检查结果。"""

    severity: str
    code: str
    path: str
    line: int
    message: str


def git_files(root: Path) -> list[Path]:
    """以 NUL 分隔读取 Git 文件清单，保留中文、空格和特殊文件名。"""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
         "--exclude-standard"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return [Path(name.decode("utf-8", "surrogateescape"))
            for name in sorted(set(result.stdout.split(b"\0"))) if name]


def _blank(text: str) -> str:
    """屏蔽非正文而保留换行及字符偏移。"""
    return "".join("\n" if char == "\n" else " " for char in text)


def markdown_prose(text: str) -> str:
    """排除围栏、缩进代码、HTML 注释及任意长度反引号行内代码。"""
    parts = []
    fence = None
    for line in text.splitlines(keepends=True):
        # 引用块中的代码围栏同样不属于正文。
        content = re.sub(r"^(?: {0,3}>[ \t]?)+", "", line)
        match = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", content.rstrip("\r\n"))
        if fence:
            parts.append(_blank(line))
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
        elif match and not (match[1][0] == "`" and "`" in match[2]):
            fence = match[1]
            parts.append(_blank(line))
        elif content.startswith("    ") or content.startswith("\t"):
            parts.append(_blank(line))
        else:
            parts.append(line)
    text = re.sub(r"<!--[\s\S]*?(?:-->|\Z)", lambda m: _blank(m[0]), "".join(parts))
    chars = list(text)
    index = 0
    while index < len(text):
        if text[index] != "`" or _escaped(text, index):
            index += 1
            continue
        end = index + 1
        while end < len(text) and text[end] == "`":
            end += 1
        delimiter = text[index:end]
        close = re.search(r"(?<!`)" + re.escape(delimiter) + r"(?!`)", text[end:])
        if close:
            stop = end + close.end()
            chars[index:stop] = _blank(text[index:stop])
            index = stop
        else:
            index = end
    return "".join(chars)


def _escaped(text: str, index: int) -> bool:
    """判断标点前连续反斜线是否为奇数。"""
    count = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        count += 1
        index -= 1
    return count % 2 == 1


def _bracket_end(text: str, start: int) -> int | None:
    """匹配允许嵌套与转义的链接文字方括号。"""
    depth = 1
    for index in range(start + 1, len(text)):
        if _escaped(text, index):
            continue
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index
    return None


def _destination(text: str, start: int) -> tuple[str, int] | None:
    """读取尖括号目标或括号平衡的裸目标，返回目标与结束偏移。"""
    if start >= len(text):
        return None
    if text[start] == "<":
        for index in range(start + 1, len(text)):
            if text[index] == "\n":
                return None
            if text[index] == ">" and not _escaped(text, index):
                return text[start + 1:index], index + 1
        return None
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if not _escaped(text, index):
            if char.isspace() or (char == ")" and depth == 0):
                break
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
        index += 1
    if depth:
        return None
    return text[start:index], index


def markdown_links(text: str):
    """提取行内链接、图片和引用定义，引用目标仅在定义处检查一次。"""
    prose = markdown_prose(text)
    definitions = []
    for match in re.finditer(r"(?m)^ {0,3}\[(?:\\.|[^\]\n])+\]:[ \t]*", prose):
        destination = _destination(prose, match.end())
        if destination:
            definitions.append((match.start(), destination[1]))
            yield prose.count("\n", 0, match.start()) + 1, destination[0]
    index = 0
    while index < len(prose):
        if prose[index] != "[" or _escaped(prose, index) or any(a <= index < b for a, b in definitions):
            index += 1
            continue
        end = _bracket_end(prose, index)
        if end is None or end + 1 >= len(prose) or prose[end + 1] != "(":
            index += 1
            continue
        start = end + 2
        while start < len(prose) and prose[start].isspace():
            start += 1
        destination = _destination(prose, start)
        if destination:
            target, stop = destination
            # 尾部只能是空白及可选标题；避免把普通括号文字误当链接。
            tail = re.match(r'''\s*(?:"[^"\n]*"|'[^'\n]*'|\([^\n)]*\))?\s*\)''', prose[stop:])
            if tail:
                yield prose.count("\n", 0, index) + 1, target
                index = stop + tail.end()
                continue
        index += 1


def local_target(root: Path, source: Path, target: str) -> Path | None:
    """解析本地路径，忽略外部协议、网络路径、空目标及片段。"""
    target = unescape(re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", target))
    if not target or target.startswith(("#", "//")):
        return None
    try:
        parsed = urlsplit(target)
    except ValueError:
        # 非法网络 URL 不属于本地存在性检查范围。
        return None
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    return root / path.lstrip("/") if path.startswith("/") else root / source.parent / path


def sensitive_filename(path: Path) -> bool:
    """识别环境凭据与常见私钥文件名，示例配置和 SSH 公钥除外。"""
    name = path.name.lower()
    if name in {".env.example", ".env.sample"}:
        return False
    return (name == ".env" or name.startswith(".env.") or name in PRIVATE_NAMES
            or path.suffix.lower() in {".key", ".p12", ".pfx"})


def content_secrets(path: Path):
    """分块扫描所有文件；重叠区捕获跨块 token 与常规 PEM，绝不返回值。

    跨块 PEM 支持至 64 KiB；超长私钥仍可由敏感文件名规则捕获。
    """
    overlap = b""
    found = set()
    with path.open("rb") as stream:
        while True:
            block = stream.read(MIB)
            if not block:
                break
            data = overlap + block
            for code, pattern in (("github-token", TOKEN_RE), ("private-key", PEM_RE)):
                match = pattern.search(data)
                if match and code not in found:
                    found.add(code)
                    yield code
            overlap = data[-65536:]


def check_repo(root: Path) -> tuple[int, list[Issue]]:
    """检查清单中的文件并返回文件数和按路径排序的结果，不写入仓库。"""
    root = root.resolve()
    files = git_files(root)
    issues = []
    for relative in files:
        path = root / relative
        name = relative.as_posix()
        if sensitive_filename(relative):
            issues.append(Issue("error", "sensitive-name", name, 0, "疑似敏感凭据或私钥文件名"))
        # 防止读取符号链接指向仓库外的个人文件；断链作为错误报告。
        if path.is_symlink():
            if not path.exists():
                issues.append(Issue("error", "missing-file", name, 0, "Git 清单中的符号链接已断开"))
            continue
        if not path.exists():
            issues.append(Issue("error", "missing-file", name, 0, "Git 清单中的文件不存在（可能尚未暂存删除）"))
            continue
        if not path.is_file():
            continue
        try:
            size = path.stat().st_size
            if size > WARNING_SIZE:
                severity = "error" if size > ERROR_SIZE else "warning"
                issues.append(Issue(severity, "large-file", name, 0, f"文件大小 {size / MIB:.2f} MiB，超过 {100 if severity == 'error' else 20} MiB"))
            for code in content_secrets(path):
                issues.append(Issue("error", code, name, 0, "检测到高置信凭据内容（已隐藏秘密值）"))
            if path.suffix.lower() in {".md", ".markdown"}:
                text = path.read_text(encoding="utf-8-sig")
                for line, target in markdown_links(text):
                    local = local_target(root, relative, target)
                    if local is not None and not local.exists():
                        issues.append(Issue("error", "broken-link", name, line, f"本地链接目标不存在：{target}"))
        except (OSError, UnicodeError, ValueError):
            issues.append(Issue("error", "read-error", name, 0, "无法读取文件或解析本地路径"))
    return len(files), issues


def safe_text(text: str) -> str:
    """在终端输出前再次隐藏 token，并转义换行与控制字符。"""
    text = TOKEN_RE.sub("[已隐藏凭据]".encode("utf-8"), text.encode("utf-8", "replace")).decode("utf-8")
    return "".join(char if char.isprintable() else repr(char)[1:-1] for char in text)


def main(argv: list[str] | None = None) -> int:
    """运行 CLI；仅 warning 时成功，有 error 或 Git 失败时返回 1。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="待检查的 Git 仓库根目录（默认脚本所属仓库）")
    args = parser.parse_args(argv)
    try:
        count, issues = check_repo(args.root)
    except (OSError, subprocess.CalledProcessError):
        print("ERROR [git-error] 无法读取 Git 文件清单，请检查仓库路径和 Git 安装。", file=sys.stderr)
        return 1
    for issue in issues:
        location = issue.path + (f":{issue.line}" if issue.line else "")
        print(safe_text(f"{issue.severity.upper()} [{issue.code}] {location}：{issue.message}"))
    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    print(f"检查 {count} 个文件：{errors} error，{warnings} warning。")
    return int(errors > 0)


if __name__ == "__main__":
    sys.exit(main())
