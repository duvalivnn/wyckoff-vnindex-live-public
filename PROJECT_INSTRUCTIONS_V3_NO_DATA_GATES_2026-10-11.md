# WYCKOFF VNINDEX — PROJECT INSTRUCTIONS V3

**Trạng thái:** Bản đề xuất cập nhật để thay thế phần data-publication của V2 sau khi người dùng phê duyệt trong Project Settings.
**Ngày:** 2026-10-11
**Phạm vi:** Data lineage, GitHub snapshot, EOD, Intraday overlay, Corporate Action, Realtime Wyckoff Alerts, Dashboard và các Thread trong Project `Wyckoff VNINDEX`.

## 1. Phạm vi thay đổi

Toàn bộ Method Authority, Operational Authority, Wyckoff rules, governance, quy tắc Method-Locked review, Locked Analysis, phân biệt Structure/Readiness/Buy Quality/Risk và các quy tắc chống look-ahead/leakage vẫn giữ nguyên.

Bản V3 chỉ thay đổi chính sách công bố dữ liệu:

- Không dùng `Data Gate` để chặn publication.
- Không dùng `Corporate Action/price basis gate` để chặn publication.
- Không dùng `Integrity Gate` để chặn publication.
- Không dùng `Market Gate` để chặn publication.

Các thông tin trên, nếu còn xuất hiện trong receipt lịch sử, chỉ được đọc như **advisory/risk metadata**. Không được diễn giải chúng thành lỗi truy cập, lý do huỷ publication hoặc lý do loại bỏ toàn bộ snapshot.

## 2. Chính sách dữ liệu KBS và publication

KBS được chấp nhận theo chính sách owner-accepted risk:

```text
publication_policy = PUBLISH_WITH_KBS_DATA_RISK_NO_DATA_CA_OR_INTEGRITY_GATES_V1
data_lane = KBS_PUBLISHED_WITH_RISK
certification_mode = OWNER_ACCEPTED_RISK_NO_DATA_GATES
risk_accepted = true
eligible_scope = ALL_KBS_SYMBOLS
```

`risk_accepted=true` là quyết định chấp nhận rủi ro công bố, không phải tuyên bố rằng dữ liệu đã được chứng minh đúng tuyệt đối. Mỗi snapshot vẫn phải giữ provider, thời điểm, hash, generation, session và cảnh báo/quarantine để người đọc đánh giá rủi ro.

Publication chỉ yêu cầu các kiểm tra vận chuyển và lineage tối thiểu:

1. Đúng run/session và đúng `publisher_generation_id`.
2. Manifest, receipt, payload và Alerts đọc được và có hash/bytes tương ứng.
3. `live_manifest.json`, `publisher_state.json`, `current_state.json` và `alerts_live.json` cùng generation hoặc có binding receipt giải thích rõ quan hệ.
4. Bridge/push và read-back phải được ghi nhận. Không claim đã public GitHub hoặc Dashboard nếu chưa có read-back từ đích.

Không yêu cầu CA receipt, price-basis proof, hard-integrity certification hoặc market-open verdict để cho phép publication.

## 3. Authority và thứ tự đọc của Thread

Khi đọc dữ liệu public, luôn thực hiện theo thứ tự:

```text
main/live_pointer.json
→ payload commit được pointer trỏ tới
→ live_manifest.json / manifest.json
→ eod_receipt.json / current_state.json / publisher_state.json
→ alerts_live.json / intraday_manifest.json / intraday_latest.csv
→ history_chain_manifest.json và các chain chunks khi cần lịch sử
```

Không hard-code commit cũ và không dùng attachment cũ để thay cho payload hiện hành. Nếu public read bị tắt hoặc payload không đọc được, trả `PUBLIC_READ_DISABLED` hoặc `PUBLIC_READ_NOT_VERIFIED` theo lỗi thực tế; không gọi đó là Data Integrity FAIL và không tự tạo payload thay thế.

## 4. EOD, Static Canonical và CA

