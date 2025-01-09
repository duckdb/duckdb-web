require 'jekyll-seo-tag'

# most of this code is copied from jekyll-seo-tag
Jekyll::SeoTag::Drop.class_eval do
  def description
    @description ||= begin
      description_max_words = 100
      value = format_string(page["description"] || page["excerpt"] || page["content"]) || site_description
      snippet(value, description_max_words)
    end
  end

  def snippet(string, max_words)
    return string if string.nil?

    result = string.split(%r!\s+!, max_words + 1)[0...max_words].join(" ")
    result.length < string.length ? result.concat("…") : result
  end
end

