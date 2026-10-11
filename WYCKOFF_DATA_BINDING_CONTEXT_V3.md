# Wyckoff VNINDEX — Data Binding Context V3

## Phạm vi

Context dùng chung cho `AUDIT`, `AUDIT PORTFOLIO`, `VNI INTRA + EOD WATCH`, `RESEARCH HOSE` và `FULL PDF` trong Project `Wyckoff VNINDEX`.

## Nguồn và thứ tự đọc

- Static Canonical Baseline: OHLCV ngày/tuần và phân loại ngành trong workspace `DỮ LIỆU OHLCV`.
- Live source: `duvalivnn/wyckoff-vnindex-live-public` và các file đã được read-back từ public repository.
- Dashboard: `https://wyckoff-vnindex-market-dashboard.vietlinhvnn.chatgpt.site/`.
- Thứ tự đọc: `live_pointer.json → payload commit → live_manifest/manifest → receipts/state → alerts/intraday → history chain`.

Không hard-code commit cũ, không dùng attachment/cache cũ để thay payload hiện hành. Nếu connector không đọc được public source, trả `PUBLIC_READ_DISABLED` hoặc `PUBLIC_READ_NOT_VERIFIED` theo lỗi thực tế.

## Publication policy hiện hành

KBS được công bố theo owner-accepted risk:

- `publication_policy = PUBLISH_WITH_KBS_DATA_RISK_NO_DATA_CA_OR_INTEGRITY_GATES_V1`.
- `data_lane = KBS_PUBLISHED_WITH_RISK`.
- `certification_mode = OWNER_ACCEPTED_RISK_NO_DATA_GATES`.
- `risk_accepted = true`.

`Data Gate`, `Corporate Action/price basis gate`, `Integrity Gate` và `Market Gate` không còn là điều kiện chặn publication, Alert Engine hoặc Dashboard. Nếu các trường cũ còn trong receipt lịch sử, chỉ đọc như advisory/evidence lịch sử.

Vẫn phải kiểm tra transport lineage: đúng session/generation, manifest binding, bytes/hash và bridge/push/read-back. Không claim đã public nếu chưa có read-back từ đích.

## EOD, CA và lịch sử

- EOD là completed bar theo cutoff đã công bố.
- CA vẫn là metadata, audit evidence và tín hiệu định tuyến rebuild lịch sử; thiếu CA hoặc price-basis proof không chặn publication.
- Provider warning hoặc lỗi dữ liệu được ghi theo mã/quarantine; không chặn toàn bộ các mã độc lập.
- Static/history chain vẫn cần manifest, hash, schema và row-count để phục vụ lịch sử; lỗi một file phụ không được làm mất quyền đọc payload đã có lineage.

## Intraday và Alerts

- Intraday là `STATUS_ONLY`/provisional overlay, không thay EOD, không ghi đè Static Canonical và không tự xác nhận Event/Phase/Zone/ADD.
- `alerts_live.json` đã nhận với `alerts=[]` hoặc counter bằng 0 là snapshot hợp lệ có 0 alert.
- Alerts phải mang timestamp, source date, generation, freshness và risk policy.
- LPS/BUEC/Spring-Test/JAC-SOS và score/support/stop/T1 vẫn là `ALGO_CANDIDATE_ONLY`/scanner proxy cho đến khi Method-Locked review.

## Dashboard

Dashboard đọc payload cùng generation với manifest. Hiển thị generation, source date, snapshot time, freshness và risk policy. Khi phiên đóng, hiển thị `Thị trường đóng cửa — snapshot cuối lúc <timestamp>`. Freshness stale là advisory, không phải publication block.

## Quy tắc Wyckoff giữ nguyên

Vẫn dùng `OBSERVATION → EVIDENCE → INTERPRETATION → LABEL → STRUCTURE/PHASE → READINESS → STRATEGY`, giữ nguyên Method Authority, Operational Authority, governance, Locked Analysis và cấm dùng overlay provisional để phát hành BUY/ADD.
