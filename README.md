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

### **1️⃣ User Authentication & Profile Management** (`auth` app)
This app handles user registration, authentication, and profile management.

#### **Endpoints:**
| Endpoint                     | Method | Description                         |
|------------------------------|--------|-------------------------------------|
| `/register/`                 | `POST` | Register a new user                |
| `/login/`                    | `POST` | User login                         |
| `/logout/`                   | `POST` | User logout                        |
| `/profile/`                  | `GET`  | View user profile                  |
| `/profile/update/`           | `PUT`  | Update user profile                |
| `/profile/change-password/`  | `POST` | Change password                    |
| `/profile/delete/`           | `DELETE` | Delete user account               |

---

### **2️⃣ Chama Management** (`chama` app)
This app allows users to create and manage **Chamas**, where each Chama has a unique **cash pool** and a structured hierarchy.

#### **Endpoints:**
| Endpoint                   | Method | Description                       |
|----------------------------|--------|-----------------------------------|
| `/chama/register/`         | `POST` | Create a new Chama               |
| `/chama/join/`             | `POST` | Join an existing Chama           |
| `/chama/<int:pk>/`         | `GET`  | Get Chama details                |
| `/chama/<int:pk>/members/` | `GET`  | List all Chama members & roles   |
| `/chama/<int:pk>/cashpool/`| `GET`  | Get Chama's current cash pool    |

---

### **3️⃣ Contribution Management** (`contributions` app)
This app enables users to **make and track their contributions** within a Chama.

#### **Endpoints:**
| Endpoint                     | Method | Description                           |
|------------------------------|--------|---------------------------------------|
| `/contribution/add/`         | `POST` | Add a new contribution               |
| `/contribution/<int:pk>/`    | `GET`  | View details of a specific contribution |
| `/contribution/list/`        | `GET`  | List all contributions in a Chama    |
| `/contribution/confirm/`     | `POST` | Confirm a contribution (Admin)       |

---

### **4️⃣ Cash Pool Management** (`cashpool` app)
Handles the **financial transactions and cash pool tracking** for each Chama.

#### **Endpoints:**
| Endpoint                     | Method | Description                           |
|------------------------------|--------|---------------------------------------|
| `/cashpool/<int:pk>/`        | `GET`  | View cash pool balance               |
| `/cashpool/update/`          | `POST` | Update cash pool balance (Admin)    |

---

## 🚀 Latest Advancements
1. **User Authentication & Profile Management** - Added full CRUD operations for user profiles.
2. **Chama Hierarchy Implementation** - Defined `Chairman`, `Treasurer`, and `Contributor` roles.
3. **Contribution Confirmation System** - Only authorized users (Treasurer/Chairman) can confirm contributions.
4. **Cash Pool Management** - Introduced automatic cash pool updates after transactions.
5. **Enhanced API Security** - Ensured only Chama members can view and interact with their group.

## 🔧 Setup & Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/42ndLight/poatan_chama.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```sh
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

