# Application Functionality

This document provides an overview of the functionality available in our financial management application.

## User Authentication

### Register
- **Endpoint:** `/api/register`
- **Method:** POST
- **Description:** Allows users to create a new account with optional profile picture upload.
- **Request Body:**
  - `username` (str): User's unique username.
  - `email` (str): User's email address.
  - `hashed_password` (str): Hashed user password.
  - `is_active` (bool): Indicates if the user's account is active.
  - `full_name` (str): User's full name.
  - `profile_picture` (file, optional): User's profile picture (optional).

### Login
- **Endpoint:** `/api/login`
- **Method:** POST
- **Description:** Allows users to log in and obtain an access token for authentication.
- **Request Body:**
  - `username` (str): User's username.
  - `password` (str): User's password.

## Investments

### Create Investment
- **Endpoint:** `/api/investments/`
- **Method:** POST
- **Description:** Create a new investment.
- **Request Body:**
  - `name` (str): Name of the investment (e.g., stock name).
  - `type` (str): Type of investment (e.g., stock, bond).
  - `quantity` (float): Number of units or shares.
  - `purchase_price` (float): Price per unit/share at purchase.
  - `user_id` (int): User's ID (for ownership).
  - `purchase_date` (datetime, optional): Date of purchase (optional).
  - `current_price` (float, optional): Current market price (optional).
  - `notes` (str, optional): Additional notes (optional).

### View Investment
- **Endpoint:** `/api/investments/{investment_id}`
- **Method:** GET
- **Description:** Retrieve details of a specific investment.
- **Request Parameters:**
  - `investment_id` (int): ID of the investment to retrieve.

### Edit Investment
- **Endpoint:** `/api/investments/{investment_id}`
- **Method:** PUT
- **Description:** Edit details of an existing investment.
- **Request Parameters:**
  - `investment_id` (int): ID of the investment to edit.
- **Request Body:** (Similar to Create Investment)

### List Investments
- **Endpoint:** `/api/investments/`
- **Method:** GET
- **Description:** List investments owned by the authenticated user.
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip (pagination).
  - `limit` (int, optional): Maximum number of records to return (pagination).

## Transactions

### Create Transaction
- **Endpoint:** `/api/transactions/`
- **Method:** POST
- **Description:** Record a new transaction for an investment.
- **Request Body:**
  - `investment_id` (int): ID of the associated investment.
  - `transaction_type` (str): Type of transaction (e.g., buy, sell).
  - `quantity` (float): Number of units or shares involved.
  - `transaction_date` (datetime): Date of the transaction.
  - `transaction_price` (float): Price per unit/share at the time.
  - `notes` (str, optional): Additional notes (optional).

### View Transaction
- **Endpoint:** `/api/transactions/{transaction_id}`
- **Method:** GET
- **Description:** Retrieve details of a specific transaction.
- **Request Parameters:**
  - `transaction_id` (int): ID of the transaction to retrieve.

### List Transactions
- **Endpoint:** `/api/transactions/`
- **Method:** GET
- **Description:** List transactions related to the authenticated user's investments.
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip (pagination).
  - `limit` (int, optional): Maximum number of records to return (pagination).

## Portfolios (Coming Soon)

### Create Portfolio
- **Endpoint:** `/api/portfolios/`
- **Method:** POST
- **Description:** Create a new portfolio for organizing investments.

### View Portfolio
- **Endpoint:** `/api/portfolios/{portfolio_id}`
- **Method:** GET
- **Description:** Retrieve details of a specific portfolio.

### Edit Portfolio
- **Endpoint:** `/api/portfolios/{portfolio_id}`
- **Method:** PUT
- **Description:** Edit details of an existing portfolio.

### List Portfolios
- **Endpoint:** `/api/portfolios/`
- **Method:** GET
- **Description:** List portfolios owned by the authenticated user.

---

## Running the FastAPI Application and PostgreSQL Database

To run the FastAPI application and PostgreSQL database using Docker, follow these steps:

**Step 1: Prerequisites**

Ensure that you have Docker installed on your system. You can download and install Docker from the official website if you haven't already: [Docker Website](https://www.docker.com/get-started).

**Step 2: Build and Start Docker Containers**

In your terminal, navigate to the directory containing your FastAPI application code and the `Dockerfile` and `docker-compose.yml` files.

**Step 3: Build the Docker Containers**

Run the following command to build the Docker containers:

```bash
docker-compose build






Investment Model
The Investment model represents individual financial assets held by users in their portfolio. It provides essential details about each investment, allowing users to track and manage their holdings effectively.

Fields
id (Primary Key): Unique identifier for the investment.
user_id (Foreign Key): The ID of the user who owns the investment.
name: The name or title of the investment (e.g., "Apple Inc. stock").
type: The type of investment (e.g., stock, bond, mutual fund).
quantity: The number of units or shares owned.
purchase_date: The date when the investment was purchased.
purchase_price: The price per unit/share at the time of purchase.
current_price: The current market price per unit/share.
notes: Additional notes or comments related to the investment.
created_at: The date and time when the investment was added to the system.
Purpose
The Investment model is used to:

Store detailed information about each financial asset.
Enable users to view their portfolio of investments.
Calculate the current value of investments based on market prices.
Track the purchase history and performance of individual assets.
Transaction Model
The Transaction model represents specific actions or events related to an investment. It records activities such as buying, selling, or receiving dividends for a particular investment.

Fields
id (Primary Key): Unique identifier for the transaction.
investment_id (Foreign Key): The ID of the investment associated with this transaction.
transaction_type: The type of transaction (e.g., buy, sell, dividend).
quantity: The number of units or shares involved in the transaction.
transaction_date: The date when the transaction occurred.
transaction_price: The price per unit/share at the time of the transaction.
notes: Additional notes or comments related to the transaction.
Purpose
The Transaction model is used to:

Record specific actions taken on individual investments.
Track the history of transactions for each investment.
Calculate investment performance, including gains or losses.
Generate reports and summaries of user activity.
By using both the Investment and Transaction models, your application can provide a complete solution for users to manage and analyze their financial assets effectively.



:- This document outlines the core functionality of our financial management application. If you have any questions or need further assistance, please refer to the API documentation or contact our support team.
