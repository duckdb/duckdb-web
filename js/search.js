let searchDataLoaded = false;

const tokenize = (string) => string.split(/[\s-.]+/);

const searchOptions = {
	fields: ['title', 'text', 'category', 'blurb'],
	storeFields: ['title', 'category', 'url', 'blurb', 'type'],
	tokenize,
	searchOptions: { tokenize }
};

const CACHE_KEY = 'duckdb_search_index';
const CACHE_VERSION_KEY = 'duckdb_search_version';

function loadFromCache() {
	try {
		var version = localStorage.getItem(CACHE_VERSION_KEY);
		var data = localStorage.getItem(CACHE_KEY);
		if (version && data) {
			return { version: version, index: JSON.parse(data) };
		}
	} catch (e) { /* localStorage unavailable or corrupted */ }
	return null;
}

function saveToCache(version, indexObj) {
	try {
		localStorage.setItem(CACHE_VERSION_KEY, version);
		localStorage.setItem(CACHE_KEY, JSON.stringify(indexObj));
	} catch (e) { /* quota exceeded, ignore */ }
}

function applyIndex(indexObj) {
	miniSearch = MiniSearch.loadJS(indexObj, searchOptions);
	searchDataLoaded = true;
	if (text_div.value.length > 0) {
		perform_search(text_div.value);
	}
}

function loadSearchData() {
	if (searchDataLoaded) return;
	searchDataLoaded = true; // prevent concurrent loads

	var cached = loadFromCache();
	if (cached) {
		applyIndex(cached.index);

		// Revalidate in background
		fetch('/data/search_index.json')
			.then(function (r) { return r.json(); })
			.then(function (json) {
				if (json.version !== cached.version) {
					applyIndex(json.index);
					saveToCache(json.version, json.index);
				}
			})
			.catch(function () { /* offline / fetch failed, cached index is fine */ });
		return;
	}

	// No cache — fetch and load
	fetch('/data/search_index.json')
		.then(function (r) { return r.json(); })
		.then(function (json) {
			applyIndex(json.index);
			saveToCache(json.version, json.index);
		})
		.catch(function (err) {
			searchDataLoaded = false;
			console.error('Failed to load search index:', err);
		});
}

// Event listeners to load search data only on interaction
const text_div = document.getElementById("q");
text_div.addEventListener('focus', loadSearchData);
text_div.addEventListener('input', loadSearchData);

let miniSearch = new MiniSearch(searchOptions);

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
function bold_blurb(blurb, query) {
	if (blurb === undefined) {
		return blurb
	}
	const querySplits = query.toLowerCase().split(" ");
	for(let split of querySplits) {
		if (split.length == 0) {
			continue
		}
		let startIndex = 0
		let splitLength = split.length
		while(startIndex < blurb.length) {
			let index = blurb.toLowerCase().indexOf(split, startIndex)
			if (index < 0) {
				break
			}
			blurb = blurb.substr(0, index) + "<u>" + blurb.substr(index, splitLength) + "</u>" + blurb.substr(index + splitLength)
			startIndex = index + splitLength + 7
		}
	}
	return blurb
}

// Check what page we are
let currentPageType = 'all'; 
if (window.location.pathname.includes('/docs/')) {
	currentPageType = 'documentation';
} else if (window.location.pathname.includes('/news/')) {
	currentPageType = 'blog';
}

