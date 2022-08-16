#!/usr/bin/env node

const jsdoc2md = require('jsdoc-to-markdown');
const fs = require('fs');

const duckdb = process.argv[2];
if (!duckdb) {
    console.error("Expected usage: ./scripts/generate_nodejs_docs.js /path/to/duckdb");
    process.exit(1);
}

let docs = jsdoc2md.renderSync({ files: duckdb + '/tools/nodejs/lib/*.js' });
docs = `\
---
layout: docu
title: NodeJS API
selected: Client APIs
---
` + docs;

fs.writeFileSync(__dirname + '/../docs/api/nodejs/reference.md', docs);
