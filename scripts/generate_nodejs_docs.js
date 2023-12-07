#!/usr/bin/env node

const jsdoc2md = require('jsdoc-to-markdown');
const fs = require('fs');

const duckdb = process.argv[2];
if (!duckdb) {
    console.error("Expected usage: ./scripts/generate_nodejs_docs.js /path/to/duckdb");
    process.exit(1);
}

let docs = jsdoc2md.renderSync({ files: duckdb + '/lib/*.js' });
docs = `\
---
layout: docu
title: Node.js API
---
` + docs;

fs.writeFileSync(__dirname + '/../docs/dev/api/nodejs/reference.md', docs);
