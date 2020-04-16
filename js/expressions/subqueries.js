
function GenerateScalarSubquery(options = {}) {
	return Diagram([
		Keyword("("),
		Expression("select-node"),
		Keyword(")")
	])
}

function GenerateExists(options = {}) {
	return Diagram([
		Optional(Keyword("NOT"), "skip"),
		Keyword("EXISTS"),
		Keyword("("),
		Expression("select-node"),
		Keyword(")")
	])
}

function GenerateIn(options = {}) {
	return Diagram([
		Optional(Keyword("NOT"), "skip"),
		Keyword("IN"),
		Choice(0, [
			Sequence([
				Keyword("("),
				Expression("select-node"),
				Keyword(")")
			]),
			Sequence([
				Keyword("("),
				OneOrMore(Expression(), ","),
				Keyword(")")
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateScalarSubquery(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateExists(options).toString();
	document.getElementById("rrdiagram3").classList.add("limit-width");
	document.getElementById("rrdiagram3").innerHTML = GenerateIn(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

