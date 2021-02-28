Sandbox Code Runner
===

# Local Build & run

```shell
docker build -t coderunner .
docker run -p 8080:8080 --expose 8080 --env-file .env.docker --name coderunner coderunner
```

# Production Build and Deploy
 
You need to have `gcloud` CLI installed on your system, or you can use the GCP shell, or the GUI Console.

You can read the official [docs](https://cloud.google.com/run/docs/quickstarts/build-and-deploy).

## Build

```shell
gcloud builds submit --tag gcr.io/${PROJECT_ID}/coderunner
```

## Deploy

We recommend doing this through the GCP Console GUI because you also need to set the environment variables.
