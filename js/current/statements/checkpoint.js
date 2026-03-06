function GenerateCheckpoint(options = {}) {
    return Diagram([
        AutomaticStack([
            Optional(Keyword("FORCE"), "skip"),
            Keyword("CHECKPOINT"),
            Optional(Sequence([
                Expression("database")
            ]))
        ])
    ])
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram1").classList.add("limit-width");
    document.getElementById("rrdiagram1").innerHTML = GenerateCheckpoint(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
