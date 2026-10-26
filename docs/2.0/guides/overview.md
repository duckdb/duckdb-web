---
layout: docu
permalink: /docs/2.0/guides/
isotope: true
redirect_from:
- /docs/guides
- /docs/guides/index
- /docs/guides/overview
- /docs/2.0/guides/overview
- /docs/stable/guides/overview
- /guides
- /docs/current/guides/overview
- /docs/lts/guides/overview
- /docs/preview/guides/overview
title: How-to Guides
---

Each how-to guide is a short, task-oriented walkthrough. Use the filters or the search box to find a guide by topic.

{% include docs_filterbar.html types="how_to" %}

<div class="post-list wrap">
	<div class="newstiles">
		{% assign how_to_pages = site.pages | where_exp: "p", "p.how_to_topic" | sort: "title" %}
		{% for guide in how_to_pages %}
			{% assign topic = guide.how_to_topic %}
			<div class="postpreview {{ topic }}" data-title="{{ guide.title | escape }}" data-search="{{ guide.title | append: ' ' | append: topic | strip | downcase | escape }}">
				<a href="{{ guide.url }}" title="{{ guide.title | escape }}" class="blocklink"></a>
				<div class="postdetails">
					<h3>{{ guide.title }}</h3>
					<div class="meta">
						<div class="tag">{{ site.data.post_types.tag_labels[topic] | default: topic }}</div>
					</div>
				</div>
			</div>
		{% endfor %}
	</div>
</div>
