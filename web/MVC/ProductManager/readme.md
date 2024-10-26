# Apparel Manufacturing Management System

## Overview

The **Apparel Manufacturing Management System** is a simple ASP.NET MVC application designed to help manage apparel products, track production status, and facilitate user authentication with role-based access control. The application allows users to perform the following actions:

- Manage apparel products, including listing, adding, editing, and deleting.
- Assign products to manufacturing departments.
- Track production status.
- Implement user authentication and role-based access (Admin for product management, User for production tracking).

## Requirements

### 1. Project Setup

- Create a new ASP.NET MVC project.
- Use Entity Framework for data access and database management.
- Create a Database called test2 using SQL Server
- Run SQL Script to set Database

### 2. Models

The application consists of three primary models:

#### 2.1 Product

- **ProductID** (int, primary key)
- **Name** (string, required) (e.g., T-Shirt, Jeans, Hoodie)
- **Category** (string, required) (e.g., Top, Bottom)
- **Quantity** (int, required)
- **DepartmentID** (int, foreign key to Department, nullable)
- **ProductionStatus** (enum: Pending, InProgress, Completed)
- **CreatedDate** (DateTime)

#### 2.2 Department

- **DepartmentID** (int, primary key)
- **DepartmentName** (string, required) (e.g., Cutting, Sewing, Pressing)

#### 2.3 User (for authentication)

- **UserID** (int, primary key)
- **Username** (string, required)
- **PasswordHash** (string, required)
- **Role** (enum: Admin, User)

## Functionality

### 3.1 Product Management (Admin Role)

- **List Products**: Display a list of products in the system with sorting and filtering options by Category, ProductionStatus, and Department.
- **Add Product**: Create a form to add new apparel products.
- **Edit Product**: Create a form to edit existing products, allowing the admin to assign or update the production department and change the ProductionStatus.
- **Delete Product**: Provide an option to delete products, including a confirmation prompt.

### 3.2 Production Tracking (User Role)

- **View Products**: Users can only view products assigned to their department and can update the production status (e.g., mark as InProgress or Completed).

### 3.3 User Authentication

- Implement a simple user authentication system:
  - Admin users can manage products and departments.
  - User-level accounts can only view and update products in their assigned department.

### 3.4 Department Management (Admin Role)

- Admins can create and manage departments.

## Getting Started

To get started with the Apparel Manufacturing Management System, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
