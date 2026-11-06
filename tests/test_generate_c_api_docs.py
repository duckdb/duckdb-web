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

SPEC_V2 = FIXTURES / "api_spec_mini_v2"
PAGES_V2 = {"mini_common": None, "gizmo": None}
TITLES_V2 = {"mini_common": "Mini Common", "gizmo": "Gizmo"}
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


def run_v2(docs_dir, spec=SPEC_V2, **overrides):
    tables = dict(pages=PAGES_V2, titles=TITLES_V2, legacy_ids={})
    tables.update(overrides)
    return gen.generate(
        spec, docs_dir / "v2", link_root="docs/2.0/clients/c/v2", **tables
    )


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
    monkeypatch.setattr(gen, "REPO_ROOT", docs_dir.parents[3])
    monkeypatch.setattr(
        gen, "APIS", {"v1": gen.Api(PAGES, TITLES, LEGACY_IDS, subdir="")}
    )
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
    assert block.startswith("\nUnstable since 1.5.0.\n")


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
    run_v2(docs_dir)
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
            str(docs_dir / "v2" / "api.md"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# The v2 spec: type headings, anchors to types, ownership tags, lists


def test_v2_complete_page_golden(docs_dir):
    run_v2(docs_dir)
    assert (docs_dir / "v2" / "api.md").read_text() == (
        FIXTURES / "expected" / "v2" / "api.md"
    ).read_text()


def test_type_headings(docs_dir):
    run_v2(docs_dir)
    text = (docs_dir / "v2" / "api.md").read_text()
    for name in (
        "duckdb_v2_gizmo_handle",
        "duckdb_v2_error_info_handle",
        "duckdb_v2_gizmo_visit_fn",
        "duckdb_v2_sel_t",
        "duckdb_v2_view",
        "DUCKDB_V2_GIZMO_KIND",
        "DUCKDB_V2_GIZMO_MAX_ITEMS",
    ):
        assert text.count(f"#### `{name}`\n") == 1, name
    types_end = text.index("### Gizmo")
    assert (
        text.index("#### `DUCKDB_V2_GIZMO_MAX_ITEMS`")
        < types_end
        < text.index("#### `duckdb_v2_gizmo_create`")
    )
    assert "Unstable since" not in text[:types_end]


def test_type_only_module_outside_the_table_is_skipped(docs_dir):
    report = run_v2(docs_dir, pages={"gizmo": None})
    text = (docs_dir / "v2" / "api.md").read_text()
    assert "#### `duckdb_v2_gizmo_handle`" not in text
    assert report.skipped_modules == ["mini_common"]
    assert "gizmo_destroy" not in report.unlinked_anchors
    assert sorted(report.unlinked_anchors) == [
        "GIZMO_KIND",
        "GIZMO_MAX_ITEMS",
        "gizmo_visit",
        "sel",
        "view",
    ]


def test_every_anchor_target_has_a_heading(docs_dir):
    report = run_v2(docs_dir)
    assert report.unlinked_anchors == [] and report.skipped_modules == []
    text = (docs_dir / "v2" / "api.md").read_text()
    assert "[[" not in text
    for href in re.findall(r"\]\(#([^)]+)\)", text):
        assert heading_id_present(text, href), href


def test_type_anchor_becomes_link(docs_dir):
    run_v2(docs_dir)
    text = (docs_dir / "v2" / "api.md").read_text()
    assert (
        "Destroy it with [`duckdb_v2_gizmo_destroy`](#duckdb_v2_gizmo_destroy)." in text
    )
    assert "see [`duckdb_v2_gizmo_handle`](#duckdb_v2_gizmo_handle)." in text
    assert "one of [`DUCKDB_V2_GIZMO_KIND`](#duckdb_v2_gizmo_kind)." in text
    assert (
        "at most [`DUCKDB_V2_GIZMO_MAX_ITEMS`](#duckdb_v2_gizmo_max_items) items."
        in text
    )
    assert (
        "A [`duckdb_v2_view`](#duckdb_v2_view) of the item names, each a [`duckdb_v2_sel_t`](#duckdb_v2_sel_t) long."
        in text
    )
    assert "see [`duckdb_v2_gizmo_visit_fn`](#duckdb_v2_gizmo_visit_fn)." in text


def test_mixed_anchor_span_fails(docs_dir, tmp_path):
    spec = tmp_path / "spec"
    shutil.copytree(SPEC_V2, spec)
    yaml_path = spec / "common" / "common.yaml"
    yaml_path.write_text(
        yaml_path.read_text().replace("`[[gizmo_destroy]]`", "`[[gizmo_destroy]]()`")
    )
    with pytest.raises(gen.MixedAnchorSpan, match=r"gizmo_destroy"):
        run_v2(docs_dir, spec=spec)


def test_parameter_kind_tags(docs_dir):
    run_v2(docs_dir)
    text = (docs_dir / "v2" / "api.md").read_text()
    create = entry(text, "duckdb_v2_gizmo_create")
    assert (
        "* `kind`: The kind, one of [`DUCKDB_V2_GIZMO_KIND`](#duckdb_v2_gizmo_kind).\n"
        in create
    )
    assert "* `out_gizmo`: Receives the new gizmo. (out)\n" in create
    assert "* `err`: (out, borrowed)\n" in create
    destroy = entry(text, "duckdb_v2_gizmo_destroy")
    assert (
        "* `gizmo`: The gizmo to destroy. (ownership passes to the callee)\n" in destroy
    )


def test_list_passes_through(docs_dir):
    run_v2(docs_dir)
    create = entry((docs_dir / "v2" / "api.md").read_text(), "duckdb_v2_gizmo_create")
    assert (
        "The kind decides the layout:\n* plain gizmos hold items in order,\n"
        "* fancy gizmos hold at most [`DUCKDB_V2_GIZMO_MAX_ITEMS`](#duckdb_v2_gizmo_max_items) items.\n\n"
        "Creation runs in two steps:\n1. the layout is chosen,\n2. the items are allocated.\n"
    ) in create


def test_callback_and_alias_syntax(docs_dir):
    run_v2(docs_dir)
    text = (docs_dir / "v2" / "api.md").read_text()
    assert (
        "```c\ntypedef bool (*duckdb_v2_gizmo_visit_fn)(\n  idx_t item,\n  void *user_data,\n"
        "  duckdb_v2_error_info_handle *err\n);\n```"
    ) in text
    assert (
        "* `err`: Live error slot. Populate it to fail the visiting call. (out, borrowed)\n"
        in text
    )
    assert "```c\ntypedef uint32_t duckdb_v2_sel_t;\n```" in text
    assert (
        "* `ptr` (`const char *`): The first byte.\n* `len` (`idx_t`): The number of bytes.\n"
        in text
    )
    assert "* `DUCKDB_V2_GIZMO_KIND_PLAIN` = 0: A plain gizmo.\n" in text
    assert "* `DUCKDB_V2_GIZMO_KIND_HOLLOW` = 2\n" in text
    assert "The most items a gizmo holds.\n\nValue: `12`.\n" in text
    assert "##### Value\n" not in text
    assert (
        "* `value` (`union`)\n    * `pointer` (`struct`)\n        * `length` (`uint32_t`)\n"
        "        * `prefix` (`char[4]`): The first four bytes.\n        * `ptr` (`char *`)\n"
        "    * `inlined` (`struct`)\n        * `length` (`uint32_t`)\n        * `inlined` (`char[12]`)\n"
    ) in text


def test_description_keeps_first_line_indentation(docs_dir, tmp_path):
    spec = tmp_path / "spec"
    shutil.copytree(SPEC_V2, spec)
    yaml_path = spec / "gizmo" / "gizmo.yaml"
    yaml_path.write_text(
        yaml_path.read_text().replace(
            "    description: |\n      Visits every item of a gizmo.\n",
            "    description: \"  - first item\\n  - second item\\n\"\n",
        )
    )
    run_v2(docs_dir, spec=spec)
    block = entry((docs_dir / "v2" / "api.md").read_text(), "duckdb_v2_gizmo_visit_all")
    assert "\n  * first item\n  * second item\n" in block
    v1 = tmp_path / "v1"
    shutil.copytree(SPEC, v1)
    yaml_path = v1 / "trinket" / "trinket.yaml"
    yaml_path.write_text(
        yaml_path.read_text().replace(
            "    description: |\n      Does nothing useful any more.\n",
            "    description: \"**DEPRECATED**: gone.\\n  - first item\\n  - second item\\n\"\n",
        )
    )
    run(docs_dir, spec=v1)
    block = entry((docs_dir / "gadget.md").read_text(), "duckdb_trinket_old")
    assert "\ngone.\n  * first item\n  * second item\n" in block


def fixture_checkout(docs_dir, with_v2=True):
    root = docs_dir.parents[3]
    checkout = root / "duckdb"
    (checkout / "api_spec").mkdir(parents=True)
    shutil.copytree(SPEC, checkout / "api_spec" / "v1")
    if with_v2:
        shutil.copytree(SPEC_V2, checkout / "api_spec" / "v2")
    return checkout


def test_two_specs_in_one_run(docs_dir, monkeypatch):
    monkeypatch.setattr(gen, "REPO_ROOT", docs_dir.parents[3])
    monkeypatch.setattr(
        gen,
        "APIS",
        {
            "v1": gen.Api(PAGES, TITLES, LEGACY_IDS, subdir=""),
            "v2": gen.Api(PAGES_V2, TITLES_V2, {}, subdir="v2"),
        },
    )
    checkout = fixture_checkout(docs_dir)
    rel = docs_dir.relative_to(docs_dir.parents[3]).as_posix()
    assert gen.main([str(checkout), "--docs-dir", rel]) == 0
    assert (docs_dir / "gadget.md").read_text() == (
        FIXTURES / "expected" / "gadget.md"
    ).read_text()
    assert (docs_dir / "v2" / "api.md").read_text() == (
        FIXTURES / "expected" / "v2" / "api.md"
    ).read_text()
    assert gen.main([str(checkout), "--docs-dir", rel, "--check"]) == 0


def test_no_spec_folder_at_all_fails(docs_dir, monkeypatch, capsys):
    monkeypatch.setattr(gen, "REPO_ROOT", docs_dir.parents[3])
    checkout = docs_dir.parents[3] / "duckdb"
    checkout.mkdir()
    rel = docs_dir.relative_to(docs_dir.parents[3]).as_posix()
    assert gen.main([str(checkout), "--docs-dir", rel]) == 1
    assert "api_spec" in capsys.readouterr().err


def test_missing_page_file_is_reported(docs_dir):
    (docs_dir / "v2" / "api.md").unlink()
    report = run_v2(docs_dir)
    assert report.skipped == ["api.md"]
    assert not (docs_dir / "v2" / "api.md").exists()


def test_missing_v2_spec_is_skipped(docs_dir, monkeypatch, capsys):
    monkeypatch.setattr(gen, "REPO_ROOT", docs_dir.parents[3])
    monkeypatch.setattr(
        gen,
        "APIS",
        {
            "v1": gen.Api(PAGES, TITLES, LEGACY_IDS, subdir=""),
            "v2": gen.Api(PAGES_V2, TITLES_V2, {}, subdir="v2"),
        },
    )
    checkout = fixture_checkout(docs_dir, with_v2=False)
    rel = docs_dir.relative_to(docs_dir.parents[3]).as_posix()
    stale_v2 = (docs_dir / "v2" / "api.md").read_text()
    assert gen.main([str(checkout), "--docs-dir", rel]) == 0
    assert (docs_dir / "v2" / "api.md").read_text() == stale_v2
    assert "api_spec/v2" in capsys.readouterr().err


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


@pytest.mark.skipif(
    "DUCKDB_CHECKOUT" not in os.environ, reason="DUCKDB_CHECKOUT is not set"
)
def test_real_v2_spec_round_trip(tmp_path):
    import capigen

    checkout = Path(os.environ["DUCKDB_CHECKOUT"])
    spec_dir = checkout / "api_spec" / "v2"
    target = tmp_path / "docs" / "2.0" / "clients" / "c"
    shutil.copytree(HERE.parent / "docs" / "2.0" / "clients" / "c", target)
    api = gen.APIS["v2"]
    report = gen.generate(
        spec_dir,
        target / api.subdir,
        link_root=f"docs/2.0/clients/c/{api.subdir}",
        pages=api.pages,
        titles=api.titles,
        legacy_ids=api.legacy_ids,
    )
    spec = capigen.load(spec_dir)
    text = (target / api.subdir / "api.md").read_text()
    functions = sorted(
        f"duckdb_v2_{n}" for m in spec.modules for n in m.get("functions", {})
    )
    types = sorted(
        spec.registry[n]
        for m in spec.modules
        for k in ("handles", "callbacks", "aliases", "structs", "enums")
        for n in m.get(k, {})
    )
    constants = sorted(
        f"DUCKDB_V2_{n}" for m in spec.modules for n in m.get("constants", {})
    )
    headings = re.findall(r"^#### `([^`]+)`$", text, re.M)
    assert (
        sorted(h for h in headings if h not in types and h not in constants)
        == functions
    )
    assert sorted(h for h in headings if h not in functions) == sorted(
        types + constants
    )
    assert len(headings) == len(set(headings))
    assert report.unlinked_anchors == [] and report.skipped == [] and report.stale == []
    assert "[[" not in text
    hrefs = [
        h for b in quick_reference(text) for h in re.findall(r'<a href="#([^"]+)">', b)
    ]
    hrefs += re.findall(r"\]\(#([^)]+)\)", text)
    unresolved = sorted({h for h in hrefs if not heading_id_present(text, h)})
    assert unresolved == []
    if shutil.which("npx"):
        result = subprocess.run(
            [
                "npx",
                "--no-install",
                "markdownlint-cli",
                "--config",
                str(HERE.parent / ".markdownlint.jsonc"),
                str(target / api.subdir / "api.md"),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr
