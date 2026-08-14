
function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = Diagram(GenerateFromClause(options)).toString();
	document.getElementById("rrdiagram").classList.add("limit-width");
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

