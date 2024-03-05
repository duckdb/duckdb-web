require 'jekyll-toc'

Jekyll::TableOfContents::Parser.class_eval do
  def inject_anchors_into_html
    @entries.each do |entry|
      # NOTE: `entry[:id]` is automatically URL encoded by Nokogiri
      entry[:text].replace(
        %(<a class="anchor" href="##{entry[:id]}">#{entry[:text]}</a>)
      )
    end

    @doc.inner_html
  end
end
