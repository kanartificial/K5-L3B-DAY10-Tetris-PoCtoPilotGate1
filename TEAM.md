# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Tetris
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Tetris-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S5

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |  Khổng Ngọc Anh         |    2A202603974  |   Kỹ sư cổng  |      x      |
|   2 |     Lý Hà Trân Trân      |   2A202603968   |   Kỹ sư cổng  |             |
|   3 |      Võ Thị Kim Ý     |   2A202603965   |  Sản phẩm và kinh doanh   |             |
|   4 |   Vương Thu Thảo         |   2A202603966   |   Vận hành và pháp lý  |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## LyHaTranTran-2A202603968

### Phần việc phụ trách

Vai **Kỹ sư cổng**.
- **Phiếu A:** câu 1.3 (mục A2, cột "Offline").
- **Phiếu B:** câu 2.2 (B2), câu 2.5 (B6, bản nháp cho cả bàn), câu 2.6 (B7.1), chốt cổng vòng 1 và nháp quyết định v1 (B8), dòng 2–3 của nhật ký B0, dòng 1 và 4 của checklist B5.
- **Phiếu C (thẻ S5):** câu 3.0 (C0 dòng 1, C1) và câu 3.1 (C2, C3.5, C4).
- **File:** `lab10/guards.py` (bản chốt `lab10/guards_round1.py`).

### Đóng góp cụ thể

- **1.3:** thiết kế offline metric "tỉ lệ ghi oan cho hãng" cho bước `file_carrier_fault`. Nhãn lấy từ `label.faults`, nối với trace theo `ticket_id`. Có quy tắc cho mẫu số bằng 0, cho ca ghi trùng và cho ca chưa có nhãn.
- **2.2:** dò `T-002@55`. Tách thành hai lỗi chìm (hoàn sai 20.000đ; ghi oan cho VNX kèm gửi thừa `customer_note`). Nguồn lỗi: đầu vào và thứ bậc hệ thống.
- **2.5:** viết nháp pre-mortem 8 lý do, đủ bốn lăng kính, mỗi lý do có bằng chứng kiểm được. Chọn 3 lý do làm cổng phòng ngừa.
- **2.6:** code ba cổng trong `lab10/guards.py`:
  - **Cổng 1 (hoàn tiền):** tính lại quyền lợi từ tracking DB và chính sách theo ngày hiệu lực, kiểm phê duyệt; `pre_guard` ghim phiên bản chính sách.
  - **Cổng 2 (ghi lỗi hãng):** chỉ ghi khi có nguyên nhân đã ghi nhận, ghi đúng kiện bị trễ, tối đa 2 lỗi mỗi hãng mỗi ngày.
  - **Cổng 3 (gửi hãng):** chỉ giữ các trường trong `carrier_notice_fields`.

  Kiểm lại: không làm hỏng ca nào trên bộ nền; tự dựng ca thử cho cổng 2 và cổng 3, vì bộ nền không có ca nào chạm hai cổng này.
- **B8:** chạy `lab10.checkpoint`, chạy eval mốc base và prepared, chạy `lab10.gate`. Nháp quyết định v1 "Tiếp tục" trong phạm vi HN + HCM, và ghi chú chỗ runbook lệch với config (`pilot_scope`).
- **3.0–3.1 (S5):** chạy grade ở mốc prepared, tách phần cổng đỡ được (chủ yếu nhờ config `business`) khỏi phần còn lọt (hoàn trùng cùng đơn). Dò 5 ticket, tìm ra 3 lỗi đến từ 3 nguồn: cờ `refund_status` cập nhật theo batch đêm; CSKH hoàn tay và trợ lý cùng ghi sổ; kho sỉ vượt hạn mức nên luôn phải chuyển người. Viết HAZOP 4 dòng, trong đó có nhánh chưa thấy trên trace là một phê duyệt bị dùng hai lần. Phát hiện lỗi `integrity: false` do CRLF trên Windows.

### Bằng chứng

