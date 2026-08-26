---
layout: post
title: "What Next for DuckDB"
author: "Hannes Mühleisen"
thumb: "/images/library/thumbs/2026-08-26-developer-voices.jpg"
image: "/images/library/thumbs/2026-08-26-developer-voices.jpg"
tags: ["Podcast"]
length: "100 min"
thirdparty: false
excerpt: ""
toc: true
pill: "Developer Voices by Kris Jenkins"
---

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/C3l4CsP1Ak0?si=u_DMOqM7NgftcqOi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

|-------|-------|
| **Podcast** | [Developer Voices](https://www.developervoices.com/) |
| **Guest** | [Hannes Mühleisen (DuckLabs)](https://hannes.muehleisen.org/) |
| **YouTube** | [What Next For DuckDB](https://www.youtube.com/watch?v=C3l4CsP1Ak0) |

## Transcript

### Introduction

<!-- [00:00:01] -->

*I'm joined today by a returning guest, Hannes Mühleisen. Hannes, how are you?*

I'm great. How are you, Kris?

*I'm very well. It's great to have you back from the duck-filled heart of Amsterdam.*

Yes. We have many ducks. We have actually adopted ducks in the zoo here as a company because we have such a deep love for ducks. There's a plaque somewhere and everything.

*You know you're doing well as a startup when you can afford that kind of sponsorship deal.* 

It's not that expensive.

*There is something of a theme running through some of our guests having or owning ducks and cats. Ducks and cats. We've got a few other duck-owning guests in the history.*

Interesting.

*Let's not get too deep into that because we can go mallard crazy. But it has been – I was checking – about two and a half years since you joined me. Took me back to school on the internals of how a database works.*

Yeah, it's been a while.

### Previously on Developer Voice

<!-- [00:01:04] -->

*So for those that haven't watched the previous episode, let's just start with a recap of what's DuckDB and why does it exist? Because aren't there a lot of databases, my friend?*

There are many databases, but obviously they're all wrong. So, DuckDB – we like to describe it as a universal data wrangling tool. We have thought about this quite a lot: what it is, what we think it is. But this idea of giving people confidence to work with data, that's really our guiding principle. And it's also why DuckDB was built from scratch, because we realized that there were really not a lot of database developers that had put user or developer experience really first. And so that was really our principle that we started DuckDB with. We said this needs to be trivial to set up, this needs to be friendly in its error messages, and the SQL dialect and all these things, like principle of least surprise, and it needs to not have the most conservative defaults but the most reasonable defaults, and all these things, right? And when we looked at these requirements, we realized that we really couldn't just take something else and repackage it. It went very deep. And that's why about eight years ago we started on this lovely journey. Mark Raasveldt, my co-creator of DuckDB, and I started on this journey of building a database from scratch, which is a bit of a daft idea in retrospect.

*But we have a lot of such lunatics come through these doors.*

Yes. I mean, I've seen some of your episodes, of course, so I'm aware. But it is definitely something where people told me it's going to take you 10 years, and I was like, nah. And now I'm like, yeah, you are right. I thought this would be done in two years, but they were correct.

*Funnily enough, I've made that mistake as well in projects, and I've realized only bad projects have a fixed deadline. The good ones keep expanding, right?*

It's also the case for system software like databases or operating systems or things of that statute, that they are never really done, right? Stuff changes. The hardware changes, the operating system changes, the compiler changes, the C library changes – there are a lot of reasons. I mean, deep down I really love the thing that TeX is doing, the typesetting thing, where it's considered done and the version number approximates pi better and better over the years, which is kind of crazy. But it's not semantic versioning, it should be burned at the stake. But the idea that software can be done, I really deeply like that. With databases, not sure.

*I've got to push back against that. A bad project – no one really uses it, it achieves all its goals and no one needs more from it. It's a good project that people keep saying, "What if we did this? I need that. You need to be supporting this platform." Right? The good projects never end.*

That's fair. We did do a bunch of stuff in DuckDB so that we don't have to do everything, right? So it's not a monolith. They have all these plugins – extensions, we call them – that you can install and build and whatever. So there is a chance that we will get to some sort of stable state with the core itself. But I'm also a very realistic person, so I think we will be doing this for a while. Fine. I'm fine with that.

### Focus on User Experience

<!--  [00:05:03] -->

*So I want to pick you up on the thing you just said about usability, right? Because I think it's a very difficult bridge to construct, and I do think you've constructed it. I want to know how. Plenty of people would say, "Let's make a database that's user friendly," and they would succeed, but it would be technically scrap. So I'm not going to single out any particular databases, but there were some, particularly in the NoSQL movement, that were incredibly easy to use, didn't work very well, didn't actually save your data to the disk, and things like that. And then you've got academics like you saying, "Oh, we should do a database properly," and they don't succeed in usability at all.*

Yeah, I think that's an excellent point, and I agree with you. I think one of the tragedies we observed before starting DuckDB is that the state of research and the state of practice were about 20, 30 years apart from each other. And indeed we saw exactly what you described. So I think the reason why we managed this is because I am actually a bit of an insider and outsider. I'm a bit of a – what do you call this ugly duck thing? Like a weird duck. There's some expression in English.

*A strange duck.*

Thank you. A strange duck. In Dutch it's “de vreemde eend”. But they have it too.

So I didn't come from the database orthodoxy. I did my PhD on something in distributed systems. I worked on ant colony optimization – a story for another time, maybe.

*And now I know why those ants are so much more efficient these days.*

Ants are amazing. But then this weird thing in my life happened where I moved to Amsterdam and I needed a job, and in a gigantic overestimation of my own skills I was like, okay, I have used a database before, I can probably work at this database research lab here that has currently a job opening. So they ended up hiring me, which – I still am amazed they hired me. I don't know why. And I actually led that lab later, and I wouldn't have hired me. So it's one of these car crashes of history. But the result was that I wasn't educated like everybody else, because a PhD in databases is a very structured thing. You go to this seminar, you go to those conferences, you talk to those people, these are the senior people in the community, and there's a sort of orthodoxy that's instilled in everybody. And user friendliness is not one of them in the curriculum. It's not in there at all.

And so I think that was why – because I wasn't really an outsider, I mean I'm still a computer scientist, I'm still a nerd, I still like stuff, right? And I still appreciate the orthodoxy of databases, but it is not absolute to me. Maybe I should say: if you think about research, you want to have impact. And I realized very early on that in order to have impact you need to appeal to as many people as possible. And how do you do that? Well, by being user friendly, right? And that is really a great driver, because it has benefits in every direction. Your papers get accepted because people know you. You get grants accepted because you can show that your software gets downloaded a gazillion times each day – that's a pretty good impact statement, right? Your papers get read. And so there's really a beneficial – what is it called? A virtuous circle. Yeah, when you go for maximum impact. And I mean, I got grumpy department heads telling me my [h-factor](https://en.wikipedia.org/wiki/H-index) was down the toilet, you know.

*Yeah, I heard this term, h-factor.*

This is something academics do. It's terrible. So, okay, minor rant: if you are a manager of multiple people and you are too lazy to actually make a call on who is good and who is bad, then you come up with some metric, right? Right. And one of those is – I think it's called officially the H-index. I don't even know what it's properly called, because I don't care about it. But it's a way of looking at your publications as a researcher and then how many times they are cited, and then there is some math going on to average all this into a single number, and that's your worth as a researcher. A bit questionable, maybe.

*How can we turn people into numbers that we can sort?*

Yes. And then your department head, you know who to give the promotion to, right? It's great.

*Yeah. And more importantly, your boss can't fire you for making the wrong call because you backed it up with a fact.*

I mean, this metric is not at all susceptible – not at all hackable, right? Nobody would ever do anything like that, right?

*So career-wise, you've just destroyed your h-factor and gone into making user-friendly databases.*

Correct. It was a gamble, absolutely a gamble. If this hadn't worked, I would have had to find somewhere else to work than research. Amazingly, it worked. But that's a different story. It was a gamble for sure. But I only took the gamble when they couldn't fire me anymore, when I got tenure at the institute.

*Tenure – it sounds like a lovely thing.*

It's a very hard thing to get, let me tell you. It's rough.

*I'm trying to get tenure as a podcast, but apparently they haven't taken my application seriously yet.*

No, the government should maybe get in on this.

### Choosing a Single-Node Database

<!-- [00:11:08] -->

*Okay, so anyway, you've started to break out of that management loop. We talked a lot about how this was built, but I think one more thing as a recap: DuckDB is a sort of local, just-point-it-at-a-file analytics database. What makes that the choice you went after? Because there are lots of kinds of databases, and you just said you had a background in distributed systems. You could have done a peer-to-peer network database. Why go for something that's kind of small?*

That's a great question, and I think that was also because there was actually nothing in that space. One answer is that back in 2016, 2017 there was a lot of choice on distributed stuff. Why make another one, right? And remember what I said about this needing to be friendly and easy to use. Distributed systems are the exact opposite of being easy to use. I have set up these things myself and it is an absolute nightmare, right? You're installing software on 32 computers at the same time, and then one of them says, "Oh, I don't like your permissions," and then everything crashes down and you have to grep logs on 32 machines. It's an absolute nightmare.

So the single node followed from this simplicity requirement, but it also followed from this insight that people went basically straight from pandas to Spark, because the most competent single-node data analysis thing there was was pandas at the time. And pandas is obviously amazing – Wes is a friend and we talk – but I think he would also admit that it's not particularly efficient, right?

*And I wouldn't say, unless you're very comfortable with it already, that it's that accessible.*

No, the API – that's another discussion. I mean, SQL can also be clunky. There are pros and cons here. I think the lack of an optimizer is the bigger problem. I think the problem in pandas is that you are the optimizer. Great – we just have another job. But I think if pandas stopped working for you, that was it: you had to go to Spark, with all the problems that come with distributed systems, and cost. So we also realized that there was a lot of space between where pandas ends and where the capabilities of your machine end. There's a huge gap, and that's where DuckDB is, of course. So DuckDB can really make the most out of the hardware that you have. And hardware has become quite amazing. It's an absolute tragedy that we use a MacBook with an M4 or whatever to run Chrome. This thing can do serious data crunching if you let it, if it has the right software.

*Yeah, we talked a lot about this in the previous podcast, but I still didn't quite believe it until I tried it: you can aggregate two billion rows in a second these days, with the hardware and the algorithms we talked about last time. Yeah. And yet it still seems like a struggle to get a spreadsheet up some days. We're doing something wrong.*

We have one of our most popular extensions in DuckDB, which is the Excel reader, which I think is hilarious. So you can actually point DuckDB at your spreadsheet as a table.

*So you can say "select star from XLS"?*

From my spreadsheet, yeah, absolutely.

*Oh god, I didn't know you could do that. Okay, I'm adding that, because I use that sort of thing. One of the things I like about DuckDB is you can query a CSV or a JSON file directly as though it were a table. Didn't know you did Excel as well.*

I think it's a community extension. I'm not sure who built it, but it exists and it's very popular.

*So maybe I should point people at the previous episode if they want to get all the details of how we get to there. But we left the last episode with DuckDB as a local, very fast, very easy to use, single-file database. To me it was SQLite but for analytics.*

That's absolutely the tagline that we went with, and I think it's still a good tagline. I think we may want to talk about the journey so far since then, but it's now changed a bit, more into an ecosystem. I would argue it used to be "SQLite for analytics" and now people call it “the Duck Stack”. Yeah. And that is true, right? We did a lot outside the single-node database. Of course, that's still a very core thing we do and we still push it like crazy, but we have done more things, we have put tentacles out.

### The Trouble with Database Protocols

<!-- [00:16:46] -->

*This is exactly where I want to go, right? Because one thing you decided to go from that was a client-server model.*

That was actually quite recent. Yeah, that was Quack. I mean, obviously it has to be called Quack, because how do two ducks talk to each other?

*Makes sense.*

We do have a rule in the company: no stupid names. And then I said, "Okay, we should call it something more boring." And then some of our DevRel people were like, "No, absolutely not. It needs to be called Quack." And I was like, "Okay."

So this is super interesting, because we actually wrote a research paper way back when, Mark and I, about how terrible database protocols are. That was pre-DuckDB.

*They are?*

Oh, you have no idea.

*No, I want some idea. Tell me.*

All right. Okay, so let me go back to our seminal 2016 paper. One of the things we were investigating is why people hated databases. And one of the things that was brought up is that it's extremely slow to get data in and out. And we thought, hm, that's interesting, why? And so we started looking at the actual client-server protocol that all the databases use, because if you have a client-server setup then getting data in and out has to go through said protocol, right?

And so we wrote a [research paper](https://duckdb.org/library/dont-hold-my-data-hostage/) that was published at VLDB, a very prestigious conference in databases, and the paper investigated the actual protocols that basically all the major databases were using. For example, we used Wireshark – that was fun. Wireshark is this low-level protocol analyzer that you can use if you want to reverse engineer your egg timer or something like that. But we could use that to reverse engineer database protocols. So we reverse engineered the Oracle protocol, because there's no specification available. We just reverse engineered it and described it in the paper. And we looked at the Postgres protocol and the MySQL protocol and, I think, the MongoDB protocol, and Oracle, and a few others. And what we could show is that they're horrible, in the sense that you are better off just piping the CSV file over the socket than using any of these bespoke protocols – by a factor of 10\.

*Oh yeah. How are they so bad? What are they doing wrong?*

Well, maybe let me rant a bit about the Postgres protocol, because it's actually quite popular and it's something that irks me a little bit, because lots of databases also use the Postgres protocol even if they're not Postgres. There are very nice properties: you can use their clients and you don't have to write your own clients. It's very annoying to write clients, trust me, I've done it. But the Postgres protocol in particular does something where every row you send back from a query result is its own protocol message. So it has a header, a length, a type. And on every row, for every field in the thing, it has bytes in there that say which data type it is, whether it's null or not. And then there's the actual byte data, which is in a binary encoding.

This is interesting, because it's a relational database where in theory all the fields in a column have the same type, right?

*But if you send back a million rows, every single row tells you what the schema of that row is.*

Correct.

*Which you could have just done once at the start, and you could have skipped it because you already know the schema of that table.*

And I would say you should have done it once. The reason they don't do that is because of Postgres's obscure roots as an object-oriented database, where every field could be a different object. That's why they do that. It's of course completely insane from today's perspective, right? But that's one of the things. So for a four-byte integer they send another four bytes of crap, pointlessly. And then, as I mentioned, they have a header for everything, and everything is a separate message, and the result of that is just horrible protocol interaction. And then also the implementations are not great, right? The client will process a row at a time, because it's a message, and there's a big switch somewhere on the message type. So it's fine if you shove 10 rows over this protocol. It's fine if you shove a couple of hundred rows over this protocol. But once you're looking at analytics – and we specifically looked at this from the perspective of analytics – once you want to transfer a million rows, you are absolutely screwed with these protocols.

*Right? So that in itself seems – no, I can imagine that's very stable. Let's call it stable. So that in itself seems pretty easy to fix if you want to add a new protocol to DuckDB, right?*

And that was actually the cool thing about Quack: we could design a protocol in 2026\. 

*What's more surprising is I don't really see it as a client-server model, DuckDB.*

That is an excellent point, because you can do much more than that. But obviously, when we build something, we think about what is the immediate thing we want to solve and what other things do we want to enable down the road.

So let me mention briefly the motivation for Quack. We had always said we are a single-node, in-process database, we don't do client-server, because we have shown conclusively how client-server is, let's say, questionable. But what happened then was that lots of people actually bolted on their own client-server protocols on top of DuckDB. There are at least five or six projects out on GitHub, and a bunch of companies that have done that. So everybody basically invented their own little RPC mechanism to talk to DuckDB, and then other people bolted something called Arrow Flight SQL onto DuckDB, which is an attempt by the Arrow project to make a database protocol, which is in my opinion flawed, but an attempt was made.

And so we watched this, and then we were like, at this point, if all these people are doing this, there's probably a demand for it. And at some point, I don't need to be right. I just want to solve people's problems. That's the orthodoxy versus pragmatism divide that we talked about earlier. At some point I was like, yeah, I have been out there and said we won't do client-server, and oh my god, how can I live with myself if I now go back and say, by the way, here's client-server for DuckDB? But as I kept thinking about this, I was like, you know what, fine – consistency is overrated. I want to solve people's problems. If that means I have to eat my words and be wrong for once, that's totally fine.

*Yeah, it's our job to solve people's actual problems, not the problems we think they ought to have.*

Correct. And I think this is a very nice way of putting it. If you tell people what problems they ought to have, or how they ought to solve their problems, that's precisely the kind of mindset that I saw in the database orthodoxy when I started working in this field, where they were basically always yelling at the users, "You're holding it wrong," right? Which is maybe a way of doing it. It's not the way of doing it. And that's something where we have a very different approach. If we see 15 times the same issue report, we say, hang on, we need a structural solution here. We can't just keep explaining to them how they're holding it wrong. We need to somehow fix this structurally. We have to, I don't know, have a warning message.

There was actually a good example recently. There was somebody, Rusty, one of the valued community members in DuckDB, and he said, guys, sometimes DuckDB doesn't have a defined result set order. For example, if you read from a source that doesn't define a result set order, and you then put an `OFFSET` without an `ORDER BY` – so SQL has this `OFFSET` thing where you can say give me everything from row 10,000 to row 20,000 of the result. If you have a non-deterministic input order and you have no sorting criteria on the query and you specify an `OFFSET`, the results are completely non-deterministic. Which is by definition – yeah, this is very true. And I was about to write back "you're holding it wrong," and then I thought about it for a couple of hours, and days, I don't know, and I went back: no, we need to fix this. And now – I pushed a pull request a couple of weeks ago where, in this situation, it will show you a warning saying, hey, this is non-deterministic, you can make it deterministic by adding an `ORDER BY`, but just be warned. We've told you. And that's the same thinking as with this Quack thing, right? It's not about being right, it's about solving people's problems with data.

*Yeah. But doesn't it open up a whole host of problems that you hadn't originally designed for? Because by the time you've got client-server, now you need to worry about concurrent writers, which is where databases just explode.*

Actually, we had support for concurrent writers for a long time. We just didn't have support for concurrent processes writing to the same database file. These are two different things. DuckDB has supported concurrent writers from different threads in the same process for a long time, so that wasn't something we had to add. We have also greatly improved this recently, where now you can commit while checkpointing, things like that. The concurrent writer thing wasn't so much the issue with Quack. The problem – client-server is quite ugly in the failure modes, let's say. So we suddenly have to deal with the fact that the connection goes away, and it goes away in various ways. You pull the cable, the other side stops responding, you're running into all these timeouts, you have to clean up resources but you don't really know when, because the other guy might still be coming back or not, we don't know. There is exhaustion of file descriptors when there are too many connections. You have all sorts of interesting systems problems that we haven't had before, and we spent quite a lot of time trying to work around them.

But the biggest problem with client-server is the cyber surface, right? DuckDB so far has no externally accessible port or anything like that, so the Russian bots couldn't attack it from the network.

*Right.*

Or other countries – there are other countries that do malicious hacking. But we didn't have that, so the attack surface for DuckDB was much smaller. Now we have a client-server protocol, which means this port is now hanging out in the open internet, possibly. Now we have to be very, very careful about what you accept and how you accept it, and that you can't do a denial of service. What happens with authenticated attacks, unauthenticated attacks? So that is a whole new space for us that we hadn't really dealt with before. I mean, obviously we're not idiots, we know the fundamentals there of how you could attack this – the classical buffer overruns, sending malicious packets, these kinds of things – but it was a new surface for us, for sure.

The other thing we had never had to deal with was authentication and authorization, two of the massive, endless black pits of databases. Yeah. Authentication is like, okay, is this user authenticated? That's kind of easy. But then the authorization is, can this user read this table? And oh my god.

*You've got to stick in a whole role-based access control stack, which enterprises love but is no fun to implement.*

And it's a huge expected feature set, right? So Postgres has a lot there, to their credit. As you said, enterprise loves this kind of stuff. Enterprise – and maybe another minor rant – enterprise loves this kind of stuff, and then they complain that their queries are slow. I see this a lot, where you have a trivial query and it would take a couple of milliseconds to compute, but to compute the rights, whether this user can do this, takes seconds. So this is also something that I tell people: guys, I know your compliance department has ideas here, but there's an actual cost associated here.

*Have you run into that problem, then? Because DuckDB is sort of built for analytics performance. Are you saying the performance has dropped just for the sake of security, or have you had to solve that?*

The way we solved it for now is we added callbacks that you can define. For authentication you can give a callback, which is a SQL-level function that I will pass the credentials the user has sent over the protocol, and your function can say yes or no, and if it says yes it will let them log in. So this is something where you can write an extension, or you can even write a SQL-level function that basically decides whether somebody should be allowed to log in. That's part one, that's authentication, right?

Then for the authorization, we have something similar now, where there's a function that gets called before the query gets executed, with the query and with the user that's authenticated. And then your function can think about whether it wants to allow this user to do this action. So we kind of abstracted ourselves out of it and said, we cannot solve all of these cases. We give you the tools to build your own thing. But obviously if that thing takes a while, your query runtime will have that as a constant factor. There's nothing we can do about that, right? It's up to you.

So it is a very interesting problem. There are some approaches in research, or in people doing open source, that are thinking about this stuff, that are quite interesting, that push some of this down into queries again – because some of these things become joins and predicate evaluations and stuff like that. But there is obviously a cost to it. I just find it very funny when the enterprise people complain about this sort of thing, because it's like, yeah, this is a you problem.

*I'm sometimes surprised that the whole thing isn't just another standard set of SQL queries, because a lot of times authentication is recursive SQL.*

Right, that is a great way of doing it. I think that's not typically how it goes. Typically this is a completely orthogonal thing in an engine, and I don't think it's a great idea. And there are some ideas internally on how to make this more of a SQL-y thing. But I'm not sure yet where this is going. It's also not something that I am particularly excited about, honestly. To be quite honest with you, every enterprise is enterprise-y in its own different way, and they have the money to solve this, so they should just leave me alone.

*Yeah, so you're just giving them the access points.*

I give them the way of doing it.

### DuckDB's Extension Mechanism

<!-- [00:33:50] -->

*But this leads to something we didn't talk about last time, but I wanted to know how it works under the hood, which is DuckDB's whole extension mechanism.*

Right, this is very cool. Fun background story there: we built this extension mechanism because we didn't want to merge a particular pull request. Somebody who we knew sent a pull request, and we were like, ah, we hate this. And this was about graph stuff in databases. I have not-so-positive feelings about graph query processing either. I think it's a bit of a distraction, but we can talk about that. Anyway, somebody sent this pull request and we're like, nah, we hate this. So let's give you hooks instead, so that you can do that yourself without bothering us anymore.

*Another solution to the "you shouldn't want this" problem. Kind of, yeah.*

And also to the feature creep, right? For example, the Excel reader I mentioned earlier: not everybody uses this, so why should we bake it in? There are other databases, I won't name names, that are just bolting every single feature that they can dream of onto the single binary that they ship, and as a result the binary is a couple of gigabytes. Great job. So we don't want to do that. We want to stay small. So we have these extensions.

The hooks are pretty straightforward. You can imagine every component of DuckDB having hooks in it that you can connect to from an extension. So for example, the simplest extension is: I'm going to add a scalar function. I have a function that computes, I don't know, the Ackermann function, that does not ship with DuckDB – we don't have the Ackermann function, as far as I know. But let's say you want to do that. Then you make an extension, and that extension will say, I have a scalar function, it's called the Ackermann function, and this is the implementation. And then you load that into DuckDB and it will be added to the internal list of functions, and you can call it from SQL. That's scalar functions, right?

*Before you go on, give me more details on that. So what do I do? Do I write a C function and give you the binary and a header file, or what?*

Typically you write against a header, yes. There is a header, `duckdb_extension.h`, and that will have the functions that you need to interact with DuckDB. For example, there will be a function in that API that says, I want to register a scalar function. Right. And so you call that function. And what does it take? Well, it takes a name. It takes some definition of the parameters that that function takes – are they strings, are they integers? What type does this return? We are a type-safe system, so we have to say which type. And you will also give it a callback that has the actual implementation of the function.

So the callback has to conform to a function signature for scalar functions, and that is a defined thing where here's a parameter that gives you the input – the vectors, because DuckDB is a vectorized system. So you get vectors as input and you produce a vector as output as a scalar function. And then there are some helper functions in the API that help you to extract, let's say, integers from this input: okay, loop over this input, give me the numbers, then you do your own thing to compute Ackermann, and then there's another set of functions that allow you to put that number back in the output vector. And that's kind of it. There's also other stuff, you know, if you want to raise an error or you want to do other things. So that's very straightforward.

It's a C function, and we are currently moving – we had two APIs. We had an internal C++ one and we had a public-facing C API, but we are currently moving everything to this public-facing C API, because it gives us cross-version stability, which is very nice. And so basically you program in this API, and this API is quite extensive. You can create functions, you can create types, you can create other kinds of functions like aggregate functions or window functions or table-producing functions. You can add settings. You can add optimizers – actually, you can add whole optimizers. You can add logical and physical operators. So you can do things like, here's my new fancy join type and this should trigger in this and this circumstance. You can ship your operator for it, you can ship your optimizer that detects that circumstance and adds the operator. There's lots of things you can do there.

And actually, it's interesting that you bring this up, because in our next release, 2.0, which is coming in October, we think, we are finally adding the last bit of the puzzle, which is the pluggable parser. That's another paper we wrote, two years ago I think, because we had everything in DuckDB was already pluggable except for the parser, because parsers are ancient technology from the sixties usually. Yeah, LALR(1) – Knuth himself has written about this, so you can kind of get an idea how old it is. And so the last puzzle piece for extensions was: can you actually change the query language? And I'm happy to report that in the next version of DuckDB you can actually change the parser. So we've completely ripped out the Postgres-based parser we had before and rewritten it into something else.

### Details of the New SQL Parser

<!-- [00:39:48] -->

*Okay, you're going to have to give me some details on that, because parsing SQL – it's like the final boss of parsing, I reckon.*

What do you mean? It's the syntax. It's a language that's obsessed with syntax.

*Maybe Ruby is the final boss.*

No, I think you're absolutely right, SQL is the final boss, because it's a language that is obsessed with syntax. If you compare SQL to Python: in Python everything is a function call or an assignment or – there are like 14 things something can be, and that's it. And then everything the user does just uses these abstractions to do something. But in SQL, on the other hand, everything is syntax. There are hundreds of keywords, right? There's `HAVING` and `USING` and all these English-y things in SQL. So parsing SQL is actually hard.

*And you get the thing where sometimes an identifier can be just an identifier or a keyword, depending on where it appears and what kind of statement.*

Yeah. And then, unquoted identifiers cannot be reserved keywords is also really fun. So some keywords are reserved and some keywords are unreserved. The reserved ones you can never use as an identifier, and the unreserved ones you can use in some cases. This is funny, because this is also something I worked on myself, so I'm very happy to talk about it. Actually, I have now handed over to Daniel, one of our guys who's working on this full time. But I wrote the first version.

*Okay, we need to get Daniel in to see what he thinks about the first version.*

No, no, he's cool. Well, you would never get to his version without the first version. It has its place in history.

So the way everybody does parsing is with `yacc` and `bison`. I don't know if you've ever worked with `yacc` or `bison`.

*It's been a while, but yeah.*

So `yacc` is actually the name of "yet another compiler compiler". But it's also very yucky, if you want to make that joke. I think it's a good one. Because it is really the mummy of computing staring you in the face. This is stuff that – I think the first paper about yacc-like parsing is from Knuth, and it is from the sixties, like 1963 or something ridiculous like that. 

*When you write in `lex` and `yacc` and bison you do feel like you've been time-warped back to the early days of C.*

Yeah, exactly. And then the problem is – there are two problems: one is the abstraction and one is the implementation. The implementation is this weird mixture of extended Backus-Naur form to define a grammar and these inline C templates that get expanded by the yacc compiler into an actual C file with a big lookup table. So one of the problems is the implementation, which by now – you're using bison, which is pretty terrible. If anybody has ever seen a shift-reduce conflict, then you know I'm with you. I now know what this is. It's funny, because I had to learn all of that for writing the paper: what is this actually?

But the other problem is the abstraction. LALR(1) is a single-lookahead parser, so you can only look at the next token to determine what this token means. Which for SQL is terrible, because SQL has a lot of things where it's like, you know, `SELECT x FROM y ORDER BY z`. You will notice that `ORDER` and `BY` are two tokens. Yes. So the Postgres parser, for example, has all these wonderful hacks where in the lexer they will glue these tokens like `ORDER BY` together again into one token so that you can detect them. However, this means that you also have to strip all the comments already in the lexer, because otherwise you could have a comment between `ORDER` and `BY` and you would not be able to detect that it's `ORDER BY`. Which again means you cannot have things like annotations in the Postgres parser, because you might want to have comments that give hints to the parser or something. Not possible, because they need to strip the comments in order to detect the two tokens that they cannot detect later in the parsing step. It's a complete mess.

*Oh yeah, that's nasty.*

It is nasty. And this is a 20,000-line grammar with C interspersed. A nightmare. So we have looked at this a lot, because we used to use the Postgres parser in DuckDB, and to its credit, it worked.

*It is a very complicated language to parse, right? There is a lot of surface area.*

It is. And it worked, and it was only painful when we tried to change things. And as you may know, we did a lot of friendly SQL things where we'd say, hey, maybe we can do `GROUP BY ALL`, or `SELECT` star is optional, you can just do `FROM` table – these kinds of things. So we actually ended up hacking that parser a lot, and therefore had to suffer a lot.

And then the biggest problem was it wasn't extensible. This was a monolith that was baked together at compile time, and our extensions couldn't do anything about it. Which is annoying, because in order to deflect more of these requests of people wanting stuff from you, they need to be able to also change the syntax, because some people want different query syntax. There's some project – I forgot the name now – PRQL, for example, is one of them, where people have proposed different kinds of SQL syntax, right? Not possible in a Postgres parser.

So we ended up rewriting the parser from scratch, accepting that memory is slightly bigger than it was in '63. And whether parsing takes a microsecond or a millisecond really doesn't matter, right? We have some more space in this whole thing now.

*And if you have to hold lots of potential parse trees before you commit to one of them, that uses up memory, but not much.*

Not a lot, no. And so we've written this into something called a PEG parser, which is a much more recent abstraction, which is also something Python has switched to, by the way. They did this too. Okay. They switched a couple of years ago, or maybe not that long ago – I think two or three years ago – Guido himself switched Python from a `yacc` parser to a PEG parser. So PEG is like a recursive descent kind of thing. It's a greedy, different abstraction, but it works better. And the nice thing is you can modify that at runtime. So now you can load an extension into DuckDB and that can say, hey, here's my new parsing rule and here's the transformer that tells you what kind of logical tree I want to make out of this parsed set of symbols. So that's very elegant.

*Sorry, now I'm curious: what do you actually use? Is there some PEG library you choose for C?*

There is, and that's what we use for the prototypes. There is `peglib`, that's actually very nice.

*Okay, `peglib`. Good name.*

I think it's called `peglib`. But we ended up writing our own. It's not complicated, really. The grammar has like five different constructs, and you can really make a trivial – I wrote a trivial interpreter for it. It's not crazy. We just ended up writing our own PEG interpreter. It's not so wild. You have to eval – it's a recursive thing. So you evaluate: oh, I see an alternative symbol here, so now I have to descend these two trees at the same time. I see a "multiple times" kind of statement, so okay, I can invoke this multiple times. There are some optimizations, because it's very easy to hit recursion depth limits there, so you have to be a bit careful with how you manage this kind of state. We're probably still going to rewrite this into an iterative algorithm, just to manage it, because one of the wonderful things about C-like languages is that you can run out of stack space.

And so we've written our own, but it is really just the normal PEG grammar. And we've actually written a SQL grammar for a PEG parser that we ship with, that other people have already started using, which is kind of cool.

*Oh, it's open source?*

Of course, everything is open source. So we have this PEG grammar now and we have this parser for it. And I've actually heard – and I'm not allowed to say who – but I have heard that another major database is interested in adopting this parser. So it's also something that might have impact beyond DuckDB, which is very cool to hear. It's like, what, you want to rip out your parser, really?

*Okay, that's a show of confidence.*

And again, something I found really amazing, similar to how nobody had ever written a scientific paper about protocols – the client protocols you just talked about – nobody had ever written a scientific paper about parsing. And you think, there are hundreds and hundreds of join papers.

*Are you specifically talking about parsing for SQL?*

There was never a paper in databases that talks about parsing SQL queries, and I am amazed by that.

*That's astonishing.*

And we wrote it, obviously. But it was amazing to see. This is my favorite thing in the world: when you as a researcher walk around on this ancient battlefield of databases, where you think that every square meter has been bombed to bits but there are these whole areas that are completely ignored, right? This is something that I find amazing.

And I think the reason is because people consider it trivial. Well, it's not.

*No, that seems like an excuse – no one wants to open that can of worms.*

Or they never think about it, right? As a database person, I can tell you: if you think about queries as trees, that syntax thing is more like, yeah, that's how the monkeys talk to us. I'm not saying I do this, I'm just saying that's the sentiment I have observed.

*Okay, getting back to user space then: have you done anything to mitigate the danger that someone can create an extension that completely banjaxes the SQL, that they can break the parsing?*

They can. That's actually a good thing. You might want to actually restrict the query language that you allow. That's actually a cool feature, because you could say, hey, I only want you to be able to do filters on this table, and maybe projections, but nothing more, because I want this to always force a streaming execution. You can't do aggregations, by the way. You can ship a parser rule that just disables everything else, and then you cannot create those plans anymore. I think it's a feature.

Obviously, people are generally responsible about which extensions they install, and if they want to break their SQL syntax, by all means.

*Yeah, and if you want to load an extension, that comes with a certain acceptance that the author of the extension is in the right.*

It's like a Python package. In fairness, a Python package cannot maybe break the parser, although I would probably manage to build one if I wanted to. Yeah, it's all the same address space, you can do whatever you want. I'm just wondering now how I would do that, and I'm sure it wouldn't be hard. You'd probably have to find some symbol that they don't export, but it's there.

*Okay, if you're listening at home, don't do this.*

It would be fun to mess with your co-workers that don't understand computers fully.

So it's an April Fool's thing.

Yeah. It's like there's this old C joke: `#define true false`. Hide that somewhere in your include files and then watch the world burn.

*And then just as you leave the company. We do not condone this behavior.*

We don't condone. No.

### The Iceberg Format

<!-- [00:53:22] -->

*Okay. So you've got quite an extension mechanism built up, and extending the parser. That leads me to one specific extension I wanted to talk about, because you're in the analytics space. It's something of the hotness in the analytics world at the moment, which is Iceberg. I know since we last talked you got Iceberg read and write support. But what I'm not sure of is how DuckDB plays in a world where it sort of gives up the analytics to a larger distributed system, right?*

Yeah, Iceberg is interesting. It's something where, I think, this was also one of these things where we looked at it when it first bubbled up and thought, what is this? And then people kept asking for it, and then we had again to go back on our convictions and say fine – but we're going to complain the whole way. So, Iceberg is a great idea, to fix this problem of naked Parquet files on S3 being the way you store data, this whole data lake idea, right? And so that's one ingredient, and the other ingredient you need is change. People always treat change as an afterthought, right? It's like, oh, the data has to change.

*Having spent a lot of time in the real-time change tracking world – yeah, it is often an afterthought at best.*

Correct. Exactly. The academics are guilty of that, because we do static benchmarks a lot and it's like, ah, it works fine, moving on. But change – everything flows. We know this. The Greeks knew this. So this idea of Iceberg is to somehow have sanity in changing data that sits on a data lake, right? You have a bunch of Parquet files on a data lake, you want to be able to add rows to this, you want to be able to delete things, you want to be able to update things, you want to be able to change your schema, with some level of sanity.

*Fill in the gap: Parquet files being "let's store everything in a column-oriented fashion for analytics performance," right?*

Yeah.

*And then the Iceberg thing on top is the catalog that says where all the data is and manages adding.*

No, not really. There are two layers there, actually. The first is the change management layer. That's another set of metadata files. It sits on top of these Parquet files. The worst format in the world – it uses Avro. I don't know if you remember Avro, but it's from Hadoop. Yeah, you do.

*We might come back to that. We might have to have that debate, but carry on.*

I have some rants there.

So the first part of Iceberg is this metadata level of files that tells you which versions exist of that table, which files are part of it, which schema exists, that kind of stuff. And then on top of that you have the Iceberg catalog stuff, and those are not files, that is a service, right? And that's a REST API kind of thing that indeed does tell you which tables exist and where they live, and gives you credentials to maybe read from S3, things like that. So there are two layers there. And actually the file metadata stuff was first, and later on they tacked on the REST API. It's also called the Iceberg REST catalog. That came later.

So that's kind of Iceberg, and yes, it is quite popular. People like it. I think the reason people like it is they don't want to be locked in. And Databricks has been pushing very hard on this. They have their own variant of Iceberg, which is called Delta, but they've also bought the Iceberg company, so it's a Databricks thing at this point. And they have been pushing on this a lot for business reasons. But in principle, the idea that people want to own their data and make sense of it, and it not being locked down.

*And sometimes being able to query it from lots of different places without having to move all the data from vendor A to vendor B.*

And without having to pay – if you do a full table scan in Snowflake it will be expensive, right? If you read the same files from S3 it will be much cheaper, because in the end Snowflake is just a margin on top of Amazon cost, right?

*I have to declare, I have worked for Snowflake in the past, so I'm staying out.*

I like these guys. They have a very competent system, don't get me wrong. It's just that I think the pricing model of companies like Snowflake and Oracle has kind of created the lakehouse formats in the first place. That's just my theory there, because they were quite expensive.

*Yeah, their whole business model – we can certainly say the business model is value-add on top of the data, and then you can debate how much value and how much add.*

Yes, exactly. So that's that. But we looked at Iceberg.

*So you wanted to get into that world of Iceberg becoming the lingua franca of analytics data?* 

Again, we were kind of pushed into it by people. I think it was the most requested feature for two years straight. And we also worked together with a bunch of companies that ended up sponsoring a lot of the Iceberg work. And this is also how our company DuckLabs operates: if you care strongly about a feature and you're a company that has lots of money, then you can pay us and we will prioritize that feature. So that's how it happened with Iceberg.

So we worked on it, and again, I wrote the very first prototype of the Iceberg integration for DuckDB myself, which is how I learned a whole lot about Iceberg. 

*That's the way to do it.*

That's the way to do it.

*You know what, if DuckDB can read natively from an Excel file, then reading from Iceberg isn't really something you should exclude, right?*

That's true. Absolutely. Now we should be able to read from Iceberg, and I think we're getting close to being the most feature-complete open source implementation at this point.

*Really? That's quite a bold claim.*

I know. 2.0 will have it. I think a blog post is in the works. We have the most check marks in the big matrix of Iceberg features, because it has been so important, and we actually have a team at this point working on this in our offices. So we have really spent a lot of time – we've spent like three years on this at this point.

*Oh, wow. So you've done it as an extension rather than in the core DuckDB. Is it one of those things where you found limitations in the extension mechanism?*

I think the extension mechanism is fine for Iceberg. What we saw was that there were some other infrastructure items that were relevant to get good Iceberg performance that are not an extension-related thing but more a general thing. For example, for 2.0 we're also adding asynchronous IO, because these Iceberg files are typically stored on object storage like S3, and to get good performance from object storage you kind of have to have asynchronous IO, which basically means that you're not blocking your database engine on reading from the network, from HTTP, but you have a separate worker pool of threads that keep the pipes full of data for the other thing to process. So that's something that we added that has nothing really to do with the extension mechanism. It's more the general engine behaving differently because of this use case in Iceberg.

*Are you saying this remote thing is in the extension, or has that gone into the core?*

That is in the Parquet reader. The Iceberg extension uses the Parquet reader to read Parquet files, and the Parquet reader now has this async stuff. So it will just be faster, and that benefits everybody that reads Parquet, including the Iceberg extension.

One thing that we had to figure out for Iceberg is how extensions have dependencies with each other, which is an absolute nightmare, because Iceberg obviously uses the Parquet extension. We're not going to duplicate the Parquet reader for Iceberg.

Fun fact, by the way: Spark, in its infinite wisdom, ships two Parquet readers – one to read Parquet, and one to read Parquet files as part of Iceberg.

*Why?*

No idea.

*Is that Conway's law, two teams not talking to each other within Spark?*

My prediction is that the people that built Iceberg, the Tabular people that got acquired by Databricks, needed to move and the Spark people weren't moving, and so they just said, fine, we'll just ship our own completely independent from-scratch reader for Parquet. Which now has the funny consequence that if you read a Parquet file from Spark you can get different results depending on whether you read it as a straight Parquet file or you read it from Iceberg.

*It's 2026 and computers are still.*

Oh, right. But we didn't do that. So we added dependencies between extensions. The Iceberg extension uses the Parquet extension. We also have an extension that reads Avro files, because obviously Iceberg uses Avro files for the metadata. It also uses JSON, because it wasn't enough to have Avro files as a metadata format, it also added JSON as a metadata format. So then the Iceberg extension also depends on the JSON reader, and we had to figure out how to do extension dependencies, let's say, to get this Iceberg stuff to work well. But it works, it's fine.

### The Avro File Format

<!-- [01:03:35] -->

*Okay, then I'm going to pick you up on your Avro thing, because you said the problem with Postgres and lots of database protocols is that they're putting the type in every row, right? And this is one of the things that Avro completely fixes – it puts all the metadata first, then just streams out compact binary data. I would have thought you'd love Avro.*

No, I don't, regrettably not. I also built an Avro reader from scratch, by the way, to understand Avro. And I've also built a Thrift reader from scratch to understand Thrift.

*How do you still look so young? You should look old and haggard by this.*

I shaved today.

Nah, I love serialization. One of the joys in my life is to figure out how to take multi-dimensional data structures and put them onto a one-dimensional storage medium and back. It's great. Somehow I love that. And I guess that's why I spend so much time on this stuff. But Avro was built for Hadoop, right? It comes from that world. It was originally built as an RPC format, and later on somebody invented a file format around it. And indeed, you have the metadata that contains a schema – as JSON, for some reason. One of the things that bothers me is if somebody invents a file format that then depends on another file format to describe something that could have been done in the file format. But okay, so they use JSON to describe the schema. Fine.

But the problem with Avro is that every value still has a type prefix, because there are things like unions and structs and they have to say which field is actually there and which is not. So there's still a byte that will tell you which field is actually there or not. That's fine. My structural problem with Avro is that you cannot read it without the schema, whereas a Thrift file you can read without the schema. They were such bit pinchers that they removed the structural information that would be required to decode it without knowing the schema. The Thrift guys have that, and protobuf. And so that means that an Avro file is completely useless without the schema, and you cannot build a generic Avro reader, which would be really nice.

So that is my gripe with Avro. There are other problems: they chunk a bunch of rows together in one compression block in the file, which means that to read a single row you have to decompress that whole block, which kind of defeats the purpose of a row-based format – at which point you might as well use Parquet. The idea is right, but in the execution, let's say, there were some problems. But yeah, it is what Iceberg uses, which is why we have a reader for it.

### The Duck Stack: DuckDB, Quack, DuckLake

<!-- [01:06:40] -->

*This almost makes me wonder if you've come up with the “duck” format for solving these. You clearly have strong opinions on the way that data should be serialized. Why is there not “.duck”?*

We do have a DuckDB storage format – DuckDB has its own storage format.

*But do you have a wire protocol format?*

Yes – well, Quack. Yeah, sure. Quack has that. And it uses our internal serialization, for sure.

But with Iceberg, we looked at it and we saw some issues. I think the biggest problem with Iceberg that I see is that they tried so hard to not have a database, right? So all this change tracking metadata is in these Avro files and the JSON file, and they tried so hard to not have a database because databases don't scale – their words, not mine. And then they slapped this Iceberg REST catalog on top of it, which has a Postgres in it.

*Yeah.*

Which was the point where we said, this thing exists now in your diagram of components – why don't you just forget about this whole metadata tracking file nonsense and just use the database for it? And that is exactly what DuckLake is. Yeah, you have the database already, you just added it to your Visio diagram.

*Yeah, by adding a proper database now you should pull all that metadata and actually use a proper database.*

And that's the funny thing: so we did this with DuckLake. The quote was, "We have a database and we're not afraid of using it." It's by the way a Shrek quote in my mind: "I have a dragon and I'm not afraid to use it." It's a great film.

So that's the idea of DuckLake. And the funny thing is that it seems to be the case that the Iceberg world has grudgingly accepted that this is a good idea. And I see movement from them to go more into that area with the Iceberg REST catalog query planning API, that's also trying to pull a lot of this metadata out of these Avro files into the centralized thing, to be able to do query planning without having to read 1,700 Avro files, right?

*Presumably you get exactly the same optimizer benefits, because you're doing a similar kind of planning for where to look for the data, right?*

So DuckLake's query planning is a single query in the metadata catalog, and that's really elegant.

*So is DuckLake an implementation of Iceberg, a replacement for Iceberg, a proof of concept?*

It's a replacement. It's not a proof of concept – we released 1.0 of DuckLake recently. The DuckLake extension is actually downloaded as much as the Iceberg extension for DuckDB. So this is actually used out there. We know it's used out there. We have customers working with DuckLake. So it's very cool to see that.

We use the same Parquet files underneath. So you can actually take an Iceberg table and, fairly cheaply, with a metadata-only operation, import it into DuckLake and vice versa. So we use the same format for data files. Okay, they're just Parquet, with some little asterisks on them. And then we also use a compatible format for the deletions. The way Iceberg stores deletes is with additional files that tell you which rows are deleted from the data file, so we are compatible there. Because we figured, we don't have to break compatibility where we don't need to. We're pragmatic people. We don't break things just because we want to break things. We usually do things because we think they're better that way. And DuckLake is definitely one of these things where we looked at this Iceberg spec and we thought, this cannot be the state of data engineering in the year of our lord 2024, or whatever it was.

### The Future of Iceberg and DuckLake

<!-- [01:10:48] -->

*Right. What do you think's going to happen then? Because you get the sense that they're already starting to pull metadata into the database. Do you think you're just ahead in the race to a similar position, with metadata as a database?*

It's very fascinating. If they end up doing what we proposed, I consider this a massive win. I could also see that DuckLake gets way more adoption, right? That's also possible. It depends a bit – if a large player would say, "Hey, we're betting on DuckLake," that would also be very good. There are multiple ways for this to have impact. It's already having impact. We already crossed the first bar, of it being ignored by the world – that hasn't happened. It is absolutely part of that world. And now the question is just, what is the endgame from here? Is it going to go into obscurity? Are the other guys adopting it? Any of those paths I consider a win, right? If our tiny team of database-crazy people from Amsterdam can make that kind of thing happen, shove Silicon Valley around, then I consider that a massive win.

*Yeah, we've got to influence those people across in California sometimes.*

Right? Sometimes.

### From Local Tool to Enterprise Adoption

<!-- [01:12:14] -->

*Please. Absolutely. Okay, so that kind of puts you in a new space, doesn't it? Again, I think of DuckDB as this small thing in my command line toolkit, but now you're getting out into the enterprise world.*

That's true. Absolutely. I think the lakehouse stuff definitely is something where we see people storing their stuff in Iceberg. We see people using DuckDB to interact with Iceberg stuff a lot – that's something we see a lot. It's one of our most downloaded extensions, as I said. We also see services out there like S3 Tables, which is managed Iceberg from AWS, that we interact with a lot from DuckDB. So there's a lot of this happening.

And yes, you're absolutely right, and this is also something we've seen: the kind of people that use DuckDB has shifted over the last two years, from "here's Kris typing on his laptop".

*If you're listening to this on Spotify, you've just mimed typing with two fingers and I'm personally offended.*

I am not. I'm so sorry, I didn't mean that. This was more like "I'm hacking." And I have a duck on my keyboard, for those on Spotify who cannot see this. Here it is.

*Ah, nice duck.*

Anyways, what we've seen is that it went from somebody running DuckDB on their laptop – they still exist and we're very grateful – to also enterprise adoption, where people are betting huge data pipelines on DuckDB. I can't talk about all of them, obviously, but there are some that have publicly spoken about this. Recently at DuckCon we had a talk from Spotify that described how they have this whole AI agent infrastructure for you to ask questions about your music history, and that just runs DuckDB under the hood, with an agent on top that basically turns the user's questions into SQL queries on that database that they instantiate for every user once you start asking questions. So that's just running DuckDB, right?

*So a separate database just for the user each time?*

Yeah, there's a talk at DuckCon, and as far as I remember, that's what they do: they instantiate the DuckDB instance once the user starts asking questions about the data, they shove all the listening history into that instance, and then the agent goes to town on it, essentially.

*Which you can only do reasonably with a database that's backed by a single file. So you pick SQLite or DuckDB, right?*

Right but it's analytics, so you probably want to use DuckDB, because SQLite isn't. Yeah. So that was something that was presented at DuckCon a couple of weeks ago in Amsterdam. We also saw somebody talking about how they changed their big pharma data analysis workflows from Spark to DuckDB and saved hundreds of millions – I don't remember the number. But you see a lot more enterprise adoption. I wouldn't have expected that somebody like Spotify or big pharma would suddenly bet on DuckDB, and I think that has been the story for the last maybe two years: just this massive adoption. And it's also something that pushed our download numbers – right now for DuckDB we're beyond a million a day, which is totally wild. That's crazy.

### Recent Changes around the Company

<!-- [01:15:55] -->

*How has that changed life for you, for the company? Because you are a kind of rebel academic building an open source database, and now suddenly you're thrust into the enterprise world. Are you going to be going all corporate and ringing the bell at NASDAQ and all this stuff?*

That's a great question. I think I haven't been a rebellious academic, maybe in my mind, but de facto. Our company has like 30-plus people right now. It's not huge, of course, but it's a fairly big operation to run on a daily basis, also revenue-wise. The amount of money you have to shovel into that fire every month is considerable.

*Yeah, 30 staff is eye-watering numbers.*

For a small self-funded company from Amsterdam, it is quite a lot. I love everybody, they are great people. There are not many teams out there that can do data engines on this level. That's also something I had to learn. I was like, doesn't every company have people like that? It turns out to be not the case.

So it's definitely been a bit of a change. Dealing with corporate purchasing departments is also really not fun.

*Oh – getting them to sign off on invoices and stuff like that.*

Yeah, or pay their invoices. It's a basic thing, you would imagine, right? But I think that's all fine, and we're really grateful to our team here that is working on that. But I've noticed that interacting with these massive enterprise customers is certainly something that a team of hackers maybe struggles with a little bit.

*Yeah, that's often the case when you're a coder who just wants to build something that people find useful. Firstly, the first hurdle you normally fall at is getting people to use it, because most of us hardcore programmers aren't marketers, right? But if you get over that hurdle, you've got the reality that you gradually get pushed out of writing version two of a PEG parser and into worrying about corporate relations.*

Yep, that's actually true. It's funny though, the marketing aspect: we had a blog post yesterday about DuckDB 2.0 coming out in fall and it was on the top of Hacker News for the entire afternoon, which still feels to me like we've got the marketing down.

But absolutely, and I think going forward it's also interesting what kind of company we want to become. It's always been clear that we want to continue doing this, we want to keep pushing database engines. But it has also become clear that we would probably have to become a different company if we wanted to really push DuckDB to the next two, three orders of magnitude of adoption, right? We would have to have, I don't know, sales, marketing, corporate stuff, account managers, these kinds of things. That's definitely something that we have been thinking about for the last maybe one year: hey, how are we actually going to scale up this operation, just to continue our mission of making data better for everyone?

*Yeah, you can't just build databases. You end up having to build the soft systems that a business is made of.*

Right. And I think we have been doing extremely well in many ways. We have never had a month where we haven't been profitable in the last five years, which is something I'm very happy about.

*Not many companies can say that, even the huge ones.*

Exactly. But it's also clear that we have to do something different.

### Joining Amazong Web Services

<!-- [01:20:03] -->

*So what are you going to do? Are you going to spin up your sales team and become that kind of guy?*

No. And it's hard for me to talk about, in a way, because it's been such a process. But by the time you hear this, we are joining Amazon, actually, as a company, as a new subsidiary. So DuckLabs, the company, will become part of Amazon Web Services, which is part of Amazon, one of the biggest companies in the world. Yeah, I've heard of them. They're big. They come to your door on a regular basis. No threat.

*Soon their drones will be dropping ducks out of the sky.*

But it's very fascinating as a direction, right? I would have never thought we would ever get to this point, that we would be acquired, which is something that I heard other people talking about and we were like, but we just – so it is actually something that we thought about a lot, as you can imagine. You can only do this once. I'm probably not going to start another company. I was a reluctant founder in the first place.

*Tell me about that from your point of view, because you must have been thinking, well, we could start up the whole sales and marketing engine and try and go down that route, the path to NASDAQ. Did you get courted by Amazon and you're thinking, well, maybe this is a road to go down that's less business work for me?*

It's actually fascinating. Yeah, less of the things I'm not excited about. Let's just say: I want to work on technology. I want to push technology. And I think that's also the case for Mark and everybody in our team. We want to push technology. I'm not that interested, let's say, in building a sales team – let me just be absolutely frank. And I think I could have found somebody to do this, yes, but it would become a different company. I'm really sure about that.

And Amazon – we've actually been working with Amazon for two years already. They have been one of our biggest customers, actually. For example, working on Iceberg stuff, they're one of the people that have been funding work on Iceberg in DuckDB for the last years. So when they basically showed up one day and said, “hey, can we maybe talk about this?”, it wasn't a bolt from the blue. It was like, hey, we actually know these people, we have a working relationship with them, and we like them, and they have a really good vision about where things should go.

But it was still a bit of an interesting discussion, because they have thousands and thousands of employees over there. What will we do with our 30-sort-of-person team? But I was really happy about the vision that they presented to us. And part of that vision is that DuckDB and DuckLake and Quack and all that stuff is currently not part of the company. Many people don't know this, but DuckDB is actually organized, or governed, if that's a good word, by the DuckDB Foundation, which is a nonprofit foundation here in Amsterdam that is a lot like, let's say, the Apache Software Foundation, right?

*Right.*

So all the projects are under that foundation, and we are not selling that. We are selling the company DuckLabs, formerly called DuckDB Labs, which is the commercial side of things where we did all these projects with commercial partners. The foundation is untouched. We leave that alone. That stays where it's at. We're selling the company. So it's very similar to what happened with Iceberg, for example, where Tabular, the company, got sold to Databricks, but the Iceberg project was and is an Apache project, which wasn't at all part of that acquisition. This is the model that we're looking at.

And it's also not only that we're going to let the project sit in that foundation and never touch it again. I'm really excited that the AWS guys are also really committed to us keeping pushing DuckDB and DuckLake and all that stuff in the foundation for years to come. In fact, we're going to have more people working on that stuff than before. So that's really fascinating.

*Is this a thing where you're going to have to think about making sure you open up the foundation to non-DuckDB and therefore non-Amazon members?*

Well, Amazon isn't part of the foundation. There are donors to the foundation, and we highly appreciate that. But opening up the foundation to get input from all DuckDB users, more than maybe we have been doing in the past, is definitely part of this. We care about the ecosystem we've built, of course, and we want to make sure everybody that uses DuckDB continues to thrive. And I think that's really unique. I think that AWS is really on board with that.

*Are you not worried? I would be worried that what they say today will change three years from now as their management structure turns over, and suddenly you find yourself in a different set of promises.*

I think that's an excellent point. We have spent a lot of time thinking about this, in the various legal documents that have been flying around. But we do have a long-term commitment all the way up. They are structured so that this is what they're planning to do for the time going forward, independent of individual people being in individual positions. So we have their commitment that they will let us continue to do that, that they want us to continue being effective and pushing things in DuckDB. I'm confident that we have the commitments that we need to keep doing that without it being dependent on, let's say, one person changing jobs.

That's definitely a case we have been thinking about.

*A situation where your one champion at AWS retires or...?*

Exactly. That is something we have actually spent quite a lot of time thinking about, talking about with them. We have gotten commitments from them that make us confident that this is really their long-term strategy. And that's really exciting. I think that's pretty unique. And again, the DuckDB Foundation doesn't change, right? We might even end up opening up more to more people having input on the foundation roadmap, for example. But the projects are not moving, the license doesn't change. If anything, we plan to increase the speed with which we're doing things in DuckDB, the amount of people being able to contribute to core. So that's exciting.

*Yeah. This deal must come with certain material benefits for you and Mark, right? But it must also come with a lot more resources for the company, I assume.*

Yeah, absolutely. I mean, they're paying to acquire a company. We're not going to tell people how much it is, because it's not important.

*I hope you've been suitably rewarded. Jeff Bezos can afford to put a few pints in your back pocket.*

I think my beer budget is safe, let's just say, for the foreseeable future. It's all that matters in the end.

But the resources – there are some things I'm excited about. Resources in terms of people, of course. We had to be quite conservative in adding people to the team, just because we are a self-funded company and whenever we signed a work contract with somebody we needed to make sure that we're able to pay that long term. So we have been quite conservative in hiring, and we actually don't have to do that anymore to the same degree. We also get a lot of infrastructure, right? There are a lot of computers we can use.

*You've done it all for the free AWS credits.*

Absolutely.

But I think what's also super interesting, and something we've always been locked out of, is the ability to see real-world workloads. And that's really a problem – maybe I should talk about this a little bit. So, you worked at Snowflake. Snowflake sees every single query that people run, right? They might pretend they don't, but they do.

*I'm not sure how much I can say legally, but that is a valuable source of intel. Any reasonable person would assume that.*

Let's just say. And I don't have any insight there.

*I don't think they look at the data – they can look at the access patterns, right?*

And the kind of queries people run.

So DuckDB – because we're European and we respect people's privacy – we don't have any telemetry in DuckDB. We don't send out the queries that you run to our central command. We don't have telemetry, we don't know what on earth you're doing with DuckDB. And that's actually been a limiting factor for us, because one of the huge advantages of the Snowflakes and the Databricks and the Amazons of this world is that they see the workloads, and they can steer development and optimization towards where it really matters.

*Yeah, real-world edge cases.*

We have always been locked out of that, because sometimes people open bug reports and say, hey, this query doesn't work, and then we fix it, but we have no idea if that's just some dude in their garage in Uzbekistan or the biggest company in the world that has this problem, because for us it's just a GitHub account with a bug report, right?

So we've always been locked out of this optimization path of real-world workloads. And that's one thing that I think will be extremely valuable for the project, for DuckDB, to be able to say, okay, we see a lot of queries that, I don't know, group on 15 string columns at the same time. Not sure, maybe that is a thing, who knows. But we can then say, all right, now we're going to actually optimize everything about these things, because we see them being such a relevant part of real-world workloads. And I think that's one part where it's really going to come together in terms of us being part of Amazon really improving DuckDB itself. I think that's going to be very exciting.

*Yeah, there's an old thing about open source being good because all bugs are shallow when you have 10,000 eyes on it, but that's only true if you have the full feedback loop available, right?* 

Right, and we don't have the feedback loop. We also have this well-known issue that one in 10 people that experience a problem will report a bug, at best, right? So there's just this undercurrent of stuff that maybe doesn't go so well, we don't know, but we never hear about it. We are fairly happy with our issue tracker load at the moment, given the insane amount of users, but we are really interested in closing that feedback loop.

There's also exciting stuff that Amazon is planning with DuckDB that I can't yet talk about, but down the road there will be announcements, of course. And that's also something that I'm looking forward to: what can be done as part of such a huge organization. And again, I'm really amazed – and it's also a big part of why we were considering this in the first place – because they said, we want you guys to be this entity that just contains database query processing expertise as an independent entity. We're going to remain DuckLabs, it's just going to be “an Amazon company”, or something like that. So that's the part where we're not going to be absorbed into 15 different product teams. We're going to stay together as a team to push query processing – you know, something I care about.

*And I suppose you can't 100% guarantee that will happen, but if you went down the "I'll start a sales pipeline and grow that way" path, you couldn't 100% guarantee that would work either.*

Fun story: I talked to some founders of some big database companies that I cannot mention, that are running SQL-as-a-service kind of stuff. Very early on, because we were thinking about whether we should have a service, a SaaS for DuckDB, and they told me, look, a couple of years down the line the sales people will run engineering, because they will dictate what you have to build for them to close more deals, because that's what the whole company and their share and the stock price is predicated on. And I heard that and I thought, that's interesting, and it's not necessarily a world I want to be in.

*Yeah. It's not an expansion that comes for free. It comes with a set of shifting priorities.*

Right. And I think AWS is kind of big enough for that to be maybe a little bit more disconnected, where we can really push on technological excellence and know that that will spill over – much like they already do in other areas, like with the CPUs, which is something I find quite impressive, where they're building their own CPUs for the data centers, the Graviton thing, and they push everybody. This is something that people benefit from: it's more efficient, it's nice to the planet. So I think it's really going to be fascinating. Obviously I don't know a lot yet – by the time we're recording this, we're in the final stages of negotiations. But it's going to happen.

*Okay, one more question about that before we get to another technical thing I want to talk about. I just want to know, because you don't often hear this story: how does that affect you? You are the co-founder of a successful company that's been profitable every month for five years. You're a big fish in your own pond. And I can see the pros and cons, but how does it feel for you?*

Oh, it's super fascinating, because one idea I really had to come to terms with is having a boss again.

*Yeah, I know that feeling, and it doesn't go easy.*

Thankfully, the person who is going to be in charge – I have been able to work with him for the last couple of years, as I mentioned, so I think I have a pretty good idea what he's like. So that's reassuring. But it's definitely going to be an adaptation for me. Obviously, in our company the only restrictions we had were what you cannot legally do, right? Especially in Holland you can do a lot of things. The Dutch are historically business-friendly in that sense, so there are not a lot of restrictions on companies. We had to follow the laws, but that was it. It's not that we did anything crazy, but it was very nice – can we buy this ridiculous thing for our team's entertainment? Absolutely. Nobody can tell me that that's not okay. So that's maybe a change. Another thing I've noticed is they're going to have to do performance reviews. It's been a while since somebody did a performance review on me.

*Oh yeah. You may find, as some people in your position have found, that at some point in the past five years you've become unemployable.*

Yeah, it's possible. But I'm okay, I have made my peace with that idea. Maybe I don't have to look at the performance review – how about that? Yeah, it gets written but I never see it. That's kind of my thinking right now.

*Ignore the performance review, ignore the sales department, and just carry on writing serialization formats.*

Pretty much. No, I think I'm going to be fine, don't worry about that. But it is definitely going to be different in terms of the parameters. Obviously, it's a big company, they have rules, and I understand that. We'll see how that goes.

*Yeah, I suppose there's also the advantage that they're a big company: they won't be paying that much attention to you in the global scheme of things.*

That's also true.

*We'll get you back in 18 months and see how it's actually gone in reality.*

Happy to.

### DuckDB v2.0

<!-- [01:38:30] -->

*So there's one more technical question I wanted to ask, because in a way it's surprising you haven't got it already. I saw it coming in the pipeline: triggers. Is that a coming DuckDB feature?*

Triggers are coming in 2.0, yep. We have this blog post out yesterday that has a preview for 2.0, and we made it a listicle, you know, “10 things coming to DuckDB 2.0. Number eight will shock you.” Kind of harking back to that.

*The question then is not why triggers, but why now?*

Because we have the year of the server in DuckDB. We had the year of the lakehouse last year, and now we have the year of the server, and triggers are one of these things that you kind of need when you're running a server, because you want things to happen based on your data changing. I think that's why we're doing it now.

And there are also other things in the pipeline that are still coming past 2.0. We're going to do a PL/SQL kind of thing where you can write actual programs, stored procedures, in DuckDB, and it's going to be fast this time around. We have Denis here, who is awesome, who did his PhD on compiling PL/SQL to recursive subqueries, and he now works for us, and we're going to implement that in DuckDB in the future. So we can have stored procedures written in pure SQL, but fast. So that's going to be exciting.

*Written in pure SQL – so it's not like a programming language wrapped around SQL? There's no PL/duck coming?*

PL/SQL is like, you have if-else, loop kind of constructs as part of SQL.

*Right. So it's to that kind of old spec, rather than just SQL, or you inventing your own language?*

We're probably going to make it nicer, because it's quite clunky, you're right. We have some ideas on how to make the syntax better. But the idea is that this is a SQL-level thing that allows you to express arbitrary computation in a SQL-y sort of way, and that gets evaluated by DuckDB in an efficient way. Okay.

*And because you compiled DuckDB to Wasm, is that also going to be available in the browser?*

Yeah, for sure. This is all coming to the browser, for sure.

*I could ask you a million more questions.*

We can do a follow-up. Yeah, there are lots of exciting things coming, for sure. We are hard at work getting 2.0 out of the door. That's always a bit of a crunch, but the team is working hard on that. I'm very grateful.

*I shall leave you to that. At the end of the year of the server, when we've found out how the AWS acquisition has actually played out, you must come back and tell us. I will be happy to. Excellent, Hannes. Thank you very much.*

Thank you so much, Kris. Absolute pleasure talking to you.

*Always. Cheers.*  
