# This file runs the external scripts that generate the search indexes in data/.
# We only want to run these scripts once, so we start them in the `:after_init` hook.
# They run in the background while Jekyll reads and renders the site,
# and we wait for them before the site is written.

module SearchIndex
  TAG = 'Search index:'
  OUTPUT_DIR = 'data'
  OUTPUT_FILES = ['search_data.json', 'search_index.json', 'docs-search.duckdb'].freeze

  # Jekyll ignores dotfiles, so it does not pick up the database (or its WAL) while it is being built
  DUCKDB_TMP_PATH = "#{OUTPUT_DIR}/.docs-search.duckdb.tmp"
  DUCKDB_PATH = "#{OUTPUT_DIR}/docs-search.duckdb"

  # each chain runs in its own thread; the steps of a chain run one after the other
  CHAINS = [
    [
      ['python3 scripts/generate_search.py', 'Search index generated', 'Failed to generate index'],
      # reads the output of generate_search.py
      ['node scripts/build_search_index.js', 'MiniSearch index built', 'Failed to build MiniSearch index'],
    ],
    [
      ["python3 scripts/generate_search_index.py --validate --output #{DUCKDB_TMP_PATH}", 'DuckDB search index generated', 'Failed to generate DuckDB search index',
       -> { File.rename(DUCKDB_TMP_PATH, DUCKDB_PATH) }],
    ],
  ].freeze

  @threads = nil

  def self.start
    Jekyll.logger.info(TAG, 'Generating search indexes in the background')
    @threads = CHAINS.map do |chain|
      Thread.new do
        chain.each do |command, success, failure, on_success|
          # gracefully fail if a script errors
          if system(command)
            on_success&.call
            Jekyll.logger.info(TAG, success)
          else
            Jekyll.logger.error(TAG, failure)
            break
          end
        end
      end
    end
  end

  def self.wait(site)
    return unless @threads

    @threads.each(&:join)
    @threads = nil
    # on a fresh checkout, the files did not exist yet when Jekyll read the site
    known = site.static_files.map(&:relative_path).to_set
    OUTPUT_FILES.each do |name|
      relative_path = "#{OUTPUT_DIR}/#{name}"
      next if known.include?(relative_path) || !File.exist?(site.in_source_dir(OUTPUT_DIR, name))

      site.static_files << Jekyll::StaticFile.new(site, site.source, OUTPUT_DIR, name)
    end
  end
end

Jekyll::Hooks.register :site, :after_init do |_site|
  SearchIndex.start
end

Jekyll::Hooks.register :site, :post_render do |site|
  SearchIndex.wait(site)
end
