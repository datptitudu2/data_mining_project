-- ==============================================================================
-- DDL THIẾT KẾ MÔ HÌNH HÌNH SAO (STAR SCHEMA) CHO HỆ THỐNG DLP & UEBA
-- Phụ trách: Trần Văn Minh (DWH Engineer)
-- Nền tảng: DuckDB / PostgreSQL
-- ==============================================================================

-- 1. BẢNG CHIỀU NGƯỜI DÙNG (Dim_User)
CREATE TABLE IF NOT EXISTS Dim_User (
    user_key VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    role_title VARCHAR,
    dept_name VARCHAR
);

-- 2. BẢNG CHIỀU PHÒNG BAN (Dim_Department)
CREATE TABLE IF NOT EXISTS Dim_Department (
    dept_key VARCHAR PRIMARY KEY,
    dept_name VARCHAR NOT NULL,
    security_tier INTEGER DEFAULT 1
);

-- 3. BẢNG CHIỀU THỜI GIAN (Dim_Time)
CREATE TABLE IF NOT EXISTS Dim_Time (
    time_key VARCHAR PRIMARY KEY,
    event_date DATE NOT NULL,
    day_of_week INTEGER,
    month INTEGER,
    is_weekend INTEGER
);

-- 4. BẢNG SỰ KIỆN TRUNG TÂM (Fact_DLP_Incident)
-- Grain: Mỗi bản ghi là tổng hợp hành vi truyền tải/truy cập của 1 người dùng trong 1 ngày
CREATE TABLE IF NOT EXISTS Fact_DLP_Incident (
    incident_id VARCHAR PRIMARY KEY,
    user_key VARCHAR,
    dept_key VARCHAR,
    time_key VARCHAR,
    logon_count INTEGER,
    after_hours_logon INTEGER,
    usb_connect_count INTEGER,
    after_hours_usb INTEGER,
    transfer_bytes BIGINT,
    is_after_hours_incident INTEGER,
    risk_score DOUBLE
);
