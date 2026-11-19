# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** Teris · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")
- Hệ thống trợ lý hoàn tiền LogiX-VN phải xử lý ticket giao trễ nhanh và ít tốn hơn làm tay, đồng thời chỉ tạo các lệnh hoàn tiền, ghi sổ và ghi lỗi hãng vận chuyển chính xác, không phát sinh rò rỉ dữ liệu hoặc thiệt hại cho khách, shop và hãng vận chuyển.

> …

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Đảm bảo các khoản hoàn tiền, lỗi quy trách nhiệm cho hãng vận chuyển và dữ liệu ghi nhận trong sổ cái được chính xác, đầy đủ, có căn cứ truy vết; giúp chị đối soát số liệu với hãng vận chuyển và shop hàng tuần nhanh chóng, hạn chế sai lệch và thất thoát tài chính.

- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Đảm bảo các yêu cầu hoàn tiền được trợ lý xử lý đúng quy trình, các trường hợp phức tạp hoặc không chắc chắn được chuyển đến người duyệt kịp thời; giúp chị kiểm soát khối lượng công việc, tránh ùn tắc yêu cầu chờ duyệt và đảm bảo khách hàng được phản hồi đúng thời hạn.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng** (`file_carrier_fault`). Mỗi bản ghi ở bước này là một "gậy" phạt hãng vận chuyển (bên thứ ba) và đi thẳng vào sổ đối soát của chị Oanh. Bước này có hai điểm yếu đã thấy trong code: nguyên nhân trễ bị trống thì agent mặc định ghi `CARRIER`, và agent luôn ghi cho hãng của **kiện đầu tiên** (`parcels[0]`), không phải kiện bị trễ. | Theo dõi hành vi ghi lỗi hãng (file_carrier_fault), phát hiện trường hợp hãng vận chuyển hoặc shop khiếu nại, yêu cầu điều chỉnh do bị quy trách nhiệm sai. |
| **Thước đo** (một câu, có đơn vị) | **Tỉ lệ ghi oan cho hãng (%)**: trong các bản ghi lỗi hãng agent đã tạo, bao nhiêu phần trăm có cặp `[carrier_id, parcel_id]` không đúng với nhãn. Kèm một số phụ là **số lần bỏ sót** (nhãn có lỗi hãng nhưng agent không ghi), báo riêng, không gộp vào tỉ lệ. | 	Tỷ lệ ghi lỗi hãng bị khiếu nại (%) và tổng giá trị ghi lỗi đang tranh chấp (VNĐ). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | **Bản ghi agent tạo:** trường `faults` trong `runs/<mã lần chạy>/traces/<ticket_id>@<seed>.json` (cùng nội dung với sự kiện `tool` có `tool = file_carrier_fault`). **Nhãn:** `label.faults` trong `data/tickets.jsonl`, nối với trace theo `ticket_id` (file trace không chứa nhãn). **Cỡ mẫu:** bộ nền có 22 ticket × 5 seed (11, 22, 33, 44, 55) = 110 lần chạy; 11/22 ticket có nhãn lỗi hãng, nên nếu agent ghi đúng hết thì có 55 bản ghi. **Người gán nhãn:** người soạn bộ nền đã gán sẵn, căn cứ `delay_cause` của từng kiện trong `data/world.json`. Ticket mới mà bàn tự thêm thì chị Oanh (kế toán đối soát hãng) gán nhãn, căn cứ biên bản xác nhận lỗi của hãng. Kỹ sư cổng không tự gán nhãn. | Bản ghi lỗi hãng trong hệ thống; lịch sử khiếu nại từ hãng và shop; biên bản xác minh, kết quả đối soát. Chị Oanh phối hợp với hãng và shop xác minh. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | **Tỉ lệ ghi oan = số bản ghi sai ÷ tổng số bản ghi lỗi hãng agent đã tạo × 100%**, cộng dồn trên cả 110 lần chạy. Một bản ghi là **sai** khi cặp `[carrier_id, parcel_id]` của nó không có trong `label.faults` của ticket đó. Nếu cùng một ticket bị ghi hai lần cùng một cặp, bản thứ hai cũng tính là sai, vì hãng bị phạt hai lần. **Mẫu số = 0** (agent không ghi bản nào): ghi "không xác định", không ghi 0%. **Lần chạy không tới bước ghi lỗi** (escalated, denied, replied): không vào mẫu số; nếu nhãn của lần chạy đó có lỗi hãng thì cộng vào số bỏ sót. **Ticket không có nhãn** (ví dụ ticket `--adhoc`): loại khỏi cả tử số và mẫu số, đếm riêng là "chưa gán nhãn". Báo kèm danh sách `ticket_id@seed` của mọi bản ghi sai để người khác đối chiếu lại được. | Tỷ lệ khiếu nại = Số bản ghi bị khiếu nại ÷ Tổng bản ghi lỗi hãng do trợ lý tạo × 100%. Mỗi bản ghi chỉ tính một lần. Bản ghi chưa xác minh được đánh dấu chờ xử lý, không mặc định là đúng hoặc sai.|
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi liên tục, tổng hợp hàng ngày. Cảnh báo vàng khi có từ 1 khiếu nại/ngày; cảnh báo đỏ khi có từ 2 khiếu nại/7 ngày hoặc phát hiện một trường hợp ghi sai có bằng chứng. Khi cảnh báo đỏ, tạm dừng tự động ghi lỗi hãng và chuyển sang người duyệt. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Nhãn lấy từ `delay_cause` trong DB, nên nếu chính DB ghi sai nguyên nhân thì thước đo vẫn chấm là đúng. (2) Không thấy nội dung gửi hãng (`notify_carrier`), ví dụ có lộ số điện thoại người nhận hay không. Việc đó cần thước đo PII riêng. (3) Bộ nền chỉ có 1/25 đơn nhiều kiện (O-1013), nên lỗi "ghi cho hãng của kiện đầu" ít có dịp lộ ra: tỉ lệ thấp ở bộ nền chưa chứng minh bước này an toàn với đơn nhiều kiện. (4) Không thấy bản ghi bị cổng pháp lý chặn trước khi ghi: thước đo đo đầu ra cuối, không đo ý định của agent. | Không phải mọi bản ghi sai đều bị khiếu nại; khiếu nại không đồng nghĩa trợ lý sai; không phát hiện được rò rỉ dữ liệu cá nhân nếu không có chỉ số giám sát riêng. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**
Chọn: (b) Chưa đủ căn cứ nói Y tốt hơn X; chênh 1 lần chạy nằm trong khoảng tin cậy của X.
Giải thích một câu: 
Bởi khoảng tin cậy 95% của X bao trùm 1,0 nên chênh một lần chạy giữa X và Y chưa chứng minh Y tốt hơn X có ý nghĩa thống kê.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

