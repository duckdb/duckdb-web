# frozen_string_literal: true

require "cgi"
require "nokogiri"

# Moves the attribution line of a `Quote` box into a figure caption:
#
#   > Quote
#   > “…”
#   >
#   > — Ilya Boyandin, creator of [SQLRooms](https://sqlrooms.org)
#
# renders as
#
#   <figure class="quote">
#     <blockquote>…</blockquote>
#     <figcaption class="quote-author"><img class="avatar" …>Ilya Boyandin, creator of …</figcaption>
#   </figure>
#
# The attribution is the last paragraph if it starts with an en dash, em dash, `--` or `-`.
# The dash is dropped. If the attribution starts with a name from _data/authors.yml that has a
# `picture`, the photo is added in front. Quotes without an attribution line stay unchanged.

module QuoteAuthor
  BLOCKQUOTE = %r{<blockquote\b[^>]*>.*?</blockquote>}m
  DASH = /\A\s*(?:–|—|--|-(?=\s))\s*/

  module_function

  def process(html, authors)
    return html unless html&.include?("<blockquote")

    html.gsub(BLOCKQUOTE) { |snippet| transform(snippet, authors) || snippet }
  end

  def transform(snippet, authors)
    fragment = Nokogiri::HTML::DocumentFragment.parse(snippet)
    blockquote = fragment.at_css("blockquote")
    children = blockquote&.element_children || []
    first = children.first
    attribution = children.last
    return unless first&.name == "p" && attribution&.name == "p" && first != attribution
    return unless first.text.strip.split(/\s+/).first == "Quote"
    return unless attribution.text.match?(DASH)

    dash = attribution.xpath(".//text()").find { |node| !node.content.strip.empty? }
    dash.content = dash.content.sub(DASH, "")
    picture = picture_for(attribution.text.strip, authors)
    avatar = picture ? %(<img src="#{CGI.escapeHTML(picture)}" alt="" class="avatar" loading="lazy">) : ""
    attribution.remove

    %(<figure class="quote">#{blockquote.to_html}<figcaption class="quote-author">#{avatar}#{attribution.inner_html.strip}</figcaption></figure>)
  end

  # The longest author name that the attribution starts with, followed by a non-word character
  def picture_for(attribution, authors)
    name = authors.keys.select do |key|
      attribution.start_with?(key) && attribution[key.length].to_s !~ /[\p{L}\p{N}]/
    end.max_by(&:length)
    name && authors.dig(name, "picture")
  end
end

Jekyll::Hooks.register [:documents, :pages], :post_convert do |doc|
  doc.content = QuoteAuthor.process(doc.content, doc.site.data["authors"] || {})
end