- EOD là completed bar theo cutoff đã công bố.
- EOD được append/rebuild và công bố theo run receipt; lỗi của một mã được ghi trong quarantine hoặc provider warning, không chặn các mã độc lập.
- Corporate Action vẫn được thu nhận làm thông tin lineage, audit và định tuyến rebuild lịch sử khi có dữ liệu; CA không còn là publication gate.
- Price basis vẫn có thể được ghi lại như metadata nguồn; thiếu price-basis proof không chặn snapshot.
- Hard-integrity findings vẫn có thể xuất hiện trong evidence lịch sử; chúng là cảnh báo, không phải điều kiện fail-closed của publication.
- `weekly_replace.csv`, history chain và static files phải có manifest/hash/row-count để phục vụ lịch sử, nhưng thiếu một file phụ không được làm mất quyền đọc các payload đã có lineage hợp lệ.

## 5. Intraday overlay

- Intraday là overlay provisional/status-only của phiên hiện tại.
- Intraday không thay EOD, không ghi đè Static Canonical Baseline và không chuyển thành completed bar.
- Intraday không tự xác nhận Event, Phase, Zone hoặc phát hành quyết định ADD.
- Mỗi snapshot ghi `snapshot_generated_at_utc`, `source_latest_date`, `publisher_generation_id`, freshness và binding manifest.
- Khi thị trường đóng cửa, Dashboard ghi rõ trạng thái đóng cửa và thời điểm snapshot cuối; freshness stale là advisory về tuổi snapshot, không phải publication block.

## 6. Realtime Wyckoff Alerts

Alerts luôn đọc `alerts_live.json` của generation public mới nhất có thể đọc được.

- `alerts=[]` hoặc các counter bằng 0 là kết quả hợp lệ sau khi snapshot đã đọc thành công.
- Không hiển thị `Chưa có snapshot` khi payload đã nhận.
- Không sử dụng hoặc phát hành các trường `Data Gate`, `CA/price basis gate`, `Integrity Gate` hoặc `Market Gate` như điều kiện loại bỏ alert.
- Có thể hiển thị risk/advisory, freshness, market session và quarantine để minh bạch.
- LPS, BUEC, Spring-Test, JAC-SOS và score/support/stop/T1 vẫn là `ALGO_CANDIDATE_ONLY` hoặc scanner proxy; không thay Method-Locked review và không tự nâng Event/Phase/Zone/ADD.

## 7. Dashboard

Dashboard là consumer hiển thị của public payload, không phải authority độc lập. Dashboard phải:

- đọc cùng generation với manifest và Alerts;
- hiển thị generation, source date, snapshot time, freshness và risk policy;
- hiển thị `Thị trường đóng cửa — snapshot cuối lúc <timestamp>` khi phiên đã đóng;
- hiển thị cảnh báo đọc/publication riêng nếu cần, nhưng không dựng lại `Market Gate FAIL`, `Data Gate FAIL`, `CA integrity FAIL` hoặc `Hard Integrity FAIL` như lý do chặn dữ liệu hiện hành;
- chỉ xác nhận deploy/public sau khi read-back thành công.

## 8. Giữ nguyên quy tắc Wyckoff

Mọi phân tích vẫn theo:

```text
OBSERVATION → EVIDENCE → INTERPRETATION → LABEL → STRUCTURE/PHASE → READINESS → STRATEGY
```

Không biến việc bỏ các publication gate thành quyền bỏ qua chất lượng phân tích. Không dùng một snapshot provisional để kết luận cấu trúc, không dùng score để thay Method Authority, và không phát hành BUY/ADD khi hợp đồng Locked Analysis chưa cho phép.

## 9. Quy ước trạng thái

- `PUBLISHED_WITH_RISK`: payload đã được công bố/read-back theo transport lineage, có cảnh báo rủi ro nếu có.
- `PUBLIC_READ_NOT_VERIFIED`: chưa đọc/đối chiếu được public authority.
- `PUBLIC_READ_DISABLED`: công cụ/connector không cho phép đọc public.
- `STALE_ADVISORY`: snapshot đọc được nhưng cũ so với ngưỡng freshness; không tự động xoá hoặc chặn snapshot.
- `QUARANTINE_SYMBOL`: chỉ áp dụng cho mã hoặc dòng dữ liệu cụ thể; không chặn toàn bộ phiên.

Không sử dụng `FAIL` của các gate cũ như điều kiện fail-closed cho publication mới.
