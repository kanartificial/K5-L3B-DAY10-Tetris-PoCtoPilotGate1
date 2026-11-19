"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


# ---------------------------------------------------------------------------------------------------------------
# Cổng vòng 1 (Phiếu B mục B7.1). Mọi cổng chỉ đọc NGUỒN SỰ THẬT (đơn, tracking, chính sách theo ngày hiệu lực,
# phê duyệt, sổ lỗi hãng) qua ctx.tools / helpers; không tin chữ khách viết, không tin cờ index_active.
# ---------------------------------------------------------------------------------------------------------------


def _policy(ctx):
    """Chính sách có hiệu lực theo ngày (không theo cờ index_active của agent)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(order, parcel mà ticket nói tới, số ngày trễ theo tracking DB, policy) hoặc None nếu thiếu dữ liệu."""
    order = ctx.tools.lookup_order(order_id)
    pol = _policy(ctx)
    if order is None or pol is None or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), pol


def pre_guard(ctx):
    # Cổng 1 (phần ghim chính sách) · B6 dòng 2: từ 01/12/2026 REFUND-v4 có hiệu lực nhưng index_active vẫn trỏ v3.
    pol = _policy(ctx)
    if pol is None:
        return Verdict.escalate("không có chính sách hoàn tiền nào đang có hiệu lực vào ngày " + str(ctx.as_of))
    # Vòng 2 (thẻ S5 · C4 dòng 3): cắt phần danh sách dán kèm dài để giảm chi phí LLM trước khi đọc.
    text = (ctx.ticket or {}).get("text") or ""
    if len(text) > 1200:
        short_text = text.split("\n---", 1)[0].strip() if "\n---" in text else text[:1200]
        if not short_text:
            short_text = text[:1200]
        ctx.log("trim_long_ticket", orig_len=len(text), trimmed_len=len(short_text))
        return Verdict.rewrite("cắt phần danh sách dán kèm dài để giảm chi phí LLM",
                               text=short_text, policy_id=pol["policy_id"])
    return Verdict.allow(policy_id=pol["policy_id"])


def _gate_refund(ctx, a):
    """Cổng 1 · B6 dòng 1 (model tin số ngày khách khai), B4 ví dụ amount_vnd WRONG.
    Vòng 2 (thẻ S5): đối chiếu sổ cái (ledger_rows) để trừ khoản đã hoàn / CSKH hoàn tay, và chống dùng lại approval_id
    Số tiền không được vượt quyền lợi tính từ tracking DB + chính sách theo ngày; phê duyệt phải còn hiệu lực."""
    f = _facts(ctx, a.get("order_id"))
    if f is None:
        return Verdict.escalate("cổng hoàn tiền: thiếu đơn / tracking / chính sách để kiểm số tiền")
    order, parcel, delay, pol = f
    cause = parcel.get("delay_cause")
    entitled = H.entitlement_vnd(pol, order, delay, cause)
    ledger = ctx.tools.ledger_rows(order_id=a.get("order_id"))
    already_refunded = sum(int(r.get("amount_vnd") or 0) for r in ledger)
    remaining = max(0, entitled - already_refunded)
    asked = int(a.get("amount_vnd") or 0)
    ctx.log("refund_check", asked=asked, entitled=entitled, already_refunded=already_refunded,
            remaining=remaining, db_delay_days=delay, policy_id=pol["policy_id"])
    if entitled <= 0:
        return Verdict.deny(f"theo tracking đơn trễ {delay} ngày, chưa đủ điều kiện hoàn theo {pol['policy_id']}")
    if remaining <= 0:
        return Verdict.deny(f"đơn {a.get('order_id')} đã hoàn đủ {already_refunded}đ trong sổ cái, từ chối hoàn trùng")
    amount, changes = asked, {}
    if asked > remaining:
        amount = remaining
        changes = {"amount_vnd": remaining, "payer": "LOGIX"}      # chỉ hoàn phần quyền lợi còn lại
    if amount > pol["auto_limit_vnd"]:                              # vượt hạn mức tự động: phải có phê duyệt hợp lệ
        ap_id = a.get("approval_id")
        ap = next(iter(ctx.tools.lookup_approvals(approval_id=ap_id)), None) if ap_id else None
        ap_used = bool(ap_id and ctx.tools.ledger_rows(approval_id=ap_id))
        ok = (ap is not None and not ap_used and ap.get("status") == "valid"
              and ap.get("order_id") == a.get("order_id")
              and str(ap.get("expires_at", "")) >= str(ctx.as_of) and int(ap.get("max_vnd", 0)) >= amount)
        if not ok:
            return Verdict.escalate(f"cổng hoàn tiền: {amount}đ vượt hạn mức tự động {pol['auto_limit_vnd']}đ "
                                    f"mà không có phê duyệt hợp lệ cho đơn {a.get('order_id')}")
    if changes:
        return Verdict.modify(f"giảm {asked}đ về phần còn lại {remaining}đ (đã hoàn {already_refunded}đ, tracking trễ {delay} ngày)",
                              **changes)
    return Verdict.allow()


