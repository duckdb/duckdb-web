
function GenerateCase(options = {}) {
	return Diagram([
		Sequence([
			Keyword("CASE"),
			Optional(Expression(), "skip"),
			OneOrMore(Sequence([
				Keyword("WHEN"),
				Expression(),
				Keyword("THEN"),
				Expression()
			])),
			Optional(Sequence([
				Keyword("ELSE"),
				Expression(),
			])),
			Keyword("END")
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCase(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

