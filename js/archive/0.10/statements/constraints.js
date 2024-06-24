function GenerateConstraintSyntax(options = {}) {
    return Diagram(
    	GenerateColumnConstraints(options)
    )
}


function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateConstraintSyntax(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

