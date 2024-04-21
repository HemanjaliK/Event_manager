**ISSUE**: 1
**Login and Registration**: In order to facilitate end users' testing of the API and eliminate the need for them to copy and paste their username and password, the data on the openapi spec page must match for both registration and login.
1. We need to Authorize then
2. Click on try it out in register and also in login
3. Then we can find the Error
4. we have to create the issue and then created the branch
5. we need change the code in app/schemas/the user_schemas.py according to the username and password
6. Then we need to run the "docker compose exec fastapi pytest tests/test_api/test_users_api.py::test_delete_user_does_not_exist"
7. And also "docker compose exec fastapi alembic upgrade head"
8. After running this two commands then we need to refresh the local/docs then we can find the out as same username and password in the both register and login
# https://github.com/HemanjaliK/event_manager/commit/90dfdf03c744bd834329e9dc1e25c3e99d9bc90b


**ISSUE**: 2
**NULL VALUES**: 
1. We need to Authorize then
2. Click on try it out in GET
3. Then we can see the issue that is:
       - full_name=Null,
       - bio=Null,
       - profile_picture_url=Null,
4. In github Repository we have to create the issue and then created the branch
5. Now I have added the below lines in the app/routers/user_routes.py:
       - full_name=user.full_name,
       - bio=user.bio,
       - profile_picture_url=user.profile_picture_url,
6. Then we need to run the "docker compose exec fastapi pytest tests/test_api/test_users_api.py::test_delete_user_does_not_exist"
7. And also "docker compose exec fastapi alembic upgrade head"
8. After running this two commands then we need to refresh the local/docs then we can see there is no Null values
# https://github.com/HemanjaliK/event_manager/commit/4620cb4eef51e911f2b0f21078f6a7f35eaf9b98

**ISSUE**: 3
**URL**:
1. We need to Authorize then
2. Click on try it out in PUT
3. Then we can see that the URL is not updating. that is the issue in the issue 3
4. In github Repository we have to create the issue and then created the branch
5. We have to change the http url to string in the app/schemas/user_schemas.py so that the issue get updated in the localhost/doc
6. After changing the code we need to refresh the localhost/doc so that it gets updated in PUT.
# https://github.com/HemanjaliK/event_manager/commit/522d6a876d1bf9f7713ab1c13fbc21d986875790

**ISSUE**: 4
# https://github.com/HemanjaliK/event_manager/commit/5ebba5233218fa8fdcbb6a9364e67397ef2d5948

**ISSUE**: 5
# https://github.com/HemanjaliK/event_manager/commit/c07465ee3f8d58d8f6fd35c9ec568806000f7ebc

**WHAT I HAVE LEARNED FROM THIS ASSIGNMENT IS**:
 I have learn about building and managing a full-stack application using technologies such as FastAPI for backend development, which offers features for easy API creation with automatic interactive documentation, user management, and secure handling of user data. The use of a database management tool like pgAdmin (accessible via http://localhost:5050/browser/) would enhance skills in database operations and management. Additionally, you'd gain experience in implementing user authentication and authorization, designing RESTful APIs, and understanding how to document and test APIs effectively using tools integrated into development environments like Swagger UI at http://localhost/docs#/User%20Management/. This project would also likely improve your ability to work with version control systems like Git and deploy applications using Docker, thereby enhancing both your development and operational skills.