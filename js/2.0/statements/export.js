
function GenerateExport(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("EXPORT DATABASE"),
			Expression("directory-name"),
			Expandable("copy-to-options", options, "copy-from-options", GenerateCopyToOptions)
		])
	])
}

function GenerateImport(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("IMPORT DATABASE"),
			Expression("directory-name"),
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateExport(options).toString()
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateImport(options).toString()
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

