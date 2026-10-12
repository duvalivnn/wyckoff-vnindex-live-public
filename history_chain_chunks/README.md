# Thread reader history chunks

Đọc `history_chain_chunks_manifest.json` trước. Mỗi mã có một file weekly và một file daily; chỉ dùng sau khi kiểm tra bytes/SHA-256/row-count. Các chunk cùng `publisher_generation_id`; payload commit được authority bên ngoài xác định sau publication; Intraday là status-only.
