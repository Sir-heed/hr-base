# HR Base

## Core Fucntionalities
- NOTE: Everyone is a User
- Every User needs to be authenticated to use the API
- A User can create an account, default role is USER
- A User can create an Organisation record, This makes a user an Org Admin
- The org_admin field of the created Organisation is updated with this user’s ID staff_access_code is an auto-generated unique 3-character code
- An Organisation can have two or more staff. Create necessary table if needed
- Only ORG_HRs can create & update jobs
- Users can see a list of all open jobs
- Users who are not staff of the Organisation that posted a Job opening can submit an Application for the job
- Only an ORG_ADMIN can see a list of his organisation’s staff and can delete/remove a staff member
- Only Org HR and Org Admin can see a list of Applications to a Job
- A User becomes a staff of an Organisation when they apply the access code of the organisation

## How to set up
- Clone the repo
- Ensure you have docker installed on your system
- Add the `.env` file in the same folder as `.sample.env` (Using the `sample.env` as template)
- Fill the database credentials with your preferred value, ensure the `POSTGRES_HOST` is left as `db`, and the port is `8432`, if you need to change these 2 values, ensure you update them in the `docker-compose` file.
- Run `docker build`
- Run `docker compose up`
- App should run by default on `0.0.0.0:8000`
