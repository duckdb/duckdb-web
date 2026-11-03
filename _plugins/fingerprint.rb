# frozen_string_literal: true

require "digest"

# Cache busting for CSS and JavaScript files. The `fingerprint` filter appends a
# digest of the file's contents to its URL:
#
#   {{ '/css/main.css' | fingerprint }}  =>  /css/main.css?3f2a9c1b0d
#
# Unlike a build timestamp, the digest only changes when the file does, so
# browsers keep their cached copy across deploys that do not touch it, and
# repeated builds produce identical output.
#
# The digest is computed from the source files: for Sass, these are the entry
# file and every file in the Sass directory (_sass), as the compiled CSS is only
# available once the page is rendered.
#
# The filter raises an error if the site has no file with the given URL.

module Fingerprint
  DIGEST_LENGTH = 10
  SASS_EXTENSIONS = %w[.sass .scss].freeze

  @digests = {}

  class << self
    def digest(site, url)
      @digests[url] ||= compute(site, url)
    end

    def reset
      @digests.clear
    end

    private

    def compute(site, url)
      files = source_files(site, url)
      raise ArgumentError, "fingerprint: the site has no file with the URL '#{url}'" if files.empty?

      sha = Digest::SHA256.new
      files.each do |file|
        # include the path so that renaming or moving a Sass partial changes the digest
        sha << file.delete_prefix(site.source) << "\0"
        sha.file(file)
      end
      sha.hexdigest[0, DIGEST_LENGTH]
    end

    def source_files(site, url)
      static_file = site.static_files.find { |f| f.url == url }
      return [static_file.path] if static_file

      page = site.pages.find { |p| p.url == url }
      return [] unless page

      entry = site.in_source_dir(page.relative_path)
      return [entry] unless SASS_EXTENSIONS.include?(page.ext)

      sass_dir = site.in_source_dir(site.config.dig("sass", "sass_dir") || "_sass")
      [entry, *Dir.glob(File.join(sass_dir, "**", "*")).select { |f| File.file?(f) }.sort]
    end
  end

  module Filter
    def fingerprint(url)
      "#{url}?#{Fingerprint.digest(@context.registers[:site], url)}"
    end
  end
end

# with `jekyll serve`, recompute the digests on every regeneration
Jekyll::Hooks.register(:site, :after_reset) { Fingerprint.reset }
Liquid::Template.register_filter(Fingerprint::Filter)
