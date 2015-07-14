# PyCon UK Proposal Voting
A simple project to enable ticket holders to vote on the proposals for PyCon UK.

## Import Users
Export a csv dump from ti.to and save it as `users.csv`.

```
DATABASE_URL=$(heroku config:get DATABASE_URL) python manage.py import_users users.csv
```

## Import Proposals
```
python manage.py import_talks
```

This is designed to be run regularly and has been scheduled on Heroku for an hourly run.
