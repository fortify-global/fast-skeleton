This is skeleton-api that should be used to create any microservices used in fortify.global
It is a way to enforce few standards.

To setup any new microservice in fast-api 
1) CLone this repo
2) Delete .git
3) Rename fast-skeleton to whatever name you want
4) Rename app instance correctly in main.py
5) Create a .env file and copy .env.dist content in .env file

Run ```docker-compose up``` ( for postgres and redis )
Run ```fastapi run```

[TODO] 
1) Create .log files outside app and fast-skeleton
2) Create Documentation of use
3) Correct way to deploy

