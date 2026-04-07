include Jekyll

# this file is used to run the external python scripts to generate search indexes
# we only want to run these scripts once, so we use the `:after_init` hook

Jekyll::Hooks.register :site, :after_init do |page|
  tag = 'Search index:'
  Jekyll.logger.info(tag, "Generating search index")

  # gracefully fail if the python script errors
  if system "python3 scripts/generate_search.py"
    Jekyll.logger.info(tag, "Search index generated")
  else
    Jekyll.logger.error(tag, "Failed to generate index")
  end

  Jekyll.logger.info(tag, "Building pre-generated MiniSearch index")

  if system "node scripts/build_search_index.js"
    Jekyll.logger.info(tag, "MiniSearch index built")
  else
    Jekyll.logger.error(tag, "Failed to build MiniSearch index")
  end

  Jekyll.logger.info(tag, "Generating DuckDB search index")

  if system "python3 scripts/generate_search_index.py --validate"
    Jekyll.logger.info(tag, "DuckDB search index generated")
  else
    Jekyll.logger.error(tag, "Failed to generate DuckDB search index")
  end

end

