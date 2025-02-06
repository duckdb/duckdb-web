function GenerateSet(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("SET VARIABLE"),
            Expression("variable-name"),
            Choice(0, ["=", Keyword("TO")]),
            Expression("variable-value")
        ])
    ])
}

function GenerateReset(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("RESET VARIABLE"),
            Expression("variable-name")
        ])
    ])
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram1").classList.add("limit-width");
    document.getElementById("rrdiagram1").innerHTML = GenerateSet(options).toString();
    document.getElementById("rrdiagram2").classList.add("limit-width");
    document.getElementById("rrdiagram2").innerHTML = GenerateReset(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
