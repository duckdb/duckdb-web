
function GenerateWindowFunction(options = {}) {
	return Diagram([
		AutomaticStack([
			Expression("function-name"),
			Keyword("("),
			ZeroOrMore(Sequence([
				Expression()
			]), Keyword(",")),
			Keyword(")"),
			Keyword("OVER"),
			Sequence(GenerateWindowSpec(options))
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateWindowFunction(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

