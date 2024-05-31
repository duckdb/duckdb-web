
function GenerateFunctions(options = {}) {
	return Diagram([
		Sequence([
			Expression(),
			Keyword("COLLATE"),
			Expression("collation-name")
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateFunctions(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

