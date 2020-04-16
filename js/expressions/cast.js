
function GenerateCast(options = {}) {
	return Diagram([
		Choice(0,[
			Sequence([
				Keyword("CAST"),
				Keyword("("),
				Expression(),
				Keyword("AS"),
				Expression("type-name"),
				Keyword(")")
			]),
			Sequence([
				Expression(),
				Keyword("::"),
				Expression("type-name")
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCast(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

