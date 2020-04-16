
function GenerateInsert(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("INSERT"),
			Keyword("INTO"),
			GenerateQualifiedTableName(),
			GenerateOptionalColumnList(),
			Choice(0, [
				Sequence(GenerateValues(options)),
				Expression("select-node"),
				Sequence([
					Keyword("DEFAULT"),
					Keyword("VALUES")
				])
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateInsert(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

