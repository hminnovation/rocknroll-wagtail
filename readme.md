Rock n roll wagtail
====================

**Note:** This is still very much a work in progress and shouldn't be used as a good example of how to make a Wagtail site!

See **[Beginner Wagtail](https://github.com/heymonkeyriot/beginner-wagtail/)** for a simpler, working, introduction to Wagtail CMS.

![No Wagtail playing](https://github.com/heymonkeyriot/rocknroll-wagtail-cookiecutter/blob/master/wagtail%20rock%20n%20roll.jpg)

#### A Wagtail project for cut 'n' paste pulling apart

## Installation
### Locally

```
git clone git@github.com:heymonkeyriot/rocknroll-wagtail.git
cd monkeywagtail
vagrant up
vagrant ssh
pip install -r requirements.txt
cd monkeywagtail/static
npm install
bower install
gulp watch
# in a new terminal tab
cd ../../
dj makemigrations   # ./manage.py makemigrations
dj migrate   # ./manage.py makemigrations
dj createsuperuser --username username   # ./manage.py createsuperuser
djrun   # ./manage.py runserver 0.0.0.0:8000
```

You should now be able to visit http://localhost:1234 and see the site


## Why

A demo project for those who are bad at reading documentation. At a code sprint for Wagtail in Philadelphia, in March 2016, there was a request for something showing different aspects of Wagtail and Django to help you get set-up with understanding how Wagtail CMS works.

From a personal perspective this was also a chance to implement a Wagtail projects without client constraint to try and get as full an insight as possible in to the software.


## What

Rock n roll Wagtail is a project using a music site content model, with different types of relationships defined between artist, album, review, feature and author apps.

The project is documented throughout with comments to explain what code is being used for. The aim of the documentation is to explain concisely to someone unfamiliar with either Django or Wagtail (but familiar with the concept of a programming language) what the code is doing with links to additional documentation. **Pull requests to improve the documentation, correct misunderstandings, or poor explanation would be very gratefully received**

The project gives recipes of how to use one-to-one relations, one-to-many relations, and many-to-many relations alongside the use of both page models, generic models and generic models with the, Wagtail-specific, `@snippet` decorator.

The project additionally gives recipes for implementing different StreamField blocks, a CMS powered menu and other utility type functionality such as related pages.

Each app within the project has been deliberately implemented in slightly different ways to show various functionality that Wagtail can be used for.

The front-end is currently powered by Foundation. This will hopefully be amended to something less opinionated in a future release, but shouldn't cause any issue in the meantime.

#### Apps

 - Album
 - Artist
 - Author
 - Core (utilities)
 - Feature Content Page
 - Genres
 - Home
 - Reviews
 - Search
 - Standard page


## Usage instructions

To-do

## Troubleshooting
#### `command not found: gulp` (or Bower, NPM etc)
To run Foundation, and compile SASS files using Django Compressor, you'll need to install some additional software if it isn't on your computer.

Assuming you're starting from zero on a Mac running OSX

 -  [Install Homebrew ](http://brew.sh/)
 -  [Install NPM with Homebrew](https://changelog.com/install-node-js-with-homebrew-on-os-x/) `brew install node`
 -  Install Bower `npm install -g bower`
 -  Install Gulp `npm install -g gulp`

## Based upon

The project is based upon [Torchbox's Wagtail Cookiecutter](https://github.com/torchbox/cookiecutter-wagtail) and includes:

 - A Django project with Wagtail preinstalled
 - Vagrant configuration (using the [torchbox/wagtail](https://github.com/torchbox/vagrant-wagtail-base) base box)
 - Heroku configuration
 - Sphinx docs


## Changelog

**06/07/16** Currently very much a work in progress. Models are working, but there aren't any templates!

**19/09/16** Models have all been re-written based on better understanding them.

**04/03/17** Still a work-in-progress(!)

## TODO 

 - [x] Finish the models and Wagtail admin UI
 - [ ] Create more reliable fixtures for initial content population
 - [x] Introduce filtering for artist and reviews
 - [ ] Template the models
 - [ ] Fully inline comments for the different models and templates
 - [ ] Put `cd monkeywagtail/static && npm install && bower install` within vagrant provision file
