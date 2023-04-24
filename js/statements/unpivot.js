/*


TODO: regrab a new CLI to get the updated UNPIVOT multi-column support
	UNPIVOT monthly_sales ON (jan, feb, mar) as q1, (apr, may, jun) as q2 INTO NAME month VALUE sales_month_1, sales_month2, sales_month3;

CREATE OR REPLACE TABLE monthly_sales(empid INT, dept TEXT, Jan INT, Feb INT, Mar INT, Apr INT, May INT, Jun INT);
INSERT INTO monthly_sales VALUES
(1, 'electronics', 1, 2, 3, 4, 5, 6),
(2, 'clothes', 10, 20, 30, 40, 50, 60),
(3, 'cars', 100, 200, 300, 400, 500, 600);

Shortened syntax
	UNPIVOT [dataset]
	ON [columns]
	INTO 
		NAME [name-column-name]
		VALUE [value-column-name]

	Can also alias the [columns] so the values are renamed as they are stacked

SQL Standard notes
	FROM [dataset]
	UNPIVOT [INCLUDE NULLS] (
		[value-column-name]
		FOR [name-column-name] IN [columns]
	)

	Can do aliases within the IN clause
		FROM monthly_sales UNPIVOT(sales FOR month IN (jan AS January, feb AS February, mar AS March, april))
	Can alias the entire subquery and give column names
		SELECT p.id, p.type, p.m, p.vals FROM monthly_sales UNPIVOT(sales FOR month IN (jan, feb, mar, april)) AS p(id, type, m, vals)

	Can have multiple columns in the output, so it isn't all stacked into just 2 columns
		SELECT empid, dept, month, sales_jan_feb, sales_mar_apr FROM monthly_sales UNPIVOT((sales_jan_feb, sales_mar_apr) FOR month IN ((jan, feb), (mar, april)));
	
	Can only have one column in the FOR though
	
	Can unpivot all columns down into just 2 columns
		SELECT * FROM monthly_sales UNPIVOT(sales FOR month IN (empid, dept, jan, feb, mar, april))

*/
function GenerateUnpivot(options) {
	return Diagram([
		AutomaticStack([
			Choice(0, [
				Keyword("UNPIVOT"),
				Keyword("PIVOT_LONGER")
			]),
			Choice(0, [
				Expression("table-name"),
				Expression("view-name"),
				Expression("table-function-name"),
				Sequence([
					Keyword('('),
					Expression("select-node"),
					Keyword(')'),
				])
			]),
			Sequence([
				Keyword("ON"),
				OneOrMore(
					Sequence([
						Choice(0, [
							Expression("unpivot-column"),
							Sequence([
								Keyword("("),
								OneOrMore(
									Expression("unpivot-column"),
									","
								),
								Keyword(")")
							]),
						]),
						Optional(Sequence([Optional(Keyword("AS")), Expression("alias")])),
					]), ",")
				]),
			Optional(
				Sequence([
					Keyword("INTO"),
					Keyword("NAME"),
					Expression("name-column-name"),
					Keyword("VALUE"),
					OneOrMore(
						Expression("value-column-name"),
						","
					),
				]),
				"skip"),
		])
	])
}


// TODO: GenerateSQLStandardUnpivot
function GenerateSQLStandardUnpivot(options) {
	return Diagram([
		AutomaticStack([
			Keyword("FROM"),
			Choice(0, [
				Expression("table-name"),
				Expression("view-name"),
				Expression("table-function-name"),
				Sequence([
					Keyword('('),
					Expression("select-node"),
					Keyword(')'),
				])
			]),
			Choice(0, [
				Keyword("PIVOT")
			]),
			Keyword("("),
			OneOrMore(
				Sequence([
					Expression("aggregate-expr"),
					Optional(Sequence([Optional(Keyword("AS")), Expression("alias")])),
				]), ","),
			Keyword("FOR"),
			Sequence([
				OneOrMore(
					Sequence([
						Expression("pivot-column"),
						Sequence([
							Keyword("IN"),
							Keyword("("),
							Expression("in-list"),
							Keyword(")"),
						])
					]), " ")
			]),
			Optional(
				Sequence([
					Keyword("GROUP BY"),
					OneOrMore(Expression("group-by-expr"), ","),
				]),
				"skip"),
			Keyword(")"),
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateUnpivot(options).toString();

	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateSQLStandardUnpivot(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

