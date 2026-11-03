# frozen_string_literal: true

require "etc"

# Renders pages in parallel, using forked worker processes.
#
# Jekyll renders pages one by one, and Ruby's global VM lock rules out speeding
# this up with threads. However, after the read and generate phases, the whole
# site is in memory, so we can fork() workers that inherit it copy-on-write.
# Each worker takes pages from a shared job queue, renders them, and writes
# them to the destination directory itself. The main process renders the
# remaining pages, then joins the workers in processing the queue.
#
# Only pages under docs/ and community_extensions/ are rendered by the forked
# workers: other pages only use their front matter (e.g., the guides overview),
# never their rendered output, so it does not matter that the main process
# never sees it. Posts are always rendered in the main process, as their
# rendered content is used by other pages (e.g., the feed and the blog index).
#
# The number of processes (including the main process) is set with the
# JEKYLL_WORKERS environment variable. It defaults to the number of CPUs,
# capped at DEFAULT_MAX_WORKERS. Set JEKYLL_WORKERS=1 to render sequentially.
#
# Note that with `--profile`, the render stats only cover the main process.

module ParallelRender
  DEFAULT_MAX_WORKERS = 12
  # below this many pages (e.g., in incremental regeneration), forking is not worth it
  MIN_PAGES = 100
  JOB_FORMAT = "L" # 32-bit unsigned job index
  JOB_SIZE = 4

  def self.worker_count
    ENV.fetch("JEKYLL_WORKERS") { [Etc.nprocessors, DEFAULT_MAX_WORKERS].min }.to_i
  end

  def self.parallel_page?(page)
    page.relative_path.start_with?("docs/", "community_extensions/") && page.output_ext == ".html"
  end

  # Concurrent reads of at most PIPE_BUF bytes from a pipe are atomic, so the
  # pipe works as a job queue shared by all processes. We use sysread to bypass
  # Ruby's IO buffering, which would read ahead and take jobs from the others.
  def self.next_job(queue)
    queue.sysread(JOB_SIZE).unpack1(JOB_FORMAT)
  rescue EOFError
    nil
  end

  module PageExtension
    attr_accessor :written_by_worker

    def write(dest)
      super unless written_by_worker
    end
  end

  module SiteExtension
    def render_pages(payload)
      process_count = ParallelRender.worker_count
      return super unless process_count > 1 && Process.respond_to?(:fork)

      jobs, local = pages.partition { |p| ParallelRender.parallel_page?(p) && regenerator.regenerate?(p) }
      return super if jobs.size < ParallelRender::MIN_PAGES

      # hand out the biggest pages first so that the processes finish at about the same time
      jobs.sort_by! { |page| -page.content.to_s.bytesize }
      queue_r, queue_w = IO.pipe
      workers = Array.new(process_count - 1) { fork_worker(jobs, payload, queue_r, queue_w) }

      begin
        feeder = Thread.new do
          jobs.each_index { |i| queue_w.syswrite([i].pack(ParallelRender::JOB_FORMAT)) }
          queue_w.close
        end
        feeder.report_on_exception = false

        # pages outside docs/ are rendered in the main process, as usual,
        # including pages added during rendering (e.g., Sass source maps)
        known_page_count = pages.size
        local.each { |page| render_regenerated(page, payload) }
        while known_page_count < pages.size
          render_regenerated(pages[known_page_count], payload)
          known_page_count += 1
        end

        # then the main process joins the workers
        while (i = ParallelRender.next_job(queue_r))
          render_regenerated(jobs[i], payload)
        end
        feeder.join
      rescue Exception # rubocop:disable Lint/RescueException
        # e.g., a Liquid error in the main process: do not leave the workers behind
        feeder&.kill
        workers.each do |pid, _|
          Process.kill("TERM", pid)
        rescue Errno::ESRCH
          nil
        end
        workers.each { |pid, _| Process.wait(pid) }
        raise
      ensure
        queue_w.close unless queue_w.closed?
        queue_r.close
      end

      collect_workers(workers, jobs)
    end

    private

    def fork_worker(jobs, payload, queue_r, queue_w)
      result_r, result_w = IO.pipe
      pid = fork do
        # the main process terminates the workers if it fails
        Signal.trap("TERM") { exit!(1) }
        status = 1
        begin
          queue_w.close
          result_r.close
          result = begin
            rendered = []
            while (i = ParallelRender.next_job(queue_r))
              page = jobs[i]
              render_regenerated(page, payload)
              page.write(dest)
              rendered << i
            end
            # the dependencies recorded by the worker are needed for incremental regeneration
            { rendered: rendered, metadata: incremental? ? regenerator.metadata : {} }
          rescue Exception => e # rubocop:disable Lint/RescueException
            { error: "#{e.class}: #{e.message}", backtrace: e.backtrace }
          end
          result_w.write(Marshal.dump(result))
          result_w.close
          status = result[:error] ? 1 : 0
        ensure
          $stdout.flush
          $stderr.flush
          # skip at_exit handlers inherited from the main process (e.g., the Sass compiler's)
          exit!(status)
        end
      end
      result_w.close
      # read the result in a thread so that a worker never blocks on a full pipe
      reader = Thread.new { result_r.read.tap { result_r.close } }
      [pid, reader]
    end

    def collect_workers(workers, jobs)
      errors = []
      workers.each do |pid, reader|
        data = reader.value
        Process.wait(pid)
        result = data.empty? ? { error: "Worker #{pid} exited with #{$?.inspect}" } : Marshal.load(data) # rubocop:disable Security/MarshalLoad
        if result[:error]
          errors << result
          next
        end
        result[:rendered].each { |i| jobs[i].written_by_worker = true }
        merge_regenerator_metadata(result[:metadata])
      end
      return if errors.empty?

      errors.each do |e|
        Jekyll.logger.error("Parallel render:", e[:error])
        Jekyll.logger.debug("Parallel render:", Array(e[:backtrace]).join("\n"))
      end
      raise errors.first[:error]
    end

    def merge_regenerator_metadata(worker_metadata)
      worker_metadata.each do |path, entry|
        existing = regenerator.metadata[path]
        if existing
          existing["deps"] |= entry["deps"]
        else
          regenerator.metadata[path] = entry
        end
      end
    end
  end
end

Jekyll::Page.prepend(ParallelRender::PageExtension)
Jekyll::Site.prepend(ParallelRender::SiteExtension)
