
function GenerateMacroParams(options = {}) {
	return Sequence([
		Keyword("("),
		Optional(
			Sequence([
				OneOrMore(Sequence([
					Expression("param-name"),
					Optional(Expression("type"), "skip")
				]), Keyword(",")),
				Optional(Keyword(","), "skip")
			]),
			"skip"
		),
		ZeroOrMore(Sequence([
			Expression("param-name"),
			Optional(Expression("type"), "skip"),
			Keyword(":="),
			Expression("default-value")
		]), Keyword(",")),
		Keyword(")")
	]);
}

function GenerateCreateMacro(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("CREATE"),
			GenerateOrReplace(),
			GenerateTemporary(),
			Choice(0, [
				Keyword("MACRO"),
				Keyword("FUNCTION"),
				]
			),
			GenerateIfNotExists(),
			Optional(Sequence([
				Expression("schema-name"),
				Keyword(".")
			]), "skip"),
			Expression("macro-name"),
			OneOrMore(Sequence([
				GenerateMacroParams(),
				Keyword("AS"),
				Optional(Keyword("TABLE"), "skip"),
				Expression("expr")
			]), ",")
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

