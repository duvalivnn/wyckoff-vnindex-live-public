# RESEARCH HOSE — Public Authority Binding 2026-10-11

## Authority

Đọc động từ `live_pointer.json` rồi resolve payload commit. Không dùng các commit ghi cứng trong tài liệu cũ. Sau đó đọc manifest, EOD receipt, Alerts, Intraday, daily/weekly bridge và history chain cùng payload lineage.

## Chính sách hiện hành

- `publication_policy`: `PUBLISH_WITH_KBS_DATA_RISK_NO_DATA_CA_OR_INTEGRITY_GATES_V1`
- `data_lane`: `KBS_PUBLISHED_WITH_RISK`
- `certification_mode`: `OWNER_ACCEPTED_RISK_NO_DATA_GATES`
- `risk_accepted`: `true`

Không có Data Gate, Corporate Action/price basis gate, Integrity Gate hoặc Market Gate nào được dùng để chặn việc đọc/public payload. CA/basis/freshness/quarantine chỉ là metadata rủi ro và phải được ghi riêng.

## Consumer rule

1. Đọc `live_pointer.json`.
2. Resolve payload commit từ pointer.
3. Đọc manifest/receipt/OHLCV/Alerts/Intraday từ cùng generation.
4. Dùng `history_chain_manifest.json` và chain chunks cho full weekly history; `weekly_replace.csv` chỉ là compatibility view.
5. Intraday là `STATUS_ONLY`/provisional; không thay completed EOD hoặc dùng để xác nhận Event/Phase/Zone/ADD.
6. Nếu body CSV lớn rỗng nhưng chain manifest/hash/schema/row count đã PASS, ghi `READER_SIZE_OR_BODY_EMPTY` và dùng chain đã materialize.
7. Nếu public read bị tắt, trả `PUBLIC_READ_DISABLED`; không fallback sang attachment cũ.

## Readiness

`RESEARCH HOSE` có thể phân tích dữ liệu đã đọc được với nhãn `PUBLISHED_WITH_RISK`. Không được tuyên bố dữ liệu “đã được chứng minh đúng tuyệt đối” chỉ vì owner chấp nhận rủi ro. Mọi nhận định phải ghi cutoff, source date, generation, timestamp, manifest/hash và caveat phù hợp.
