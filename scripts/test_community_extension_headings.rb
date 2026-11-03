require 'liquid'
require_relative '../_plugins/community_extension_headings'

include CommunityExtensionHeadings

def assert(condition, message)
  raise message unless condition
end

html = <<~HTML
  <h3 id="compatibility-matrix">Compatibility Matrix</h3>
  <h3 id="about-demo">About demo</h3>
  <h1 id="readme">Readme</h1>
  <h2 id="usage">Usage</h2>
  <h3 id="example">A nested example</h3>
  <pre><code>### Added Functions</code></pre>
  <h3 id="added-functions">Added Functions</h3>
  <h3 id="added-settings">Added Settings</h3>
HTML

result = Nokogiri::HTML::DocumentFragment.parse(community_extension_headings(html, 'demo'))
expected = {
  'compatibility-matrix' => 'h2', 'about-demo' => 'h2', 'readme' => 'h3',
  'usage' => 'h4', 'example' => 'h5', 'added-functions' => 'h2', 'added-settings' => 'h2'
}
expected.each do |id, level|
  assert(result.at_css("##{id}").name == level, "Wrong heading level for #{id}")
end
assert(result.at_css('code').text == '### Added Functions', 'Code example changed')
assert(community_extension_headings(html, nil) == html, 'Regular documentation changed')

html = '<h3>Installing and Loading</h3><h3>Added Functions</h3>'
result = Nokogiri::HTML::DocumentFragment.parse(community_extension_headings(html, 'demo'))
assert(result.css('h2').size == 2, 'Sections without an About section were not promoted')

html = '<h3>About demo</h3><h2>Usage</h2><h3>Options</h3><h3>Added Functions</h3>'
result = Nokogiri::HTML::DocumentFragment.parse(community_extension_headings(html, 'demo'))
assert(result.css('h2, h3, h4').map(&:name) == %w[h2 h3 h4 h2], 'Description nesting is incorrect')

html = '<h3>Added Functions</h3><h1 id="function-example">Function example</h1><h3>Added Settings</h3>'
normalized = community_extension_headings(html, 'demo')
result = Nokogiri::HTML::DocumentFragment.parse(normalized)
assert(result.at_css('#function-example').name == 'h3', 'Heading inside a generated section escaped its parent')
assert(community_extension_headings(normalized, 'demo') == normalized, 'Normalization is not idempotent')

html = '<h3>About demo</h3><h4>First</h4><h2>Second</h2><h4>Nested</h4><h3>Added Functions</h3>'
result = Nokogiri::HTML::DocumentFragment.parse(community_extension_headings(html, 'demo'))
assert(result.css('h2, h3, h4').map(&:name) == %w[h2 h3 h3 h4 h2], 'Skipped source levels produced skipped output levels')

puts 'Community extension heading checks passed'
