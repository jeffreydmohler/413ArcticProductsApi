Lots of ways to install, even on the same architecture.
Not all tutorials are useful. Lots of variation.

Overview of platforms for Django deployment:
    Full VM: Amazon EC2, Digital Ocean, Azure
    PaaS: Amazon Beanstalk, Google App Engine, Heroku
    Lots of others

Overview of infrastructure:
    Database
    Python + Django + DRF + Your Code
    Connector
    Web server (nginx or IIS)
        Some way for the web server to know to pass control to the connector
    Handling static files
        Templates vs. Static Files
        React client

How to use my project:
    Download and unzip.
    If you use npm, switch from yarn with:
        rm yarn.lock
        npm install

1. Create a free account at heroku.com
2. Create a new Python app (not JS!)
3. Install the heroku command line
    Heroku offers two ways: not doing GitHub because I don't want everyones' code public
    Student accounts can be private, but logistics of ensuring that are too difficult right now
    But if you'd rather do GitHub with pipelines, feel free.

4. Deploy procedure for the API - just a guide
    # connect our arcticapi project to heroku
    heroku login
    # git init                         # we already did this earlier in the semester
    heroku git:remote -a arcticapi     # this adds heroku as a remote git repo we sync with

    # ensure everything is merged to master
    # don't forget to activate your python env
    git status                          # ensure all changes committed and project works
    git checkout master                 # if git complains here, you probably need to commit your changes
    git merge some-branch               # if you've been working in a branch, merge its changes into master
                                        # (merging is always towards you)

    # collect your static files         # https://devcenter.heroku.com/articles/django-assets
                                        # https://docs.djangoproject.com/en/3.0/howto/static-files/
    # code arcticapi/settings.py        # add STATIC_ROOT=... to your settings.py file
    python manage.py collectstatic

    # record our dependencies
    pip install gunicorn                # gunicorn connects the web server and django
    pip freeze > requirements.txt       # python -m pip freeze > requirements.txt
                                        # you may want to edit out some libraries afterward
    code runtime.txt                    # https://devcenter.heroku.com/articles/python-runtimes

    # create a procfile
    code Procfile                        # web: gunicorn arcticapi.wsgi --log-file -

    # push to our repo on heroku
    git add .
    git commit -am "make it better"
    git push heroku master

    # if everything works, click the "Open app" button in your dashboard on heroku
    heroku open                         # or let heroku open your web browser
    heroku logs --tail                  # if it didn't, look at the heroku logs
                                        # show my log

    # I got the "DisallowedHost at /" error, but the error page told me exactly what to do
    # add '*' to ALLOWED_HOSTS (not very secure for a real production site, btw):
        ALLOWED_HOSTS = [ '*' ]

    # Now my static files didn't load, so I looked in the browser console network tab.
    # One file it wanted was: https://arcticapi.herokuapp.com/static/rest_framework/js/bootstrap.min.js.
    # So at least it is specifying the static/ folder. I checked my local project's staticfiles folder,
    # and sure enough, it was there.  Grrr.  The error page was from **django**, not from the web server,
    # so I know it went to the web server. It means the web server isn't set to handle /static/* urls.
    # Reading the docs again, it looks like I need to install `whitenoise`:
    # https://devcenter.heroku.com/articles/django-assets#whitenoise
    # If you also add this, don't forget to get it into your requirements.txt

    # It works!!!! https://arcticapi.herokuapp.com/api/product/


5. Build the react client and place in the Django project:
    # create a new app called "client"
    cd arcticapi/
    python manage.py startapp client
    # add to APPS in settings.py
    # add to urls.py                    # path('/', include('client.urls'))
    # create client/urls.py             # use your api/urls.py as a template:
                                        # I got help from https://stackoverflow.com/a/14400341/12270327
                                        from django.urls import path
                                        from django.views.generic import TemplateView
                                        urlpatterns = [
                                            path('', TemplateView.as_view(template_name='index.html')),
                                        ]

    # build your react project
    cd arcticjs/
    npm build                           # you should now have a build/ folder with index.html

    # move the build to your arcticapi project's client app
    cd arcticapi/
    mkdir ./client/static/
    cp -rf ../arcticjs/build ./client/static/
    # move your index.html file into the location django expects it
    mkdir client/templates
    mkdir client/templates/client
    cp client/static/build/index.html client/templates/client/

    # Add static file lookup to your urls.py. Here's what mine is set to:
        from django.contrib import admin
        from django.urls import include, path
        from django.conf.urls.static import static
        from django.conf import settings

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api/', include('api.urls')),
            path('', include('client.urls')),
        ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Ensure your settings.py static files variables are set up:
        STATIC_URL = '/static/'
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # Run your server and load http://localhost:8000/
    # You should get a blank page. Look at the HTML source and see where the links go to.
    # It likely needs a prefix on the front of all the urls it points to: /static/client/build
    # https://create-react-app.dev/docs/deployment/#building-for-relative-paths
    # Move back to the JS project and set the "homepage" variable:
    cd ../arcticjs
    code package.json                   # add "homepage": "/static/build"
    npm build

    # after build, inspect the build/index.html file and ensure the prefix got added to JS and CSS links.
    # copy your react build folder into your api project client app:
    cd ../arcticapi
    cp -rf ../arcticjs/build ./client/static/
    cp client/static/build/index.html client/templates/client/

    # run and try again!
    python manage.py runserver

    # Once I got the static files right, I had to go back to the js project and
    # change all image paths in the code to use process.env.PUBLIC_URL var:
        src={`${process.env.PUBLIC_URL}/media/products/${row.product.filename}-1.png`}


    # ensure collectstatic still works
    python3 manage.py collectstatic

    # CHECK YOUR NETWORK TAB for bad urls.
    # I had to change my axios urls so http://localhost:8000 wasn't there
        await axios.get('/api/category')