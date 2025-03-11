# **Europeana-DB**

Europeana-DB is a dataset designed for **AI research and development**, focusing
on **image captioning and cultural heritage object (CHO) analysis**. The dataset
includes a collection of objects metadata sourced from the **Europeana API**.

## **🚀 Key Features**

- **CHO Coverage**: The dataset includes all types of
  **cultural heritage objects** tagged with open and media on the  
  Europeana Database.
- **Image Captioning**: Designed to generate to be a base for **training
  AI models**.
- **Automated Data Pipeline**: Fully automated **data retrieval, processing,  
  and storage**.
- **Customizable Filters**: Configure included/excluded categories via  
  **`constants.py`**.
- **Dockerized Execution**: Run the pipeline **inside a container** with  
  **MongoDB integration**.
- **Persistent Storage**: **Data is stored locally** using **Docker volumes**.

---

## **📁 Project Structure**

```text
europena_db
├── europeana_crawler
│   ├── config
│   ├── europeana
│   ├── helpers
│   ├── main.py
│   ├── notebooks
│   └── tests
├── Dockerfile
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## **⚡ Quick Start Guide**

### **1️⃣ Run the Pipeline with Docker**

> **This method runs the full pipeline inside a container with MongoDB support.**

#### **🚀 Step 1: Build and Start Containers**

```sh
docker-compose up -d --build
```

This will:

- Build and start **MongoDB** (`europeana-mongo`).
- Build and start **Europeana Crawler** (`europeanadb_vagner`).
- Automatically begin downloading **cultural heritage objects**.

#### **🔍 Step 2: Monitor the Logs**

```sh
docker logs -f europeanadb
```

This will **stream logs** to monitor the downloading and database insertion  
process.

#### **Step 3: Stop the Containers**

```sh
docker-compose down
```

This will **stop all containers** but **keep downloaded data**.

---

## **🛠️ Manual Installation (Without Docker)**

> **If you prefer to run without Docker, follow these steps:**

### **1️⃣ Install Poetry**

Ensure **Poetry** is installed:

```sh
pip install poetry
```

### **2️⃣ Install Dependencies**

Navigate to the **project directory**:

```sh
cd europeanadb
poetry install
```

### **3️⃣ Activate the Virtual Environment**

```sh
poetry shell
```

---

## **Running the Data Crawler**

Run the **Europeana Dataset Downloader** manually:

```sh
python main.py --limit 50
```

### **🛠 Options**

| Flag          | Description                                           |
| ------------- | ----------------------------------------------------- |
| `--limit [N]` | Limits the number of items to download (default: 10). |
| `--all`       | Downloads all available items.                        |

### **📝 Example**

```sh
python main.py --limit 100
```

> This downloads **100 items** from the **Europeana API** and stores metadata  
> in the `data/` directory.

---

## **🗄️ MongoDB Integration**

**If running manually (without Docker), ensure MongoDB is running:**

```sh
sudo systemctl start mongod
```

Or start via Docker:

```sh
docker run -d --name europeana-mongo -p 27017:27017 mongo:latest
```

---

## **📊 Database and Local Storage**

> **Track the number of items in MongoDB and locally.**

Every batch update prints:

```
MongoDB total: 5200 items | Local total: 5200 items
```

To **manually check MongoDB:**

```sh
docker exec -it europeana-mongo mongosh
use europeana_db
db.cultural_objects.countDocuments({})
```

---

## **Cleaning Up Data**

> **If you need to delete local files and reset MongoDB:**

### **🗑️ Clear Local Data**

```sh
rm -rf europeanadb/data/
```

### **🗑️ Delete MongoDB Data**

```sh
docker-compose down -v
```

> This **removes MongoDB volumes** and deletes **all stored documents**.

---

## **Future Plans**

- **Optimize MongoDB indexing** for faster searches.

---

## **📜 License**

Europeana-DB is released under the **MIT License**.
