set -x

rm -r _site
bundle install 
bundle exec jekyll build
cp -r _site/* /var/www/html/