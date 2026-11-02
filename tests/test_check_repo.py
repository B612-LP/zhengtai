"""仓库质量检查器的离线回归测试，所有样例均在临时 Git 仓库中构造。"""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_repo.py"
SPEC = importlib.util.spec_from_file_location("check_repo", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


class MarkdownTests(unittest.TestCase):
    """覆盖 Markdown 解析与路径解释，避免代码示例引发误报。"""

    def test_chinese_angles_encoded_fragment_directory_and_title(self):
        """中文、空格、URL 编码、标题、目录及片段能正确提取。"""
        text = '[中文](<资料/中文 文件.md#标题>) [编码](%E4%B8%AD%E6%96%87.md)\n![图](图片.png "说明") [目录](../资料/)'
        self.assertEqual(list(checker.markdown_links(text)), [
            (1, '资料/中文 文件.md#标题'), (1, '%E4%B8%AD%E6%96%87.md'),
            (2, '图片.png'), (2, '../资料/'),
        ])

    def test_skip_code_and_comments_keep_real_line_numbers(self):
        """反引号/波浪线围栏、缩进和跨行行内代码均应屏蔽。"""
        text = ('```md\n[假](不存在1)\n```\n~~~\n[假](不存在2)\n~~~\n'
                '    [假](不存在3)\n`[假](不存在4)` ``a ` [假](不存在5)``\n'
                '<!-- [假](不存在6) -->\n`跨行\n[假](不存在7)`\n[真](真.md)\n')
        self.assertEqual(list(checker.markdown_links(text)), [(12, '真.md')])

    def test_code_inside_blockquote(self):
        """引用块内的围栏和缩进代码不产生坏链。"""
        text = '> ```md\n> [假](missing.md)\n> ```\n>     [假](missing2.md)\n> [真](ok.md)'
        self.assertEqual(list(checker.markdown_links(text)), [(5, 'ok.md')])

    def test_unclosed_fence_and_different_closer(self):
        """较短围栏和不同字符不能结束已有代码块。"""
        self.assertEqual(list(checker.markdown_links('````\n```\n[假](a)\n~~~\n[假](b)')), [])

    def test_escaped_brackets_parentheses_and_nested_label(self):
        """转义链接不检查；目标允许转义和嵌套括号。"""
        text = r'\[假](fake.md) [真](a\(b\).md) [嵌套[文字]](目录(a)/b.md)'
        self.assertEqual(list(checker.markdown_links(text)), [(1, r'a\(b\).md'), (1, '目录(a)/b.md')])

    def test_reference_definition(self):
        """引用式/折叠式/快捷式目标在定义处只检查一次。"""
        text = '[链接][id]\n[id][] [id]\n[id]: <缺失 文件.md> "标题"\n'
        self.assertEqual(list(checker.markdown_links(text)), [(3, '缺失 文件.md')])

    def test_non_links_and_unmatched_inline_backtick(self):
        """普通括号、未闭合链接和单独反引号不应制造假目标。"""
        text = '[不是](普通 文字) [断开](abc\n普通文字 ` [真](ok.md)'
        self.assertEqual(list(checker.markdown_links(text)), [(2, 'ok.md')])

    def test_external_empty_anchor_and_protocol_relative(self):
        """不访问外网，任何协议及纯锚均跳过。"""
        for target in ('https://example.com/a', 'http://example.com', 'mailto:x@y',
                       'data:image/png;base64,abc', 'ftp://x', '//host/a', '#中文', '', '?q=x'):
            with self.subTest(target=target):
                self.assertIsNone(checker.local_target(Path('/仓库'), Path('文档/a.md'), target))

    def test_url_decoding_occurs_after_fragment_removal(self):
        """编码后的井号、问号属于文件名，不是链接片段/查询参数。"""
        root = Path('/仓库')
        source = Path('文档/a.md')
        self.assertEqual(checker.local_target(root, source, '../中文%20文件%23%3F.md#标题'), root / '文档/../中文 文件#?.md')
        self.assertEqual(checker.local_target(root, source, '/资源/a.md'), root / '资源/a.md')
        self.assertEqual(checker.local_target(root, source, r'a\(b\).md'), root / '文档/a(b).md')
        self.assertEqual(checker.local_target(root, source, 'a&amp;b.md'), root / '文档/a&b.md')


@unittest.skipUnless(shutil.which('git'), '需要本机 Git，但不需要网络')
class RepositoryTests(unittest.TestCase):
    """构造 Git 清单，验证 CLI、敏感信息和大文件阈值。"""

    def setUp(self):
        """为每个用例初始化隔离的临时仓库。"""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')

    def git(self, *args):
        """仅运行本机 Git 元数据命令，不提交、不连接网络。"""
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def write(self, name, text=''):
        """写入临时测试文件。"""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def issues(self):
        """执行完整检查并返回结果。"""
        return checker.check_repo(self.root)[1]

    def cli(self, root=None, cwd=None):
        """从指定目录启动 CLI。"""
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(root or self.root)],
                              cwd=cwd or self.root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_tracked_untracked_and_ignored_files(self):
        """已跟踪 ignored 文件仍检查，未跟踪 ignored 文件跳过。"""
        self.write('.gitignore', 'ignored/\n')
        self.write('已跟踪.md', '[坏](missing.md)')
        self.git('add', '已跟踪.md')
        self.write('新 文件.md', '[坏](new-missing.md)')
        self.write('ignored/跳过.md', '[坏](ignored-missing.md)')
        self.write('ignored/保留.md', '[坏](tracked-missing.md)')
        self.git('add', '-f', 'ignored/保留.md')
        links = [issue.path for issue in self.issues() if issue.code == 'broken-link']
        self.assertEqual(set(links), {'已跟踪.md', '新 文件.md', 'ignored/保留.md'})

    def test_existing_paths_and_precise_broken_link(self):
        """现有文件/目录、片段与中文合法链接通过；坏链带准确行号。"""
        self.write('资料/中文 文件.md')
        self.write('文档/首页.md', '[好](<../资料/中文 文件.md#不存在的锚>)\n'
                   '[目录](../资料/) [编码](../资料/%E4%B8%AD%E6%96%87%20%E6%96%87%E4%BB%B6.md)\n'
                   '[坏](../资料/丢失.md) [网络](https://example.invalid/x)')
        issues = self.issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual((issues[0].code, issues[0].path, issues[0].line), ('broken-link', '文档/首页.md', 3))

    def test_sensitive_names_and_allowed_examples(self):
        """示例配置、公钥、普通证书允许；环境凭据和私钥名禁止。"""
        bad = ['.env', '.env.local', '目录/.env.production', 'id_rsa', 'id_ed25519', '秘密.key', 'a.p12', 'a.pfx']
        good = ['.env.example', '.env.sample', 'id_rsa.pub', '证书.pem', '普通.txt']
        for name in bad + good:
            self.write(name)
        self.assertEqual({issue.path for issue in self.issues()}, set(bad))

    def test_github_token_formats_and_no_secret_output(self):
        """高置信经典和细粒度 token 均报错，输出不含 token 原文。"""
        tokens = [prefix + '_' + 'A' * 36 for prefix in ('ghp', 'gho', 'ghu', 'ghs', 'ghr')]
        tokens.append('github_' + 'pat_' + 'B' * 22 + '_' + 'C' * 59)
        for number, token in enumerate(tokens):
            self.write(f'token{number}.txt', 'secret=' + token)
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count('[github-token]'), len(tokens))
        for token in tokens:
            self.assertNotIn(token, result.stdout + result.stderr)

    def test_short_or_embedded_token_not_high_confidence(self):
        """短占位、被更长单词包裹的模式不视作完整 token。"""
        self.write('样例.txt', 'ghp_placeholder\n' + 'xghp_' + 'A' * 36 + '\n' + 'ghp_' + 'A' * 37)
        self.assertEqual(self.issues(), [])

    def test_pem_private_but_not_public_or_marker_only(self):
        """完整 PEM 私钥检测覆盖常见算法，公钥/单独说明标记不误报。"""
        for index, kind in enumerate(('PRIVATE KEY', 'RSA PRIVATE KEY', 'EC PRIVATE KEY', 'DSA PRIVATE KEY', 'OPENSSH PRIVATE KEY', 'ENCRYPTED PRIVATE KEY')):
            self.write(f'密钥{index}.txt', '-----BEGIN ' + kind + '-----\n' + 'A' * 64 + '\n-----END ' + kind + '-----')
        self.write('说明.txt', '-----BEGIN PRIVATE KEY-----\n说明文字\n-----BEGIN PUBLIC KEY-----\n' + 'A' * 64 + '\n-----END PUBLIC KEY-----')
        issues = self.issues()
        self.assertEqual(len(issues), 6)
        self.assertEqual({issue.code for issue in issues}, {'private-key'})

    def test_traditional_encrypted_pem_and_cross_chunk_pem(self):
        """旧式加密 RSA 头和跨块 PEM 也能识别。"""
        pem = ('-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\n'
               'DEK-Info: AES-256-CBC,' + 'A' * 32 + '\n\n' + 'B' * 64 +
               '\n-----END RSA PRIVATE KEY-----')
        self.write('加密.txt', pem)
        (self.root / '跨块.bin').write_bytes(b'\0' * (checker.MIB - 20) + pem.encode())
        self.assertEqual([issue.code for issue in self.issues()], ['private-key', 'private-key'])

    def test_binary_and_chunk_boundary_secret(self):
        """二进制文件同样检查，跨读取分块边界的 token 不丢失。"""
        token = ('ghp_' + 'A' * 36).encode()
        (self.root / 'binary.bin').write_bytes(b'\0' * (checker.MIB - 10) + token + b'\0')
        self.assertEqual([issue.code for issue in self.issues()], ['github-token'])

    def test_size_thresholds_and_warning_only_exit_zero(self):
        """使用小阈值验证严格大于比较及仅警告返回 0，避免分配大文件。"""
        for name, size in [('equal-warning.bin', 20), ('warning.bin', 21), ('equal-error.bin', 100), ('error.bin', 101)]:
            (self.root / name).write_bytes(b'\0' * size)
        with patch.object(checker, 'WARNING_SIZE', 20), patch.object(checker, 'ERROR_SIZE', 100):
            issues = self.issues()
        self.assertEqual({issue.path: issue.severity for issue in issues}, {
            'warning.bin': 'warning', 'equal-error.bin': 'warning', 'error.bin': 'error'})
        # 稀疏文件占用很少磁盘空间，但仍走 CLI 的真实 MiB 阈值。
        with (self.root / 'only-warning.bin').open('wb') as stream:
            stream.truncate(checker.WARNING_SIZE + 1)
        result = self.cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn('1 warning', result.stdout)

    def test_symlinks_not_followed_and_deleted_tracked_file(self):
        """不读取符号链接指向的私有文件，断链和未暂存删除明确报错。"""
        self.write('原文件.txt')
        self.git('add', '原文件.txt')
        (self.root / '原文件.txt').unlink()
        (self.root / '断链').symlink_to(self.root / '不存在')
        (self.root / '外部链接').symlink_to(SCRIPT)
        issues = self.issues()
        self.assertEqual({issue.path for issue in issues}, {'原文件.txt', '断链'})
        self.assertEqual({issue.code for issue in issues}, {'missing-file'})

    def test_cli_from_unrelated_temporary_directory(self):
        """当前目录不在仓库内时，显式根目录仍可正常工作。"""
        self.write('首页.md', '[好](首页.md#标题)')
        with tempfile.TemporaryDirectory() as other:
            result = self.cli(cwd=other)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('0 error', result.stdout)

    def test_default_root_is_script_location_not_cwd(self):
        """复制脚本到临时仓库验证默认根目录由脚本位置而非 cwd 决定。"""
        scripts = self.root / 'scripts'
        scripts.mkdir()
        copy = scripts / 'check_repo.py'
        shutil.copyfile(SCRIPT, copy)
        self.write('首页.md', '[坏](missing.md)')
        with tempfile.TemporaryDirectory() as other:
            result = subprocess.run([sys.executable, str(copy)], cwd=other, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('[broken-link] 首页.md:1', result.stdout)

    def test_non_git_root_failure(self):
        """非 Git 目录明确失败，不打印 Git 原始错误或秘密值。"""
        with tempfile.TemporaryDirectory() as other:
            result = self.cli(root=Path(other))
        self.assertEqual(result.returncode, 1)
        self.assertIn('[git-error]', result.stderr)

    def test_redaction_in_link_target(self):
        """即便秘密出现在坏链目标中，也必须在所有诊断中隐藏。"""
        token = 'ghp_' + 'A' * 36
        self.write('首页.md', '[坏](' + token + '.md)')
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(token, result.stdout)
        self.assertIn('[已隐藏凭据]', result.stdout)


if __name__ == '__main__':
    unittest.main()
