function GenerateCreateTrigger(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("CREATE"),
				GenerateOrReplace(),
				Keyword("TRIGGER"),
				GenerateIfNotExists(),
				Expression("name"),
			]),
			Sequence([
				Choice(0, [
					Keyword("BEFORE"),
					Keyword("AFTER")
				]),
				Choice(0, [
					Keyword("INSERT"),
					Sequence([
						Keyword("UPDATE"),
						Optional(Sequence([
							Keyword("OF"),
							OneOrMore(Expression("column"), Keyword(","))
						]), "skip")
					]),
					Keyword("DELETE")
				]),
				Keyword("ON"),
				Expression("table"),
			]),
			Optional(Sequence([
				Keyword("REFERENCING"),
				OneOrMore(Sequence([
					Choice(0, [
						Keyword("OLD"),
						Keyword("NEW")
					]),
					Keyword("TABLE"),
					Keyword("AS"),
					Expression("alias")
				]))
			]), "skip"),
			Sequence([
				Keyword("FOR EACH"),
				Choice(0, [
					Keyword("ROW"),
					Keyword("STATEMENT")
				]),
				Expression("triggered-statement")
			])
		])
	])
}

function GenerateDropTrigger(options = {}) {
	return Diagram([
		Sequence([
			Keyword("DROP TRIGGER"),
			GenerateIfExists(),
			Expression("name"),
			Keyword("ON"),
			Expression("table")
		]),
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCreateTrigger(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateDropTrigger(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()
