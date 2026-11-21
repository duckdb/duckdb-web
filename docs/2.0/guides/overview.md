---
layout: docu
breadcrumbs: false
permalink: /docs/2.0/guides/
isotope: true
body_class: guides-index
toc: false
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
- /docs/2.0/guides/file_formats/overview
- /docs/guides/file_formats/overview
- /docs/stable/guides/file_formats/overview
- /docs/current/guides/file_formats/overview
- /docs/lts/guides/file_formats/overview
- /docs/preview/guides/file_formats/overview
- /docs/2.0/guides/network_cloud_storage/overview
- /docs/guides/network_cloud_storage/overview
- /docs/stable/guides/network_cloud_storage/overview
- /docs/current/guides/network_cloud_storage/overview
- /docs/lts/guides/network_cloud_storage/overview
- /docs/preview/guides/network_cloud_storage/overview
- /docs/2.0/guides/database_integration/overview
- /docs/guides/database_integration/overview
- /docs/stable/guides/database_integration/overview
- /docs/current/guides/database_integration/overview
- /docs/lts/guides/database_integration/overview
- /docs/preview/guides/database_integration/overview
title: How-to Guides
---

Each how-to guide is a short, task-oriented walkthrough. Use the filters or the search box to find a guide by topic.

{% include docs_filterbar.html types="how_to" %}

<div class="post-list guides-list">
	<div class="newstiles">
		{% assign how_to_pages = site.pages | where_exp: "p", "p.how_to_topic" | sort: "title" %}
		{% for guide in how_to_pages %}
			{% assign topic = guide.how_to_topic %}
			<a href="{{ guide.url }}" class="postpreview guide-card {{ topic }}" data-title="{{ guide.title | escape }}" data-search="{{ guide.title | append: ' ' | append: topic | strip | downcase | escape }}">
				<span class="guide-card-topic">{{ site.data.post_types.tag_labels[topic] | default: topic }}</span>
				<span class="guide-card-title">{{ guide.title }}</span>
			</a>
		{% endfor %}
	</div>
</div>
