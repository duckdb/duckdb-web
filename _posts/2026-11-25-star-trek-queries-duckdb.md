---
layout: post
title: "I Don’t Want a Lesson in Computer Science!"
authors:
  - Hannes Mühleisen
thumb: /images/blog/thumbs/star-trek.svg
image: /images/blog/thumbs/star-trek.png
excerpt: "For seven seasons, the crew of the Enterprise talked to the ship’s computer and solved hard data problems. We gave Claude a DuckDB database and the crew’s actual lines to see whether we have the Enterprise computer now."
tags: ["using DuckDB"]
toc: false
body_class: wide-post
---

<!-- markdownlint-disable MD036 -->

I have been a “Trekkie” ever since I watched [Star Trek: The Next Generation](https://en.wikipedia.org/wiki/Star_Trek:_The_Next_Generation) (TNG) on weekday afternoons back in the ’90s. We had grainy terrestrial TV reception because my parents refused to pay for cable. Also, I had to fight my younger sister because she wanted to watch [The Nanny](https://en.wikipedia.org/wiki/The_Nanny) instead, which was on at the same time. Oh, and it was all dubbed into German with a terrible translation. But the magic caught on regardless. Decades later, I am still a huge fan and re-watch episodes regularly.

Recently, the [great Patrick Stewart](https://www.theguardian.com/culture/2026/oct/30/patrick-stewart-jean-luc-picard-star-trek) departed on his last voyage. He is the best captain there ever was. [Captain Picard](https://memory-alpha.fandom.com/wiki/Jean-Luc_Picard)’s style of leadership has always been an inspiration to me. In his honor, let’s revisit some classic *Star Trek: The Next Generation* dialogues in which things happen with data. Let’s start with a quick teaser:

In [“The Battle”](https://www.st-minutiae.com/resources/scripts/110.txt), Picard’s old ship, the [Stargazer](https://memory-alpha.fandom.com/wiki/USS_Stargazer_(NCC-2893)), is handed back to him with a personal log aboard in which he appears to confess to an unprovoked attack on the [Ferengi](https://memory-alpha.fandom.com/wiki/Ferengi). [Data](https://memory-alpha.fandom.com/wiki/Data) (the TNG character, not the bits of information) compares the personal log with the ship’s main computer log and reports to the first officer, commander [William T. Riker](https://memory-alpha.fandom.com/wiki/William_T._Riker).

![Data reports to Riker, with La Forge between them.]({% link images/blog/star-trek/enterprise-computer/the_battle.jpg %}){: width="480" }
*Data reports to Riker, with La Forge between them. <em>Star Trek: The Next Generation</em>, “The Battle” (1987). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>On the bridge</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** By comparing the main Stargazer computer log with Captain Picard’s personal log, I have found “checksum” discrepancies, sir.

**RIKER:** What does that mean?

**DATA:** All information is time-coded by entry, and the bits when totaled produce an aggregate amount which...

**RIKER:** I don’t want a lesson in computer science! Bottom line?

**DATA:** One of these two logs is a forgery.

</td><td markdown="1">

```sql
SELECT log_type,
       count(*) AS entries,
       count(*) FILTER (WHERE checksum = md5(entry))
         AS checksum_valid,
       count(*) FILTER (WHERE checksum <> md5(entry))
         AS checksum_mismatch,
       list(id ORDER BY id)
         FILTER (WHERE checksum <> md5(entry))
         AS mismatched_ids
FROM ship_logs
WHERE ship='USS Stargazer'
GROUP BY log_type
ORDER BY log_type
```

<table class="result">
<tr><th>log_type</th><th>entries</th><th>checksum_valid</th><th>checksum_mismatch</th><th>mismatched_ids</th></tr>
<tr><td>captain&#x27;s personal log</td><td>5</td><td>2</td><td>3</td><td>[9, 10, 11]</td></tr>
<tr><td>main computer log</td><td>7</td><td>7</td><td>0</td><td>NULL</td></tr>
</table>

</td></tr>
</table>

Despite his shocking disregard for Computer Science, Riker gets his bottom line. If we were to express this request for information as a SQL query, it is a `GROUP BY`: recompute the checksum of every log entry, compare it with the one stored when the entry was recorded, and count the mismatches per log. Three of the five entries in the captain’s personal log fail. The main computer log is clean. A smoking gun.

## Do We Have the Enterprise Computer Now?

Even as a wee lad, I noticed something very cool about the Enterprise [D](https://en.wikipedia.org/wiki/USS_Enterprise_(NCC-1701-D)): You could interact with its massive central computer by just talking to it. Very complex questions about all sorts of things would be answered (if Data did not already blurt out the answer immediately). Over many episodes, I watched the intrepid crew of the Enterprise to talk to the computer and solve hard data problems. Back then this was a wild idea. But now, we have things like Claude and we have DuckDB, one component being able to translate human language into more formal things like SQL queries, and the other component being able to process those queries at hard-to-believe speeds.

For Science, we took the actual [shooting scripts](https://www.st-minutiae.com/resources/scripts/) of TNG and had Claude find some of the interactions with the computer that looked like data analysis. I picked eleven scenes.

We then generated a DuckDB database ([`enterprise_computer.duckdb`](https://blobs.duckdb.org/data/enterprise_computer.duckdb)) to stand in for the ship’s records. The data is made up, but it is built so the results are the same as in the dialogue, given correct queries. For example, if the computer says there are 15,525 undetectable substances, the table has 15,525 of them. It also holds believable rows that each condition has to filter out: “Darmok” entries in other sectors and in non-linguistic databases, substances that alter glass but show up on scans, log entries from another ship. The ship’s own date and position sit in a one-row `ship_status` table, which is how “this sector” and “the past six months” get resolved.

Then, we gave a fresh Claude Code session that database and *fed it the actual dialog lines from the Enterprise crew*, translated their data requests to SQL and had them run on DuckDB. Claude was simply told that it is the main computer of the USS Enterprise, the ship’s records are in that database, and it should answer each crew member’s line from it.

Results have been amazing: not only did the “Enterprise computer” answer all the questions, by our reading 40 out of 49 answers matched what the dialogue says. Below are some particularly nice examples:

## More from the Ship’s Records

In [“Darmok”](https://www.st-minutiae.com/resources/scripts/202.txt), the Enterprise meets a people who speak only in references to their own stories. It is a strong contender for my favorite episode of TNG. Counselor [Troi](https://memory-alpha.fandom.com/wiki/Deanna_Troi) and Data have two words to go on, “Darmok” and “Tanagra”. They start talking to the computer.

![Counselor Troi, waiting for the computer.]({% link images/blog/star-trek/enterprise-computer/darmok.jpg %}){: width="480" }
*Counselor Troi, waiting for the computer. <em>Star Trek: The Next Generation</em>, “Darmok” (1991). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>On the bridge</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**TROI:** Computer, search for the term “Darmok” in all linguistic databases compiled for this sector.

**COMPUTER:** Searching... “Darmok” is the name of a seventh dynasty emperor on Kanda Four... A mytho-historical hunter on Shantil Three... A colony on Malindi Seven... A frozen dessert on Razna Five... A --

</td><td markdown="1">

```sql
SELECT l.entry_id, l.term, l.description,
       l.planet, l.sector, l.database_name
FROM library l
WHERE l.category = 'linguistic'
  AND l.term ILIKE '%Darmok%'
  AND l.sector = (SELECT sector FROM ship_status
                  WHERE ship = 'USS Enterprise'
                  ORDER BY ship_date DESC LIMIT 1)
ORDER BY l.database_name, l.planet, l.entry_id
```

<table class="result">
<tr><th>entry_id</th><th>term</th><th>description</th><th>planet</th><th>sector</th><th>database_name</th></tr>
<tr><td>202010</td><td>Darmok</td><td>river</td><td>Beludan II</td><td>El-Adrel</td><td>Federation Linguistic Survey</td></tr>
<tr><td>202127</td><td>Darmok</td><td>clan title</td><td>Belugath V</td><td>El-Adrel</td><td>Federation Linguistic Survey</td></tr>
<tr><td>202091</td><td>Darmok</td><td>harvest festival</td><td>Corarin IX</td><td>El-Adrel</td><td>Federation Linguistic Survey</td></tr>
<tr><td>202055</td><td>Darmok</td><td>spice</td><td>Drensel V</td><td>El-Adrel</td><td>Federation Linguistic Survey</td></tr>
<tr><td>202019</td><td>Darmok</td><td>unit of weight</td><td>Ethamar IX</td><td>El-Adrel</td><td>Federation Linguistic Survey</td></tr>
</table>
<p class="result-note">First 5 of 47 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**TROI:** -- Stop search. Computer, how many entries for “Darmok”?

**COMPUTER:** Forty-seven.

</td><td markdown="1">

```sql
SELECT count(*) AS darmok_entries
FROM library l
WHERE l.category = 'linguistic'
  AND l.term ILIKE '%Darmok%'
  AND l.sector = (SELECT sector FROM ship_status
                  WHERE ship = 'USS Enterprise'
                  ORDER BY ship_date DESC LIMIT 1)
```

<table class="result">
<tr><th>darmok_entries</th></tr>
<tr><td>47</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** Computer, search for the term “Tanagra.” All databases.

**COMPUTER:** Searching... Tanagra is the name of the ruling family on Gallos Two... A ceremonial drink on Lerishi Four... An island-continent on Shantil Three --

**DATA:** -- Stop.

</td><td markdown="1">

```sql
SELECT entry_id, term, description, planet,
       sector, database_name, category
FROM library WHERE term ILIKE '%Tanagra%'
ORDER BY database_name, planet, entry_id
```

<table class="result">
<tr><th>entry_id</th><th>term</th><th>description</th><th>planet</th><th>sector</th><th>database_name</th><th>category</th></tr>
<tr><td>202205</td><td>Tanagra</td><td>wedding dance</td><td>Ethadan V</td><td>El-Adrel</td><td>Federation Cultural Survey</td><td>cultural</td></tr>
<tr><td>202209</td><td>Tanagra</td><td>winter solstice feast</td><td>Ivomar IV</td><td>Ostrel</td><td>Federation Cultural Survey</td><td>cultural</td></tr>
<tr><td>202202</td><td>Tanagra</td><td>ceremonial drink</td><td>Lerishi IV</td><td>El-Adrel</td><td>Federation Cultural Survey</td><td>cultural</td></tr>
<tr><td>202201</td><td>Tanagra</td><td>ruling family</td><td>Gallos II</td><td>El-Adrel</td><td>Federation Historical Archive</td><td>historical</td></tr>
<tr><td>202208</td><td>Tanagra</td><td>guild of weavers</td><td>Halithos VII</td><td>Mendar</td><td>Federation Linguistic Survey</td><td>linguistic</td></tr>
</table>
<p class="result-note">First 5 of 11 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**TROI:** Shantil Three? Computer, cross-reference the last entry with the previous search index.

**COMPUTER:** “Darmok” is the name of a mytho-historical hunter on Shantil Three.

</td><td markdown="1">

```sql
SELECT t.planet, t.sector,
       d.term AS darmok_term,
       d.description AS darmok_meaning,
       d.database_name AS darmok_database,
       t.term AS tanagra_term,
       t.description AS tanagra_meaning,
       t.database_name AS tanagra_database
FROM library t
JOIN library d ON d.planet = t.planet
              AND d.term ILIKE '%Darmok%'
WHERE t.term ILIKE '%Tanagra%'
  AND t.planet = 'Shantil III'
```

<table class="result">
<tr><th>planet</th><th>sector</th><th>darmok_term</th><th>darmok_meaning</th><th>darmok_database</th><th>tanagra_term</th><th>tanagra_meaning</th><th>tanagra_database</th></tr>
<tr><td>Shantil III</td><td>El-Adrel</td><td>Darmok</td><td>mytho-historical hunter</td><td>Starfleet Xenolinguistics Archive</td><td>Tanagra</td><td>island-continent</td><td>Stellar Cartography Gazetteer</td></tr>
</table>

</td></tr>
</table>

A search with too many hits, a count, a second search, and a join (a join!) that takes 47 rows down to one. Nobody on the bridge wrote any of the right-hand column. They asked, the computer answered, and they asked a sharper question.

In [“Hollow Pursuits”](https://www.st-minutiae.com/resources/scripts/169.txt) the ship is about to tear itself apart and Geordi narrows the cause one sentence at a time.

![The five remaining substances on the Engineering console.]({% link images/blog/star-trek/enterprise-computer/hollow_pursuits.jpg %}){: width="480" }
*The five remaining substances on the Engineering console. <em>Star Trek: The Next Generation</em>, “Hollow Pursuits” (1990). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In Engineering</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Computer, list all physical substances that wouldn’t normally be picked up by internal scans.

**COMPUTER:** There are fifteen thousand five hundred twenty-five known substances that cannot be detected by standard scans.

</td><td markdown="1">

```sql
SELECT name, stable_in_oxygen, alters_materials,
       half_life_s, toxicity, last_used_year
FROM substances
WHERE NOT detectable_by_internal_scan
ORDER BY name
```

<table class="result">
<tr><th>name</th><th>stable_in_oxygen</th><th>alters_materials</th><th>half_life_s</th><th>toxicity</th><th>last_used_year</th></tr>
<tr><td>Bryakbenate</td><td>false</td><td>[polymer]</td><td>309.0</td><td>high</td><td>NULL</td></tr>
<tr><td>Bryakbenide</td><td>false</td><td>[duranium, polymer]</td><td>inf</td><td>low</td><td>2187</td></tr>
<tr><td>Bryakbenon</td><td>false</td><td>[]</td><td>263026.8</td><td>low</td><td>2343</td></tr>
<tr><td>Bryakboride</td><td>false</td><td>[tritanium, ceramic]</td><td>186208.7</td><td>moderate</td><td>2239</td></tr>
<tr><td>Bryakborite</td><td>false</td><td>[]</td><td>inf</td><td>moderate</td><td>2222</td></tr>
</table>
<p class="result-note">First 5 of 15,525 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Great. How many of those can exist in an oxygen atmosphere?

**COMPUTER:** Five hundred thirty-two.

</td><td markdown="1">

```sql
SELECT count(*) AS undetectable_and_stable_in_oxygen
FROM substances
WHERE NOT detectable_by_internal_scan
  AND stable_in_oxygen
```

<table class="result">
<tr><th>undetectable_and_stable_in_oxygen</th></tr>
<tr><td>532</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** And could alter molecular structure when it comes in contact with... with glass.

**COMPUTER:** Five.

</td><td markdown="1">

```sql
SELECT name, alters_materials, half_life_s,
       toxicity, last_used_year, molecular_structure
FROM substances
WHERE NOT detectable_by_internal_scan
  AND stable_in_oxygen
  AND list_contains(alters_materials, 'glass')
ORDER BY name
```

<table class="result">
<tr><th>name</th><th>alters_materials</th><th>half_life_s</th><th>toxicity</th><th>last_used_year</th><th>molecular_structure</th></tr>
<tr><td>Invidium</td><td>[glass]</td><td>inf</td><td>low</td><td>2259</td><td>MSG-16900005</td></tr>
<tr><td>Jakmanite</td><td>[glass]</td><td>15.0</td><td>moderate</td><td>NULL</td><td>MSG-16900001</td></tr>
<tr><td>Lucrovexitrin</td><td>[glass]</td><td>inf</td><td>extreme</td><td>NULL</td><td>MSG-16900003</td></tr>
<tr><td>Saltzgadum</td><td>[glass]</td><td>inf</td><td>low</td><td>2331</td><td>MSG-16900004</td></tr>
<tr><td>Selgninaem</td><td>[glass]</td><td>inf</td><td>extreme</td><td>NULL</td><td>MSG-16900002</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BARCLAY:** Jakmanite has a half life of about fifteen seconds. There wouldn’t be enough time to spread it around the ship.

**WESLEY:** Selgninaem and Lucrovexitrin are extremely toxic.

**GEORDI:** We’d all be dead by now. That leaves Saltzgadum and Invidium.

</td><td markdown="1">

```sql
SELECT name, half_life_s, toxicity, last_used_year,
  CASE WHEN half_life_s <= 15
         THEN 'eliminated: half-life too short'
       WHEN toxicity = 'extreme'
         THEN 'eliminated: extremely toxic'
       ELSE 'remaining' END AS status
FROM substances
WHERE NOT detectable_by_internal_scan
  AND stable_in_oxygen
  AND list_contains(alters_materials, 'glass')
ORDER BY status DESC, name
```

<table class="result">
<tr><th>name</th><th>half_life_s</th><th>toxicity</th><th>last_used_year</th><th>status</th></tr>
<tr><td>Invidium</td><td>inf</td><td>low</td><td>2259</td><td>remaining</td></tr>
<tr><td>Saltzgadum</td><td>inf</td><td>low</td><td>2331</td><td>remaining</td></tr>
<tr><td>Jakmanite</td><td>15.0</td><td>moderate</td><td>NULL</td><td>eliminated: half-life too short</td></tr>
<tr><td>Lucrovexitrin</td><td>inf</td><td>extreme</td><td>NULL</td><td>eliminated: extremely toxic</td></tr>
<tr><td>Selgninaem</td><td>inf</td><td>extreme</td><td>NULL</td><td>eliminated: extremely toxic</td></tr>
</table>

</td></tr>
</table>

Every sentence is one more predicate: 15,525, then 532, then 5, then 2.

## Try It Yourself

The database is one single DuckDB database, and DuckDB can attach it straight from the web:

```sql
ATTACH 'https://blobs.duckdb.org/data/enterprise_computer.duckdb';
USE enterprise_computer;
```

Run any of the queries above, or hand the file to your assistant, tell it that it is the main computer of the USS Enterprise, and start with: *Computer, search for the term “Darmok” in all linguistic databases compiled for this sector.* No lesson in computer science required, I promise. If you want, you can even [install our Claude plugin](https://duckdb.org/docs/2.0/installation?platform=macos&environment=claude) to make it even smoother.

**To boldly go where no-one has gone before.** I think we can claim that at least that part of the Enterprise computer is now a reality, at least given enough data.

## Appendix: The Other Scenes

The rest of the scenes we picked, run the same way. On the left is the script. On the right is the query Claude ran for that step, with the first rows of its actual result. Where Claude’s answer departed from the dialogue, a note says how.

### Conspiracy

[Script](https://www.st-minutiae.com/resources/scripts/125.txt). Season 1. Picard suspects Starfleet Command has been infiltrated and sets Data to reading its orders.

![The “Starbase Ops Status” display, with the posts Data flagged marked in red.]({% link images/blog/star-trek/enterprise-computer/conspiracy.jpg %}){: width="480" }
*The “Starbase Ops Status” display, with the posts Data flagged marked in red. <em>Star Trek: The Next Generation</em>, “Conspiracy” (1988). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** Computer -- this is Lieutenant Commander Data. Access all Starfleet Command orders to starships, starbases and colonies, for the past six months.

**COMPUTER:** Working.

</td><td markdown="1">

```sql
SELECT o.id, o.issued_at, o.issued_by, o.recipient_type, o.recipient,
       o.order_type, o.personnel_id, o.new_post, o.division
FROM starfleet_orders o
WHERE o.recipient_type IN ('starship','starbase','colony')
  AND o.issued_at > (SELECT max(ship_date) FROM ship_status
    WHERE ship='USS Enterprise') - INTERVAL 6 MONTH
  AND o.issued_at <= (SELECT max(ship_date) FROM ship_status
    WHERE ship='USS Enterprise')
ORDER BY o.issued_at, o.id
```

<table class="result">
<tr><th>id</th><th>issued_at</th><th>issued_by</th><th>recipient_type</th><th>recipient</th><th>order_type</th><th>personnel_id</th><th>new_post</th><th>division</th></tr>
<tr><td>185</td><td>2368-04-11</td><td>Starfleet Command, Personnel</td><td>starbase</td><td>Starbase 69</td><td>survey directive</td><td>NULL</td><td>NULL</td><td>medical</td></tr>
<tr><td>549</td><td>2368-04-11</td><td>Starfleet Command, Security</td><td>starbase</td><td>Starbase 162</td><td>maintenance schedule</td><td>NULL</td><td>NULL</td><td>engineering</td></tr>
<tr><td>913</td><td>2368-04-11</td><td>Starfleet Command, Operations</td><td>colony</td><td>Sandoval Prime colony</td><td>training exercise</td><td>NULL</td><td>NULL</td><td>sciences</td></tr>
<tr><td>1277</td><td>2368-04-11</td><td>Starfleet Command, Logistics</td><td>colony</td><td>Corlan VII outpost</td><td>escort duty</td><td>NULL</td><td>NULL</td><td>operations</td></tr>
<tr><td>1641</td><td>2368-04-11</td><td>Starfleet Command, Tactical</td><td>starship</td><td>USS Castellan</td><td>patrol assignment</td><td>NULL</td><td>NULL</td><td>command</td></tr>
</table>
<p class="result-note">First 5 of 1,207 rows.</p>

*Not what the script says: Reports 1,207 orders, not 1,214: it used a strict ‘>’ on the six-month boundary, so the seven orders dated exactly six months back (2368-04-10) are left out.*

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** My orders were to search for abnormal patterns in Starfleet’s directives. I believe I have found just that.

**DATA:** These are various outposts and starbases where I have detected unusual activity over the past few months.

</td><td markdown="1">

```sql
SELECT recipient, recipient_type,
  count(*) AS irregular_reassignments,
  count(*) FILTER (WHERE division='command') AS command_posts,
  count(*) FILTER (WHERE division='security') AS security_posts,
  count(*) FILTER (WHERE division='operations') AS operations_posts,
  count(DISTINCT issued_by) AS issuing_offices,
  min(issued_at) AS first_issued, max(issued_at) AS last_issued
FROM starfleet_orders
WHERE order_type='personnel reassignment'
  AND issued_by <> 'Starfleet Command, Personnel'
GROUP BY recipient, recipient_type
ORDER BY irregular_reassignments DESC, recipient
```

<table class="result">
<tr><th>recipient</th><th>recipient_type</th><th>irregular_reassignments</th><th>command_posts</th><th>security_posts</th><th>operations_posts</th><th>issuing_offices</th><th>first_issued</th><th>last_issued</th></tr>
<tr><td>Starbase 93</td><td>starbase</td><td>11</td><td>9</td><td>1</td><td>1</td><td>5</td><td>2368-06-05</td><td>2368-08-25</td></tr>
<tr><td>Tyrus Minor outpost</td><td>colony</td><td>10</td><td>8</td><td>1</td><td>1</td><td>5</td><td>2368-06-10</td><td>2368-08-21</td></tr>
<tr><td>Starbase 175</td><td>starbase</td><td>9</td><td>7</td><td>1</td><td>1</td><td>5</td><td>2368-06-15</td><td>2368-08-27</td></tr>
<tr><td>Starbase 31</td><td>starbase</td><td>8</td><td>6</td><td>1</td><td>1</td><td>5</td><td>2368-06-20</td><td>2368-09-09</td></tr>
<tr><td>Lyris Beta outpost</td><td>colony</td><td>7</td><td>5</td><td>1</td><td>1</td><td>5</td><td>2368-07-04</td><td>2368-09-22</td></tr>
</table>

```sql
SELECT issued_by <> 'Starfleet Command, Personnel' AS outside_personnel_office, issued_at > DATE '2368-04-10' AS past_six_months, count(*) n, count(DISTINCT recipient) recipients, min(issued_at), max(issued_at)
FROM starfleet_orders
WHERE order_type='personnel reassignment'
GROUP BY ALL
ORDER BY ALL
```

<table class="result">
<tr><th>outside_personnel_office</th><th>past_six_months</th><th>n</th><th>recipients</th><th>min(issued_at)</th><th>max(issued_at)</th></tr>
<tr><td>false</td><td>false</td><td>271</td><td>76</td><td>2367-08-20</td><td>2368-04-10</td></tr>
<tr><td>false</td><td>true</td><td>238</td><td>76</td><td>2368-04-11</td><td>2368-10-02</td></tr>
<tr><td>true</td><td>true</td><td>45</td><td>5</td><td>2368-06-05</td><td>2368-09-22</td></tr>
</table>

*Not what the script says: Finds the same five installations, but by a different signal: reassignments issued by offices other than Personnel (45 orders). It does not report the command reassignment counts 13, 11, 10, 9, 8.*

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**PICARD:** What sort of activity?

**DATA:** An uncustomary reshuffling of personnel, usually in the command areas. The new officers have had abnormally frequent contact with the highest levels of Starfleet Command.

</td><td markdown="1">

```sql
SELECT order_type, division, count(*) AS orders,
       count(DISTINCT personnel_id) AS officers_moved,
       count(DISTINCT new_post) AS destinations,
       count(DISTINCT issued_by) AS issuing_offices,
       min(issued_at) AS first_issued, max(issued_at) AS last_issued
FROM starfleet_orders
WHERE order_type='personnel reassignment'
  AND issued_by <> 'Starfleet Command, Personnel'
GROUP BY order_type, division ORDER BY orders DESC
```

<table class="result">
<tr><th>order_type</th><th>division</th><th>orders</th><th>officers_moved</th><th>destinations</th><th>issuing_offices</th><th>first_issued</th><th>last_issued</th></tr>
<tr><td>personnel reassignment</td><td>command</td><td>35</td><td>35</td><td>5</td><td>5</td><td>2368-06-05</td><td>2368-08-25</td></tr>
<tr><td>personnel reassignment</td><td>security</td><td>5</td><td>5</td><td>5</td><td>1</td><td>2368-07-01</td><td>2368-08-22</td></tr>
<tr><td>personnel reassignment</td><td>operations</td><td>5</td><td>5</td><td>5</td><td>1</td><td>2368-08-01</td><td>2368-09-22</td></tr>
</table>

*Not what the script says: Describes the reshuffling, mainly in command areas, but does not look at communications, so the ‘abnormally frequent contact with Starfleet Command’ part is missing.*

</td></tr>
</table>

### The Neutral Zone

[Script](https://www.st-minutiae.com/resources/scripts/126.txt). Season 1. Clare Raymond, revived after 370 years in cryonic sleep, asks what became of her sons. Even has a recursive subquery!

![The record the search ends on: Thomas Raymond, with residence, employment, spouse and offspring.]({% link images/blog/star-trek/enterprise-computer/neutral_zone.jpg %}){: width="480" }
*The record the search ends on: Thomas Raymond, with residence, employment, spouse and offspring. <em>Star Trek: The Next Generation</em>, “The Neutral Zone” (1988). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**TROI:** Computer - this is Counselor Troi. Request personal history on... What are their names?

**CLARE:** Tommy -- he’s eight, and Eddie’s five.

**COMPUTER:** Full names -- Date and place of birth.

</td><td markdown="1">

```sql
SELECT p.full_name, p.birth_date, p.birth_place, p.occupation,
       p.residence, p.living, src.source, src.record_date,
       src.record_type, src.details
FROM people p
JOIN people m ON m.id = p.parent_id AND m.full_name = 'Clare Raymond'
  AND m.occupation = 'homemaker'
LEFT JOIN (
  SELECT person_id, 'civil' AS source, record_date, record_type,
         planet || ': ' || details AS details
  FROM civil_records
  UNION ALL
  SELECT person_id, 'medical', record_date, 'death',
         concat_ws('; ', cause_of_death, pathogen, facility)
  FROM medical_records
) src ON src.person_id = p.id
WHERE p.full_name IN ('Thomas Raymond','Edward Raymond')
ORDER BY p.id, src.record_date
```

<table class="result">
<tr><th>full_name</th><th>birth_date</th><th>birth_place</th><th>occupation</th><th>residence</th><th>living</th><th>source</th><th>record_date</th><th>record_type</th><th>details</th></tr>
<tr><td>Thomas Raymond</td><td>1986-02-17</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td><td>NULL</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>Edward Raymond</td><td>NULL</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td><td>NULL</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
</table>

*Not what the script says: The script’s computer asks for full names, date and place of birth. Claude found both sons under Clare Raymond straight away.*

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**CLARE:** They were born in Secaucus - that’s in Jersey.

**CLARE:** Date of birth. Tommy was born February seventeenth...

</td><td markdown="1">

```sql
SELECT p.id, p.full_name, p.birth_date, p.birth_place,
       par.full_name AS parent, p.occupation, p.living
FROM people p LEFT JOIN people par ON par.id = p.parent_id
WHERE p.birth_place ILIKE 'Secaucus%' AND month(p.birth_date) = 2
  AND day(p.birth_date) = 17
  AND (p.full_name ILIKE 'Thomas %' OR p.full_name ILIKE 'Tom%')
ORDER BY p.birth_date, p.id
```

<table class="result">
<tr><th>id</th><th>full_name</th><th>birth_date</th><th>birth_place</th><th>parent</th><th>occupation</th><th>living</th></tr>
<tr><td>2</td><td>Thomas Raymond</td><td>1986-02-17</td><td>Secaucus, New Jersey</td><td>Clare Raymond</td><td>NULL</td><td>false</td></tr>
<tr><td>22</td><td>Thomas Ramirez</td><td>1986-02-17</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**CLARE:** I’m in a world of strangers. I wish I knew what happened to my children. Did they get married, did they have kids...

**TROI:** Let’s see if we can find out.

**TROI:** I have found something.

**TROI:** I have been able to locate a family living outside of Indianapolis. The man’s name is Thomas Raymond.

</td><td markdown="1">

```sql
WITH RECURSIVE tree AS (
  SELECT c.id, c.full_name, c.birth_date, c.birth_place, c.occupation,
         c.residence, c.living, c.parent_id, 1 AS generation,
         c.full_name AS line
  FROM people c JOIN people m ON m.id = c.parent_id
  WHERE m.full_name = 'Clare Raymond' AND m.occupation = 'homemaker'
  UNION ALL
  SELECT c.id, c.full_name, c.birth_date, c.birth_place, c.occupation,
         c.residence, c.living, c.parent_id, t.generation + 1,
         t.line || ' > ' || c.full_name
  FROM people c JOIN tree t ON c.parent_id = t.id
)
SELECT t.generation, t.full_name, t.birth_date, t.birth_place,
       t.occupation, t.residence, t.living, par.full_name AS parent,
  (SELECT count(*) FROM people k WHERE k.parent_id = t.id) AS children,
  (SELECT string_agg(cr.record_type || ' ' || cr.record_date || ': ' || cr.details, ' | ') FROM civil_records cr WHERE cr.person_id = t.id) AS civil_records
FROM tree t JOIN people par ON par.id = t.parent_id
ORDER BY t.generation, t.birth_date
```

<table class="result">
<tr><th>generation</th><th>full_name</th><th>birth_date</th><th>birth_place</th><th>occupation</th><th>residence</th><th>living</th><th>parent</th><th>children</th><th>civil_records</th></tr>
<tr><td>1</td><td>Thomas Raymond</td><td>1986-02-17</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td><td>Clare Raymond</td><td>2</td><td>NULL</td></tr>
<tr><td>1</td><td>Edward Raymond</td><td>NULL</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td><td>Clare Raymond</td><td>0</td><td>NULL</td></tr>
<tr><td>2</td><td>Helen Raymond</td><td>2041-09-30</td><td>Newark, New Jersey</td><td>teacher</td><td>NULL</td><td>false</td><td>Thomas Raymond</td><td>1</td><td>NULL</td></tr>
<tr><td>2</td><td>Paul Raymond</td><td>2046-06-02</td><td>Newark, New Jersey</td><td>musician</td><td>NULL</td><td>false</td><td>Thomas Raymond</td><td>0</td><td>NULL</td></tr>
<tr><td>3</td><td>Marcus Raymond</td><td>2099-04-12</td><td>Chicago, Illinois</td><td>engineer</td><td>NULL</td><td>false</td><td>Helen Raymond</td><td>2</td><td>NULL</td></tr>
</table>
<p class="result-note">First 5 of 14 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**TROI:** Computer -- let us see Thomas Raymond.

**CLARE:** Oh, my God... It’s Donald... that’s my husband.

**TROI:** Actually, it’s your great, great, great, great, great grandson.

</td><td markdown="1">

```sql
SELECT p.id, p.full_name, p.birth_date, p.birth_place,
       par.full_name AS parent, p.residence, p.living, p.portrait
FROM people p LEFT JOIN people par ON par.id = p.parent_id
WHERE p.full_name = 'Thomas Raymond'
ORDER BY p.portrait IS NULL, p.birth_date DESC
```

<table class="result">
<tr><th>id</th><th>full_name</th><th>birth_date</th><th>birth_place</th><th>parent</th><th>residence</th><th>living</th><th>portrait</th></tr>
<tr><td>9</td><td>Thomas Raymond</td><td>2338-05-14</td><td>Indianapolis, Indiana</td><td>Catherine Raymond</td><td>outside Indianapolis, Indiana, Earth</td><td>true</td><td>semi-line drawing of a man around thirty</td></tr>
<tr><td>2</td><td>Thomas Raymond</td><td>1986-02-17</td><td>Secaucus, New Jersey</td><td>Clare Raymond</td><td>NULL</td><td>false</td><td>NULL</td></tr>
<tr><td>19</td><td>Thomas Raymond</td><td>1971-02-17</td><td>Dayton, Ohio</td><td>NULL</td><td>NULL</td><td>false</td><td>NULL</td></tr>
<tr><td>20</td><td>Thomas Raymond</td><td>1952-08-17</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td><td>NULL</td></tr>
<tr><td>21</td><td>Thomas Raymond</td><td>1947-02-07</td><td>Secaucus, New Jersey</td><td>NULL</td><td>NULL</td><td>false</td><td>NULL</td></tr>
</table>

</td></tr>
</table>

### The Vengeance Factor

[Script](https://www.st-minutiae.com/resources/scripts/157.txt). Season 3. Two people have died of the same engineered virus, decades apart. The Acamarian databases say what they had in common.

![Volnoth’s entry in the Acamarian planetary database, with the clan affiliation that links the two deaths.]({% link images/blog/star-trek/enterprise-computer/vengeance_factor.jpg %}){: width="480" }
*Volnoth’s entry in the Acamarian planetary database, with the clan affiliation that links the two deaths. <em>Star Trek: The Next Generation</em>, “The Vengeance Factor” (1989). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** Commander, I’m afraid the only entry on Volnoth in the Acamarian database is a birth record.

**RIKER:** Probably one of the last of the Gatherers to be born on their planet.

*Nobody speaks this request in the script. Claude was asked: “Data -- got anything in the Acamarian database on Volnoth?”*

</td><td markdown="1">

```sql
SELECT p.name, p.affiliation, p.clan, p.born, p.died,
       date_diff('year', p.born, p.died) AS age_at_death,
  (SELECT count(*) FROM image_archive i WHERE i.planet ILIKE 'Acamar%'
    AND (array_to_string(i.people_tagged,
         ',') ILIKE '%Volnoth%' OR i.caption ILIKE '%Volnoth%')) AS images,
  (SELECT string_agg(f.clan_a || ' vs ' || f.clan_b || ' (' || f.started || '-' || coalesce(f.ended::VARCHAR,'') || '): ' || f.outcome || ', survivors ' || f.survivors, ' | ') FROM clan_feuds f WHERE p.clan IN (f.clan_a, f.clan_b)) AS clan_feuds
FROM persons p WHERE p.name ILIKE '%Volnoth%'
```

<table class="result">
<tr><th>name</th><th>affiliation</th><th>clan</th><th>born</th><th>died</th><th>age_at_death</th><th>images</th><th>clan_feuds</th></tr>
<tr><td>Volnoth</td><td>Gatherer</td><td>Lornack</td><td>2264-03-14</td><td>2366-07-24</td><td>102</td><td>0</td><td>Tralesta vs Lornack (2086-2286): Tralesta clan massacred by the Lor…</td></tr>
</table>

*Not what the script says: Gives the birth date and clan Lornack, plus the death and clan history; the dialogue’s point is that the Acamarian database holds only the birth record.*

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BEVERLY:** I’ve been digging through the medical database from Acamar Three for hours and I’ve found another victim of the microvirus that killed Volnoth. But just one.

**BEVERLY:** Fifty-three years ago. A Gatherer named Penthor-Mul.

*Nobody speaks this request in the script. Claude was asked: “Computer, search the medical database from Acamar Three for any other victims of the microvirus that killed Volnoth.”*

</td><td markdown="1">

```sql
SELECT m.id, p.name, p.affiliation, p.clan, p.born, p.died,
       m.record_date, m.cause_of_death, m.pathogen, m.facility
FROM medical_records m JOIN persons p ON p.id = m.person_id
WHERE m.pathogen = (SELECT v.pathogen FROM medical_records v
    JOIN persons vp ON vp.id = v.person_id WHERE vp.name = 'Volnoth')
ORDER BY m.record_date
```

<table class="result">
<tr><th>id</th><th>name</th><th>affiliation</th><th>clan</th><th>born</th><th>died</th><th>record_date</th><th>cause_of_death</th><th>pathogen</th><th>facility</th></tr>
<tr><td>157201</td><td>Penthor-Mul</td><td>Gatherer</td><td>Lornack</td><td>NULL</td><td>2313-05-02</td><td>2313-05-02</td><td>heart attack</td><td>Acamarian microvirus</td><td>Acamar III medical database</td></tr>
<tr><td>157202</td><td>Volnoth</td><td>Gatherer</td><td>Lornack</td><td>2264-03-14</td><td>2366-07-24</td><td>2366-07-24</td><td>cardiac arrest</td><td>Acamarian microvirus</td><td>USS Enterprise sickbay</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**RIKER:** Data -- got anything in your files on this Penthor-Mul?

**DATA:** Yes. He was captured while leading a Gatherer raid on an Acamarian outpost. He died of a heart attack before his trial ended. Commander, he was a member of the Lornack Clan.

</td><td markdown="1">

```sql
SELECT 'person' AS src, p.id, p.name AS item, p.born::VARCHAR AS date1,
       p.died::VARCHAR AS date2,
       p.affiliation || ', clan ' || p.clan AS detail
FROM persons p
WHERE p.name ILIKE '%Penthor%'
UNION ALL
SELECT 'medical', m.id, m.cause_of_death, m.record_date::VARCHAR, NULL,
       m.pathogen || '; ' || m.facility
FROM medical_records m
JOIN persons p ON p.id = m.person_id
WHERE p.name ILIKE '%Penthor%'
UNION ALL
SELECT 'civil', c.id, c.record_type, c.record_date::VARCHAR, NULL,
       c.planet || ': ' || c.details
FROM civil_records c
JOIN persons p ON p.id = c.person_id
WHERE p.name ILIKE '%Penthor%'
UNION ALL
SELECT 'image', i.id, i.caption, i.taken::VARCHAR, NULL,
       i.planet || '; tagged: ' || array_to_string(i.people_tagged,
       ', ')
FROM image_archive i
WHERE i.caption ILIKE '%Penthor%' OR array_to_string(i.people_tagged,
       ',') ILIKE '%Penthor%'
UNION ALL
SELECT 'library', l.entry_id, l.term, NULL, NULL, l.description
FROM library l
WHERE l.term ILIKE '%Penthor%' OR l.description ILIKE '%Penthor%'
ORDER BY src, date1
```

<table class="result">
<tr><th>src</th><th>id</th><th>item</th><th>date1</th><th>date2</th><th>detail</th></tr>
<tr><td>civil</td><td>157103</td><td>arrest</td><td>2313-03-11</td><td>NULL</td><td>Acamar III: Captured while leading a Gatherer raid on an Acamarian …</td></tr>
<tr><td>civil</td><td>157104</td><td>trial</td><td>2313-04-20</td><td>NULL</td><td>Acamar III: Trial opened</td></tr>
<tr><td>civil</td><td>157105</td><td>death</td><td>2313-05-02</td><td>NULL</td><td>Acamar III: Died of a heart attack before his trial ended</td></tr>
<tr><td>image</td><td>157402</td><td>Gatherer raid leader Penthor-Mul in custody at the outpost</td><td>2313-03-11</td><td>NULL</td><td>Acamar III; tagged: Penthor-Mul</td></tr>
<tr><td>image</td><td>157401</td><td>Penthor-Mul being led from his trial</td><td>2313-04-27</td><td>NULL</td><td>Acamar III; tagged: Penthor-Mul</td></tr>
</table>
<p class="result-note">First 5 of 7 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**RIKER:** Display Volnoth’s birth record again.

**BEVERLY:** Lornack... the same clan....

**RIKER:** The only two recorded deaths from this microvirus... members of the same clan... what does that tell us, Doctor?

**BEVERLY:** If these microbes were engineered for murder, I’d say somebody’s going after the whole family.

</td><td markdown="1">

```sql
SELECT p.name, p.affiliation, p.clan, p.born, c.record_type,
       c.record_date, c.planet, c.details
FROM persons p
LEFT JOIN civil_records c ON c.person_id = p.id
  AND c.record_type ILIKE '%birth%'
WHERE p.name = 'Volnoth'
```

<table class="result">
<tr><th>name</th><th>affiliation</th><th>clan</th><th>born</th><th>record_type</th><th>record_date</th><th>planet</th><th>details</th></tr>
<tr><td>Volnoth</td><td>Gatherer</td><td>Lornack</td><td>2264-03-14</td><td>birth</td><td>2264-03-14</td><td>Acamar III</td><td>Born to the clan Lornack</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** Commander, Chorgan, the present leader of the Gatherers, is also from the Lornack clan.

*Nobody speaks this request in the script. Claude was asked: “Data, is anyone else from the Lornack clan still alive?”*

</td><td markdown="1">

```sql
SELECT p.id, p.name, p.affiliation, p.clan, p.born, p.died
FROM persons p
WHERE p.clan = 'Lornack' AND p.died IS NULL
  AND NOT EXISTS (SELECT 1 FROM civil_records c WHERE c.person_id = p.id
    AND c.record_type = 'death')
  AND NOT EXISTS (SELECT 1 FROM medical_records m
      WHERE m.person_id = p.id AND m.cause_of_death IS NOT NULL)
ORDER BY p.born
```

<table class="result">
<tr><th>id</th><th>name</th><th>affiliation</th><th>clan</th><th>born</th><th>died</th></tr>
<tr><td>157003</td><td>Chorgan</td><td>Gatherer</td><td>Lornack</td><td>NULL</td><td>NULL</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**RIKER:** I want to know just how this clan was involved in the Acamarian blood feuds... any clues to their enemies you can find...

**DATA:** Sir, eighty years ago, the Lornacks massacred a rival clan, the Tralestas. It ended a feud that had lasted for two hundred years.

**RIKER:** Ended it?

**DATA:** According to these records, there were no survivors. The Tralesta clan was annihilated.

</td><td markdown="1">

```sql
SELECT f.id, f.planet, f.clan_a, f.clan_b, f.started, f.ended,
       f.ended - f.started AS years, f.outcome, f.survivors,
  CASE WHEN f.clan_a = 'Lornack' THEN f.clan_b ELSE f.clan_a END AS enemy_clan,
  (SELECT count(*) FROM persons p
      WHERE p.clan = CASE WHEN f.clan_a = 'Lornack' THEN f.clan_b ELSE f.clan_a END) AS enemy_persons_on_file,
  (SELECT string_agg(p.name || ' (' || coalesce(p.affiliation,'?') || ', born ' || coalesce(p.born::VARCHAR,'?') || ', died ' || coalesce(p.died::VARCHAR,'no record') || ')', '; ') FROM persons p WHERE p.clan = CASE WHEN f.clan_a = 'Lornack' THEN f.clan_b ELSE f.clan_a END) AS enemy_persons
FROM clan_feuds f
WHERE 'Lornack' IN (f.clan_a, f.clan_b)
ORDER BY f.started
```

<table class="result">
<tr><th>id</th><th>planet</th><th>clan_a</th><th>clan_b</th><th>started</th><th>ended</th><th>years</th><th>outcome</th><th>survivors</th><th>enemy_clan</th><th>enemy_persons_on_file</th><th>enemy_persons</th></tr>
<tr><td>157301</td><td>Acamar III</td><td>Tralesta</td><td>Lornack</td><td>2086</td><td>2286</td><td>200</td><td>Tralesta clan massacred by the Lornacks</td><td>0</td><td>Tralesta</td><td>3</td><td>Hesra (Acamarian, born 2231-07-19, died 2286-10-05); Dovan (Acamari…</td></tr>
<tr><td>157302</td><td>Acamar III</td><td>Lornack</td><td>Dovrak</td><td>2170</td><td>2231</td><td>61</td><td>truce</td><td>NULL</td><td>Dovrak</td><td>2</td><td>Nessa (Acamarian, born 2322-11-30, died no record); Orlen (Acamaria…</td></tr>
</table>

```sql
SELECT entry_id, term, category, database_name, description
FROM library
WHERE description ILIKE '%Lornack%' OR term ILIKE '%Lornack%' OR description ILIKE '%Tralesta%' OR term ILIKE '%Tralesta%' OR term ILIKE '%blood feud%'
```

<table class="result">
<tr><th>entry_id</th><th>term</th><th>category</th><th>database_name</th><th>description</th></tr>
</table>
<p class="result-note">No rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BEVERLY:** Computer, any members of the Acamarian delegation in the Tralesta clan?

**COMPUTER:** Clan affiliation is not within provided records.

</td><td markdown="1">

```sql
SELECT pa.name, pa.role, count(p.id) AS person_records,
       count(*) FILTER (WHERE p.clan = 'Tralesta') AS tralesta_records,
       string_agg(DISTINCT p.clan, ', ') AS clans_on_file
FROM passengers pa
LEFT JOIN persons p ON pa.name IS NOT NULL
  AND (p.name ILIKE '%' || pa.name || '%' OR pa.name ILIKE '%' || p.name || '%')
WHERE pa.delegation = 'Acamarian'
GROUP BY pa.id, pa.name, pa.role ORDER BY pa.id
```

<table class="result">
<tr><th>name</th><th>role</th><th>person_records</th><th>tralesta_records</th><th>clans_on_file</th></tr>
<tr><td>Marouk</td><td>Sovereign of Acamar III</td><td>1</td><td>0</td><td>NULL</td></tr>
<tr><td>Yuta</td><td>servant: cook and food taster</td><td>0</td><td>0</td><td>NULL</td></tr>
<tr><td>NULL</td><td>bodyguard</td><td>0</td><td>0</td><td>NULL</td></tr>
<tr><td>NULL</td><td>servant</td><td>0</td><td>0</td><td>NULL</td></tr>
<tr><td>NULL</td><td>servant</td><td>0</td><td>0</td><td>NULL</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**RIKER:** There’s got to be a missing link here...

**DATA:** Commander, I believe I have found a correlation between the two deaths... your “missing link” ...

**DATA:** That is Penthor-Mul being led from his trial.

</td><td markdown="1">

```sql
SELECT i.id, i.planet, i.taken, i.caption, i.people_tagged,
  (SELECT string_agg(pa.name || ' (' || pa.role || ')', ', ')
      FROM passengers pa WHERE pa.delegation = 'Acamarian'
    AND list_contains(i.people_tagged,
         pa.name)) AS delegation_members_present,
  (SELECT string_agg(p.name || ' [' || p.clan || ', died ' || coalesce(p.died::VARCHAR,'-') || ']', ', ') FROM persons p WHERE p.clan IS NOT NULL AND list_contains(i.people_tagged, p.name)) AS clan_members_present
FROM image_archive i
WHERE i.planet ILIKE 'Acamar%'
ORDER BY i.taken
```

<table class="result">
<tr><th>id</th><th>planet</th><th>taken</th><th>caption</th><th>people_tagged</th><th>delegation_members_present</th><th>clan_members_present</th></tr>
<tr><td>157402</td><td>Acamar III</td><td>2313-03-11</td><td>Gatherer raid leader Penthor-Mul in custody at the outpost</td><td>[Penthor-Mul]</td><td>NULL</td><td>Penthor-Mul [Lornack, died 2313-05-02]</td></tr>
<tr><td>157404</td><td>Acamar III</td><td>2313-04-20</td><td>Crowd outside the courthouse as a Gatherer trial opens</td><td>[]</td><td>NULL</td><td>NULL</td></tr>
<tr><td>157401</td><td>Acamar III</td><td>2313-04-27</td><td>Penthor-Mul being led from his trial</td><td>[Penthor-Mul]</td><td>NULL</td><td>Penthor-Mul [Lornack, died 2313-05-02]</td></tr>
<tr><td>157405</td><td>Acamar III</td><td>2344-06-01</td><td>Clan elders of the Dovrak at the harvest assembly</td><td>[Orlen, Nessa]</td><td>NULL</td><td>Nessa [Dovrak, died -], Orlen [Dovrak, died 2344-09-12]</td></tr>
<tr><td>157403</td><td>Acamar III</td><td>2349-03-02</td><td>Opening day of the trial of the Gatherer Tavik-Dar</td><td>[Tavik-Dar]</td><td>NULL</td><td>Tavik-Dar [Ramsar, died 2349-04-21]</td></tr>
</table>

*Not what the script says: Reports that no image tags a delegation member and concludes ‘no link found’; it does not offer the image of Penthor-Mul being led from his trial.*

</td></tr>
</table>

### Sins of the Father

[Script](https://www.st-minutiae.com/resources/scripts/165.txt). Season 3. Captured Romulan logs say Worf’s father betrayed the Khitomer outpost. Data and Geordi check them against a second source.

![Data, La Forge and Riker compare the Klingon data file with the Intrepid’s sensor log.]({% link images/blog/star-trek/enterprise-computer/sins_of_the_father.jpg %}){: width="480" }
*Data, La Forge and Riker compare the Klingon data file with the Intrepid’s sensor log. <em>Star Trek: The Next Generation</em>, “Sins of the Father” (1990). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**PICARD:** Mister Data... I want you to find out everything you can about the destruction of the Khitomer outpost. Cross reference with Romulan tactics and strategic information on the region. Request access to the Klingon central information net.

**DATA:** Commander, I have discovered the basis of the charges against Worf’s father.

**DATA:** Apparently the Klingons recently captured a Romulan ship with logs that provided new information on the Khitomer attack. They clearly indicate a transmission from the outpost to the Romulans moments before the shields dropped.

</td><td markdown="1">

```sql
WITH r AS (SELECT seq, ts, row_number() OVER (ORDER BY ts) AS n
    FROM romulan_logs WHERE signal_type = 'distress signal'
  AND source = 'Khitomer outpost'),
     i AS (SELECT seq, ts, row_number() OVER (ORDER BY ts) AS n
         FROM sensor_logs WHERE ship_name = 'USS Intrepid'
       AND signal_type = 'distress signal'
       AND source = 'Khitomer outpost')
SELECT i.n AS signal_no, i.seq AS intrepid_seq, i.ts AS intrepid_ts,
       r.seq AS romulan_seq, r.ts AS romulan_ts,
       r.ts - i.ts AS romulan_offset
FROM i FULL JOIN r USING (n) ORDER BY n
```

<table class="result">
<tr><th>signal_no</th><th>intrepid_seq</th><th>intrepid_ts</th><th>romulan_seq</th><th>romulan_ts</th><th>romulan_offset</th></tr>
<tr><td>1</td><td>1</td><td>2346-08-19 03:12:04</td><td>3</td><td>2346-08-19 03:12:04</td><td>00:00:00</td></tr>
<tr><td>2</td><td>2</td><td>2346-08-19 03:12:19</td><td>4</td><td>2346-08-19 03:12:19</td><td>00:00:00</td></tr>
<tr><td>3</td><td>3</td><td>2346-08-19 03:12:31</td><td>5</td><td>2346-08-19 03:12:31</td><td>00:00:00</td></tr>
<tr><td>4</td><td>4</td><td>2346-08-19 03:12:47</td><td>6</td><td>2346-08-19 03:12:47</td><td>00:00:00</td></tr>
<tr><td>5</td><td>5</td><td>2346-08-19 03:13:02</td><td>7</td><td>2346-08-19 03:13:02</td><td>00:00:00</td></tr>
</table>
<p class="result-note">First 5 of 14 rows.</p>

```sql
SELECT l.seq, l.ts, l.signal_type, l.source, l.security_code,
       p.name AS code_holder, p.post
FROM romulan_logs l
LEFT JOIN personnel p ON p.security_code = l.security_code
WHERE l.signal_type <> 'distress signal' ORDER BY l.seq
```

<table class="result">
<tr><th>seq</th><th>ts</th><th>signal_type</th><th>source</th><th>security_code</th><th>code_holder</th><th>post</th></tr>
<tr><td>1</td><td>2346-08-19 02:40:00</td><td>transmission</td><td>Khitomer outpost</td><td>KDF-1-0012-QOR</td><td>NULL</td><td>Khitomer outpost commander</td></tr>
<tr><td>2</td><td>2346-08-19 03:11:52</td><td>transmission</td><td>Romulan patrol ship</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>11</td><td>2346-08-19 03:14:03</td><td>sensor sweep</td><td>Khitomer outpost</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>12</td><td>2346-08-19 03:14:11</td><td>sensor sweep</td><td>Khitomer outpost</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>13</td><td>2346-08-19 03:14:19</td><td>subspace handshake</td><td>Khitomer outpost</td><td>KDF-7-2291-TAJ</td><td>Mogh</td><td>Khitomer outpost</td></tr>
</table>
<p class="result-note">First 5 of 10 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** From Worf’s father?

**DATA:** It does correspond to Mogh’s personal security code.

</td><td markdown="1">

```sql
SELECT l.seq, l.ts, l.signal_type, l.source, l.security_code,
       p.name AS code_holder, p.species, p.post,
  EXISTS (SELECT 1 FROM sensor_logs s
      WHERE s.signal_type = l.signal_type AND s.source = l.source
    AND s.ts BETWEEN l.ts - INTERVAL 3 SECOND
    AND l.ts + INTERVAL 3 SECOND) AS seen_by_starfleet_sensors
FROM romulan_logs l
JOIN personnel p ON p.security_code = l.security_code
WHERE p.name = 'Mogh'
ORDER BY l.seq
```

<table class="result">
<tr><th>seq</th><th>ts</th><th>signal_type</th><th>source</th><th>security_code</th><th>code_holder</th><th>species</th><th>post</th><th>seen_by_starfleet_sensors</th></tr>
<tr><td>13</td><td>2346-08-19 03:14:19</td><td>subspace handshake</td><td>Khitomer outpost</td><td>KDF-7-2291-TAJ</td><td>Mogh</td><td>Klingon</td><td>Khitomer outpost</td><td>false</td></tr>
<tr><td>14</td><td>2346-08-19 03:14:20</td><td>transmission</td><td>Khitomer outpost</td><td>KDF-7-2291-TAJ</td><td>Mogh</td><td>Klingon</td><td>Khitomer outpost</td><td>false</td></tr>
<tr><td>15</td><td>2346-08-19 03:14:24</td><td>transmission</td><td>Romulan patrol ship</td><td>KDF-7-2291-TAJ</td><td>Mogh</td><td>Klingon</td><td>Khitomer outpost</td><td>false</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**RIKER:** How can we be sure these records haven’t been falsified?

**GEORDI:** We can cross check them against the Intrepid’s sensor logs...

**DATA:** Both the Intrepid and Romulan logs show a series of distress signals from Khitomer...

**GEORDI:** Gaps in the Intrepid logs, missing information because of the range...

**DATA:** This is where Mogh’s alleged transmission should be.

</td><td markdown="1">

```sql
WITH r AS (SELECT seq, ts, row_number() OVER (ORDER BY ts) AS n
    FROM romulan_logs WHERE signal_type = 'distress signal'
  AND source = 'Khitomer outpost'),
     i AS (SELECT seq, ts, row_number() OVER (ORDER BY ts) AS n
         FROM sensor_logs WHERE ship_name = 'USS Intrepid'
       AND signal_type = 'distress signal'
       AND source = 'Khitomer outpost'),
     x AS (SELECT n, i.ts AS intrepid_ts, r.ts AS romulan_ts,
            r.seq AS romulan_seq,
            epoch(r.ts - i.ts) AS offset_s FROM i FULL JOIN r USING (n))
SELECT offset_s AS romulan_minus_intrepid_seconds,
       count(*) AS distress_signals, min(n) AS first_signal,
       max(n) AS last_signal,
  min(intrepid_ts) AS intrepid_from, max(intrepid_ts) AS intrepid_to,
         min(romulan_seq) AS romulan_seq_from,
         max(romulan_seq) AS romulan_seq_to,
  (SELECT count(*) FROM romulan_logs l WHERE l.security_code IS NOT NULL
    AND l.seq > (SELECT max(romulan_seq) FROM x x2
      WHERE x2.offset_s = 0) AND l.seq < (SELECT min(romulan_seq)
      FROM x x3
      WHERE x3.offset_s <> 0)) AS coded_entries_between_segments
FROM x GROUP BY offset_s ORDER BY first_signal
```

<table class="result">
<tr><th>romulan_minus_intrepid_seconds</th><th>distress_signals</th><th>first_signal</th><th>last_signal</th><th>intrepid_from</th><th>intrepid_to</th><th>romulan_seq_from</th><th>romulan_seq_to</th><th>coded_entries_between_segments</th></tr>
<tr><td>0.0</td><td>8</td><td>1</td><td>8</td><td>2346-08-19 03:12:04</td><td>2346-08-19 03:13:49</td><td>3</td><td>10</td><td>3</td></tr>
<tr><td>2.5</td><td>6</td><td>9</td><td>14</td><td>2346-08-19 03:14:41</td><td>2346-08-19 03:15:51</td><td>19</td><td>24</td><td>3</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Wait a second, Data. Back up.

**GEORDI:** Look at this... just before the Intrepid gap begins, the timebase of both files are in perfect sync... but look at the signals just after the shields dropped.

**DATA:** They are no longer synchronous.

**GEORDI:** Commander, somebody’s been rewriting history.

</td><td markdown="1">

```sql
WITH drop_t AS (SELECT ts FROM romulan_logs
    WHERE signal_type = 'shield collapse'),
r AS (SELECT seq, ts, signal_type, source,
       row_number() OVER (ORDER BY ts) AS n FROM romulan_logs
    WHERE ts > (SELECT ts FROM drop_t)),
i AS (SELECT seq, ts, signal_type, source,
       row_number() OVER (ORDER BY ts) AS n FROM sensor_logs
    WHERE ship_name = 'USS Intrepid'
  AND ts > (SELECT ts FROM drop_t) - INTERVAL 3 SECOND)
SELECT n, i.seq AS intrepid_seq, i.ts AS intrepid_ts,
       i.signal_type AS intrepid_signal, i.source AS intrepid_source,
       r.seq AS romulan_seq, r.ts AS romulan_ts,
              r.signal_type AS romulan_signal,
              epoch(r.ts - i.ts) AS romulan_offset_s,
       epoch(i.ts - lag(i.ts) OVER (ORDER BY n)) AS intrepid_interval_s,
              epoch(r.ts - lag(r.ts) OVER (ORDER BY n)) AS romulan_interval_s
FROM i FULL JOIN r USING (n) ORDER BY n
```

<table class="result">
<tr><th>n</th><th>intrepid_seq</th><th>intrepid_ts</th><th>intrepid_signal</th><th>intrepid_source</th><th>romulan_seq</th><th>romulan_ts</th><th>romulan_signal</th><th>romulan_offset_s</th><th>intrepid_interval_s</th><th>romulan_interval_s</th></tr>
<tr><td>1</td><td>9</td><td>2346-08-19 03:14:41</td><td>distress signal</td><td>Khitomer outpost</td><td>19</td><td>2346-08-19 03:14:43.5</td><td>distress signal</td><td>2.5</td><td>NULL</td><td>NULL</td></tr>
<tr><td>2</td><td>10</td><td>2346-08-19 03:14:55</td><td>distress signal</td><td>Khitomer outpost</td><td>20</td><td>2346-08-19 03:14:57.5</td><td>distress signal</td><td>2.5</td><td>14.0</td><td>14.0</td></tr>
<tr><td>3</td><td>11</td><td>2346-08-19 03:15:09</td><td>distress signal</td><td>Khitomer outpost</td><td>21</td><td>2346-08-19 03:15:11.5</td><td>distress signal</td><td>2.5</td><td>14.0</td><td>14.0</td></tr>
<tr><td>4</td><td>12</td><td>2346-08-19 03:15:22</td><td>distress signal</td><td>Khitomer outpost</td><td>22</td><td>2346-08-19 03:15:24.5</td><td>distress signal</td><td>2.5</td><td>13.0</td><td>13.0</td></tr>
<tr><td>5</td><td>13</td><td>2346-08-19 03:15:38</td><td>distress signal</td><td>Khitomer outpost</td><td>23</td><td>2346-08-19 03:15:40.5</td><td>distress signal</td><td>2.5</td><td>16.0</td><td>16.0</td></tr>
</table>
<p class="result-note">First 5 of 8 rows.</p>

</td></tr>
</table>

### Violations

[Script](https://www.st-minutiae.com/resources/scripts/212.txt). Season 5. Crew members are falling into unexplained comas while a delegation of telepaths is aboard. One investigation in three scenes.

**In Engineering: every possible cause**

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Computer, locate the electropathic pattern described in medical database four-delta-one.

**COMPUTER:** Electropathic pattern located.

</td><td markdown="1">

```sql
SELECT pattern_id, name, database_ref FROM medical_patterns
WHERE database_ref = '4-delta-1' AND name = 'electropathic pattern'
```

<table class="result">
<tr><th>pattern_id</th><th>name</th><th>database_ref</th></tr>
<tr><td>41</td><td>electropathic pattern</td><td>4-delta-1</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Okay, we’re gonna track down any possible cause of that brain pattern. First, what are the medical conditions that might account for it?

**COMPUTER:** Iresine Syndrome is a cause of the electropathic pattern.

</td><td markdown="1">

```sql
SELECT c.cause_id, c.agent, c.agent_type, c.agent_class
FROM pattern_causes c JOIN medical_patterns p USING (pattern_id)
WHERE p.name = 'electropathic pattern' AND p.database_ref = '4-delta-1'
  AND c.agent_type = 'medical'
ORDER BY c.agent
```

<table class="result">
<tr><th>cause_id</th><th>agent</th><th>agent_type</th><th>agent_class</th></tr>
<tr><td>1</td><td>Iresine Syndrome</td><td>medical</td><td>condition</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Right. And Doctor Crusher’s already eliminated that. How many nonmedical forces or substances might cause the pattern?

**COMPUTER:** There are twenty-two nonmedical agents.

</td><td markdown="1">

```sql
SELECT count(*) AS nonmedical_causes
FROM pattern_causes c JOIN medical_patterns p USING (pattern_id)
WHERE p.name = 'electropathic pattern' AND p.database_ref = '4-delta-1'
  AND c.agent_type = 'nonmedical'
```

<table class="result">
<tr><th>nonmedical_causes</th></tr>
<tr><td>22</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Okay. And how many of those are present on the Enterprise?

**COMPUTER:** None is present on the Enterprise.

</td><td markdown="1">

```sql
SELECT c.agent, c.agent_class,
  EXISTS (SELECT 1 FROM internal_sensor_logs l
      WHERE l.ship = 'Enterprise'
    AND lower(l.substance) = lower(c.agent)) AS detected_on_enterprise,
  s.routinely_scanned
FROM pattern_causes c JOIN medical_patterns p USING (pattern_id)
LEFT JOIN sensor_scan_config s ON lower(s.substance) = lower(c.agent)
WHERE p.name = 'electropathic pattern' AND p.database_ref = '4-delta-1'
  AND c.agent_type = 'nonmedical'
ORDER BY c.agent_class, c.agent
```

<table class="result">
<tr><th>agent</th><th>agent_class</th><th>detected_on_enterprise</th><th>routinely_scanned</th></tr>
<tr><td>chrysimite</td><td>chemical</td><td>false</td><td>true</td></tr>
<tr><td>dardilion</td><td>chemical</td><td>false</td><td>true</td></tr>
<tr><td>ferrazene</td><td>chemical</td><td>false</td><td>true</td></tr>
<tr><td>hylanatine</td><td>chemical</td><td>false</td><td>true</td></tr>
<tr><td>manzene</td><td>chemical</td><td>false</td><td>true</td></tr>
</table>
<p class="result-note">First 5 of 22 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Are the ship’s sensors calibrated to detect all those agents?

**COMPUTER:** All agents are scanned by the sensors.

</td><td markdown="1">

```sql
SELECT count(*) AS nonmedical_agents,
  count(*) FILTER (WHERE s.routinely_scanned) AS routinely_scanned,
  count(*) FILTER (WHERE s.routinely_scanned IS NOT TRUE) AS not_scanned,
  string_agg(c.agent,
         ', ') FILTER (WHERE s.routinely_scanned IS NOT TRUE) AS agents_not_scanned
FROM pattern_causes c JOIN medical_patterns p USING (pattern_id)
LEFT JOIN sensor_scan_config s ON lower(s.substance) = lower(c.agent)
WHERE p.name = 'electropathic pattern' AND p.database_ref = '4-delta-1'
  AND c.agent_type = 'nonmedical'
```

<table class="result">
<tr><th>nonmedical_agents</th><th>routinely_scanned</th><th>not_scanned</th><th>agents_not_scanned</th></tr>
<tr><td>22</td><td>22</td><td>0</td><td>NULL</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Okay. Let’s start with the chemical substances. Name them.

**COMPUTER:** Ferrazene, hylanatine, dardilion, chrysimite, and manzene.

</td><td markdown="1">

```sql
SELECT c.agent
FROM pattern_causes c JOIN medical_patterns p USING (pattern_id)
WHERE p.name = 'electropathic pattern' AND p.database_ref = '4-delta-1'
  AND c.agent_type = 'nonmedical' AND c.agent_class = 'chemical'
ORDER BY c.agent
```

<table class="result">
<tr><th>agent</th></tr>
<tr><td>chrysimite</td></tr>
<tr><td>dardilion</td></tr>
<tr><td>ferrazene</td></tr>
<tr><td>hylanatine</td></tr>
<tr><td>manzene</td></tr>
</table>

*Not what the script says: The right five chemicals, but in alphabetical order rather than the script’s read-out order.*

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Ferrazene has a complex molecular structure... it breaks down into bilenium and tarrisite. Do the sensors scan for those?

**COMPUTER:** Ship’s sensors scan for both compounds.

</td><td markdown="1">

```sql
SELECT b.compound, b.byproduct, s.routinely_scanned,
  EXISTS (SELECT 1 FROM internal_sensor_logs l
      WHERE l.ship = 'Enterprise'
    AND lower(l.substance) = lower(b.byproduct)) AS detected_on_enterprise
FROM compound_byproducts b
LEFT JOIN sensor_scan_config s ON lower(s.substance) = lower(b.byproduct)
WHERE lower(b.compound) = 'ferrazene'
ORDER BY b.byproduct
```

<table class="result">
<tr><th>compound</th><th>byproduct</th><th>routinely_scanned</th><th>detected_on_enterprise</th></tr>
<tr><td>ferrazene</td><td>bilenium</td><td>true</td><td>false</td></tr>
<tr><td>ferrazene</td><td>tarrisite</td><td>true</td><td>false</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** And are they present on the Enterprise?

**COMPUTER:** Bilenium and tarrisite are not present.

</td><td markdown="1">

```sql
SELECT b.byproduct, count(l.log_id) AS detections_on_enterprise
FROM compound_byproducts b
LEFT JOIN internal_sensor_logs l ON lower(l.substance) = lower(b.byproduct) AND l.ship = 'Enterprise'
WHERE lower(b.compound) = 'ferrazene'
GROUP BY b.byproduct ORDER BY b.byproduct
```

<table class="result">
<tr><th>byproduct</th><th>detections_on_enterprise</th></tr>
<tr><td>bilenium</td><td>0</td></tr>
<tr><td>tarrisite</td><td>0</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Do any of the substances break down into by-products that are not scanned for?

**COMPUTER:** Dardilion contains the byproduct nilizene. Sensors do not routinely scan for that substance.

</td><td markdown="1">

```sql
SELECT c.agent AS substance, b.byproduct, s.routinely_scanned
FROM pattern_causes c JOIN medical_patterns p USING (pattern_id)
JOIN compound_byproducts b ON lower(b.compound) = lower(c.agent)
LEFT JOIN sensor_scan_config s ON lower(s.substance) = lower(b.byproduct)
WHERE p.name = 'electropathic pattern' AND p.database_ref = '4-delta-1'
  AND c.agent_type = 'nonmedical' AND c.agent_class = 'chemical'
  AND s.routinely_scanned IS NOT TRUE
ORDER BY c.agent, b.byproduct
```

<table class="result">
<tr><th>substance</th><th>byproduct</th><th>routinely_scanned</th></tr>
<tr><td>dardilion</td><td>nilizene</td><td>false</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Well, this isn’t a routine situation. Scan for nilizene.

**COMPUTER:** There is no nilizene on the Enterprise.

</td><td markdown="1">

```sql
SELECT log_id, ship, location, substance, stardate
FROM internal_sensor_logs WHERE lower(substance) = 'nilizene'
ORDER BY stardate, log_id
```

<table class="result">
<tr><th>log_id</th><th>ship</th><th>location</th><th>substance</th><th>stardate</th></tr>
<tr><td>212210</td><td>SS Kallisto</td><td>Cargo Hold 1</td><td>nilizene</td><td>45427.4</td></tr>
</table>

*Not what the script says: Says it cannot start a scan from records; the logs hold no nilizene reading aboard, but since nilizene is not routinely scanned that does not show the ship is clear. The script’s computer answers ‘There is no nilizene on the Enterprise.’*

</td></tr>
</table>

**On the bridge: the right query with the wrong filter**

![The search as the episode shows it: “Search parameters: instances of unexplained coma or medical cases diagnosed as Iresine Syndrome during periods when Ullian telepathic historians were present on the planet.”]({% link images/blog/star-trek/enterprise-computer/violations_bridge.jpg %}){: width="480" }
*The search as the episode shows it: “Search parameters: instances of unexplained coma or medical cases diagnosed as Iresine Syndrome during periods when Ullian telepathic historians were present on the planet.” <em>Star Trek: The Next Generation</em>, “Violations” (1992). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**PICARD:** Mister Data, I want you to investigate those eleven planets the Ullians have visited. See if there have been any reports of unexplained comas.

**DATA:** Yes, Captain.

**GEORDI:** Well, that’s it for Melina Two. No unexplained comas during the time the Ullians were working there. We’re striking out everywhere.

**DATA:** We have yet to receive transmissions from the two planets of the Nel system. Perhaps they will show different results.

</td><td markdown="1">

```sql
WITH ullian AS (SELECT DISTINCT planet FROM missions
    WHERE delegation = 'Ullian'),
reports AS (
  SELECT 'coma incident report' AS source, planet, stardate,
         NULL AS patient, NULL AS diagnosis
  FROM coma_incidents
  UNION ALL
  SELECT 'planetary medical record', planet, stardate, patient,
         coalesce(diagnosis, 'undiagnosed')
  FROM planetary_medical_records
  WHERE condition = 'coma'
)
SELECT r.planet, r.stardate, r.source, r.patient, r.diagnosis,
  EXISTS (SELECT 1 FROM missions m WHERE m.delegation = 'Ullian'
    AND m.planet = r.planet AND r.stardate BETWEEN m.arrived_stardate
    AND m.departed_stardate) AS during_ullian_visit
FROM reports r JOIN ullian u ON u.planet = r.planet
ORDER BY r.planet, r.stardate, r.source
```

<table class="result">
<tr><th>planet</th><th>stardate</th><th>source</th><th>patient</th><th>diagnosis</th><th>during_ullian_visit</th></tr>
<tr><td>Hurada III</td><td>41194</td><td>planetary medical record</td><td>HUR-1310</td><td>Iresine Syndrome</td><td>false</td></tr>
<tr><td>Hurada III</td><td>43531</td><td>coma incident report</td><td>NULL</td><td>NULL</td><td>true</td></tr>
<tr><td>Hurada III</td><td>43531</td><td>planetary medical record</td><td>HUR-2207</td><td>Iresine Syndrome</td><td>true</td></tr>
<tr><td>Hurada III</td><td>43580</td><td>planetary medical record</td><td>HUR-2215</td><td>cranial trauma</td><td>true</td></tr>
<tr><td>Hurada III</td><td>43657</td><td>coma incident report</td><td>NULL</td><td>NULL</td><td>true</td></tr>
</table>
<p class="result-note">First 5 of 20 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** We didn’t look into the comas that were explained.

**DATA:** You are checking for instances of Iresine Syndrome...

**GEORDI:** Right... and correlating them with visits by the Ullians -- and there we are.

**DATA:** Two cases of Iresine Syndrome on Hurada Three -- right at the time Tarmin and his group was there.

</td><td markdown="1">

```sql
SELECT r.case_id, r.planet, r.patient, r.stardate,
  (SELECT m.arrived_stardate || '-' || m.departed_stardate
      FROM missions m WHERE m.delegation = 'Ullian'
    AND m.planet = r.planet AND r.stardate BETWEEN m.arrived_stardate
    AND m.departed_stardate) AS ullian_visit,
  (SELECT string_agg(DISTINCT l.member, ', ' ORDER BY l.member)
      FROM mission_logs l WHERE l.delegation = 'Ullian'
    AND l.planet = r.planet AND r.stardate BETWEEN l.arrived_stardate
    AND l.departed_stardate) AS ullians_present,
  (SELECT string_agg(DISTINCT m.delegation, ', ') FROM missions m
      WHERE m.delegation <> 'Ullian' AND m.planet = r.planet
    AND r.stardate BETWEEN m.arrived_stardate
    AND m.departed_stardate) AS other_delegations_present
FROM planetary_medical_records r
WHERE r.diagnosis = 'Iresine Syndrome'
ORDER BY r.stardate
```

<table class="result">
<tr><th>case_id</th><th>planet</th><th>patient</th><th>stardate</th><th>ullian_visit</th><th>ullians_present</th><th>other_delegations_present</th></tr>
<tr><td>212105</td><td>Hurada III</td><td>HUR-1310</td><td>41194</td><td>NULL</td><td>NULL</td><td>Vulcan Science Academy</td></tr>
<tr><td>212107</td><td>Varnis VI</td><td>VAR-0802</td><td>42603</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>212101</td><td>Teloria III</td><td>TEL3-0418</td><td>43304</td><td>43186-43380</td><td>Inad, Jev, Tarmin</td><td>NULL</td></tr>
<tr><td>212102</td><td>Hurada III</td><td>HUR-2207</td><td>43531</td><td>43424-43712</td><td>Inad, Jev, Tarmin</td><td>NULL</td></tr>
<tr><td>212106</td><td>Brevin V</td><td>BRV-0551</td><td>43547</td><td>NULL</td><td>NULL</td><td>Vulcan Science Academy</td></tr>
</table>
<p class="result-note">First 5 of 7 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** Let’s try the other planets. I think we may have something.

**PICARD:** How’s your search coming?

**DATA:** We have uncovered several cases, sir, but we have not yet completed our search.

</td><td markdown="1">

```sql
WITH comas AS (
  SELECT planet, stardate FROM coma_incidents
  UNION
  SELECT planet, stardate
  FROM planetary_medical_records
  WHERE diagnosis = 'Iresine Syndrome'
)
SELECT m.planet, m.arrived_stardate, m.departed_stardate,
       c.stardate AS coma_stardate,
  (SELECT r.diagnosis FROM planetary_medical_records r
      WHERE r.planet = c.planet AND r.stardate = c.stardate
    AND r.condition = 'coma') AS recorded_diagnosis,
  (SELECT string_agg(DISTINCT l.member, ', ' ORDER BY l.member)
      FROM mission_logs l WHERE l.delegation = 'Ullian'
    AND l.planet = c.planet AND c.stardate BETWEEN l.arrived_stardate
    AND l.departed_stardate) AS ullians_present
FROM missions m
LEFT JOIN comas c ON c.planet = m.planet
  AND c.stardate BETWEEN m.arrived_stardate AND m.departed_stardate
WHERE m.delegation = 'Ullian'
ORDER BY m.arrived_stardate, c.stardate
```

<table class="result">
<tr><th>planet</th><th>arrived_stardate</th><th>departed_stardate</th><th>coma_stardate</th><th>recorded_diagnosis</th><th>ullians_present</th></tr>
<tr><td>Jessen I</td><td>42186</td><td>42465</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>Jessen IV</td><td>42498</td><td>42786</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>Jessen I</td><td>42810</td><td>42900</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>Teloria II</td><td>43030</td><td>43172</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>Teloria III</td><td>43186</td><td>43380</td><td>43304</td><td>Iresine Syndrome</td><td>Inad, Jev, Tarmin</td></tr>
</table>
<p class="result-note">First 5 of 14 rows.</p>

```sql
WITH comas AS (
  SELECT planet, stardate FROM coma_incidents
  UNION
  SELECT r.planet, r.stardate
  FROM planetary_medical_records r
  JOIN missions m ON m.delegation='Ullian' AND m.planet = r.planet
    AND r.stardate BETWEEN m.arrived_stardate AND m.departed_stardate
  WHERE r.diagnosis = 'Iresine Syndrome'
)
SELECT l.member,
       count(DISTINCT (c.planet, c.stardate)) AS comas_present_for,
       (SELECT count(*) FROM comas) AS total_comas
FROM comas c
JOIN mission_logs l ON l.delegation = 'Ullian' AND l.planet = c.planet
  AND c.stardate BETWEEN l.arrived_stardate AND l.departed_stardate
GROUP BY l.member ORDER BY comas_present_for DESC, l.member
```

<table class="result">
<tr><th>member</th><th>comas_present_for</th><th>total_comas</th></tr>
<tr><td>Jev</td><td>6</td><td>6</td></tr>
<tr><td>Inad</td><td>5</td><td>6</td></tr>
<tr><td>Tarmin</td><td>4</td><td>6</td></tr>
</table>

*Not what the script says: The three planets were already given on the previous line; here it adds the two Nel III comas, which the dialogue has not received yet at this point.*

</td></tr>
</table>

**The alibi, and the one who was always there**

![The follow-up search of the Nel system records, correlated with the Ullians’ mission logs.]({% link images/blog/star-trek/enterprise-computer/violations_alibi.jpg %}){: width="480" }
*The follow-up search of the Nel system records, correlated with the Ullians’ mission logs. <em>Star Trek: The Next Generation</em>, “Violations” (1992). © CBS Studios Inc.*{: .caption .caption-left }

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**GEORDI:** We just got the transmission from the Nel system. No mention of Iresine Syndrome... but there are two unexplained comas on one planet... none on the other.

**DATA:** And were the Ullians present?

**GEORDI:** Checking their mission logs... That’s funny...

**DATA:** What is it?

**GEORDI:** On stardates 45321 and 45323, when the comas occurred... Tarmin was on his home planet. He wasn’t anywhere near the Nel system.

</td><td markdown="1">

```sql
SELECT m.planet, m.arrived_stardate, m.departed_stardate, c.incident_id,
       c.stardate AS coma_stardate,
  (SELECT string_agg(DISTINCT l.member, ', ' ORDER BY l.member)
      FROM mission_logs l WHERE l.delegation = 'Ullian'
    AND l.planet = c.planet AND c.stardate BETWEEN l.arrived_stardate
    AND l.departed_stardate) AS ullians_present,
  (SELECT string_agg(l.member || ' on ' || l.planet, ', ')
      FROM mission_logs l WHERE l.delegation = 'Ullian'
    AND l.planet <> m.planet AND c.stardate BETWEEN l.arrived_stardate
    AND l.departed_stardate) AS ullians_elsewhere
FROM missions m
LEFT JOIN coma_incidents c ON c.planet = m.planet
  AND c.stardate BETWEEN m.arrived_stardate AND m.departed_stardate
WHERE m.delegation = 'Ullian' AND m.planet LIKE 'Nel %'
ORDER BY m.arrived_stardate, c.stardate
```

<table class="result">
<tr><th>planet</th><th>arrived_stardate</th><th>departed_stardate</th><th>incident_id</th><th>coma_stardate</th><th>ullians_present</th><th>ullians_elsewhere</th></tr>
<tr><td>Nel II</td><td>45123</td><td>45260</td><td>NULL</td><td>NULL</td><td>NULL</td><td>NULL</td></tr>
<tr><td>Nel III</td><td>45273</td><td>45383</td><td>5</td><td>45321</td><td>Inad, Jev</td><td>Tarmin on Ullian homeworld</td></tr>
<tr><td>Nel III</td><td>45273</td><td>45383</td><td>6</td><td>45323</td><td>Inad, Jev</td><td>Tarmin on Ullian homeworld</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**DATA:** We discovered two instances of unexplained comas on Nel Three while the Ullians were there... but Tarmin was not part of the group. A closer examination revealed that only one Ullian was present at all incidents of coma -- Jev.

*Nobody speaks this request in the script. Claude was asked: “Were any of the Ullians present at all incidents of coma?”*

</td><td markdown="1">

```sql
SELECT l.member, count(DISTINCT c.incident_id) AS incidents_present,
       (SELECT count(*) FROM coma_incidents) AS total_incidents
FROM coma_incidents c
JOIN mission_logs l ON l.delegation = 'Ullian' AND l.planet = c.planet
  AND c.stardate BETWEEN l.arrived_stardate AND l.departed_stardate
GROUP BY l.member
HAVING count(DISTINCT c.incident_id) = (SELECT count(*)
    FROM coma_incidents)
ORDER BY l.member
```

<table class="result">
<tr><th>member</th><th>incidents_present</th><th>total_incidents</th></tr>
<tr><td>Jev</td><td>6</td><td>6</td></tr>
</table>

</td></tr>
</table>

### Realm of Fear

[Script](https://www.st-minutiae.com/resources/scripts/228.txt). Season 6. Barclay, who is afraid of the transporter, looks up what it might be doing to him.

<table class="script-split" markdown="1">
<tr markdown="1"><th>In the script</th><th>What the computer ran</th></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BARCLAY:** Computer... access Starfleet Medical Data Base. Tell me about... describe the disorder known as... Transporter Psychosis.

**COMPUTER:** Transporter Psychosis was diagnosed in the year twenty-two-oh-nine by researchers on Delinia Two --

</td><td markdown="1">

```sql
SELECT disorder, summary, year_diagnosed, diagnosed_by, diagnosed_at,
       cause
FROM medical_database WHERE disorder ILIKE 'Transporter Psychosis'
```

<table class="result">
<tr><th>disorder</th><th>summary</th><th>year_diagnosed</th><th>diagnosed_by</th><th>diagnosed_at</th><th>cause</th></tr>
<tr><td>Transporter Psychosis</td><td>Transporter Psychosis was diagnosed in the year twenty-two-oh-nine …</td><td>2209</td><td>researchers</td><td>Delinia II</td><td>It is caused by a breakdown of neuro-chemical molecules during tran…</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BARCLAY:** No, no... stop. All I need is the... what causes it?

**COMPUTER:** It is caused by a breakdown of neuro-chemical molecules during transport, affecting the body’s motor functions, autonomic systems, and the brain’s higher reasoning centers.

</td><td markdown="1">

```sql
SELECT cause
FROM medical_database
WHERE disorder ILIKE 'Transporter Psychosis'
```

<table class="result">
<tr><th>cause</th></tr>
<tr><td>It is caused by a breakdown of neuro-chemical molecules during tran…</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BARCLAY:** What are the symptoms?

**COMPUTER:** Victims suffer from paranoid delusions... multi-infarct dementia... hallucinations...

</td><td markdown="1">

```sql
SELECT symptom_id, symptom, category, detail, is_peripheral
FROM disorder_symptoms WHERE disorder ILIKE 'Transporter Psychosis'
ORDER BY symptom_id
```

<table class="result">
<tr><th>symptom_id</th><th>symptom</th><th>category</th><th>detail</th><th>is_peripheral</th></tr>
<tr><td>22801</td><td>paranoid delusions</td><td>delusion</td><td>NULL</td><td>false</td></tr>
<tr><td>22802</td><td>multi-infarct dementia</td><td>dementia</td><td>NULL</td><td>false</td></tr>
<tr><td>22803</td><td>hallucinations</td><td>hallucination</td><td>Victims experience somatic, tactile and visual hallucinations, acco…</td><td>false</td></tr>
<tr><td>22804</td><td>sleeplessness</td><td>sleep</td><td>NULL</td><td>true</td></tr>
<tr><td>22805</td><td>accelerated heart-rate</td><td>cardiac</td><td>NULL</td><td>true</td></tr>
</table>
<p class="result-note">First 5 of 8 rows.</p>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BARCLAY:** Hallucinations? What kind of hallucinations?

**COMPUTER:** Victims experience somatic, tactile and visual hallucinations, accompanied by psychogenic hysteria.

</td><td markdown="1">

```sql
SELECT symptom, detail FROM disorder_symptoms
WHERE disorder ILIKE 'Transporter Psychosis'
  AND category = 'hallucination'
```

<table class="result">
<tr><th>symptom</th><th>detail</th></tr>
<tr><td>hallucinations</td><td>Victims experience somatic, tactile and visual hallucinations, acco…</td></tr>
</table>

</td></tr>
<tr valign="top" markdown="1"><td markdown="1">

**BARCLAY:** Computer... what is the treatment for Transporter Psychosis?

**COMPUTER:** There is no known treatment.

</td><td markdown="1">

```sql
SELECT m.disorder, count(t.treatment_id) AS treatments_on_file,
       (SELECT count(*)
    FROM disorder_treatments) AS treatments_in_database
FROM medical_database m
LEFT JOIN disorder_treatments t ON t.disorder ILIKE '%' || m.disorder || '%' OR t.disorder ILIKE '%transporter%' OR t.disorder ILIKE '%psychosis%'
WHERE m.disorder ILIKE 'Transporter Psychosis' GROUP BY m.disorder
```

<table class="result">
<tr><th>disorder</th><th>treatments_on_file</th><th>treatments_in_database</th></tr>
<tr><td>Transporter Psychosis</td><td>0</td><td>6</td></tr>
</table>

</td></tr>
</table>

*Stills from* Star Trek: The Next Generation *are © CBS Studios Inc. STAR TREK and related marks are trademarks of CBS Studios Inc. They are reproduced here in reduced size for the purpose of commentary on the scenes discussed. This post is not affiliated with or endorsed by CBS Studios or Paramount.*
