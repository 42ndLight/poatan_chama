# Chama CashPool App

## Overview
The **Chama CashPool App** is a financial management system designed to help self-organized savings groups (Chamas) efficiently manage contributions, payouts, and membership. Each Chama operates independently with a hierarchical structure of roles (Chairman, Treasurer, Contributor), ensuring transparency and accountability.

## Features
- **Chama Management**: Users can register a Chama and assign an administrator.
- **User Roles**: Members have distinct roles (Chairman, Treasurer, Contributor) with different permissions.
- **Cash Pool**: Each Chama has a unique cash pool to track contributions and withdrawals.
- **Member Management**: Users can join a Chama, and admins can view all members.
- **Contribution Tracking**: Users can contribute funds, and transactions are recorded.
- **Payout Management**: Funds can be disbursed from the Chama’s cash pool to members.

## Application Structure
The project is organized into multiple Django apps, each handling a specific function.

### 1. **Users App**
- Manages authentication and user roles.
- Allows users to register and log in.
- Supports different permissions based on roles.

### 2. **Chama App**
- Handles Chama creation and administration.
- Allows users to join existing Chamas.
- Fetches Chama details and members.

### 3. **Contributions App**
- Tracks all user contributions.
- Allows users to add contributions.
- Stores confirmation status of transactions.

### 4. **CashPool App**
- Manages each Chama’s financial pool.
- Tracks total balance based on contributions and payouts.
- Ensures financial transparency within the Chama.

## API Endpoints
| **Endpoint** | **Method** | **Description** |
|-------------|-----------|----------------|
| `/chama/register/` | `POST` | Register a new Chama |
| `/chama/join/` | `POST` | Join an existing Chama |
| `/chama/<int:pk>/` | `GET` | Retrieve Chama details |
| `/chama/<int:pk>/members/` | `GET` | List all members of a Chama |
| `/chama/<int:pk>/cashpool/` | `GET` | Retrieve Chama cash pool balance |
| `/contribution/add/` | `POST` | Add a contribution |
| `/payout/request/` | `POST` | Request a payout from the cash pool |

## Latest Advancements
- **Hierarchical Structure**: Introduced distinct roles with specific permissions.
- **Enhanced Serializers**: Added `ChamaMemberSerializer` to fetch structured member data.
- **Join Chama Feature**: Users can now join a Chama via an API request.
- **Improved Security**: Enforced authentication and permission checks for all critical actions.
- **Cash Pool Integration**: Each Chama has a real-time updated balance for financial tracking.

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/chama-cashpool.git
   cd chama-cashpool
   ```
2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
6. **Test API endpoints using Postman or Django’s API browser**.

## Next Steps
- Implement **automated payouts** with approval workflows.
- Add **mobile app support** for easy access.
- Integrate **notifications** for contribution updates.

## Contributors
- **Your Name** – Lead Developer
- **Other Contributors** – Backend, UI/UX, Data Analysts

## License
This project is licensed under the MIT License.