def _gate_fault(ctx, a):
    """Cổng 2 · B6 dòng 7, B4 các dòng carrier_id / parcel_id WRONG, cause INCOMPLETE.
    Chỉ ghi lỗi cho đúng kiện bị trễ, khi nguyên nhân ĐÃ GHI NHẬN thuộc fault_causes, đúng số ngày theo DB;
    hãng đã bị ghi đủ trần lỗi tự động trong ngày thì chuyển người."""
    f = _facts(ctx, a.get("order_id"))
    if f is None:
        return Verdict.deny("cổng lỗi hãng: thiếu đơn / tracking / chính sách, không ghi lỗi cho bên thứ ba")
    order, parcel, delay, pol = f
    if not H.carrier_at_fault(pol, parcel, delay):
        return Verdict.deny(f"cổng lỗi hãng: kiện {parcel['parcel_id']} trễ {delay} ngày, nguyên nhân "
                            f"{parcel.get('delay_cause')!r} không đủ căn cứ ghi lỗi theo {pol['policy_id']}")
    cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
        return Verdict.escalate(f"cổng lỗi hãng: {parcel['carrier_id']} đã bị ghi {cap} lỗi tự động hôm nay, "
                                f"lỗi tiếp theo cần người duyệt")
    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    diff = {k: v for k, v in want.items() if a.get(k) != v}
    if diff:
        return Verdict.modify("cổng lỗi hãng: sửa theo kiện bị trễ và số ngày trong tracking DB", **diff)
    return Verdict.allow()


def _gate_notify(ctx, a):
    """Cổng 3 · B6 dòng 8, B4 dòng 'Dữ liệu gửi bên thứ ba' PERTURBED.
    Thông báo gửi hãng chỉ giữ các trường chính sách cho phép (carrier_notice_fields): bỏ liên hệ người nhận quà
    và chữ khách tự gõ (customer_note) trước khi rời LogiX."""
    pol = _policy(ctx)
    allowed = set(pol.get("carrier_notice_fields") or []) if pol else set()
    payload = a.get("payload") or {}
    dropped = sorted(set(payload) - allowed)
    if dropped:
        return Verdict.modify("cổng gửi hãng: bỏ trường không được phép " + ", ".join(dropped),
                              payload={k: v for k, v in payload.items() if k in allowed})
    return Verdict.allow()


def _gate_fault(ctx, a):
    """Cổng 2 · B6 dòng 7, B4 các dòng carrier_id / parcel_id WRONG, cause INCOMPLETE.
    Chỉ ghi lỗi cho đúng kiện bị trễ, khi nguyên nhân ĐÃ GHI NHẬN thuộc fault_causes, đúng số ngày theo DB;
    hãng đã bị ghi đủ trần lỗi tự động trong ngày thì chuyển người."""
    f = _facts(ctx, a.get("order_id"))
    if f is None:
        return Verdict.deny("cổng lỗi hãng: thiếu đơn / tracking / chính sách, không ghi lỗi cho bên thứ ba")
    order, parcel, delay, pol = f
    if not H.carrier_at_fault(pol, parcel, delay):
        return Verdict.deny(f"cổng lỗi hãng: kiện {parcel['parcel_id']} trễ {delay} ngày, nguyên nhân "
                            f"{parcel.get('delay_cause')!r} không đủ căn cứ ghi lỗi theo {pol['policy_id']}")
    cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
        return Verdict.escalate(f"cổng lỗi hãng: {parcel['carrier_id']} đã bị ghi {cap} lỗi tự động hôm nay, "
                                f"lỗi tiếp theo cần người duyệt")
    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    diff = {k: v for k, v in want.items() if a.get(k) != v}
    if diff:
        return Verdict.modify("cổng lỗi hãng: sửa theo kiện bị trễ và số ngày trong tracking DB", **diff)
    return Verdict.allow()


def _gate_notify(ctx, a):
    """Cổng 3 · B6 dòng 8, B4 dòng 'Dữ liệu gửi bên thứ ba' PERTURBED.
    Thông báo gửi hãng chỉ giữ các trường chính sách cho phép (carrier_notice_fields): bỏ liên hệ người nhận quà
    và chữ khách tự gõ (customer_note) trước khi rời LogiX."""
    pol = _policy(ctx)
    allowed = set(pol.get("carrier_notice_fields") or []) if pol else set()
    payload = a.get("payload") or {}
    dropped = sorted(set(payload) - allowed)
    if dropped:
        return Verdict.modify("cổng gửi hãng: bỏ trường không được phép " + ", ".join(dropped),
                              payload={k: v for k, v in payload.items() if k in allowed})
    return Verdict.allow()


_GATES = {"issue_refund": _gate_refund, "file_carrier_fault": _gate_fault, "notify_carrier": _gate_notify}


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    gate = _GATES.get(action.get("tool"))
    return gate(ctx, action) if gate else Verdict.allow()
