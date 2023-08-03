# frozen_string_literal: true

require 'json'
require 'jekyll'
require 'word_wrap'

def code(child)
  "`#{child}`"
end

def bold(child)
  "*#{child}*"
end

def _render_function(function)
  name = function['name']
  params = function['parameters']
  params = params.map { |it| bold(code(it)) } if params

  if name =~ /^[[:punct:]]+$/
    if params.size == 2 # infix
      "#{params[0]} `#{name}` #{params[1]}"
    elsif ['@'].include? name # prefix
      "`#{name}`#{params[0]}"
    else # postfix
      "#{params[0]}`#{name}`"
    end
  else
    "`#{name}(`#{params.join('`, `')}`)`"
  end
end

class Html
  attr_accessor :html

  def initialize
    @html = ""
  end

  def method_missing(symbol, *args, &block)
    @html += "<#{symbol}>"
    if block_given?
      instance_eval(&block)
    elsif !args.empty?
      @html += args.join(' ')
    end
    @html += "</#{symbol}>"
  end
end

# @return [Array<Object>, nil]
def get_functions
  JSON.parse File.read 'docs/functions.json'
end

def generate_index(page, filtered)
  filtered.map do |function|
    {
      'title' => function['name'],
      'text' => function['description'],
      'category' => "#{page['title'].capitalize} Functions",
      'url' => page['url'].gsub(/\.html/, ''),
      'blurb' => WordWrap.ww(function['description'], 120)
    }
  end
end

module Jekyll
  class DuckDBFunctionsTag < Liquid::Tag
    @tag_name = ''
    @filter_expression = ''

    def initialize(tag_name, text, tokens)
      @tag_name = tag_name
      @filter_expression = text
      super
    end

    def render(context)
      site = context.registers[:site]
      page = context.registers[:page]
      @converter = site.find_converter_instance(::Jekyll::Converters::Markdown)
      filter_expression = Liquid::Template.parse(@filter_expression).render context
      this = self

      functions = get_functions
      Jekyll.logger.info(@tag_name, "Loaded #{functions.size} functions")
      filtered = functions.filter { |function| this.select_function(filter_expression, function) }.sort_by { |f| f['name'] }
      Jekyll.logger.info(@tag_name, "Filtered down to #{filtered.size} functions with expression: #{filter_expression}")

      puts generate_index(page, filtered)

      html = Html.new
      html.table {
        thead {
          tr {
            th "Function"
            th "Description"
            th "Example"
            th "Result"
            th "Aliases"
          }
        }
        tbody {
          filtered.each do |function|
            tr {
              td this.render_function(function)
              td function['description']

              example = function['example']
              unless example.nil? || example.empty?
                td(this.markdown_to_html(code(example)))
                result = function['result']
                if result.nil?
                  td('')
                else
                  td(this.markdown_to_html code result)
                end
              end

              if function['aliases']
                td(this.markdown_to_html(function['aliases'].map { |it| code(it) }.join(', ')))
              else
                td('')
              end
            }
          end
        }
      }

      html.html
    end

    def markdown_to_html(input)
      @converter.convert(input)
    end

    def render_function(function)
      markdown_to_html(_render_function(function))
    end

    # @param [string] filter_expression
    # @param [Object] function
    def select_function(filter_expression, function)
      def get_binding(function)
        binding  # binding is an instance of the variable resolution scope
      end

      begin
        eval(filter_expression, get_binding(function))
      rescue StandardError => e
        Jekyll.logger.error(@tag_name, "Failed to select function with expression #{filter_expression}: #{e}")
        false
      end
    end
  end
end

Liquid::Template.register_tag('duckdb_functions', Jekyll::DuckDBFunctionsTag)
