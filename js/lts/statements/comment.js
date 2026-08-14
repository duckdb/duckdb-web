
function GenerateCommentOn(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COMMENT ON"),
			Choice(0, [
				Keyword("TABLE"),
				Keyword("COLUMN"),
				Keyword("VIEW"),
				Keyword("INDEX"),
				Keyword("SEQUENCE"),
				Keyword("TYPE"),
				Sequence([Keyword("MACRO"), Optional(Keyword("TABLE"), "skip")]),
			]),
			Expression("entity-name"),
			Keyword("IS"),
			Choice(0, [
				Expression("string-literal"),
				Keyword("NULL"),
			]),
		])
	])
}


function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCommentOn(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()
