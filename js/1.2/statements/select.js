

function GenerateSelect(options = {}) {
	return Diagram([
		Stack([
			Optional(Expandable("common-table-expr", options, "common-table-expr", GenerateCTE), "skip"),
			OneOrMore(Choice(0, [
				Expandable("select-node", options, "select-node", GenerateSelectNode),
				Expandable("values-list", options, "values", GenerateValues)
			]), Expandable("set-operation", options, "set-operation", GenerateSetOperation))
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = GenerateSelect(options).toString();
	document.getElementById("rrdiagram2").innerHTML = Diagram(GenerateCTE(options)).toString();
	document.getElementById("rrdiagram3").innerHTML = Diagram(GenerateSelectClause(options)).toString();
	document.getElementById("rrdiagram4").innerHTML = Diagram(GenerateFromClause(options)).toString();
	document.getElementById("rrdiagram5").innerHTML = Diagram(GenerateWhereClause(options)).toString();
	document.getElementById("rrdiagram6").innerHTML = Diagram(GenerateGroupByClause(options)).toString();
	document.getElementById("rrdiagram7").innerHTML = Diagram(GenerateWindowClause(options)).toString();
	document.getElementById("rrdiagram8").innerHTML = Diagram(GenerateLimitAndOrderBy(options)).toString();
	document.getElementById("rrdiagram9").innerHTML = Diagram(GenerateValues(options)).toString();
	document.getElementById("rrdiagram10").innerHTML = Diagram(GenerateSampleClause(options)).toString();
	document.getElementById("rrdiagram11").innerHTML = Diagram(GenerateQualifyClause(options)).toString();

	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram3").classList.add("limit-width");
	document.getElementById("rrdiagram4").classList.add("limit-width");
	document.getElementById("rrdiagram5").classList.add("limit-width");
	document.getElementById("rrdiagram6").classList.add("limit-width");
	document.getElementById("rrdiagram7").classList.add("limit-width");
	document.getElementById("rrdiagram8").classList.add("limit-width");
	document.getElementById("rrdiagram9").classList.add("limit-width");
	document.getElementById("rrdiagram10").classList.add("limit-width");
	document.getElementById("rrdiagram11").classList.add("limit-width");
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

