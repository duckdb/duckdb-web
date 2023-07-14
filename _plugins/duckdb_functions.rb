require 'json'

class Html
  attr_accessor :html

  def initialize
    @html = ""
  end

  def method_missing(m, *args, &block)
    @html += "<#{m}>"
    if block_given?
      instance_eval &block
    elsif args.length > 0
      @html += args.join(' ')
    end
    @html += "</#{m}>"
  end
end

module Jekyll
  class DuckDBFunctionsTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      puts tag_name
      puts text
      puts tokens
      super
    end

    def render(context)
      html = Html.new
      html.h2 "Functions"
      html.table {
        thead {
          tr {
            th "Function"
            th "Description"
            th "Example"
            th "Aliases"
          }
        }
        tbody {
          Dir.glob('/home/me/duckdb/src/core_functions/**/*.json').each do |file|
            puts "reading from #{file}"
            json = File.open file
            json = JSON.load json

            json.each do |function|
              puts function['name']

              tr {
                td "#{function['name']}(#{function['parameters']})"
                td function['description']
                td "<pre><code>#{function['example']}</code></pre>"
                td function['aliases'].join(', ') if function['aliases']
              }
            end
          end
        }
      }

      html.html
    end
  end
end

Liquid::Template.register_tag('duckdb_functions', Jekyll::DuckDBFunctionsTag)
