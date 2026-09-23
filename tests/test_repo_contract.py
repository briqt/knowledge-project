# 仓库确定性门禁。触发条件：提交前手动运行（见 CLAUDE.md §Agent 行为规则）。
# 依 SKILL §门禁的有效性：每项检查配证伪用例（*_negative），证明它抓得住该抓的东西。
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "SKILL.md"


# ---------- 可复用检查函数（度量单位写在各自 docstring） ----------

def machine_paths(text: str) -> list:
    """度量：换台机器即失效的机器路径字面量。SKILL §自包含的判据 的机械可判子集。"""
    return re.findall(r"(?:/home/\w+|/Users/\w+|[A-Za-z]:\\\\Users)", text)


def extract_seed_template(skill_text: str):
    """种子模板 = SKILL 中「种子模板」之后第一个 markdown 代码围栏。"""
    m = re.search(r"\*\*种子模板\*\*.*?```markdown\n(.*?)\n```", skill_text, re.S)
    return m.group(1) if m else None


def seed_backrefs(seed_text: str) -> list:
    """度量：种子模板中出现产品名（生成物反向依赖生成器的最直接形式）。"""
    return [w for w in ("knowledge-project",) if w in seed_text]


def yaml_blocks(text: str) -> list:
    return re.findall(r"```yaml\n(.*?)\n```", text, re.S)


TIMESTAMP_KEYS = {"at", "stale_after", "last_modified", "from", "to"}
OFFSET_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$")


def timestamp_values(block: str) -> list:
    """取 yaml 示例里所有时间字段的原文。用 BaseLoader：safe_load 会把时间转成对象，丢掉原文写法。"""
    lines = [l for l in block.splitlines() if l.strip() != "---"]
    found = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in TIMESTAMP_KEYS and isinstance(v, str):
                    found.append(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(yaml.load("\n".join(lines), Loader=yaml.BaseLoader))
    return found


def offsetless_timestamps(block: str) -> list:
    """度量：不是「ISO 8601 datetime + 显式时区偏移」的时间字段值（OKF v0.2 §5 前言）。"""
    return [v for v in timestamp_values(block) if not OFFSET_DATETIME.match(v)]


def frontmatter_of(text: str):
    if not text.startswith("---\n"):
        return None
    return yaml.safe_load(text.split("---", 2)[1])


# ---------- 对本仓的正向检查 ----------

class RepoContractTests(unittest.TestCase):
    def test_claude_agents_identical(self):
        self.assertEqual(
            (ROOT / "CLAUDE.md").read_bytes(),
            (ROOT / "AGENTS.md").read_bytes(),
            "CLAUDE.md 与 AGENTS.md 必须逐字一致",
        )

    def test_skill_frontmatter_parses(self):
        fm = frontmatter_of(SKILL.read_text(encoding="utf-8"))
        self.assertIsInstance(fm, dict)
        self.assertEqual(fm.get("name"), "knowledge-project")
        self.assertTrue(str(fm.get("description", "")).strip())

    def test_skill_yaml_examples_parse(self):
        blocks = yaml_blocks(SKILL.read_text(encoding="utf-8"))
        self.assertTrue(blocks, "SKILL.md 应至少含一个 yaml 示例")
        for i, block in enumerate(blocks):
            with self.subTest(block=i):
                # frontmatter 形态的示例：去掉 --- 定界行后应可解析为映射
                lines = [l for l in block.splitlines() if l.strip() != "---"]
                self.assertIsInstance(yaml.safe_load("\n".join(lines)), dict)

    def test_skill_yaml_timestamps_have_offset(self):
        blocks = yaml_blocks(SKILL.read_text(encoding="utf-8"))
        # 触发面不能为空：示例里一个时间字段都没有时，这道检查跑出来也是绿的
        self.assertTrue(any(timestamp_values(b) for b in blocks), "yaml 示例中应至少有一个时间字段")
        for i, block in enumerate(blocks):
            with self.subTest(block=i):
                self.assertEqual(offsetless_timestamps(block), [])

    def test_seed_template_exists_and_has_no_backref(self):
        seed = extract_seed_template(SKILL.read_text(encoding="utf-8"))
        self.assertIsNotNone(seed, "SKILL.md 应包含种子模板围栏")
        self.assertEqual(seed_backrefs(seed), [], "种子模板不得回引本 skill 名字")

    def test_no_machine_paths_in_repo_docs(self):
        for f in list(ROOT.glob("*.md")) + list((ROOT / "skills").glob("*.md")):
            with self.subTest(file=f.name):
                self.assertEqual(machine_paths(f.read_text(encoding="utf-8")), [])


# ---------- 证伪用例：构造应失败的输入，确认检查器真的会叫 ----------

class GateFalsificationTests(unittest.TestCase):
    def test_machine_path_detector_negative(self):
        self.assertTrue(machine_paths("材料在 /home/alice/downloads/x.csv"))
        self.assertTrue(machine_paths("见 /Users/bob/tmp/a.md"))

    def test_seed_backref_detector_negative(self):
        bad_seed = "## Agent 行为规则\n完整方法论见 knowledge-project skill。"
        self.assertTrue(seed_backrefs(bad_seed))

    def test_timestamp_offset_detector_negative(self):
        bad = "stale_after: 2026-12-31\ngenerated:\n  at: 2026-08-13T10:00:00\nverified:\n  - { by: human:a, at: 2026-08-13 }"
        self.assertEqual(len(offsetless_timestamps(bad)), 3)
        self.assertEqual(offsetless_timestamps("stale_after: 2026-12-31T00:00:00+08:00\nat: 2026-06-30T14:00:00Z"), [])

    def test_frontmatter_detector_negative(self):
        self.assertIsNone(frontmatter_of("# 没有 frontmatter 的文件\n"))

    def test_yaml_detector_negative(self):
        with self.assertRaises(yaml.YAMLError):
            yaml.safe_load("a: [未闭合")


if __name__ == "__main__":
    unittest.main()
