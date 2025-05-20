import sqlite3

db_path = 'DB.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

create_view_sql = """
CREATE VIEW PLAN AS
SELECT
  *,
  datetime(
    substr(ar_time, 1, 4) || '-' ||
    substr(ar_time, 5, 2) || '-' ||
    substr(ar_time, 7, 2) || ' ' ||
    substr(ar_time, 9, 2) || ':' ||
    substr(ar_time, 11, 2)
  ) AS parsed_datetime
FROM plan_schedule;
"""

cursor.execute(create_view_sql)
conn.commit()
conn.close()

print("View успешно создан.")
