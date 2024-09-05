#!/usr/bin/env node

const jsdoc2md = require("jsdoc-to-markdown");
const fs = require("fs/promises");

const duckdb = process.argv[2];
if (!duckdb) {
    console.error("Expected usage: ./scripts/generate_nodejs_docs.js /path/to/duckdb");
    process.exit(1);
}

async function generate_docs() {
  let docs = await jsdoc2md.render({ files: duckdb + "/lib/*.js" });

  // Add newline after headers to conform to the Markdown linter's rules.
  // To achieve this, the regex looks for headers starting with two or more # characters,
  // that are followed by a non-empty line, using global and multi-line matching.
  add_newline_after_headers = /^(##+ .*\n)([^\n])/gm;
  docs = docs.replace(add_newline_after_headers, "$1\n$2");

  docs =
    `\
---
layout: docu
title: Node.js API
---

` + docs;

  await fs.writeFile(__dirname + "/../docs/api/nodejs/reference.md", docs);
}

generate_docs().catch((e) => {
  console.error(e);
  process.exit(1);
});
