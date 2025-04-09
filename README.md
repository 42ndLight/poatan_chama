# CashPool Chama Management System

## Overview
CashPool is a **Chama (informal savings group) management system** designed to facilitate user registration, contribution tracking, cash pool management, and hierarchical governance within a Chama. This system allows users to **register, join, and manage a Chama**, interact with contributions, and oversee payouts seamlessly.

## Features
- **User Authentication & Profile Management** (Registration, Login, Profile Updates, Password Management)
- **Chama Management** (Create, Join, and View Chama details)
- **Cash Pool Management** (Track available funds per Chama)
- **User Roles & Hierarchy** (Contributor, Treasurer, Chairman)
- **Contribution Tracking**
- **Payout Management**

---

## Apps & Their Functionalities

### **1️⃣ User Authentication & Profile Management** (`users` app)
This app handles user registration, authentication, and profile management.

#### **Endpoints:**
| Endpoint                     | Method | Description                         |
|------------------------------|--------|-------------------------------------|
| `users/register/`                 | `POST` | Register a new user                |
| `users/login/`                    | `POST` | User login                         |
| `users/logout/`                   | `POST` | User logout                        |
| `users/profile/`                  | `GET`  | View user profile                  |
| `users/profile/update/`           | `PUT`  | Update user profile                |
| `users/profile/change-password/`  | `POST` | Change password                    |
| `users/profile/delete/`           | `DELETE` | Delete user account               |

 EACH APP has it own README file containing all the payloads to test app
Click ME : 
   [User Module README](poatan/users/READMEUSER.md)

---

### **2️⃣ Chama Management** (`cashpool` app)
This app allows users to create and manage **Chamas**, where each Chama has a unique **cash pool** and a structured hierarchy.

#### **Endpoints:**
| Endpoint                   | Method | Description                       |
|----------------------------|--------|-----------------------------------|
| `/cashpool/new/`         | `POST` | Create a new Chama               |
| `/cashpool/list/`         | `GET` | Create a new Chama               |
| `/cashpool/detail/<int:pk>/`         | `GET` | Create a new Chama               |
| `/cashpool/join/`             | `POST` | Join an existing Chama           |
| `/cashpool/<int:pk>/`         | `GET`  | Get Chama details                |
| `/cashpool/members/<int:pk>/` | `GET`  | List all Chama members & roles   |
| `/cashpool/cashpool/<int:pk>/`| `GET`  | Get Chama's current cash pool    |

EACH APP has it own README file containing all the payloads to test app
Click ME : 
   [CHAMA Module README](poatan/cashpool/READMEChama.md)

---

### **3️⃣ Contribution Management** (`contributions` app)
This app enables users to **make and track their contributions** within a Chama.

#### **Endpoints:**
| Endpoint                     | Method | Description                           |
|------------------------------|--------|---------------------------------------|
| `/contributions/new/`         | `POST` | Add a new contribution               |
| `/contributions/detail//`         | `GET` | Add a new contribution               |
| `/contributions/chama/<int:pk>/`    | `GET`  | View details of a specific contribution |
| `/contributions/confirm/{contribution_id}/`     | `PATCH` | Confirm a contribution (Admin)       |

EACH APP has it own README file containing all the payloads to test app
Click ME : 
   [Contribution Module README](poatan/contributions/READMECont.md)

---

### **4️⃣ Payout Management** (`payout` app)
This app handles the management of payouts from Chama cash pools to members.

#### **Endpoints:**
| Endpoint                     | Method | Description                           |
|------------------------------|--------|---------------------------------------|
| `/payout/`                   | `GET`  | List all payouts                     |
| `/payout/`                   | `POST` | Create a new payout request          |
| `/payout/{payout_id}/process/`      | `PATCH`| Process payout request (approve/reject)|

EACH APP has it own README file containing all the payloads to test app
Click ME : 
   [Payout Module README](poatan/payout/READMEPayout.md)

---

### **5️⃣ Transaction Management** (`transactions` app)
This app manages the ledger system, tracking all financial transactions within Chamas including deposits, withdrawals, and transfers.

#### **Endpoints:**
| Endpoint                     | Method | Description                           |
|------------------------------|--------|---------------------------------------|
| `/transactions/`             | `GET`  | List all transactions with filters   |

EACH APP has it own README file containing all the payloads to test app
Click ME : 
   [Transaction Module README](poatan/transactions/READMETrans.md)

---

## 🔧 Setup & Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/42ndLight/poatan_chama.git
   cd poatan_chama/poatan
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run the development server:
   ```sh
   python manage.py runserver
   ```

## 🔑 Future Enhancements
- **Automated Payout Management**
- **SMS & Email Notifications for Transactions**
- **Advanced Reporting Dashboard**

---
**Developed by:** *Leicht : 42ndLight* 🚀

