# SocialAPI

SocialAPI is a RESTful API designed to streamline user interactions within a social networking context. It simplifies the process of user authentication and provides a suite of features to manage friendships and search capabilities within the network.

## Overview

The API offers the following features:

- **User Authentication**
- **User Search**
- **Friend Requests**
- **Friend List**
- **Pending Requests**
- **Rate Limiting**

## Installation

To get started with SocialAPI, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Musawir-ap/social-api.git
   ```

2. Navigate to the project directory:
   ```bash
   cd social-api
   ```

3. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

The application will be accessible at `http://localhost:8000`.

> **Note:** This repository includes a `.env` file to facilitate easy installation and testing of the API. Please ensure to update the `.env` file with your own environment variables before deployment.

## Sample Data

The database comes pre-loaded with sample data for users and tokens to aid in testing. Check the `/api/fixtures/` directory for details.

## Testing

To test the API endpoints, import the `Social-API.postman_collection.json` file from the root directory into Postman.

## Usage

Once the project is set up, you can:

- **Login**: Authenticate with your email and password.
- **Signup**: Register a new account using your email.
- **Search Users**: Find users by email or name.
- **Manage Friend Requests**: Send, accept, or reject friend requests.
- **List Friends**: View your list of friends.
- **View Pending Requests**: Check pending friend requests.

## Contributing

We welcome contributions from everyone. Feel free to fork the repository, make your changes, and submit a pull request. If you find any issues or have suggestions for improvements, please open an issue in the tracker.
