# WYCKOFF VNINDEX — Shared Public Authority Binding 2026-10-11

Áp dụng cho `RESEARCH HOSE`, `AUDIT`, `AUDIT PORTFOLIO`, `VNI INTRA + EOD WATCH`, `FULL PDF` và các Thread phân tích trong Project.

## Authority resolution

1. Đọc `live_pointer.json` trước.
2. Lấy payload commit từ nội dung pointer; không hard-code commit cũ.
3. Đọc `manifest.json`, `live_manifest.json`, receipts/state, `alerts_live.json`, `intraday_manifest.json` và OHLCV từ cùng payload lineage.
4. Full weekly history dùng `history_chain_manifest.json` và chain chunks; `weekly_replace.csv` là compatibility view khi có binding tương ứng.

## Publication contract V3

KBS hiện dùng `PUBLISH_WITH_KBS_DATA_RISK_NO_DATA_CA_OR_INTEGRITY_GATES_V1`. `Data Gate`, CA/price basis gate, Integrity Gate và Market Gate không còn chặn publication, Alert Engine hoặc Dashboard. Các trường còn trong evidence cũ chỉ là advisory/risk metadata.

Các kiểm tra còn bắt buộc là session/generation binding, manifest/bytes/hash, Alerts binding và bridge/push/read-back. Không đọc được public source thì trả `PUBLIC_READ_DISABLED` hoặc `PUBLIC_READ_NOT_VERIFIED`; không fallback sang attachment/cache cũ.

## Consumer contract

- Completed EOD/canonical cutoff lấy từ EOD receipt mới nhất đã public.
- Intraday là `STATUS_ONLY`/provisional overlay, không thay completed EOD/weekly bar và không tự xác nhận Event, Phase, Zone hoặc ADD.
- CA, price basis, freshness, quarantine và provider warnings được báo riêng, không dùng để chặn toàn bộ payload.
- `alerts=[]`/counter 0 sau khi snapshot đọc thành công là snapshot hợp lệ; không hiển thị `Chưa có snapshot`.
- Khi thị trường đóng cửa, Dashboard hiển thị thời điểm snapshot cuối; freshness stale là `STALE_ADVISORY`.

## Local staging note

Gói Project Sources là bản staging cục bộ. Không coi việc cập nhật file trong gói là GitHub push hoặc Dashboard deployment; hai việc đó chỉ được xác nhận sau read-back ở đích.
