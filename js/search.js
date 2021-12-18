// Create a search engine that indexes the 'title' and 'text' fields for
// full-text search. Search results will include 'title' and 'category' (plus the
// id field, that is always stored and returned)
const miniSearch = new MiniSearch({
fields: ['title', 'text', 'blurb'],
storeFields: ['title', 'text', 'category', 'url', 'blurb']
})
// Add documents to the index
miniSearch.addAll(documents)

// read GET parameters (https://stackoverflow.com/questions/12049620/how-to-get-get-variables-value-in-javascript)
// lord knows why this needs a regex and hasn't been part of the JS standard since day 1
var $_GET = {};
if(document.location.toString().indexOf('?') !== -1) {
    var query = document.location
                   .toString()
                   // get the query string
                   .replace(/^.*?\?/, '')
                   // and remove any existing hash string (thanks, @vrijdenker)
                   .replace(/#.*$/, '')
                   .split('&');

    for(var i=0, l=query.length; i<l; i++) {
       var aux = decodeURIComponent(query[i]).split('=');
       $_GET[aux[0]] = aux[1];
    }
}
function perform_search(query) {
	// Search for documents:
	let results = miniSearch.search(query, { boost: { title: 100, blurb: 2 }, prefix: true, fuzzy: 0.2});
	let search_div = document.getElementById("search_results");
	let search_html = "";
	let max_index = 20;
	for(let i = 0; i < results.length; i++) {
		search_html += "<div class='search_result'>";
		search_html += "<h2 class='search_title'>";
		search_html += "<a href='" + results[i].url + "'>";
		search_html += results[i].title;
		search_html += "</a>";
		search_html += "</h2>";
		search_html += "<div class='search_text'>";
		search_html += results[i].blurb;
		search_html += "</div>";
		search_html += "</div>";
		if (i >= max_index) {
			break;
		}
	}
	search_div.innerHTML = search_html;
}

//get the 'index' query parameter
if ($_GET['q']!==undefined) {
	perform_search($_GET['q']);
}

function on_update(e) {
	perform_search(e.target.value);
}

let text_div = document.getElementById("q");
text_div.addEventListener('keyup', on_update);
