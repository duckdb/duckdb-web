
function GenerateLike(options = {}) {
	return Diagram([
		Expression("string"),
		Optional(Keyword("NOT"), "skip"),
		Keyword("LIKE"),
		Expression("pattern"),
		Optional(
			Sequence([
				Keyword('ESCAPE'),
				Expression('escape_character')
			])
		)
	])
}

function GenerateSimilarTo(options = {}) {
	return Diagram([
		Expression("string"),
		Optional(Keyword("NOT"), "skip"),
		Keyword("SIMILAR"),
		Keyword("TO"),
		Expression("pattern")
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateLike(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateSimilarTo(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

