require 'jekyll-seo-tag'

# most of this code is copied from jekyll-seo-tag
Jekyll::SeoTag::Drop.class_eval do
  def description
    @description ||= begin
      description_max_words = 100
      # skip empty values, e.g., library entries set 'excerpt: ""'
      value = [page["description"], page["excerpt"]].map { |s| format_string(s.to_s) }.compact.first ||
        format_string(strip_tables_and_headers(page["content"].to_s)) ||
        site_description
      snippet(value, description_max_words)
    end
  end

  # tables (e.g., the metadata tables of library entries) and headers (e.g., "Abstract")
  # do not make for a readable description
  def strip_tables_and_headers(string)
    string
      .gsub(%r!<table\b.*?</table>!m, " ")
      .gsub(%r!<h[1-6]\b.*?</h[1-6]>!m, " ")
      # paragraphs consisting of bold text only, used as headers (e.g., "**Part 1**")
      .gsub(%r!<p>\s*<strong>[^<]*</strong>\s*</p>!, " ")
  end

  def snippet(string, max_words)
    return string if string.nil?

    result = string.split(%r!\s+!, max_words + 1)[0...max_words].join(" ")
    result.length < string.length ? result.concat("…") : result
  end
end
