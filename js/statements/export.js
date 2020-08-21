
function GenerateExport(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("EXPORT"),
			Keyword("DATABASE"),
			Expression("directory-name"),
			Expandable("copy-options", options, "copy-from-options", GenerateCopyOptions)
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateExport(options).toString()
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

