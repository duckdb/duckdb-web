
function GenerateCreateMacro(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("CREATE"),
			Choice(0, [
				Keyword("MACRO"),
				Keyword("FUNCTION"),
				]
			),
			Keyword("AS"),
			Expression("expr")
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateMacro(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

