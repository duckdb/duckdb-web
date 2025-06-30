
function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = Diagram(GenerateCTE(options)).toString();
	document.getElementById("rrdiagram").classList.add("limit-width");

	SwitchImages(localStorage.getItem("mode") === 'dark');

	$('.mode').click(function() {
		SwitchImages($(this).attr('data-mode') === 'dark');
	});
}

function SwitchImages(mode) {
	if (mode) {
		document.getElementById("tree-example").setAttribute("src", "/images/examples/with-recursive-tree-example-dark.svg");
		document.getElementById("graph-example").setAttribute("src", "/images/examples/with-recursive-graph-example-dark.svg");
		document.getElementById("uk-example").setAttribute("src", "/images/examples/using-key-graph-example-dark.svg");
	} else {
		document.getElementById("tree-example").setAttribute("src", "/images/examples/with-recursive-tree-example.svg");
		document.getElementById("graph-example").setAttribute("src", "/images/examples/with-recursive-graph-example.svg");
		document.getElementById("uk-example").setAttribute("src", "/images/examples/using-key-graph-example.svg");
	}
}
function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

