# imdb_api

### Register
* POST
* endpoint: /v1/auth/register
* body: {
            "first_name": "{f_name}",
            "last_name": "{l_name}",
            "email": "{e-mail}",
            "password": "{pwd}",
            "country": "{country}"
        }


### Login
* POST
* endpoint: /v1/auth/login
* body: {
            "email": "{registered_email}",
            "password": "{password}"
        }

### Get Movies Data
* GET
* endpoint: /v1/movies
* parameters: name, director, imdb_score


### Add Movie Data
* POST
* endpoint: /v1/movie/add
* body: {
            "name": "{name}",
            "director": "{director}",
            "popularity": "{score (0-100)}",
            "rating": "{score (0-10)}"
        }

### Update Movie Data
* PUT
* endpoint: /v1/movie/update
* body: {
            "name": "{name}",
            "director": "{director}",
            "popularity": "{score (0-100)}",
            "rating": "{score (0-10)}"
        }

### Delete Movie Data
* DELETE
* endpoint: /v1/movie/delete
* param: name
 