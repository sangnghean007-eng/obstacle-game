# Instagram Reels: hồ sơ đăng tải "The GOATs Clock Out" (v5, bản chốt)

Ký hiệu mức độ tin cậy: **[CHÍNH THỨC]** = trang của Meta/Instagram · **[THAM KHẢO]** = nguồn bên thứ ba (đã đối chiếu ít nhất 2 nguồn) · **[KIỂM TRA]** = xác nhận lại trên app của bạn.

## A. Kiểm tra trước khi đăng
| # | Hạng mục | Trạng thái |
|---|---|---|
| 1 | Video 1080x1920 (9:16), 21 s, MP4 | Đạt |
| 2 | Chữ quan trọng nằm ngoài vùng bị giao diện che (công cụ `studio/qa_sheet.py`) | Đạt (các khung còn bị gắn cờ là báo nhầm do lưới khung thành và tờ giấy trắng) |
| 3 | Dữ kiện đã kiểm chứng; có nhãn parody trong video | Đạt |
| 4 | Âm thanh gốc tự tạo, không nhạc bản quyền | Đạt |
| 5 | Ảnh bìa `cover-9x16.jpg` có chữ nằm giữa khung (lưới trang cá nhân cắt phần giữa) | Đạt |

## B. Các bước trong app (Instagram → + → Reel)
**1. Chọn video** → Next. Không thêm nhạc thịnh hành, vì sẽ đè lên âm thanh gốc chứa các tiếng đập, tiếng "ting" là phần của câu đùa.

**2. Ảnh bìa (Edit cover)**: tải lên `cover-9x16.jpg`. Kiểm tra phần xem trước của ô vuông trên lưới trang cá nhân: chữ "SAME YEAR?!" phải nằm trọn trong khung [KIỂM TRA].

**3. Caption** (tối đa 2.200 ký tự; chỉ khoảng 125 ký tự đầu hiện trước nút "more" [THAM KHẢO]). Câu đầu chứa từ khóa người ta tìm, vì Instagram đọc caption để quyết định gợi ý cho ai [THAM KHẢO]:
```
Messi & Ronaldo both retired from their national teams in 2026… same year?! 🐐🐐

Messi: "Retirement v2.0" (2016 says hi 👋)
Ronaldo: first World Cup knockout goal after 20 years ⚽ then a €255 fine → "keep the change" 💸

Team 10 or Team 7 — who comes back first? 👇

Real 2026 facts · parody cartoon · both still play club football.
#messi #ronaldo #footballmemes #worldcup2026 #football
```
**Hashtag: tối đa 5 cho mỗi bài**, tính chung cả caption và bình luận. Instagram công bố giới hạn này ngày 18/12/2025, thay cho mức 30 trước đó [THAM KHẢO: nhiều nguồn trích tài khoản @creators và trang Help]. Không thêm hashtag vào bình luận.

**4. Tag people / Collaborators**: không gắn thẻ tài khoản cầu thủ (tránh hiểu lầm là được họ xác nhận). Nếu hợp tác với một trang fan bóng đá thì mời làm **Collaborator**: bài hiện ở cả hai trang.

**5. Add location**: bỏ trống.

**6. Topics** (nếu app hiện mục này): Sports / Soccer, Comedy [KIỂM TRA].

**7. Trial reel** [THAM KHẢO]: tùy chọn. Bật nếu muốn thử Reel với người chưa theo dõi trước khoảng 24 giờ rồi mới quyết định chia sẻ cho người theo dõi. Khuyến nghị: **tắt** cho video này, vì tin đang nóng nên cần đăng thẳng.

**8. Share to Facebook**: **tắt**. Đăng Facebook riêng theo `FACEBOOK.md` để dùng caption và hashtag phù hợp với Facebook.

**9. AI label** ("AI info" / "Made with AI"): **không bật**. Meta yêu cầu nhãn khi video hoặc âm thanh trông và nghe như thật mà được tạo hoặc chỉnh sửa kỹ thuật số; ví dụ "không cần nhãn" trên trang Help của Meta là video phong cách hoạt hình [CHÍNH THỨC, KIỂM TRA vì trang đó đang lỗi tiêu đề]. Nếu sau này dùng hình hoặc giọng giống người thật thì phải bật.

**10. More options / Advanced settings** [KIỂM TRA tên mục trong app]:
- **Allow remixing / templates**: bật (giúp lan truyền).
- **Allow downloads**: bật hoặc tắt tùy bạn; bật thì dễ được chia sẻ lại, nhưng dễ bị đăng lại mà không ghi nguồn.
- **Alt text / Accessibility**: điền `Cartoon parody: Messi and Ronaldo characters retire from national teams, a €255 fine paid from a giant wallet, and two goats with 10 and 7 headbutting.`
- **Hide like counts**: tắt.
- **Comments**: bật; bật bộ lọc từ ngữ xúc phạm (Settings → Hidden words).

**11. Share**.

## C. Sau khi đăng
| Thời điểm | Việc cần làm |
|---|---|
| 0–60 phút | Bình luận đầu và ghim: `Did you spot the RETIREMENT v3.0 draft? 👀 Team 10 or Team 7?`. Trả lời 5–10 bình luận đầu. Chia sẻ Reel lên Story kèm sticker bình chọn "10 or 7?". |
| 24 h | Gửi studio: Views, Reach, Average watch time, tỉ lệ người xem không phải follower, Shares, Saves, Comments [KIỂM TRA tên chỉ số trong Insights]. |
| 48 h | Studio cập nhật `studio/scorecard.csv` và PLAYBOOK. |
| Khi có tin mới | Sửa caption nếu thông tin không còn đúng. |

## D. Rủi ro
- **Fan hai bên cãi nhau hoặc xúc phạm cầu thủ**: dùng Hidden words, ẩn hoặc xóa bình luận xúc phạm.
- **Báo cáo sai sự thật**: caption đã ghi "both still play club football" và "parody".
- **Bị đăng lại không ghi nguồn**: video có tên kênh hoặc dòng nhãn cuối; cân nhắc tắt Allow downloads.

## E. Nguồn
[Meta: khi nào cần nhãn AI](https://www.meta.com/help/artificial-intelligence/1783222608822690/) · [Meta Transparency: Labeling AI content](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content) · [Instagram Reels features](https://about.instagram.com/features/reels/) · Giới hạn 5 hashtag: [Later](https://later.com/blog/ultimate-guide-to-using-instagram-hashtags/), [Creator Lane](https://creatorlanehq.com/blog/instagram-5-hashtag-limit-2026), [Presly](https://presly.ai/blog/instagram-hashtag-limit) · Trial reels: [MacRumors](https://www.macrumors.com/2024/12/10/instagram-trial-reels/) · Độ dài caption: [Sendible](https://www.sendible.com/insights/instagram-character-limit), [ClipSpeed](https://www.clipspeed.ai/blog/instagram-reels-captions.html).
