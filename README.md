# Webscanner

## Instructions
1. Must have docker installed (docker for desktop) and this project use twocaptcha api to solve captcha.
2. CD into the root of the project.
3. Create a .env file with the following env variables. Place it in the root directory (same level as docker-compose.yaml).
   ```
    TWOCAPTCHA_KEY=youkey
    UPWORK_USER=your-email
    UPWORK_PASS=your-password

   ```
4. Build the containers
   ```
   docker-compose up --build
   ```

5. We have two routes, one is to get information on the website
   ```
   http://localhost:5000/api/scanning/search
   ```
   And only accept the params with the key `page`, for example:
   ```
   http://localhost:5000/api/scanning/search?page=1
   ```
6. You can consult the json file with the results in the directory
   ```
   ../webscanner/app/api_uploaded_files
   ```
7. To see what is happening inside the firefox container:
   ```
   access: http://localhost:7900
   password: secret
   ```
8. To see the monitor http://localhost:8888