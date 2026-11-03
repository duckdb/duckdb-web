# Enable YJIT, Ruby's JIT compiler, which speeds up the build by about 30%.
# RubyVM::YJIT.enable is available since Ruby 3.3, if Ruby was built with YJIT.
if defined?(RubyVM::YJIT) && RubyVM::YJIT.respond_to?(:enable) && !RubyVM::YJIT.enabled?
  RubyVM::YJIT.enable
end
