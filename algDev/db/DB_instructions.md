### Downloading and Setting up Google Cloud CLI
Our database is hosted on Google Cloud, so before setting up a local client connection to the DB, you'll need to install the Google Cloud command line tool from here: https://cloud.google.com/sdk/docs#install_the_latest_cloud_sdk_version 

Once you've downloaded that, initialize the tool with `gcloud init` and authenticate into FML's Google Cloud account by running  `gcloud auth login` and signing in on your browser.

### Setting up the Proxy
For mac, WHILE IN THE `backend/db` directory, run the following command to download the proxy into the correct location:
`curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64`
Other OS' instructions can be found here: https://cloud.google.com/sql/docs/postgres/quickstart-proxy-test 

You may also need to make the proxy's permissions accessible to all users, which you can do by running `chmod +x cloud_sql_proxy` once you've downloaded it.

Once you've downloaded the proxy, run the following command:
`./cloud_sql_proxy -instances=fml-partners:us-east1:fmlv1=tcp:5432`
This will begin a connection to the DB from your local machine/testing environment hosted on port 5432. The output should end with a message that looks something like:
`Listening on 127.0.0.1:5432 for fml-partners:us-east1:fmlv1`.
Ready for new connections

### Connecting to the DB
Since we're using a Python backend, we'll be using the psycopg2 module, which is most commonly used to interface between Python and a PostgreSQL database. (see a pretty handy tutorial here: https://pynative.com/python-postgresql-insert-update-delete-table-data-to-perform-crud-operations/#Python_PostgreSQL_INSERT_into_database_Table)

The most important thing is to, before you connect to the database, ensure that you have the correct credentials to do so. In the db folder in the backend, duplicate the `credentials.prod` file and rename it to `credentials.py`. Then, replace the fake/temporary values with the values that I, Jaiveer (jay - vEEr), give you. 

Once you've done that, you can import the credentials and connect to the db WHILE THE PROXY IS RUNNING. You won't be able to connect to the database unless the proxy is running. Both the primer script and the tutorial linked above are two examples that show how to run SQL queries on the DB, the most important of which is to actually connect to the client from your script:
`conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password)`

This line, taken from the primer script, imports the credentials from the credentials.py file and plugs them into the `psycopg2.connect()` function.

### Fetching Information From the DB
To fetch data from the DB, you can use the `wrapper.py` script. Right now, the only implemented functions are `getData()`, which takes in a ticker as an argument and returns a list of tuples of historical data for that ticker, and `getTickers()` which returns a list of all the tickers in the DB.










