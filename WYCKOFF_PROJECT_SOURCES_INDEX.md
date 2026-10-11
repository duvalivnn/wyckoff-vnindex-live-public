# Wyckoff VNINDEX — Project Sources Index

Ngày rà soát: 2026-10-11  
Phạm vi: `AUDIT`, `AUDIT PORTFOLIO`, `VNI INTRA + EOD WATCH`, `RESEARCH HOSE`, `FULL PDF`.

## 1. Tài liệu điều hành hiện hành

1. `PROJECT_INSTRUCTIONS_V3_NO_DATA_GATES_2026-10-11.md` — bản đề xuất Project Instructions mới.
2. `01_CONTEXT/PUBLICATION_POLICY_NO_DATA_GATES_V1.md` — amendment áp dụng trong gói Project Sources.
3. `01_CONTEXT/THREAD_CHUNK_READ_COMMAND_V1.md` — câu lệnh bắt buộc đọc authority và history chunks trước Method-Locked audit.
4. `WYCKOFF_DATA_BINDING_CONTEXT_V3.md` — hợp đồng đọc dữ liệu và lineage.
5. `runtime/architecture/SYSTEM_ARCHITECTURE_MODERN_V1.md` — sơ đồ runtime và file mapping.

## 2. Chính sách nguồn

KBS được đưa vào public lane với owner-accepted risk. Các gate `Data Gate`, `Corporate Action/price basis`, `Integrity Gate` và `Market Gate` không chặn publication. Chúng không được tái tạo trong Thread, Alert Engine hoặc Dashboard từ receipt cũ.

Kiểm tra bắt buộc còn lại là transport/provenance: pointer/payload, session, generation, manifest, bytes/hash, Alert binding và read-back. Chưa read-back thì không claim GitHub/Dashboard đã cập nhật.

## 3. Active Project Sources

### Static/history

- `02_STATIC_CANONICAL/stock_weekly_ohlcv.csv`
- `02_STATIC_CANONICAL/universe.csv`
- `02_STATIC_CANONICAL/vn30_constituents.csv`
- `02_STATIC_CANONICAL/vci_industries_icb.json`
- `02_STATIC_CANONICAL/validation_report.json`
- `05_HISTORY_CHAIN/history_chain_manifest.json`
- `05_HISTORY_CHAIN/stock_weekly_ohlcv_chain.csv`
- `06_THREAD_READER_CHUNKS/` khi Thread cần đọc chunk theo mã/ngày/tuần.

### Live/public

- `03_PUBLIC_WEEKLY/live_pointer.json`
- `03_PUBLIC_WEEKLY/live_manifest.json`
- `03_PUBLIC_WEEKLY/manifest.json`
- `03_PUBLIC_WEEKLY/current_state.json`
- `03_PUBLIC_WEEKLY/publisher_state.json`
- `03_PUBLIC_WEEKLY/eod_receipt.json`
- `03_PUBLIC_WEEKLY/intraday_manifest.json`
- `03_PUBLIC_WEEKLY/intraday_latest.csv`
- `03_PUBLIC_WEEKLY/alerts_live.json`
- `03_PUBLIC_WEEKLY/daily_bridge.csv`, `index_daily_bridge.csv`, `market_scan.csv`, `sector_scan.csv`, `weekly_replace.csv`.

### Advisory/evidence

`ca_receipt.json`, provider warnings, quarantine, freshness, risk policy và receipt lịch sử được giữ để audit. Chúng không được dùng làm publication gate.

## 4. Hợp đồng cho các Thread

- `RESEARCH HOSE`: dùng static/history chain cho lịch sử; dùng live payload khi cần current; Intraday không thay EOD.
- `AUDIT` và `AUDIT PORTFOLIO`: kiểm tra lineage, generation, hash và risk metadata; không dừng vì gate cũ.
- `VNI INTRA + EOD WATCH`: dùng EOD cho completed bar và Intraday cho overlay provisional/status-only.
- `FULL PDF`: trích dẫn cutoff, source date, generation, timestamp, manifest/hash và risk policy.

`alerts=[]` hoặc counter 0 sau khi payload đọc thành công là trạng thái hợp lệ “đã nhận snapshot — 0 alerts”.

## 5. File cũ

Các bản payload cũ, V2, CA addendum cũ, evidence có `Market Gate FAIL` hoặc `hard_integrity` được giữ trong archive để truy vết, nhưng không đưa vào active source set và không được chọn thay cho file trong generation hiện hành.
