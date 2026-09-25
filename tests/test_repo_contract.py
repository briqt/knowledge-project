# 仓库确定性门禁。触发条件：提交前手动运行（见 AGENTS.md §Agent 行为规则）。
# 依 skills/references/governance.md §门禁的有效性：每项检查配证伪用例（*_negative），证明它抓得住该抓的东西。
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills"
SKILL = SKILL_DIR / "SKILL.md"
REFERENCES = SKILL_DIR / "references"
SEED = REFERENCES / "seed.md"


def skill_docs() -> list:
    """产品本体的全部文件：SKILL.md（常驻层）+ references/（任务层）。"""
    return sorted(SKILL_DIR.rglob("*.md"))


# ---------- 可复用检查函数（度量单位写在各自 docstring） ----------

def machine_paths(text: str) -> list:
    """度量：换台机器即失效的机器路径字面量。structure.md §自包含的判据 的机械可判子集。"""
    return re.findall(r"(?:/home/\w+|/Users/\w+|[A-Za-z]:\\\\Users)", text)


def extract_seed_template(seed_text: str):
    """种子模板 = seed.md 中「种子模板」之后第一个 markdown 代码围栏。"""
    m = re.search(r"\*\*种子模板\*\*.*?```markdown\n(.*?)\n```", seed_text, re.S)
    return m.group(1) if m else None


def seed_backrefs(seed_text: str) -> list:
    """度量：种子模板中出现产品名（生成物反向依赖生成器的最直接形式）。"""
    return [w for w in ("knowledge-project",) if w in seed_text]


def seed_boundary_problems(seed_text: str) -> list:
    """度量：种子块的起止标记是否齐全（seed.md §演化一致性：升级只替换这两个标记之间的内容）。"""
    return [m for m in ("seed-version", "<!-- /seed -->") if m not in seed_text]


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


LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
SECTION = re.compile(r"(?<!OKF )§([^\s，。；、,)）」\]`*]+)")


def section_targets(text: str) -> list:
    """一个文件里能被 §X 指到的名字：标题文本 + 加粗段首（如 **关键约束——…**）。"""
    heads = [m.group(1).strip() for m in re.finditer(r"^#{1,6} (.+)$", text, re.M)]
    bolds = re.findall(r"\*\*([^*\n]+)", text)
    return heads + bolds


def broken_refs(path: Path, text: str = None) -> list:
    """度量：①相对 .md 链接指向不存在的文件；②§X 在目标文件（链接文本里的 § 指链接目标，
    裸 § 指本文件）中找不到以 X 开头的标题或加粗段首。
    盲区：前缀匹配——§X 只要是某标题的前缀就算命中，改名后仍残留同前缀标题时抓不到。
    `OKF §n` 指外部规范，不在检查范围。"""
    text = path.read_text(encoding="utf-8") if text is None else text
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # 代码块里的链接是示例，不是引用
    problems = []
    for label, href in LINK.findall(text):
        if re.match(r"^[a-z]+://", href) or href.startswith("#"):
            continue
        target = (path.parent / href.split("#")[0]).resolve()
        if not target.exists():
            problems.append(f"{path.name}: 链接 {href} 目标不存在")
            continue
        if target.suffix == ".md":
            names = section_targets(target.read_text(encoding="utf-8"))
            for sec in SECTION.findall(label):
                if not any(n.startswith(sec) for n in names):
                    problems.append(f"{path.name}: [{label}] 在 {href} 中找不到 §{sec}")
    own = section_targets(text)
    for sec in SECTION.findall(LINK.sub("", text)):
        if not any(n.startswith(sec) for n in own):
            problems.append(f"{path.name}: 本文件找不到 §{sec}")
    return problems


def unrouted_references(skill_text: str, reference_names: list) -> list:
    """度量：references/ 下没有被 SKILL.md 链接到的文件（零人加载，governance.md §规则的分层加载）。"""
    linked = {Path(h.split("#")[0]).name for _, h in LINK.findall(skill_text) if h.startswith("references/")}
    return [n for n in reference_names if n not in linked]


# ---------- 对本仓的正向检查 ----------

