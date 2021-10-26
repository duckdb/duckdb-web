# duckdb-web

## Notes
Notes are highlighted as light blue boxes. To create a note use the `>` (Quote) in Markdown.
The Headline will be added automatically.

## Adding Pages

### 1. Layout
The `layout` of documentation pages is `docu`, the layout of the landing page is `default`. 

### 2. Menu-Items
Please define the `selected:` & `expanded:` value in the beginning of the Markdown file. (Only important on overview pages)

### 3. Menu
There are two menus on the website, both have a json file from which they are generated. `menu.json` (located in the `_data` folder) is the main menu on the documentation page, `secondarymenu.json` is the small hover. To add or remove or change the menu you need to make the appropriate changes in these json files. 

## News

To add a blog post, all you need is to add a new .md-file to folder `_posts`. 
The file name pattern should be like this: `2020-07-20-my-blog-post.md`. 

**Front matter** of a single post: 

	---
	layout: post  
	title:  "Your Post Title"  
	author: Max Mustermann  
	excerpt_separator: <!--more-->
	---
	
Include the excerpt_separator `<!--more-->` when you wish to end the post preview.

## Building
The site is built using [Jekyll](https://jekyllrb.com/). To build the site locally, install the minima theme `bundle` and
run `bundle exec jekyll serve --livereload`.
