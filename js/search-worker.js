// Web Worker for building loading index

importScripts('minisearch.js');

self.onmessage = function(e) {
    const { data } = e.data;

    const documents = data.map((item, id) => ({id, ...item}));

    const miniSearch = new MiniSearch({
        fields: ['title', 'text', 'category', 'blurb'],
        storeFields: ['title', 'text', 'category', 'url', 'blurb', 'type'],
        tokenize: (string) => string.split(/[\s-.]+/),
        searchOptions: {
            tokenize: (string) => string.split(/[\s-.]+/)
        }
    });

    const miniPredictor = new MiniSearch({
        fields: ['title', 'category', 'blurb'],
        storeFields: ['title', 'category', 'blurb', 'type'],
        tokenize: (string) => string.split(/[\s-.]+/),
        searchOptions: {
            tokenize: (string) => string.split(/[\s-.]+/)
        }
    });

    miniSearch.addAll(documents);
    miniPredictor.addAll(documents);

    self.postMessage({
        miniSearchIndex: miniSearch.toJSON(),
        miniPredictorIndex: miniPredictor.toJSON()
    });
};
