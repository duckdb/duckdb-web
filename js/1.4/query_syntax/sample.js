
function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = Diagram(GenerateSampleClause(options)).toString();
	document.getElementById("rrdiagram").classList.add("limit-width");
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

