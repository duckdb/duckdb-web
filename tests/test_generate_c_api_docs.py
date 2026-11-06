"""Tests for scripts/generate_c_api_docs.py.

The fixture spec under tests/fixtures/api_spec_mini holds one of every case
the generator handles; tests/fixtures/expected holds the pages the run must
write from it.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"
SPEC = FIXTURES / "api_spec_mini"
SCRIPT = HERE.parent / "scripts" / "generate_c_api_docs.py"

sys.path.insert(0, str(SCRIPT.parent))
import generate_c_api_docs as gen  # noqa: E402

PAGES = {"gadget": "gadget", "trinket": "gadget", "widget": None}
TITLES = {
    "gadget": "Gadget Interface",
    "trinket": "Trinket Interface",
    "widget": "Widget Interface",
}
LEGACY_IDS = {
    "legacy-gadgets": ("gadget_count", "an old heading id that the fixture keeps alive")
}


@pytest.fixture
def docs_dir(tmp_path):
    target = tmp_path / "docs" / "2.0" / "clients" / "c"
    shutil.copytree(FIXTURES / "pages", target)
    return target


def run(docs_dir, spec=SPEC, **overrides):
    tables = dict(pages=PAGES, titles=TITLES, legacy_ids=LEGACY_IDS)
    tables.update(overrides)
    return gen.generate(spec, docs_dir, link_root="docs/2.0/clients/c", **tables)


def heading_id_present(text, anchor_id):
    """Whether a heading, under kramdown GFM auto ids, or an explicit anchor yields anchor_id."""
    if re.search(rf'<a (?:id|name)="{re.escape(anchor_id)}"', text):
        return True
    seen = {}
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        heading = None if in_fence else re.match(r"#{1,6}[ \t]+(.*?)[ \t#]*$", line)
        if not heading:
            continue
        slug = (
            re.sub(r"[^\w\- \t]", "", heading.group(1).lower())
            .replace(" ", "-")
            .replace("\t", "-")
        )
        seen[slug] = seen.get(slug, 0) + 1
        if (slug if seen[slug] == 1 else f"{slug}-{seen[slug] - 1}") == anchor_id:
            return True
    return False


def entry(text, name):
    """The block of one function entry, from its heading to its <br>."""
    m = re.search(rf"^#### `{name}`\n(.*?)^<br>\n", text, re.S | re.M)
    assert m, f"no entry for {name}"
    return m.group(1)


# Splice


def test_splice_keeps_prose_above_marker(docs_dir):
    run(docs_dir)
    assert (docs_dir / "gadget.md").read_text() == (
        FIXTURES / "expected" / "gadget.md"
    ).read_text()
    assert (docs_dir / "api.md").read_text() == (
        FIXTURES / "expected" / "api.md"
    ).read_text()


def test_check_mode_exit_codes(docs_dir, monkeypatch):
    monkeypatch.setattr(gen, "PAGES", PAGES)
    monkeypatch.setattr(gen, "TITLES", TITLES)
    monkeypatch.setattr(gen, "LEGACY_IDS", LEGACY_IDS)
    monkeypatch.setattr(gen, "REPO_ROOT", docs_dir.parents[3])
    rel = docs_dir.relative_to(docs_dir.parents[3]).as_posix()
    checkout = docs_dir.parents[3] / "duckdb"
    (checkout / "api_spec").mkdir(parents=True)
    shutil.copytree(SPEC, checkout / "api_spec" / "v1")
    stale = (docs_dir / "gadget.md").read_text()
    assert gen.main([str(checkout), "--docs-dir", rel, "--check"]) == 1
    assert (docs_dir / "gadget.md").read_text() == stale
    assert gen.main([str(checkout), "--docs-dir", rel]) == 0
    assert gen.main([str(checkout), "--docs-dir", rel, "--check"]) == 0
    (docs_dir / "gadget.md").write_text(
        stale.replace("## API Reference Overview", "## Reference")
    )
    assert gen.main([str(checkout), "--docs-dir", rel, "--check"]) == 1
    assert gen.main([str(checkout), "--docs-dir", rel]) == 1


def test_stale_page_fails_the_run(docs_dir):
    run(docs_dir)
    generated = (docs_dir / "gadget.md").read_text()
    report = run(docs_dir, pages={"gadget": None, "trinket": None, "widget": None})
    assert report.stale == ["gadget.md"]
    assert (docs_dir / "gadget.md").read_text() == generated


def test_page_without_marker_is_reported(docs_dir):
    before = (docs_dir / "nomarker.md").read_text()
    report = run(
        docs_dir, pages={"gadget": "nomarker", "trinket": None, "widget": None}
    )
    assert (docs_dir / "nomarker.md").read_text() == before
    assert "nomarker.md" in report.skipped


# Module to page


def test_every_module_is_placed(docs_dir):
    report = run(docs_dir)
    assert report.placed == {
        "gadget": "gadget.md",
        "trinket": "gadget.md",
        "widget": None,
    }


def test_unknown_module_fails(docs_dir):
    with pytest.raises(gen.UnplacedModule, match="widget"):
        run(docs_dir, pages={"gadget": "gadget", "trinket": "gadget"})
    with pytest.raises(gen.UnplacedModule, match="trinket"):
        run(
            docs_dir,
            titles={"gadget": "Gadget Interface", "widget": "Widget Interface"},
        )


def test_complete_page_lists_every_function_once(docs_dir):
    run(docs_dir)
    text = (docs_dir / "api.md").read_text()
    headings = re.findall(r"^#### `(duckdb_\w+)`$", text, re.M)
    assert sorted(headings) == sorted(
        [
            "duckdb_create_gadget",
            "duckdb_destroy_gadget",
            "duckdb_gadget_count",
            "duckdb_gadget_data",
            "duckdb_gadget_peek",
            "duckdb_gadget_size",
            "duckdb_trinket_count",
            "duckdb_trinket_old",
            "duckdb_widget_from_gadget",
        ]
    )
    assert len(headings) == len(set(headings))


# Section titles and legacy ids


def test_legacy_section_ids_exist(docs_dir):
    run(docs_dir)
    text = (docs_dir / "api.md").read_text()
    assert "### Gadget Interface\n" in text
    assert "### Widget Interface\n" in text
    assert '<a id="legacy-gadgets"></a>' in text
    assert (
        text.index("#### `duckdb_destroy_gadget`")
        < text.index('<a id="legacy-gadgets">')
        < text.index("#### `duckdb_gadget_count`")
    )
    assert text.count('<a id="legacy-gadgets">') == 1


def test_topic_page_titles_modules_after_the_first(docs_dir):
    run(docs_dir)
    text = (docs_dir / "gadget.md").read_text()
    assert "### Gadget Interface" not in text
    assert text.count("### Trinket Interface\n") == 1
    assert (
        text.index("#### `duckdb_gadget_size`")
        < text.index("### Trinket Interface")
        < text.index("#### `duckdb_trinket_count`")
    )


# Function entry


def test_function_entry_golden(docs_dir):
    run(docs_dir)
    text = (docs_dir / "gadget.md").read_text()
    expected = (FIXTURES / "expected" / "gadget.md").read_text()
    assert entry(text, "duckdb_create_gadget") == entry(
        expected, "duckdb_create_gadget"
    )


def test_void_function_has_no_return_value(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_destroy_gadget")
    assert "##### Return Value" not in block
    assert "##### Parameters" in block


def test_parameter_without_text_is_not_listed(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_trinket_count")
    assert "##### Parameters\n\n* `n`: How many to count.\n" in block
    assert "* `trinket`" not in block


def test_missing_return_description_falls_back_to_type(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_count")
    assert "##### Return Value\n\n`idx_t`\n" in block


# Quick reference


def quick_reference(text):
    """The HTML quick reference blocks of a page, in order."""
    _, _, section = text.partition("<!-- This section")
    return re.findall(
        r'<div class="language-c highlighter-rouge">.*?</code></pre></div></div>',
        section,
        re.S,
    )


def test_quick_reference_lists_each_prototype_once(docs_dir):
    run(docs_dir)
    blocks = quick_reference((docs_dir / "gadget.md").read_text())
    assert len(blocks) == 2
    names = re.findall(r'<span class="nf">duckdb_(\w+)</span></a>\(', blocks[0])
    assert names == [
        "create_gadget",
        "destroy_gadget",
        "gadget_count",
        "gadget_data",
        "gadget_peek",
        "gadget_size",
    ]
    assert blocks[0].count("\n") == 6


def test_quick_reference_links_resolve_on_the_page(docs_dir):
    run(docs_dir)
    for page in ("gadget.md", "api.md"):
        text = (docs_dir / page).read_text()
        hrefs = [
            h
            for b in quick_reference(text)
            for h in re.findall(r'<a href="#([^"]+)">', b)
        ]
        headings = set(re.findall(r"^#### `(duckdb_\w+)`$", text, re.M))
        assert hrefs, page
        assert set(hrefs) == headings, page


def test_quick_reference_tags_spec_types(docs_dir):
    run(docs_dir)
    block = quick_reference((docs_dir / "api.md").read_text())[2]
    assert '<span class="kt">duckdb_widget</span>' in block
    assert '<span class="kt">duckdb_gadget</span>' in block
    assert '<span class="kt">DUCKDB_MINI_KIND</span>' in block
    assert '<span class="nv">kind</span>' in block
    assert (
        re.search(
            r'<span class="nv">(duckdb_\w+|DUCKDB_\w+|idx_t|bool|void|char|const)</span>',
            block,
        )
        is None
    )


# Lifecycle


def test_deprecated_function_gets_callout(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_data")
    assert block.startswith(
        "\n> Deprecated Deprecated since 1.0.0, stable since 0.2.9.\n"
    )


def test_unstable_function_is_marked(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_peek")
    assert block.startswith("\n> Warning Unstable since 1.5.0.")


def test_renamed_function_names_old_name(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_size")
    assert block.startswith(
        "\nStable since 1.2.0. Renamed from `duckdb_gadget_length` in 1.4.0.\n"
    )


def test_deprecated_without_stable_and_renamed(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_trinket_old")
    assert block.startswith(
        "\n> Deprecated Deprecated since 1.5.0. Renamed from `duckdb_trinket_ancient` in 1.4.0.\n"
    )


def test_deprecation_prose_loses_its_label(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_data")
    assert "**DEPRECATION NOTICE**" not in block
    assert "\nThis method is scheduled for removal in a future release.\n" in block


# Description text


def test_fence_passes_through(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_data")
    assert (
        '```c\nint32_t *data = (int32_t *) duckdb_gadget_data(gadget, 0);\nprintf("Data for row %d: %d\\n", row, data[row]);\n/* see [[create_gadget]] for the "col0" layout */\n```\n'
        in block
    )


def test_angle_brackets_outside_code_are_escaped(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_count")
    assert "`MinValue<idx_t>`" in block
    assert re.search(r"(?<!`)MinValue<idx_t>", block) is None


def test_relative_link_becomes_link_tag(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_data")
    assert "[the types section]({% link docs/2.0/clients/c/types.md %})" in block
    assert "](types)" not in block


def test_relative_link_to_missing_page_fails(docs_dir, tmp_path):
    spec = tmp_path / "spec"
    shutil.copytree(SPEC, spec)
    yaml_path = spec / "gadget" / "gadget.yaml"
    yaml_path.write_text(
        yaml_path.read_text().replace(
            "[the types section](types)", "[the types section](nowhere)"
        )
    )
    with pytest.raises(gen.MissingLinkTarget, match="nowhere"):
        run(docs_dir, spec=spec)


def test_quotes_follow_site_style(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_count")
    assert "“items”" in block
    assert '"items"' not in block


def test_quoted_identifier_becomes_code_span(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_data")
    assert "`col_data` when the gadget is “plain”." in block


def test_anchor_inside_fence_is_untouched(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_data")
    assert '/* see [[create_gadget]] for the "col0" layout */' in block


# Anchors


def test_function_anchor_becomes_link(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "api.md").read_text(), "duckdb_widget_from_gadget")
    assert "[`duckdb_create_gadget`](#duckdb_create_gadget)" in block
    assert "[[" not in block


def test_off_page_anchor_links_the_complete_page(docs_dir):
    run(docs_dir)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_gadget_peek")
    assert (
        "See [`duckdb_widget_from_gadget`]({% link docs/2.0/clients/c/api.md %}#duckdb_widget_from_gadget)."
        in block
    )
    block = entry((docs_dir / "api.md").read_text(), "duckdb_gadget_peek")
    assert "See [`duckdb_widget_from_gadget`](#duckdb_widget_from_gadget)." in block


def test_non_function_anchor_is_code_span(docs_dir):
    report = run(docs_dir)
    block = entry((docs_dir / "api.md").read_text(), "duckdb_widget_from_gadget")
    assert "Builds a `duckdb_widget` from a gadget." in block
    assert "see `DUCKDB_MINI_KIND`." in block
    assert sorted(report.unlinked_anchors) == ["MINI_KIND", "widget"]


# Lint


@pytest.mark.skipif(shutil.which("npx") is None, reason="node is not installed")
def test_output_passes_markdownlint(docs_dir):
    run(docs_dir)
    config = HERE.parent / ".markdownlint.jsonc"
    result = subprocess.run(
        [
            "npx",
            "--no-install",
            "markdownlint-cli",
            "--config",
            str(config),
            str(docs_dir / "api.md"),
            str(docs_dir / "gadget.md"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# Real spec


@pytest.mark.skipif(
    "DUCKDB_CHECKOUT" not in os.environ, reason="DUCKDB_CHECKOUT is not set"
)
def test_real_spec_round_trip(tmp_path):
    import capigen

    checkout = Path(os.environ["DUCKDB_CHECKOUT"])
    spec_dir = checkout / "api_spec" / "v1"
    target = tmp_path / "docs" / "2.0" / "clients" / "c"
    shutil.copytree(HERE.parent / "docs" / "2.0" / "clients" / "c", target)
    report = gen.generate(spec_dir, target, link_root="docs/2.0/clients/c")
    spec = capigen.load(spec_dir)
    names = sorted(f"duckdb_{n}" for m in spec.modules for n in m.get("functions", {}))
    text = (target / "api.md").read_text()
    headings = re.findall(r"^#### `(duckdb_\w+)`$", text, re.M)
    assert sorted(headings) == names
    for legacy in (
        "arrow-interface",
        "scalar-functions",
        "pending-result-interface",
        "extract-statements",
    ):
        assert heading_id_present(text, legacy)
    assert report.skipped == [] and report.stale == []
    for page in sorted(target.glob("*.md")):
        page_text = page.read_text()
        hrefs = [
            h
            for b in quick_reference(page_text)
            for h in re.findall(r'<a href="#([^"]+)">', b)
        ]
        unresolved = [h for h in hrefs if not heading_id_present(page_text, h)]
        assert unresolved == [], page.name
    for module in spec.modules:
        page = report.placed.get(module["module"])
        if not page:
            continue
        page_text = (target / page).read_text()
        for name in module["functions"]:
            assert page_text.count(f"#### `duckdb_{name}`\n") == 1, (page, name)
