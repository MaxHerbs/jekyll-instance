# Jekyll-instance
![Spelling Checks](https://github.com/maxherbs/jekyll-instance/actions/workflows/spell-checker.yml/badge.svg)
![Image Path Checks](https://github.com/maxherbs/jekyll-instance/actions/workflows/check-images.yml/badge.svg)
![Image Build](https://github.com/maxherbs/jekyll-instance/actions/workflows/build-img.yml/badge.svg)

This is the portfolio itself. `myblog` contains the blog, with all the corresponding posts and images.

The repository uses a [base image](https://github.com/maxherbs/jekyll-base) which contains an apache webserver, and the requirements to build the static site.


# Development
The image has a dev container which can be used to view the site locally before making the site public.

From the container, run 

```bash 
$ cd myblog
$ bash ../build.sh
```

Then check VSCode to see what port has been forwarded from the containers port 80 to see the site.


# CI/CD

1. **Docker Image Builder** - This builds a docker image on tag.

2. **Spell Checker** - Checks the spellings off all the blog posts.

3. **Check Images** - Verifies image links in blog posts exist.