

## Project structure

Our project uses python to build telegram bot, uses docker `container` as the basis, uses `azure container app` to deploy, uses cloud services such as `azure cosmosDB`, `google map`, `yelp api`, etc. to implement functions, uses the telegram program as the front-end interface, and uses `git` as version control. Use `github` as a deployment platform and `github action` as continuous deployment tool.

```mermaid
graph TD
    A[Python Telegram Bot] -->|Deployed in| B[Docker Container]
    B -->|Hosted on| C[Azure Container App]
    C -->|Interacts with| D[Azure CosmosDB]
    C -->|Interacts with| E[Google Map API]
    C -->|Interacts with| F[Yelp API]
    A -->|Front-end Interface| G[Telegram Program]
    H[Git] -->|Version Control| A
    I[GitHub] -->|Deployment Platform| A
    J[GitHub Actions] -->|CI/CD Tool| I
    H -->|Triggers|J
    J -->|Deploy|C
```

## Cloud service platform

### Azure cosmosDB

- Free for HKBU students
- Have `mongodb` API that is convenient for python program to use
- Use `mongodb compass` to easily manage data
- Store dialog records so that GPT can have continuous conversations

### Azure container app

- Free for HKBU students
- Use k8s as a container cluster management platform to automatically deploy, scale and manage containerized applications.
- Use github action as a continuous deployment tool
