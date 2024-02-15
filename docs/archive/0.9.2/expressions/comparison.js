
function GenerateBetween(options = {}) {
	return Diagram([
		Choice(0, [
			Sequence([
				Expression(),
				Optional(Keyword("NOT"), "skip"),
				Keyword("BETWEEN"),
				Expression(),
				Keyword("AND"),
				Expression()
			]),
			Sequence([
				Expression(),
				Keyword("IS"),
				Optional(Keyword("NOT"), "skip"),
				Keyword("NULL"),
			])
		])
	])
}

function GenerateComparison(options = {}) {
	return Diagram([
		Sequence([
			Expression(),
			Expression("binary-operator"),
			Expression()
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateBetween(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateComparison(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

