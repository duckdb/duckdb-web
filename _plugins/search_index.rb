include Jekyll

# this file is used to run the external python script to generate the search index
# we only want to run this script once, so we use the `:after_init` hook to run the script

Jekyll::Hooks.register :site, :after_init do |page|
  tag = 'Search index:'
  Jekyll.logger.info(tag, "Generating search index")

  # gracefully fail if the python script errors
  if system "python3 scripts/generate_search.py"
    Jekyll.logger.info(tag, "Search index generated")
  else
    Jekyll.logger.error(tag, "Failed to generate index")
  end

end

