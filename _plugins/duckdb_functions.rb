require 'json'
require 'jekyll'

def code(child)
  "`#{child}`"
end

def bold(i)
  "*#{i}*"
end

def _render_function(function)
  params = function['parameters']
  params = params.split(',').map { |it| bold(code(it)) }.join('`, `')

  "#{code(function['name'] + '(')}#{params}#{code(')')}"
end

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
      site = context.registers[:site]
      @converter = site.find_converter_instance(::Jekyll::Converters::Markdown)

      this = self

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
          files = Dir.glob('/home/me/duckdb/src/core_functions/**/*.json')
          div "No files found" if files.size == 0
          files.each do |file|
            json = File.open file
            json = JSON.load json

            json.each do |function|

              tr {
                td this.render_function(function)
                td function['description']

                example = function['example']
                td(this.markdown_to_html(code(example))) unless example.empty? or example.nil?

                td(this.markdown_to_html(function['aliases'])) if function['aliases']
              }
            end
          end
        }
      }

      html.html
    end

    def markdown_to_html(i)
      @converter.convert(i)
    end

    def render_function(function)
      markdown_to_html(_render_function(function))
    end
  end
end

Liquid::Template.register_tag('duckdb_functions', Jekyll::DuckDBFunctionsTag)
