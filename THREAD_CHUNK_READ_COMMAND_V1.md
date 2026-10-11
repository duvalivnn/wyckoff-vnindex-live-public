# Thread Chunk Read Command V1

## Câu lệnh bắt buộc trước Method-Locked audit

Đọc `authority_receipt.json` và `live_pointer.json` trước. Sau đó đọc `history_chain_chunks_manifest.json` từ payload commit hiện hành, rồi đọc weekly/daily chunk theo từng mã và kiểm tra SHA-256, bytes, row-count, header, symbol và duplicate key. Chỉ khi toàn bộ chunk yêu cầu đạt mới thực hiện Method-Locked audit. Không dùng `weekly_replace.csv`, `daily_bridge.csv`, cache hoặc attachment cũ để thay thế chunk.

## Cách áp dụng

1. Resolve payload commit động từ `live_pointer.json`; không dùng commit hard-code.
2. Đọc `authority_receipt.json` và `history_chain_chunks_manifest.json` từ cùng payload lineage.
3. Chỉ tải các chunk weekly/daily được yêu cầu cho mã đang audit.
4. Đối chiếu độc lập SHA-256, bytes, row-count, header, symbol và duplicate key với manifest.
5. Nếu một kiểm tra không đạt, dừng Method-Locked audit cho mã/phạm vi chunk đó và báo cáo lỗi cụ thể.
6. Không dùng compatibility view, cache, attachment hoặc commit cũ để lấp dữ liệu chunk bị thiếu.

Public payload hiện hành phải có `authority_receipt.json`, `live_pointer.json`, `history_chain_chunks_manifest.json` và `history_chain_chunk_binding_receipt.json` trong cùng lineage. Nếu một file không đọc được hoặc binding không khớp, trả `PUBLIC_READ_NOT_VERIFIED`; không dùng staging, attachment, cache hoặc commit cũ để thay thế. `source_payload_commit` và `previous_projection_source_payload_commit` chỉ là provenance khi binding receipt đã xác nhận quan hệ với payload hiện hành.

Quy tắc này là kiểm tra lineage/đọc dữ liệu cho lịch sử. Nó không phải Data Gate, Corporate Action/price basis gate, Integrity Gate hoặc Market Gate dùng để chặn publication của snapshot hiện hành.
