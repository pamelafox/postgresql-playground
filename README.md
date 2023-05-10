
# FastAPI and Postgres Dev Environment with Codespadces

## Pydantic versus SQLAlchemy

[Pydantic]() is for
[SQLAlchemy]() is an ORM

https://www.reddit.com/r/FastAPI/comments/lmywl6/orm_or_pydantic_model/

The genius of the Pydantic models is data validation in my opinion. So you can specify expected types, required/optional fields, etc, and have FastAPI use that validation on the requests. In my work I’ve found it best if inter-application communication is the only place you utilize Pydantic models, and for internal data work, using ORM models.

As an example, let’s say you have a User model. This ORM model likely contains tons of fields that may or may not even be utilized by the API at any point, so you don’t want to build a Pydantic model directly based off of the ORM model. You instead build custom User Pydantic models. This allows you to define a bunch of different types of User data, so maybe you have an Admin API that should return more user data than you get through a public end-user API, you can have separate Pydantic models for each set of data.

In short, I find it’s best to use Pydantic models solely during API communication(validating request data, and what you return from the API), and use ORM models for the APIs internal processing(finding relational data, etc).

## Running the sample

1. Copy *.env.devcontainer* to *.env*.

2. Start the web app:

  ```
  uvicorn app:app --reload
  ```

## Files in the project

/devcontainer
  devcontainer.json
  docker-compose.yaml
  Dockerfile
.env.devcontainer
main.py
requirements.txt