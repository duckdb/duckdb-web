
function GenerateLogicalFunctions(options = {}) {
	return Diagram([
		Choice(0, [
			Sequence([
				Expression(),
				Choice(0, [
					Keyword("AND"),
					Keyword("OR")
				]),
				Expression()
			]),
			Sequence([
				Keyword("NOT"),
				Expression()
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateLogicalFunctions(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

