## Notes, Ideas & TODOs for this project

Consider the following as a developers note. I'll keep updating this file with ideas & possible ways to improve the project. Please feel free to contribute or add any suitable features.

#### _What are trying to accomplish with this project?_

You know those times when you've deployed your applications on the cloud, which logs every step of way precisely onto your `*.log` files, and now everytime you know the application misbehaves you cannot be bothered to look into those log files.

This never happened to you?

Let's not lie of course it has, and you know settings up Elastic stack will fix alot of your problems, but thats just ALOT OF WORK!!

That is where we want this project to come in, The `monolg` package should give you an easy to use API for logging all of your steps in your local MongoDB instance or even better your MongoDB Cloud (For which you know you have plenty out of those 512 MBs laying around)

## Ideas

- [ ] Have options to create a session id, which will tie multiple log belonging to a single big task.
- [ ] There should be multiple ways of connecting to the MongoDB instance, research & implement all of those.


## Note

There are 2 ways to specify MongoDB connection string
+ [Standard Connection String Format](https://www.mongodb.com/docs/manual/reference/connection-string/#std-label-connections-standard-connection-string-format)

```
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```

There are various subtypes for different categories as well `Standalone`, `Replica Set`, `Shared Cluster`, `Atlas Deployment`
Lets start off with `Standalone` we'll add other version in future runs.

+ For a standalone
```
mongodb://mongodb0.example.com:27017
```

+ For a standalone that [enforces access control](https://www.mongodb.com/docs/manual/tutorial/enable-authentication/):
```
mongodb://mongodb0.example.com:27017
```


+ [DNS Seed List Connection Format](https://www.mongodb.com/docs/manual/reference/connection-string/#std-label-connections-dns-seedlist)

### Some helpful mongo commands
* #### Checking available users in mongo
```mongo
use admin
db.system.users.find()
```

* #### Creating a new user
```mongo
db.createUser({user: "mongo", pwd: "mongo", roles: [{role: "userAdminAnyDatabase", db: "admin"}]})
```