function perform_search(query) {
	let searchOptions = {
		boost: { title: 100, category: 20, blurb: 2 },
		prefix: true,
		fuzzy: 0.2
	};
	
	// Filter search results depening on what page we are
	if (currentPageType === 'documentation') {
		searchOptions.filter = (doc) => doc.type === 'documentation';
	} else if (currentPageType === 'blog') {
		searchOptions.filter = (doc) => doc.type === 'blog';
	}
	
	let results = miniSearch.search(query, searchOptions);
	let search_div = document.getElementById("search_results");
	let search_html = "";
	let max_index = 20;
	for(let i = 0; i < results.length; i++) {
		search_html += "<div class='search_result ";
		if (i % 2 == 0) {
			search_html += "search_result_even";
		} else {
			search_html += "search_result_uneven";
		}
		search_html += "'>";
		search_html += "<a href='" + results[i].url + "'>";
		search_html += "</a> ";
		search_html += "<h2 class='search_title'>";
		search_html += bold_blurb(results[i].title, query);
		search_html += "</h2>";
		search_html += "<div class='search_text'>";
		search_html += bold_blurb(results[i].blurb, query);
		search_html += "</div>";
		search_html += "<span class='search_category'>";
		search_html += results[i].category;
		search_html += "</span>";
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

text_div.addEventListener('keyup', on_update);
text_div.addEventListener('input', on_update);

// autocomplete
// see https://www.w3schools.com/howto/howto_js_autocomplete.asp
inp = document.getElementById("q")
/*the autocomplete function takes two arguments,
the text field element and an array of possible autocompleted values:*/
var currentFocus;
/*execute a function when someone writes in the text field:*/

/* APPEND AUTOCOMPLETE SUGGESTIONS */
// inp.addEventListener("input", function(e) {
//   var a, b, i, val = this.value;
//   /*close any already open lists of autocompleted values*/
//   closeAllLists();
//   if (!val) { return false;}
//   currentFocus = -1;
//   /*create a DIV element that will contain the items (values):*/
//   a = document.createElement("DIV");
//   a.setAttribute("id", this.id + "autocomplete-list");
//   a.setAttribute("class", "autocomplete-items");
//   /*append the DIV element as a child of the autocomplete container:*/
//   this.parentNode.appendChild(a);

//   let suggestions = miniPredictor.search(val, { boost: { title: 100, category: 20, blurb: 2 }, prefix: true});
//   let max_count = 4;
//   let current_count = 0;
//   for (suggest_index in suggestions) {
//     current_count += 1;
//     if (current_count > max_count) {
//       break;
//     }
//     let suggest = suggestions[suggest_index];
//     /*create a DIV element for each matching element:*/
//     b = document.createElement("DIV");
//     let result = suggest.title.toLowerCase().indexOf(val.toLowerCase());
//     /*make the matching letters bold (if any):*/
//     if (result >= 0) {
//       if (result > 0) {
//         b.innerHTML += suggest.title.substr(0, result);
//       }
//       b.innerHTML += "<u>" + suggest.title.substr(result, val.length) + "</u>";
//       let final_pos = result + val.length;
//       if (final_pos < suggest.title.length) {
//         b.innerHTML += suggest.title.substr(final_pos, suggest.title.length - final_pos);
//       }
//     } else {
//       b.innerHTML = suggest.title;
//     }
//     /*insert a input field that will hold the current array item's value:*/
//     b.innerHTML += "<input type='hidden' value='" + suggest.title + "'>";
//     /*execute a function when someone clicks on the item value (DIV element):*/
//     b.addEventListener("click", function(e) {
//       inp.value = this.getElementsByTagName("input")[0].value;
//       perform_search(inp.value);
//       closeAllLists();
//     });
//     a.appendChild(b);
//   }
// });


/*execute a function presses a key on the keyboard:*/
inp.addEventListener("keydown", function(e) {
	var x = document.getElementById(this.id + "autocomplete-list");
	if (x) x = x.getElementsByTagName("div");
	if (e.keyCode == 40) {
		/*If the arrow DOWN key is pressed,
		increase the currentFocus variable:*/
		currentFocus++;
		/*and and make the current item more visible:*/
		addActive(x);
	} else if (e.keyCode == 38) { //up
		/*If the arrow UP key is pressed,
		decrease the currentFocus variable:*/
		currentFocus--;
		/*and and make the current item more visible:*/
		addActive(x);
	} else if (e.keyCode == 13) {
		/*If the ENTER key is pressed, prevent the form from being submitted,*/
		e.preventDefault();
		if (currentFocus > -1) {
			/*and simulate a click on the "active" item:*/
			if (x) x[currentFocus].click();
		} else {
			/*Close the suggestion list on enter so that the user can view the main document list */
			closeAllLists();
		}
	}
});
function addActive(x) {
	/*a function to classify an item as "active":*/
	if (!x) return false;
	/*start by removing the "active" class on all items:*/
	removeActive(x);
	if (currentFocus >= x.length) currentFocus = 0;
	if (currentFocus < 0) currentFocus = (x.length - 1);
	/*add class "autocomplete-active":*/
	x[currentFocus].classList.add("autocomplete-active");
}
function removeActive(x) {
	/*a function to remove the "active" class from all autocomplete items:*/
	for (var i = 0; i < x.length; i++) {
		x[i].classList.remove("autocomplete-active");
	}
}
function closeAllLists(elmnt) {
	/*close all autocomplete lists in the document,
	except the one passed as an argument:*/
	var x = document.getElementsByClassName("autocomplete-items");
		for (var i = 0; i < x.length; i++) {
		if (elmnt != x[i] && elmnt != inp) {
			x[i].parentNode.removeChild(x[i]);
		}
	}
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
	closeAllLists(e.target);
});
