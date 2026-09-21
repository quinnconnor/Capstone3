from app.sql_validator import validate_sql
def test_safe(): assert validate_sql("SELECT 1")["valid"]
def test_drop(): assert not validate_sql("DROP TABLE x")["valid"]
def test_stacked(): assert not validate_sql("SELECT 1; DROP TABLE x;")["valid"]
def test_update(): assert not validate_sql("UPDATE x SET y=1")["valid"]
def test_comment(): assert validate_sql("SELECT * FROM x -- DROP TABLE x")["valid"]
