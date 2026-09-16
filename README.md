# Multi-Channel E-Commerce Data Pipeline & Reconciliation Engine

### 🔍 Overview
An automated Python-based data architecture pipeline built to extract, transform, and reconcile fragmented, multi-channel financial data exports. This system ingests separate transaction data streams from discrete digital marketplaces (such as eBay and Poshmark) and standardizes them into a centralized, clean operational ledger.

Developed by a **Mathematics & Computer Information Systems (CIS)** graduate to solve real-world multi-channel retail infrastructure friction.

---

### 💡 The Business Problem Solved
Operating across multiple consumer-facing digital storefronts requires tracking disparate platform fee structures, varying shipping mechanics, and inconsistent column naming schemas. Manual reconciliation in traditional spreadsheets introduces massive human error and data duplicates. 

This engine replaces manual sorting by executing a programmatic pipeline that enforces:
1. **Strict Data Hygiene:** Deduplicates data across platforms and standardizes transaction columns.
2. **Financial Auditing:** Mathematically reconciles platform transaction fees and gross merchandise value (GMV) to calculate true net revenue.
3. **Operational Visibility:** Automatically flags transactional anomalies (such as negative-margin listings or shipping overages) for immediate business review.

---

### 🛠️ Tech Stack & Key Frameworks
* **Language:** Python
* **Data Manipulation & Processing:** `pandas` (DataFrames, vectorization, and data merging structures)
* **File Processing Frameworks:** `openpyxl` (Automated engine for direct Excel spreadsheet interface)

---

### 📊 How It Works (The ETL Pipeline)
1. **Ingest (Extract):** The script reads raw `.xlsx` or `.csv` transaction reports exported from active storefronts.
2. **Transform (Clean):** Mismatched columns (e.g., eBay's `Total Paid By Buyer` vs Poshmark's `Order_Price`) are mapped to unified schemas.
3. **Load (Consolidate):** A consolidated master ledger is compiled and automatically exported into a production-ready spreadsheet.
