# Jekyll plugin to replace emojis with SVG sprites globally
module EmojiReplacer
  EMOJI_MAP = {
    '✅' => 'check',
    '❌' => 'minus'
  }.freeze

  def self.replace_emojis(output)
    return output unless output

    emoji_pattern = Regexp.union(EMOJI_MAP.keys)
    output.gsub(emoji_pattern) do |emoji|
      svg_id = EMOJI_MAP[emoji]
      %(<svg class="icon #{svg_id}"><use xlink:href="##{svg_id}"></use></svg>)
    end
  end
end

[:documents, :pages, :posts].each do |hook|
  Jekyll::Hooks.register hook, :post_render do |item|
    item.output = EmojiReplacer.replace_emojis(item.output)
  end
end