- **Commit:**
  - `d9f1d6f`: 1.3
  - `abf0304`: 2.2
  - `c948adf`: 2.5
  - `b762dc4`: 2.6
  - `6b8f904`: chốt vòng 1 + v1
  - `5941fed`: 3.0 + 3.1
- **Mã lần chạy:**
  - `R-base-after-20261119-164251-844614`: cổng vòng 1, pass_rate 1,0, 0/0/0.
  - `R-base-before-20261119-170700-94d269`: base.
  - `R-base-prepared-20261119-170701-94d269`: prepared, đạt cả 5 ngưỡng bắt buộc và 3 ngưỡng kinh doanh, vận hành.
  - `R-S5-grade-20261119-171427-94d269`: grade S5, kèm `R-S5-before-…-94d269` và `R-S5-prepared-…-94d269`.
- **Hash chốt vòng 1:** `ae87608c`.
- **Dòng trong phiếu:**
  - Phiếu A mục A2, cột Offline.
  - Phiếu B mục B2, B6, B7.1, B8, B0 dòng 2–3, B5 dòng 1 và 4.
  - Phiếu C mục C0 dòng 1, C1, C2, C3.5, C4.

### Exit ticket

- **Học được:** một cổng "đạt 100% bộ nền" vẫn có thể bỏ lọt cả một loại lỗi. Cổng 1 so số tiền với quyền lợi của **một** lần hoàn, nên hoàn trùng cùng đơn ở thẻ S5 lọt qua, vì bộ nền không bao giờ có hai ticket cùng đơn trong một ngày. Phải hỏi "trường này là nguồn sự thật hay bản sao" (`refund_status` so với sổ cái) trước khi tin nó.
- **Còn chưa chắc:** cổng trần lỗi hãng (`escalate` ở bước ghi lỗi) chạy **sau** khi tiền đã hoàn. Chưa rõ nên chặn sớm hơn ở `issue_refund`, hay giữ như hiện tại để không làm khách chờ.

## KhongNgocAnh-2A202603974

### Phần việc phụ trách

**Trưởng nhóm** & vai **Kỹ sư cổng**.
- **CP1:** thiết lập repo nhóm, cập nhật `TEAM.md` và `submission/submission.json`.
- **Phiếu B:** câu 2.1 (B0 dòng 1, B1), câu 2.7 (B7.2), câu 2.8 (B7.3).
- **Phiếu C (thẻ S5):** kéo thẻ `incidents/S5`, câu 3.4 (C6), câu 3.5 (C7, cập nhật C0 dòng 2–4), câu 3.6 (C8).
- **File:** `TEAM.md`, `submission/submission.json`, `incidents/S5/`, `lab10/guards.py` (vòng 2), `lab10/monitors.py`, `config/operating_gates.json` (vòng 2).

### Đóng góp cụ thể

- **CP1:** Điền thông tin nhóm, bảng thành viên trong `TEAM.md` và danh sách `members` trong `submission/submission.json`.
- **2.1:** Chạy đánh giá baseline và `lab10.gate`, phân tích các ngưỡng `[CHƯA]` đạt (`wrongful_refund_vnd = 20000`, `wrongful_carrier_faults = 1`), phân khúc kho/hãng xấu nhất (HCM, `?`, VNX) và đề xuất khuyến nghị kết hợp.
- **2.7–2.8:** Nêu 2 bước tránh rò rỉ dữ liệu; thiết kế và chạy 2 ticket hiểm `--adhoc` (`O-1002 · C-02` và `O-1001 · C-01`) ở mốc `after` để kiểm tra tính chất chống tự khai số ngày trễ và tiêm lệnh.
- **Nhận thẻ S5:** Fetch và commit thư mục `incidents/S5` (4 file) vào repo nhóm.
- **3.4 (C6):** Dựng fault tree trước khi sửa gồm 3 nhánh (hoàn trùng cùng đơn, hoàn trùng khoản CSKH hoàn tay, chi phí LLM + công người vượt làm tay & ROI âm ở độ phủ thấp) kèm bảng specification và giả định môi trường.
- **3.5 (C7, C0):** Sửa `lab10/guards.py` (`pre_guard` dùng `Verdict.rewrite` cắt phần dán kèm dài; `_gate_refund` đối chiếu `ledger_rows` trừ khoản đã hoàn kể cả `basis: manual` và kiểm `approval_id` chưa dùng); cập nhật `config/operating_gates.json` (mở `pilot_scope` sang 4 kho bán lẻ `HN, HCM, DN, CT`, điền `operations` và `legal`); chạy `eval` (`S5 · after`, `base · after`) và `grade`.
- **3.6 (C8):** Thêm hàm `max_cost_per_ticket_by_warehouse_vnd` vào `lab10/monitors.py` và điền bảng thước đo → dữ liệu → cách tính.

