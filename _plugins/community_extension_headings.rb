require 'nokogiri'

module CommunityExtensionHeadings
  SECTION_TITLES = [
    'Compatibility Matrix', 'Installing and Loading', 'Example',
    'Added Functions', 'Overloaded Functions', 'Added Types', 'Added Settings'
  ].freeze

  def community_extension_headings(html, extension_name)
    return html unless extension_name

    fragment = Nokogiri::HTML::DocumentFragment.parse(html)
    headings = fragment.css('h1, h2, h3, h4, h5, h6')
    sections = headings.select do |heading|
      heading.parent == fragment && %w[h2 h3].include?(heading.name) &&
        (SECTION_TITLES.include?(heading.text.strip) || heading.text.strip == "About #{extension_name}")
    end

    sections.each_with_index do |section, index|
      following_section = sections[index + 1]
      child_headings = headings.drop(headings.index(section) + 1)
      child_headings = child_headings.take_while { |heading| heading != following_section }
      levels = []
      child_headings.each do |heading|
        original_level = heading.name[1].to_i
        levels.pop while levels.last && levels.last >= original_level
        heading.name = "h#{[levels.size + 3, 6].min}"
        levels << original_level
      end
    end

    sections.each { |heading| heading.name = 'h2' }
    fragment.to_html
  end
end

Liquid::Template.register_filter(CommunityExtensionHeadings)
