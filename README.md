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