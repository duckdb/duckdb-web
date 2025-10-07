module Jekyll
  module DomainExtractor
    def extract_domain(url)
      return "" if url.nil? || url.empty?
      
      domain = url.gsub(%r{^https?://}, '')
      domain = domain.gsub(/^www\./, '')
      domain = domain.split('/').first
      domain = domain.split(':').first
      
      domain
    end
  end
end

Liquid::Template.register_filter(Jekyll::DomainExtractor)
