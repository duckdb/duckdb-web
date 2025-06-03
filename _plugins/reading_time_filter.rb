module ReadingTimeFilter
  include Liquid::StandardFilters

  def reading_time(input)
    # Get words count.
    total_words = get_plain_text(input).split.size

    # Load configuration.
    config = @context.registers[:site].config["reading_time"]

    # Setup default value.
    if ! config
      second_plural = "sec"
      minute_singular = "min"
      minute_plural = "min"
    else
      second_plural = config["second_plural"] ? config["second_plural"] : "sec"
      minute_singular = config["minute_singular"] ? config["minute_singular"] : "min"
      minute_plural = config["minute_plural"] ? config["minute_plural"] : "min"
    end

    # Average reading words per minute.
    words_per_minute = 150

    # Calculate reading time.
    case total_words
    when 0 .. 75
      return "30 #{second_plural}"
    when 76 .. 150
      return "1 #{minute_singular}"
    else
      minutes = ( total_words / words_per_minute ).floor
      return "#{minutes} #{minute_plural}";
    end
  end

  def get_plain_text(input)
    strip_html(strip_pre_tags(input))
  end

  def strip_pre_tags(input)
    empty = ''.freeze
    input.to_s.gsub(/<pre(?:(?!<\/pre).|\s)*<\/pre>/mi, empty)
  end
end

Liquid::Template.register_filter(ReadingTimeFilter)
