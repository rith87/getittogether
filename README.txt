Tutorials used:
1. http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
2. http://flask.pocoo.org/docs/tutorial/

Production:

1. Create database:
    python db_create.py
    
2. 'Migrate' database; this creates (not execute) a migration script:
    python db_migrate.py
    
3. Upgrade database to utilize latest in models.py:
    python db_upgrade.py
    
4. Start app server    
    python run.py
    
Testing:

1. Run all tests:
    python getItTogether_tests.py

2. Run individual test:
    python -m unittest getItTogether_tests.getItTogetherTestCase.test_user_points