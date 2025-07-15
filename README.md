# Airport Database System

This project simulates the core flight scheduling and data management operations of a modern airport, using a relational database and a Python-based graphical user interface. It was developed as part of a university course on database systems.

## Features

- Models flight departures and arrivals of the LAX airport
- Stores data for airlines, aircrafts, flights, gates, and check-in counters
- Supports scheduled and real flight tracking
- Implements user interaction via a GUI using PyQt5
- Provides CRUD functionality (Create, Read, Update, Delete)
- Includes analytics and SQL queries for statistics (e.g., delays, flight trends)
  
## Technologies Used

- **SQLite** – database backend
- **SQL** – for table creation and complex queries
- **Python** – data generation and interface logic
- **PyQt5** – GUI development
- **CSV** – import of real-world aviation data

## Entity-Relationship Design

The database design is based on real-world entities such as:
- `Airlines`
- `Aircraft`
- `Scheduled Flights`
- `Actual Flights`
- `Airports`, `Gates`, and `Check-in Counters`

A complete ER diagram and logical model were designed and implemented.


## Statistical Analysis

The system supports:
- Popular destination analysis (e.g. top 3 cities in 2021)
- Flight volume per month for 2020 & 2021
- Average delays per year
- Airline with most scheduled flights
- Visualization of results using Matplotlib

## Sample Queries

```sql
-- Average delay by year
SELECT AVG(delay) FROM flight WHERE year = 2021;

-- Most popular destinations
SELECT destination_city, COUNT(*) FROM flight GROUP BY destination_city ORDER BY COUNT(*) DESC LIMIT 3;
```

## Built By
Vasiliki Karagiannidi 

Aliki Panou

Developed as part of the Database course (year 2022) at University of Patras – Electrical & Computer Engineering

## Requirements
Python 3.5+

PyQt5: pip install PyQt5

SQLite or DB Browser for SQLite

Note: This repo includes the core controller logic. Some auxiliary UI modules were part of the original project but are not included here for brevity.
