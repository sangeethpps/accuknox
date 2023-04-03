Installation Steps

-Step1 pull the project

-Step2 run the command docker-compose up

-Step3 run the command docker-compose exec app python manage.py makemigrations

-Step4 run the command docker-compose exec app python manage.py migrate

-Step5 run the following command if dummy users up to 12 should be created for you

    docker-compose  docker-compose exec app python manage.py create_dummy_users

- Step4 if you would like to test the api in postman then you need a token and this can be created using below command 



    http POST http://0.0.0.0:8000/api-token-auth/ username='sangeeth@gmail.com' password="sangeeth"


-to view post man collection use the link https://crimson-resonance-474833.postman.co/workspace/Accuknox~ca019467-5c0b-4169-b653-e6b8664a30dc/collection/16127464-c0f75e83-a641-4ce5-b8ba-31bdcd482a6a?action=share&creator=16127464
