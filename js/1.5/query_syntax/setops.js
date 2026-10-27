
function GenerateSetOperationLoop(options) {
	return [OneOrMore(Keyword("select-statement"), Sequence(GenerateSetOperation(options)))]
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = Diagram(GenerateSetOperationLoop(options)).toString();
	document.getElementById("rrdiagram").classList.add("limit-width");
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