### Bằng chứng

- **Commit:**
  - `d85fba9`: cập nhật `TEAM.md` và `submission/submission.json`
  - `da6ae03`: câu 2.1 (`B0`, `B1`)
  - `b1a598a`: nhận thẻ `incidents/S5`
  - `fabd8f3`: câu 2.7 và 2.8 (`B7.2`, `B7.3`)
  - `afa325b`: câu 3.4, 3.5, 3.6 (`guards.py`, `monitors.py`, `operating_gates.json`, `C0`, `C6`, `C7`, `C8`)
- **Mã lần chạy:**
  - `R-base-before-20261119-170700-94d269` (baseline vòng 1)
  - `R-S5-after-20261119-224240-73d630` (`S5 · after`: `pass_rate = 1.0`, hoàn sai `0đ`, lỗi oan `0`, `ROI = 3.15`)
  - `R-base-after-20261119-224241-73d630` (`base · after`: 110/110 đạt, không regression)
  - `R-S5-grade-20261119-224250-73d630` (`visible ✅`, `regression ✅`, `monitor ✅`)
  - *(Chạy lại trên máy gom bài để mã có trong `submission/runs/journal.jsonl`; số liệu giống hệt lần chạy gốc vì MockLLM tất định.)*
- **Dòng trong phiếu:** Phiếu B mục B0 dòng 1, B1, B7.2, B7.3; Phiếu C mục C0 dòng 2–4, C6, C7, C8.

### Exit ticket

- **Học được:** Kiểm soát rủi ro cần đi từ cả nguồn sự thật dữ liệu (`ledger_rows` thay cho cờ batch `refund_status`) lẫn bài toán kinh doanh (cân bằng chi phí LLM, công người và độ phủ pilot để ROI không bị âm).
- **Còn chưa chắc:** Ngưỡng cắt `> 1200` ký tự hoặc tách theo `\n---` ở `pre_guard` có thể làm mất thông tin nếu khách ngoài thực tế viết dài nhưng đặt nội dung chính ở cuối đoạn văn bản.


## VuongThuThao–2A202603966

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý.
- **Phụ trách:** Phiếu A mục 1.2, 1.4, phiếu B mục B4, B5, B7.5, B7.6, phiếu C mục C9, C10, C11.
- **File liên quan:** `templates\form-a-criteria.md`, `templates\form-b-evaluation-gates.md`., `templates\form-c-incidents.md`

### Đóng góp cụ thể

- Đánh giá rủi ro vận hành, chi phí và ảnh hưởng pháp lý của sự cố S5.
- Đề xuất ngưỡng cảnh báo chi phí 10.000đ/ticket, kiểm tra mẫu 10% và thu hẹp phạm vi pilot.
- Xây dựng Risk register và Runbook xử lý các tình huống phát sinh.
- Cập nhật checklist vận hành và trách nhiệm xử lý sau sự cố.

### Bằng chứng

- Commit: 
  - `f72b8fd`: cập nhật C9, C10, C11
  - `3e0d8d8`: cập nhật B7.5, B7.6
  - `da6ae03`: cập nhật A1.2, A1.4

### Exit ticket

- Điều học được: Triển khai AI cần kiểm soát cả hiệu quả chi phí, con người và rủi ro pháp lý, không chỉ độ chính xác kỹ thuật.
- Điều chưa chắc: Ngưỡng cảnh báo và tỷ lệ kiểm tra mẫu hiện tại đã phù hợp khi triển khai thực tế hay chưa.
