function GenerateMerge(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("MERGE INTO"),
            GenerateQualifiedTableName(),
            Optional(
                Sequence([
                    Keyword("AS"),
                    GenerateQualifiedTableName()
                ]),
                "skip"
            ),
            Keyword("USING"),
            Choice(0, [
                Expression("source-table-or-subquery"),
                Sequence([
                    Keyword("("),
                    Expression("select-statement"),
                    Keyword(")")
                ])
            ]),
            Keyword("ON"),
            Expression("match-condition"),
            OneOrMore(
                Choice(0, [
                    Sequence([
                        Keyword("WHEN MATCHED"),
                        Optional(Sequence([Keyword("AND"), Expression("condition")]), "skip"),
                        Keyword("THEN"),
                        Choice(0, [
                            Sequence([
                                Keyword("UPDATE"),
                                Optional(OneOrMore(
                                    Sequence([
                                        Keyword("SET"),
                                        Expression("column-name"),
                                        Keyword("="),
                                        Expression("value-expr")
                                    ]), Keyword(",")
                                ), "skip")
                            ]),
                            Sequence([
                                Keyword("DELETE")
                            ])
                        ])
                    ]),
                    Sequence([
                        Keyword("WHEN NOT MATCHED"),
                        Optional(Sequence([Keyword("AND"), Expression("condition")]), "skip"),
                        Keyword("THEN"),
                        Keyword("INSERT"),
                        Keyword("VALUES"),
                        GenerateOptionalColumnList()
                    ])
                ])
            ),
            Optional(
                Expandable("returning-clause", options, "returning-clause", GenerateReturning),
                "skip"
            )
        ])
    ])
}

function GenerateReturning(options) {
    return [
        Sequence([
            Keyword("RETURNING"),
            Optional(Keyword("*"), "skip"),
            Choice(0, [
                new Skip(),
                OneOrMore(
                    Sequence([Expression(), Optional(Sequence([Optional(Keyword("AS")), Expression("alias")]), "skip")]),
                    ","
                ),
            ]),
        ])
    ]
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram").classList.add("limit-width");
    document.getElementById("rrdiagram").innerHTML = GenerateMerge(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
