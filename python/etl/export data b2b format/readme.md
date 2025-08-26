# PRIME4 → VISA Concur Integration  

This project contains an **Apache Airflow DAG** that automates the process of extracting transaction data from PRIME4, formatting it, encrypting it using PGP, and securely transferring it to VISA Concur via SFTP.  

The pipeline ensures compliance with VISA Concur requirements and provides a reproducible, auditable process for B2B transaction exchange.  

---

## 📋 Features  

- **SQL Extraction**: Executes a SQL query on PRIME4 to fetch allowed credit card transactions.  
- **Data Export**: Writes the result set into a text file with a pipe (`|`) delimiter.  
- **File Naming Convention**: Files follow the format:  
B2B_123456_TRANSACTIONS_YYYYMMDD.txt
- **PGP Encryption**: Encrypts the exported file with a public key provided by VISA Concur.  
- **Secure File Transfer**: Uploads the encrypted file to VISA Concur’s SFTP endpoint.  
- **Error Handling**: Fails safely if query results are empty or if encryption/upload steps fail.  
- **Modular Tasks**: Airflow DAG splits the workflow into three tasks:  
1. Export transactions  
2. Encrypt file with PGP  
3. Transfer file via SFTP  

---

## ⚙️ Requirements  

### System  
- Python 3.9+  
- Apache Airflow 2.6+  
- GnuPG (`gpg`) installed in the Airflow environment  

### Airflow Dependencies  
The DAG uses the following Airflow providers:  
- `apache-airflow-providers-sftp`  

Install with:  
```bash
pip install apache-airflow-providers-sftp
pip install cx_Oracle
```
---

## 🔑 Configuration

This DAG relies on **Airflow Variables and Connections** for configuration.

### Airflow Variables

| Variable Name             | Description                                                                | Example Value                         |
| ------------------------- | -------------------------------------------------------------------------- | ------------------------------------- |
| `B2B_OUTPUT_DIR`          | Local directory where intermediate/export files will be written            | `/opt/airflow/output`                 |
| `B2B_CUSTOM_FILE_PREFIX`  | Prefix used in generated filenames                                         | `B2B_123456_TRANSACTIONS`             |
| `B2B_PGP_PUBLIC_KEY_PATH` | Path to the VISA Concur-provided PGP public key                            | `/opt/airflow/keys/concur_pubkey.asc` |
| `B2B_PGP_RECIPIENT`       | Key identifier (email, fingerprint, or key ID) for the PGP encryption      | `concur-key@example.com`              |
| `B2B_SFTP_CONN_ID`        | Airflow Connection ID for the SFTP target                                  | `sftp_b2b`                            |
| `B2B_SFTP_REMOTE_DIR`     | Remote directory on SFTP server where encrypted files should be placed     | `/incoming/b2b`                       |
| `B2B_DELETE_PLAINTEXT`    | Whether to delete the unencrypted file after PGP encryption (`true/false`) | `true`                                |

### Airflow Connection

- Create a connection in Airflow UI (Admin > Connections):
1. Conn Id: sftp_b2b (or match your B2B_SFTP_CONN_ID variable)
2. Conn Type: SFTP
3. Login: Username provided by VISA Concur
4. Password / Key file: Authentication details (password or private key)

### DAG Structure

export_transactions_dag
│
├── export_transactions  # Run SQL query & write TXT file
│
├── pgp_encrypt_file     # Encrypt TXT file using GPG public key
│
└── sftp_upload_encrypted # Upload encrypted .gpg file via SFTP


---

## 📑 Output File

- **Plaintext file (.txt)**: Main.Primary files for validations
- **Encrypted file (.gpg)**: Encrypted file to be transfered. Named consistently with plaintext, but with .gpg suffix
B2B_123456_TRANSACTIONS_20250826.txt.gpg

---

## 🧩 Customization

- **Schedule**: Modify the DAG schedule_interval (default: @daily) to match your delivery requirements.
- **Retention**: Adjust B2B_DELETE_PLAINTEXT if you need to retain unencrypted copies for audit.
- **Query**: Update the SQL query in the DAG if VISA Concur changes data requirements.

---

## 🛡 Security Considerations

- Never commit private keys or plaintext files to version control.
- Ensure file permissions are restrictive in the Airflow environment.
- Use Airflow Connections for storing SFTP credentials securely (not in plain code).
- Enable logging redaction for sensitive variables.

---

## 📖 License

This project is provided as an example integration. Adapt and secure it according to your organization’s policies.
