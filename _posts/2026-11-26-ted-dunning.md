---
layout: post
title: "The Five-Minute Test: Ted Dunning on Why DuckDB Makes Analytics Easier"
authors:
  - Ted Dunning in conversation with Geertjan Wielenga and Tim Cox
thumb: "/images/blog/thumbs/ted-dunning.svg"
image: "/images/blog/thumbs/ted-dunning.png"
excerpt: "Ted Dunning has spent decades building distributed data systems, including Apache Drill. He queries a year of home sensor data, around 100 million rows, on a Raspberry Pi in a fraction of a second with DuckDB. This is his case for why a single machine, and a tool that proves itself in five minutes, now goes a very long way."
tag: using-duckdb
---

Ted Dunning has spent decades building distributed data systems. He was one of the founders of [Apache Drill](https://drill.apache.org/), and the vectorized in-memory ideas from that project went on to shape Apache Arrow. So it is worth paying attention when he says that much of what used to require a cluster now fits comfortably on a single machine, and that [DuckDB](https://duckdb.org/) is one of the tools that changed his mind about where that line sits.

> Quote A project out of the blue has to show you some value in five minutes, and preferably the first 30 seconds.
>
> -- Ted Dunning

## A Year of Sensor Data on a Raspberry Pi

Dunning collects environmental data from sensors scattered around his home, measuring temperature, air quality, and other conditions. He originally developed the approach for agricultural meteorological data. A year of readings adds up to around 100 million rows.

Two numbers from the project stand out, and they come from different parts of the stack. The first is storage. By sorting the readings by device ID and time before writing them out, Dunning gets dramatic compression from Parquet. **"Parquet is just astonishing at compressing that data,"** he says, and for his sensor readings, five measurements alongside a long device ID, **"it compresses 300 to one."**

The second is query speed, and this is where DuckDB comes in. **"On my little Raspberry Pi, I could search 100 million rows of data, a year of data, in a quarter second,"** he says. On top of that he built a small application. The readings come back from DuckDB as a pandas or NumPy structure, and his configuration data, which sensor sat in which room and when he moved it, lives in a pandas table that DuckDB can join against. **"100 lines of Python later, I had a little web server that did visualization"** and querying of the history. It was completely responsive, and, he adds, **"it was trivial to do."**

None of that needs a server, a cluster, or a warehouse. A small board on a home network reads Parquet files and answers questions about a year of data in the time it takes to click.

## The Five-Minute Test

Dunning has a rule of thumb for new software. **"A project out of the blue has to show you some value in five minutes,"** he says, **"before you're willing to spend the hour to really dig into it."** The best tools go further still: **"preferably the first 30 seconds, which is now lately possible with some software."**

Heavyweight distributed systems rarely clear that bar. Drill, [Presto](https://prestodb.io/), and [Impala](https://impala.apache.org/) all expect a server or cluster to stand up and data that already lives somewhere commonly networked. By the time you have an answer, he says, **"I don't remember why I was looking."** DuckDB was different. **"It definitely met the first five-minute test,"** he says, and the WebAssembly build, running in a browser tab with nothing installed, **"meets the first 30 second sort of test."**

## Making Other Tools More Valuable

For Dunning, DuckDB's value is bound up in everything around it. **"One of the things about DuckDB isn't DuckDB,"** he says. **"It's all of the things around it that it takes advantage of quite well."** He traces a line back through his own work: the value vectors in Apache Drill, a relocatable in-memory representation of data, fed into [Apache Arrow](https://arrow.apache.org/), which in turn made formats like [Parquet](https://parquet.apache.org/) fast to move and share. DuckDB, he argues, makes those virtues vividly apparent, because the data is right there and you can mix it with CSV files, **"which are everywhere."**

That fits how he actually works. For a conference he helps run, the reviewer and review data is published internally on Git, and he uses DuckDB to **"suck it into various other tools ... especially [Julia](https://julialang.org/)."** His working philosophy is to use each tool for what it is good at. **"SQL is terrible for building a neural net,"** he says. **"But SQL is great for rejiggering and massaging and presenting the data."** Because DuckDB **"hooks in so easily"** to Julia, Python, and Go, he can grab and reshape data in SQL and hand the numerics to a language built for matrix algebra. **"The queries stay very simple and maintainable, and the numerics stay very focused on numerics,"** he says.

Asked to name what makes DuckDB so well suited to this, Dunning points to three things. The obvious one is that **"it uses popular data formats well, and it can query from the network, from the files, from whatever easily."** The second is under the covers: vectorized execution and effective multithreading, which a casual user would never name but which make applications feel instant. **"A big network cluster-driven query system takes half a second just to get started,"** he says, before it has even finished planning, **"and DuckDB finished several hundred milliseconds before that."** The third, which he rates as practically a feature in its own right, is installation. **"The install is painless, tiny, and quick."** You can drop it in a container, install it without privileges, or wipe it out and **"leave no traces."** The installer **"doesn't show off, but there's an enormous amount of work making it look trivial,"** he says, comparing it to gifted musicians and rock climbers who make the hard thing look easy. He credits Peter Boncz and the wider team: **"This is not his first rodeo. He's been involved in these ideas of vectorized computation for decades."**

## A Single Machine Goes Further

Behind the sensor project sits a broader argument, and Dunning is well placed to make it. **"Whereas 15 years ago we needed clusters to scale to large scale data, there's an awful lot you can do on one machine lately,"** he says, **"and that limit isn't even hard and fast."** Put DuckDB on something more capable than a Raspberry Pi and the results, he says, get enormously performant.

He is careful not to overstate it, catching himself before he reverts into, as he puts it, an old codger. But the hardware really has changed. As an intern at Los Alamos he touched the first Cray-1, then the fastest computer in the world, and he notes it was **"so enormously slower than a Raspberry Pi."** A generation of engineering went into contorting problems to fit tiny machines and slow networks. **"That level of contortion just to be able to do something simple is no longer necessary,"** he says. **"Computers now match the scale of our world."**

This is not an argument that distributed computing is obsolete. The genuinely enormous data sets, he notes, do not belong in a database at all. It is an argument that the default no longer has to be a cluster, and that for a large class of analytical work a single machine running DuckDB is the simpler and faster answer. **"The first step is quite modest,"** he says, **"but there doesn't seem to be a last step."**

## An Accessible Engine, and a Look Ahead

Dunning also sees DuckDB turning up where he did not put it. Using an AI assistant on the sensor project, he was surprised when it reached for DuckDB on its own. **"Without prompting it said, 'Oh here's a DuckDB query,'"** he recalls. **"It's not just obvious to me, it's obvious to AIs."** He reads that as a sign of how far DuckDB has spread, and of how accessible it is to people who are experts in something other than databases.

His own research in recent years has centered on security, specifically on how permissions are granted and delegated. He cites a survey finding that **"80% of data breaches ... were due to misconfigurations,"** and argues that the real problem is systems too complex for people to use safely. He wants to build systems where security is **"so simple that you can just see it at a glance,"** and he sees both DuckDB and AI agents fitting into that. He describes giving **"a little bit of privilege to an agent to pass on to the thing that's actually gonna do the work, which might well involve DuckDB three relays down,"** without any relay inheriting his identity. **"I want them acting on this one permission to do this one task,"** he says. 

This is a direction he is exploring rather than a system he has deployed, but it follows the same instinct as the rest of his work with DuckDB: keep the moving parts few, and let a simple tool do more than its size suggests.
