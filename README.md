# Pitch Deck uploader

A simple app that converts PDF pitch decks to images and displays them.

## Tech stack:

- Django, PostgreSQL, Redis & RQ.
- PDF conversion is done by the [pdf2image](https://github.com/Belval/pdf2image) library.
- PPTX conversion is done via libreoffice, the pdf2image. (experimental)
- Project template from [key/django-project-template](https://github.com/key/django-project-template)

## How to install

The easiest way to get this up and running is with docker. Assuming you already have docker installed, run:

```
docker compose up
```

Then go to http://localhost:8000/

### Without docker

If you really want to run this without docker, here's what you'll need first:

- Python
- Pipenv
- PostgreSQL
- Redis
- `poppler-utils` (may already be installed on many linux distros)

To setup and install the app itself:

1. Create a database and user
2. Copy `.env.example` to `.env`. Update DATABASE_URL and REDIS to match your local setup
3. Run
    ```
    pipenv install --dev
    pipenv run ./manage.py runserver_plus
    ```
4. Go to `http://localhost:8000/`

## Running tests

```
docker/pytest
```

## Deployment

Docker containers can be deployed to Heroku directly. Checkout the code and the follow the [steps here](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#creating-your-app-from-setup) to create an app directly from the heroku.yml

## License

The MIT License (MIT)
