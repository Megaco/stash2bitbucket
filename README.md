##Bitbucket Server (formerly Stash) to Bitbucket Cloud migrator.

To start migrating your stash repositories into Bitbucket cloud.

* Fill the all required variables in, i.e.:

**Stash (Bitbucket server) credentials and server's URL**:


```
stash_url (stash server URL in format 'stash.example.com', without 'https://' prefix)
stash_login
stash_password
```

**Bitbucket Cloud credentials and workspace name**:

```
bitbucket_workspace
bitbucket_login
bitbucket_password
```

* Execute run.sh script (it will create a virtual python environment and start the migration process)
* Enjoy!

#Requirements:
* python3
* git
* shell