class RepoContractTests(unittest.TestCase):
    def test_skill_frontmatter_parses(self):
        fm = frontmatter_of(SKILL.read_text(encoding="utf-8"))
        self.assertIsInstance(fm, dict)
        self.assertEqual(fm.get("name"), "knowledge-project")
        desc = str(fm.get("description", "")).strip()
        self.assertTrue(desc)
        self.assertLessEqual(len(desc), 1024, "description 超出 skill 规范的 1024 字符上限")

    def test_skill_yaml_examples_parse(self):
        blocks = [b for f in skill_docs() for b in yaml_blocks(f.read_text(encoding="utf-8"))]
        self.assertTrue(blocks, "产品文件中应至少含一个 yaml 示例")
        for i, block in enumerate(blocks):
            with self.subTest(block=i):
                # frontmatter 形态的示例：去掉 --- 定界行后应可解析为映射
                lines = [l for l in block.splitlines() if l.strip() != "---"]
                self.assertIsInstance(yaml.safe_load("\n".join(lines)), dict)

    def test_skill_yaml_timestamps_have_offset(self):
        blocks = [b for f in skill_docs() for b in yaml_blocks(f.read_text(encoding="utf-8"))]
        # 触发面不能为空：示例里一个时间字段都没有时，这道检查跑出来也是绿的
        self.assertTrue(any(timestamp_values(b) for b in blocks), "yaml 示例中应至少有一个时间字段")
        for i, block in enumerate(blocks):
            with self.subTest(block=i):
                self.assertEqual(offsetless_timestamps(block), [])

    def test_seed_template_exists_and_has_no_backref(self):
        seed = extract_seed_template(SEED.read_text(encoding="utf-8"))
        self.assertIsNotNone(seed, "seed.md 应包含种子模板围栏")
        self.assertEqual(seed_backrefs(seed), [], "种子模板不得回引本 skill 名字")
        self.assertEqual(seed_boundary_problems(seed), [], "种子模板须带起止标记")

    def test_no_machine_paths_in_repo_docs(self):
        for f in list(ROOT.glob("*.md")) + skill_docs():
            with self.subTest(file=f.name):
                self.assertEqual(machine_paths(f.read_text(encoding="utf-8")), [])

    def test_cross_refs_resolve(self):
        # 触发面不能为空：产品文件里一条跨文件引用都没有时，这道检查跑出来也是绿的
        self.assertTrue(any(LINK.search(f.read_text(encoding="utf-8")) for f in skill_docs()))
        for f in skill_docs() + [ROOT / "README.md", ROOT / "AGENTS.md"]:
            with self.subTest(file=f.name):
                self.assertEqual(broken_refs(f), [])

    def test_every_reference_is_routed(self):
        names = sorted(p.name for p in REFERENCES.glob("*.md"))
        self.assertTrue(names, "references/ 不应为空")
        self.assertEqual(unrouted_references(SKILL.read_text(encoding="utf-8"), names), [])


# ---------- 证伪用例：构造应失败的输入，确认检查器真的会叫 ----------

class GateFalsificationTests(unittest.TestCase):
    def test_machine_path_detector_negative(self):
        self.assertTrue(machine_paths("材料在 /home/alice/downloads/x.csv"))
        self.assertTrue(machine_paths("见 /Users/bob/tmp/a.md"))

    def test_seed_backref_detector_negative(self):
        bad_seed = "## Agent 行为规则\n完整方法论见 knowledge-project skill。"
        self.assertTrue(seed_backrefs(bad_seed))

    def test_seed_boundary_detector_negative(self):
        self.assertEqual(seed_boundary_problems("<!-- seed-version: 2026-09-23 -->\n规则"), ["<!-- /seed -->"])

    def test_timestamp_offset_detector_negative(self):
        bad = "stale_after: 2026-12-31\ngenerated:\n  at: 2026-08-13T10:00:00\nverified:\n  - { by: human:a, at: 2026-08-13 }"
        self.assertEqual(len(offsetless_timestamps(bad)), 3)
        self.assertEqual(offsetless_timestamps("stale_after: 2026-12-31T00:00:00+08:00\nat: 2026-06-30T14:00:00Z"), [])

    def test_broken_ref_detector_negative(self):
        src = REFERENCES / "structure.md"
        self.assertTrue(broken_refs(src, "见 [x](不存在.md)"))
        self.assertTrue(broken_refs(src, "见 [seed.md §没有这一节](seed.md)"))
        self.assertTrue(broken_refs(src, "见 §没有这一节"))
        self.assertEqual(broken_refs(src, "## 甲乙\n见 §甲乙、[seed.md §关键约束](seed.md)、OKF §5.4"), [])
        self.assertEqual(broken_refs(src, "```markdown\n* [示例](不存在.md)\n```"), [])
        self.assertTrue(broken_refs(src, "```markdown\n示例\n```\n见 [x](不存在.md)"))

    def test_unrouted_reference_detector_negative(self):
        self.assertEqual(unrouted_references("见 [a](references/a.md)", ["a.md", "b.md"]), ["b.md"])

    def test_frontmatter_detector_negative(self):
        self.assertIsNone(frontmatter_of("# 没有 frontmatter 的文件\n"))

    def test_yaml_detector_negative(self):
        with self.assertRaises(yaml.YAMLError):
            yaml.safe_load("a: [未闭合")


if __name__ == "__main__":
    unittest.main()
