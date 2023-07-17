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
  params = params.split(',').map { |it| bold(code(it)) }.join('`, `') if params

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

# @return [Array<Object>, nil]
def get_functions
  files = Dir.glob('duckdb/src/core_functions/**/*.json')
  throw "No files found" if files.size == 0
  files.map do |file|
    functions = JSON.load File.open file
    category = File.basename File.dirname file
    functions.each do |function|
      function['category'] = category
    end
    functions
  end.flatten!
end


# @param [String] example
def get_result(example)
  exe = '/home/me/duckdb/build/debug/duckdb'
  return unless File.exists exe
  args = [exe, '-json', '-c', "select #{example} as result"]
  json_load = JSON.load IO.popen(args, :err => File::NULL).gets
  (json_load[0]['result'] unless json_load.nil?).to_s
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
      @converter = site.find_converter_instance(::Jekyll::Converters::Markdown)
      filter_expression = Liquid::Template.parse(@filter_expression).render context
      this = self

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
          functions = get_functions
          Jekyll.logger.info(@tag_name, "Loaded #{functions.size} functions")
          filtered = functions.filter { |function| this.select_function(filter_expression, function) }
          Jekyll.logger.info(@tag_name, "Filtered down to #{filtered.size} functions with expression: #{filter_expression}")

          filtered.each do |function|
            tr {
              td this.render_function(function)
              td function['description']

              example = function['example']
              unless example.nil? or example.empty?
                td(this.markdown_to_html(code(example)))
                result = get_result example
                td(this.markdown_to_html code result)
              end

              td(this.markdown_to_html(function['aliases'].map { |it| code(it) }.join(', '))) if function['aliases']
            }
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

    # @param [string] filter_expression
    # @param [Object] function
    def select_function(filter_expression, function)
      def get_binding(function)
        binding  # binding is an instance of the variable resolution scope
      end

      begin
        eval(filter_expression, get_binding(function))
      rescue => e
        Jekyll.logger.error(@tag_name, "Failed to select function with expression #{filter_expression}: #{e}")
        false
      end
    end
  end
end

Liquid::Template.register_tag('duckdb_functions', Jekyll::DuckDBFunctionsTag)
