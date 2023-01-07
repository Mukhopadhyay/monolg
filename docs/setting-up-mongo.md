# Setting up MongoDB

MongoDB is one of the hard dependencies for this project. `Monolg` works the way it does because of MongoDB. Let's look at the installation process of **MongoDB**.

To learn more about **MongoDB** installation check out their official page.

[MongoDB Installation](https://www.mongodb.com/docs/manual/installation/){ .md-button }

Here are some of the insllation tutorials of **MongoDB Community Edition** on popular platforms.

!!! note "**MongoDB Atlas**"
    [MongoDB Atlas](https://www.mongodb.com/atlas/database) is a hosted MongoDB service option in the cloud which requires no installation overhead and offers a free tier to get started.

## Docker <small>[[ref]](https://www.mongodb.com/compatibility/docker)</small>

MongoDB can run in a container. The official image is available on [**Docker Hub**](https://hub.docker.com/_/mongo)

**Pulling the image**
```bash
docker pull mongo
```

**Running MongoDB as a Docker Container**

You canstart a MongoDB container using Docker with the following command:
```bash
docker run --name mongodb -d -p 27017:27017 mongo
```

This command will start a MongoDB server running the latest available version in detached mode (as a background process). As a best prractive, it's recommended to use a tag to specify the MongoDB version to ensure consistency.

Since `Monolg` will need to connect to MongoDB, we're exposing the port using the `-p` argument. Using this method, you will be able to connect to your MongoDB instance on `mongodb://localhost:27017`.

!!! warning "Data Persistance"
    Any data created as part of the lifecycle of that container will be destroyed once the container is deleted. If you want to persist the data on your local machine. You can mount a volume using the `-v` argumenjt.

    ```bash
    docker run --name mongodb -d -v YOUR_LOCAL_DIR:/data/db mongo
    ```
