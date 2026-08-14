#!/usr/bin/env node
// Reads data/search_data.json and outputs a pre-built MiniSearch index to
// data/search_index.json.  The index includes the `text` field for full-text
// search but does NOT store it in results, keeping the download small.

const MiniSearch = require('../js/minisearch.js');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');

const { data } = JSON.parse(
    fs.readFileSync(path.join(root, 'data/search_data.json'), 'utf8')
);

const documents = data.map((item, id) => ({ id, ...item }));

const tokenize = (string) => string.split(/[\s-.]+/);

const miniSearch = new MiniSearch({
    fields: ['title', 'text', 'category', 'blurb'],
    storeFields: ['title', 'category', 'url', 'blurb', 'type'],
    tokenize,
    searchOptions: { tokenize },
});

miniSearch.addAll(documents);

const indexJson = JSON.stringify(miniSearch.toJSON());
const version = crypto.createHash('md5').update(indexJson).digest('hex').slice(0, 12);

const output = JSON.stringify({ version, index: miniSearch.toJSON() });
fs.writeFileSync(path.join(root, 'data/search_index.json'), output);

const inputSize = fs.statSync(path.join(root, 'data/search_data.json')).size;
const outputSize = Buffer.byteLength(output);
console.log(
    `Search index built: ${(inputSize / 1024).toFixed(1)} KB → ${(outputSize / 1024).toFixed(1)} KB (version: ${version})`
);
