FROM rockstorm/jekyll:pages-v228-minimal

RUN mkdir /app

COPY Gemfile /app
COPY Gemfile.lock /app

RUN apk add --update gcc g++ make ruby-bundler
RUN cd /app && bundle install

EXPOSE 4000
EXPOSE 35729
