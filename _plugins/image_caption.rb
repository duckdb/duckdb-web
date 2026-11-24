# frozen_string_literal: true

# Turns an image followed by a caption into a figure, so the caption can be limited to the image width:
#
#   ![Alt text](image.png){: .center width="480" }
#   *Caption text*{: .caption }
#
# renders as
#
#   <figure class="image"><img …><figcaption>Caption text</figcaption></figure>
#
# This works with and without an empty line between image and caption, and with several images
# (e.g. a light and a dark mode variant) in front of one caption. A caption without an image in
# front of it stays unchanged.

module ImageCaption
  IMAGES = %r{(?:\s*(?:<a\b[^>]*>\s*)?<img\b[^>]*>(?:\s*</a>)?)+\s*}
  CAPTION = %r{<em class="caption">((?:(?!</p>).)*?)</em>\s*</p>}m
  FIGURE = %r{<p>(#{IMAGES})(?:</p>\s*<p>\s*)?#{CAPTION}}m

  module_function

  def process(html)
    return html unless html&.include?('class="caption"')

    html.gsub(FIGURE) do
      %(<figure class="image">#{Regexp.last_match(1).strip}<figcaption>#{Regexp.last_match(2).strip}</figcaption></figure>)
    end
  end
end

Jekyll::Hooks.register [:documents, :pages], :post_convert do |doc|
  doc.content = ImageCaption.process(doc.content)
end