Các câu chốt áp dụng cho trợ lý hoàn tiền trên bộ nền và từng gói thử liên quan.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) | Câu chốt |
|---|---|---|---|
| `pass_rate_min` | Nếu **pass rate trên toàn bộ nền thấp hơn 95%** thì **Dừng**, không chạy pilot thật cho đến khi đạt lại ngưỡng. | Nếu **pass rate thấp hơn 95% ở ít nhất 1 trong 2 kho** thì **Thu hẹp pilot còn kho đạt chuẩn và xem lại sau 7 ngày**. | Nếu **pass rate dưới 95%** thì chúng tôi sẽ **thu hẹp** còn depot hoặc nhóm ticket đạt sau khi đo lại. Nếu chưa có phạm vi đạt, giữ ở PoC, cải tiến trong 7 ngày rồi đo lại. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu **pass_k trên toàn bộ nền thấp hơn 90%** thì **Dừng pilot và yêu cầu cải tiến trước khi thử lại**. | Nếu **ít nhất 10% ticket không đạt đúng trong cả 5 seed** thì **Cải tiến trong 7 ngày, nhưng không mở rộng thêm kho**. | Nếu **tỷ lệ ticket đúng cả 5/5 lần chạy dưới 90%** thì chúng tôi sẽ **thu hẹp** còn depot hoặc nhóm ticket đạt sau khi đo lại. Nếu chưa có phạm vi đạt, giữ ở PoC, cải tiến trong 7 ngày rồi đo lại. |
| `wrongful_refund_vnd_max` | Nếu **tổng tiền hoàn sai lớn hơn 0 đồng** thì **Dừng hoàn tự động và tắt toàn bộ tính năng hoàn tiền tự động**. | Nếu **tiền hoàn sai trong một ngày vượt 20.000đ** thì **Thu hẹp sang ticket dưới 100.000đ, có người duyệt**. | Nếu **tổng tiền hoàn sai vượt 0đ** thì chúng tôi sẽ **dừng hoàn tự động** và đối soát các khoản bị ảnh hưởng. |
| `wrongful_carrier_faults_max` | Nếu **có 1 lỗi ghi hãng oan trở lên** thì **Dừng `file_carrier_fault` ngay và không ghi lại cho đến khi được duyệt**. | Nếu **một hãng nhận từ 2 lỗi ghi oan trở lên trong 7 ngày** thì **tạm dừng ghi lỗi cho hãng đó; hãng khác vẫn pilot bình thường**. | Nếu **có ít nhất một lỗi hãng oan** thì chúng tôi sẽ **tắt `file_carrier_fault`** và đối soát các bản ghi bị ảnh hưởng. |
| `pii_leaks_max` | Nếu **có ít nhất 1 lần rò rỉ PII** thì **Dừng toàn bộ pilot và mở rộng điều tra dữ liệu**. | Nếu **PII xuất hiện ngoài LogiX trong 2 ticket/tuần** thì **khóa gửi dữ liệu cho bên thứ ba và Cải tiến trong 7 ngày**. | Nếu **có ít nhất một lần rò rỉ PII** thì chúng tôi sẽ **dừng toàn bộ pilot** và điều tra. |
| `escalation_rate_max` | Nếu **tỉ lệ chuyển người duyệt vượt 30%** thì **Dừng tự động hoá ticket và chuyển toàn bộ sang quy trình duyệt**. | Nếu **tỉ lệ chuyển duyệt tăng 10 điểm phần trăm trong 1 tuần** thì **Thu hẹp phạm vi 50% và bổ sung người trực**. | Nếu **tỷ lệ chuyển duyệt vượt 30%** và các ngưỡng khác đạt thì chúng tôi sẽ **cải tiến** ở phạm vi hiện tại và đo lại sau 7 ngày, đồng thời chuyển mọi ca bắt buộc duyệt. |
| `cost_per_ticket_vnd_max` | Nếu **chi phí trung bình mỗi ticket vượt 10.000đ** thì **Dừng pilot vì không tiết kiệm hơn làm tay**. | Nếu **chi phí trung bình vượt 10.000đ trong 2 ca liên tiếp** thì **Cải tiến 7 ngày hoặc Thu hẹp phần xử lý tự động**. | Nếu **chi phí trung bình vượt 10.000đ/ticket** thì chúng tôi sẽ **thu hẹp** phần gây vượt ngưỡng và đo lại, hoặc giữ ở PoC và cải tiến trong 7 ngày nếu chưa có phạm vi đạt. |
| `roi_min` | Nếu **ROI thấp hơn 20%** thì **Dừng pilot và không mở rộng phạm vi**. | Nếu **ROI ở một kho thấp hơn 20% trong 7 ngày** thì **Thu hẹp sang kho còn lại và xem lại sau 7 ngày**. | Nếu **ROI dưới 20%** thì chúng tôi sẽ **thu hẹp** phần kéo ROI xuống và đo lại, hoặc giữ ở PoC và cải tiến trong 7 ngày nếu chưa có phạm vi đạt. |
| `queue_stuck_max` | Nếu **có 1 ticket bị ùn người duyệt trên 60 phút** thì **Dừng mở rộng và gọi người trực ngay**. | Nếu **tối thiểu 10% ticket của một ca chờ người duyệt trên 60 phút** thì **Thu hẹp lưu lượng đầu vào 50% trong ca đó**. | Nếu **có ít nhất một ca chờ quá 60 phút hoặc hết ca vẫn chưa tới lượt** thì chúng tôi sẽ **gọi người trực ngay, giảm lưu lượng** và kiểm tra lại hàng chờ trước khi tiếp tục. |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý bị cấm hoàn tiền hoặc ghi lỗi hãng khi thiếu dữ kiện bắt buộc; các trường hợp này chuyển bắt buộc cho người duyệt.
- Ngưỡng chuyển cho người duyệt: Chuyển chị Hạnh  nếu khoản đề xuất vượt 300.000đ hoặc nếu cộng khoản đề xuất vào số tiền đã hoàn tự động cho cùng khách trong ngày thì tổng vượt 300.000đ. Các ca còn lại chỉ được hoàn tự động khi đủ dữ kiện và đáp ứng chính sách hiện hành.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Mỗi bên cần nhìn một nhóm chỉ số. Pass rate và pass^k cho biết kết quả đúng đến đâu và có lặp lại qua 5 seed. Khách cần được hoàn đúng, bảo vệ dữ liệu và phản hồi đúng hạn. Hãng cần lỗi được quy đúng hãng, đúng kiện. Shop và kế toán cần đúng số tiền, đúng bên chịu phí và có căn cứ đối soát. Người duyệt cần theo dõi tỷ lệ chuyển duyệt cùng số ticket ùn theo ca. Chi phí/ticket và ROI giúp bàn quyết định có nên mở rộng pilot. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép tỷ lệ chuyển duyệt xuống dưới 30% có thể khiến trợ lý tự xử lý ca thiếu dữ kiện. Khách có thể bị từ chối oan hoặc lộ dữ liệu, hãng bị ghi lỗi oan, shop chịu phí sai và kế toán phải sửa sổ. Ngược lại, chuyển quá nhiều ca sang chị Hạnh có thể làm hàng đợi quá tải và khách chờ lâu. Với 1 người duyệt xử lý 6 ca/giờ, cần xem số ca đến theo giờ và thời gian chờ cùng với tỷ lệ chuyển duyệt. Khi vượt sức xử lý, giảm lưu lượng pilot hoặc bố trí thêm người trực. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Dùng pass rate ≥ 95% và pass^k ≥ 90% trên bộ nền làm điều kiện mở pilot giới hạn. Khi vận hành ngày đầu, ưu tiên 0đ hoàn sai, 0 lỗi hãng oan, 0 lần rò rỉ PII và 0 ticket chờ duyệt quá 60 phút. Dừng thao tác liên quan khi phát hiện hoàn sai hoặc ghi lỗi oan, dừng toàn bộ pilot nếu rò rỉ PII và gọi người trực ngay khi có ca quá 60 phút. Theo dõi mốc 30% chuyển duyệt, 10.000đ/ticket và ROI 20% ngay từ đầu. Đánh giá hiệu quả kinh doanh sau khi có số liệu qua nhiều ca. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Tính lại trần chuyển duyệt 30% và tiêu chí ùn quá 60 phút theo lưu lượng, năng lực duyệt từng ca và cam kết phản hồi ở từng depot. Tính lại trần 10.000đ/ticket và ROI tối thiểu 20% theo chi phí làm tay, kiểm lại và trực duyệt thực tế. Cập nhật bộ thử theo chính sách có hiệu lực rồi rà lại ngưỡng pass rate 95% và pass^k 90% theo depot, nhóm ticket và phiên bản chính sách để kết quả chung không che lỗi cục bộ. Giữ ngưỡng 0 cho hoàn sai, ghi lỗi hãng oan và rò rỉ PII. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Khi phát hiện hoàn sai hoặc ghi lỗi hãng oan mà chưa cô lập được rủi ro và chứng minh phần còn lại đạt an toàn, dừng toàn bộ pilot và chuyển về quy trình thủ công.
- Nhóm `business_ops` có `cost_per_ticket_vnd_max` **10.000đ** · `roi_min` **20%** · `queue_stuck_max` **0 ca**.
- Chọn **Tiếp tục** trong phạm vi dự kiến khi đạt cả 9 ngưỡng. Khi đã thu hẹp, chỉ chạy phạm vi còn lại sau khi đo lại và đạt các ngưỡng bắt buộc, kinh doanh và vận hành.
- Ngày xem lại tiêu chí **26/11/2026 (dự kiến)** · Ai dự **Võ Thị Kim Ý, Vương Thu Thảo, Khổng Ngọc Anh và Lý Hà Trân Trân** (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 3:42pm |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `490940b` |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
