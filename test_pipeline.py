import unittest
import sqlite3
import os
import pandas as pd

class TestETLPipeline(unittest.TestCase):
    DB_PATH = "warehouse.db"
    REJECTED_PATH = "rejected_records.csv"

    def setUp(self):
        # Run before test cases
        self.assertTrue(os.path.exists(self.DB_PATH), "Database file warehouse.db was not found. Run etl.py first.")

    def test_database_tables_exist(self):
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        tables = [row[0] for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        conn.close()
        
        self.assertIn("sales", tables, "Table 'sales' does not exist in database.")
        self.assertIn("product_performance_summary", tables, "Table 'product_performance_summary' does not exist in database.")

    def test_zero_null_values_in_sales(self):
        conn = sqlite3.connect(self.DB_PATH)
        df = pd.read_sql("SELECT * FROM sales", conn)
        conn.close()

        self.assertEqual(df.isnull().sum().sum(), 0, "There are NULL values in the cleaned 'sales' table.")

    def test_date_format_is_iso(self):
        conn = sqlite3.connect(self.DB_PATH)
        df = pd.read_sql("SELECT date FROM sales", conn)
        conn.close()

        for date_val in df['date']:
            self.assertRegex(str(date_val), r"^\d{4}-\d{2}-\d{2}$", f"Date '{date_val}' is not in YYYY-MM-DD ISO format.")

    def test_rejection_audit_log_created(self):
        self.assertTrue(os.path.exists(self.REJECTED_PATH), "rejected_records.csv audit log is missing.")
        rejected_df = pd.read_csv(self.REJECTED_PATH)
        self.assertGreater(len(rejected_df), 0, "Audit log contains no rejected records.")
        self.assertIn("validation_status", rejected_df.columns, "Validation reason column is missing in audit log.")

    def test_gold_summary_metrics(self):
        conn = sqlite3.connect(self.DB_PATH)
        summary_df = pd.read_sql("SELECT * FROM product_performance_summary", conn)
        conn.close()

        self.assertGreater(len(summary_df), 0, "Summary table is empty.")
        self.assertTrue((summary_df['total_revenue'] > 0).all(), "Revenue numbers must be strictly positive.")

if __name__ == "__main__":
    unittest.main()
