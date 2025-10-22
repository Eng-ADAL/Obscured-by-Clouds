# Obscured-by-Cloud (OBC)


<img src="obc_banner.png" alt="Project Banner" width="500" />

<br>

**Obscured-by-Cloud (OBC)** is a modular ETL pipeline project designed to handle data transformation securely and transparently, revealing what’s *obscured by the cloud*.  
This first phase focuses on the **local data pipeline**, establishing clean, reproducible processes before extending to cloud infrastructure.

<br>


## 🌍 Project Overview

OBC is a two-phase ETL system:

1. **Local ETL Pipeline (Current Phase)**  
   - Extracts raw transaction data from local sources.  
   - Hashes and anonymises personally identifiable information (PII).  
   - Cleans and transforms data into a **3NF database structure** (Transactions, Basket Items, etc.).  
   - Loads processed data into a local database for validation and testing.

2. **Cloud Integration (Next Phase)**  
   - Data synchronisation with **Cloud** for automated ingestion.  
   - Scalable orchestration for distributed processing.  
   - Secure access control and monitoring via cloud-native tools.


## 🧩 Local Architecture

```text
raw_data/
   ↓
extract.py
   ↓  (hash PII using salted hash)
clean_transform.py
   ↓
save_cleaned.csv
   ↓
load_to_db.py
   ↓
local_database/
````


## 🧠 Design Principles

* **Privacy-first**: Hash and drop PII fields immediately after extraction.
* **Transparency**: Each ETL step logged locally for audit and debugging.
* **Modularity**: Each stage (extract, transform, load) runs independently or in sequence.
* **Reproducibility**: Deterministic transformations and testable outputs.


## 📅 Roadmap

* [ ] Local ETL pipeline
* [ ] Unit testing for each ETL component
* [ ] Cloud ETL orchestration
* [ ] Logging and monitoring system
* [ ] Documentation and CLI interface


## 🧭 Vision

OBC aims to bridge **local data reliability** with **cloud-scale automation** — a pipeline that evolves from your laptop to the stratosphere. Every dataset has its hidden truths; OBC is about revealing them responsibly.

<br>

---

"Data, much like a symphony, reveals its true form only when the chaos is silenced and each note is precisely orchestrated."