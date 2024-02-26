FROM rockstorm/jekyll:pages-v228-minimal

ARG UID=1000
ARG UNAME=user
ARG GID=1000
ARG GNAME=group

RUN apk add --update gcc g++ make ruby-bundler linux-headers

RUN groupadd -g $GID -o $GNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN mkdir /app && chown $UNAME:$GNAME /app
USER $UNAME

COPY --chown=$UNAME:$GNAME Gemfile /app
COPY --chown=$UNAME:$GNAME Gemfile.lock /app
RUN cd /app && bundle config set --local path /home/$UNAME/.gem && bundle install

EXPOSE 4000
EXPOSE 35729
