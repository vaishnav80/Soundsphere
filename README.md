# SoundSphere

**SoundSphere** is a full-featured e-commerce web application designed for selling earphones. Built with **Django**, it provides a seamless shopping experience with secure authentication, online payments, and profile management.

## 🚀 Features

### **Core E-commerce Features**
- 🛍 **Product Listing & Categories** – Browse and filter earphones by brand, type, and price.
- 🛒 **Shopping Cart** – Add/remove items and update quantities.
- 💳 **Checkout & Payments** – Secure payment processing via **Razorpay**.
- 📦 **Order Management** – Track order status from placement to delivery.
- 🎫 **Coupons & Discounts** – Apply promotional offers for savings.
- 📄 **Invoice Generation** – Download invoices in PDF format.

### **Authentication & User Management**
- 🔐 **Google Authentication** – One-click sign-in via Google.
- 📧 **Email-based Login** – Login using email (no username required).
- 👤 **Profile Management** – Update personal details and address.

### **Shipping & Delivery**
- 🚚 **Postcode-based Delivery Charge** – Delivery charges are dynamically calculated based on the shipping location.
- 📌 **Address Management** – Save multiple delivery addresses.

### **Admin Dashboard**
- 📊 **Sales Reports** – View detailed reports with filtering options.
- 📦 **Product Management** – Add, edit, and delete products.
- 🛒 **Order Processing** – Manage orders and update status.
- 🏷 **Offer Management** – Create and manage product-specific offers.

## 🛠️ Tech Stack
- **Backend:** Django, PostgreSQL
- **Frontend:** Bootstrap, JavaScript, jQuery
- **Database:** PostgreSQL
- **Authentication:** Django Allauth (Google Login)
- **Payments:** Razorpay
- **Deployment:** AWS, Nginx, Gunicorn

## 🚀 Installation Guide

### **1️⃣ Clone the Repository**
```sh
$ git clone https://github.com/vaishnav80/Soundsphere.git
$ cd soundsphere
```

### **2️⃣ Create Virtual Environment & Install Dependencies**
```sh
$ python -m venv venv
$ source venv/bin/activate   # On Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```

### **3️⃣ Set Up Database**
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### **4️⃣ Run the Development Server**
```sh
$ python manage.py runserver
```
Open `http://127.0.0.1:8000/` in your browser.

## 📜 License
This project is open-source and available under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

⚡ **SoundSphere – Your Ultimate Destination for Earphones!** 🎧

