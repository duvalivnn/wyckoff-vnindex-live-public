# Gói Project Sources — Publication Policy V1

## Mục đích

Gói này là bản staging cục bộ để cập nhật Project Sources của `Wyckoff VNINDEX`. Nó phù hợp với runtime hiện hành sau khi bỏ các publication gate `Data Gate`, `Corporate Action/price basis`, `Integrity Gate` và `Market Gate`.

## Tài liệu cần đưa vào active Project Sources

1. `01_CONTEXT/PUBLICATION_POLICY_NO_DATA_GATES_V1.md`
2. `01_CONTEXT/THREAD_PUBLIC_AUTHORITY_BINDING_2026-10-11.md`
3. `01_CONTEXT/RESEARCH_HOSE_PUBLIC_AUTHORITY_2026-10-11.md`
4. `02_STATIC_CANONICAL/validation_report.json`
5. `03_PUBLIC_WEEKLY/live_pointer.json`
6. `03_PUBLIC_WEEKLY/live_manifest.json`
7. `03_PUBLIC_WEEKLY/manifest.json`
8. `03_PUBLIC_WEEKLY/current_state.json`
9. `03_PUBLIC_WEEKLY/publisher_state.json`
10. `03_PUBLIC_WEEKLY/eod_receipt.json`
11. `03_PUBLIC_WEEKLY/intraday_manifest.json`
12. `03_PUBLIC_WEEKLY/intraday_latest.csv`
13. `03_PUBLIC_WEEKLY/alerts_live.json`
14. `03_PUBLIC_WEEKLY/daily_bridge.csv`, `index_daily_bridge.csv`, `market_scan.csv`, `sector_scan.csv`, `weekly_replace.csv`
15. `03_PUBLIC_WEEKLY/kbs_public_acceptance_policy_v1.json`
16. `SOURCE_MANIFEST.json`

`authority_receipt.json` là file bắt buộc của payload public theo Thread Chunk Read Command. Bản staging hiện tại chưa có receipt hiện hành cùng payload; không được đưa receipt trong `04_EVIDENCE/LEGACY_PUBLIC_AUTHORITY_2026-10-11/` vào active set để lấp thiếu.

Các static canonical và history-chain files vẫn dùng theo danh sách trong `WYCKOFF_PROJECT_SOURCES_INDEX.md`.

## Chính sách đọc

Thread phải đọc `live_pointer.json → payload commit → manifest/receipt/OHLCV cùng generation`. Khi public read bị tắt, trả `PUBLIC_READ_DISABLED`; không fallback sang attachment hoặc cache cũ.

## Trạng thái đồng bộ

- Pointer local staging: `3dd289534ae1c036af2c308e0b0418042ba85325`.
- Publisher generation: `r33-2026-10-09-93b1903d50602387`.
- Policy: `PUBLISH_WITH_KBS_DATA_RISK_NO_DATA_CA_OR_INTEGRITY_GATES_V1`.
- Authority: `LOCAL_STAGING_NOT_REMOTE_VERIFIED`.
- Đây là cập nhật file cục bộ; chưa tự động upload vào ChatGPT Project Sources, chưa GitHub push và chưa Dashboard deploy. Chỉ xác nhận các việc đó sau read-back từ đích.

## Legacy

`04_EVIDENCE/LEGACY_PUBLIC_AUTHORITY_2026-10-11/` chứa authority snapshot cũ có gate lịch sử. Không đưa thư mục này vào active Project Sources.
