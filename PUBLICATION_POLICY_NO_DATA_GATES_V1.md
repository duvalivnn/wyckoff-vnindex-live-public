# Publication Policy V1 — Không chặn publication bằng Data/CA/Integrity/Market Gate

Tài liệu này là amendment dùng chung cho các Thread `RESEARCH HOSE`, `AUDIT`, `AUDIT PORTFOLIO`, `VNI INTRA + EOD WATCH` và `FULL PDF`.

## Chính sách hiện hành

KBS được công bố theo owner-accepted risk:

- `publication_policy`: `PUBLISH_WITH_KBS_DATA_RISK_NO_DATA_CA_OR_INTEGRITY_GATES_V1`
- `data_lane`: `KBS_PUBLISHED_WITH_RISK`
- `certification_mode`: `OWNER_ACCEPTED_RISK_NO_DATA_GATES`
- `risk_accepted`: `true`

Các gate `Data Gate`, `Corporate Action/price basis`, `Integrity Gate` và `Market Gate` không còn là điều kiện chặn publication, Alert Engine hoặc Dashboard. Nếu receipt lịch sử còn các trường này, chỉ ghi nhận như advisory/evidence lịch sử.

## Kiểm tra tối thiểu còn giữ

Vẫn phải kiểm tra đúng generation/session, bytes/hash, manifest binding, Alerts binding, bridge/push và read-back. Không được tuyên bố GitHub/Dashboard đã cập nhật khi chưa có read-back từ đích.

## CA, EOD và Intraday

CA vẫn là metadata và tín hiệu định tuyến rebuild lịch sử; thiếu CA hoặc price-basis proof không chặn công bố. Lỗi dữ liệu được quarantine theo mã hoặc ghi provider warning.

EOD là completed bar. Intraday là `STATUS_ONLY`/provisional overlay, không thay EOD và không xác nhận Event, Phase, Zone hoặc ADD.

## Alerts và Dashboard

`alerts_live.json` đã nhận với `alerts=[]` là snapshot hợp lệ có 0 alert. Dashboard phải hiển thị snapshot time/generation/freshness/risk policy; khi đóng cửa phải ghi rõ snapshot cuối. Không dựng lại các nhãn gate cũ để chặn dữ liệu.

## Đọc public

Thread phải đọc `live_pointer.json → payload commit → manifest/receipt/OHLCV cùng payload`. Khi gặp `DisabledError`, dừng với `PUBLIC_READ_DISABLED`; không fallback sang attachment hoặc cache cũ.
