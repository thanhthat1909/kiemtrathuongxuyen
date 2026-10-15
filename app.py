from datetime import datetime
import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="Kiểm tra Trực tuyến Môn Tin học", page_icon="💻", layout="centered"
)

# Khởi tạo cơ sở dữ liệu lưu kết quả tạm thời trong Session State
if "results_db" not in st.session_state:
    st.session_state.results_db = []

# Danh sách 20 câu hỏi trắc nghiệm
QUIZ_DATA = [
    {
        "id": 1,
        "question": "Hệ điều hành Windows 7 được hãng Microsoft phát hành vào năm nào?",
        "options": ["A. 2007", "B. 2008", "C. 2009", "D. 2010"],
        "answer": "C",
    },
    {
        "id": 2,
        "question": "Hệ điều hành mã nguồn mở Linux có nguồn gốc phát triển từ hệ điều hành nào?",
        "options": ["A. UNIX", "B. Windows", "C. iOS", "D. Android"],
        "answer": "A",
    },
    {
        "id": 3,
        "question": "Đâu là một hệ điều hành phổ biến được thiết kế chuyên dụng cho thiết bị di động?",
        "options": ["A. Ubuntu", "B. iOS", "C. Windows", "D. Mac OS"],
        "answer": "B",
    },
    {
        "id": 4,
        "question": "Trong các phần mềm sau đây, đâu là ví dụ tiêu biểu của phần mềm nguồn mở?",
        "options": [
            "A. Microsoft Word",
            "B. Adobe Photoshop",
            "C. Python",
            "D. AutoCAD",
        ],
        "answer": "C",
    },
    {
        "id": 5,
        "question": "Giấy phép nào dưới đây là giấy phép điển hình và phổ biến nhất đối với phần mềm nguồn mở?",
        "options": [
            "A. GNU GPL",
            "B. Windows EULA",
            "C. Commercial License",
            "D. Proprietary License",
        ],
        "answer": "A",
    },
    {
        "id": 6,
        "question": "Thiết bị nào sau đây nằm bên trong thân máy tính và đóng vai trò thực hiện các phép toán cùng điều khiển toàn bộ hoạt động của máy?",
        "options": [
            "A. Màn hình",
            "B. Bộ xử lý trung tâm (CPU)",
            "C. Bàn phím",
            "D. Máy in",
        ],
        "answer": "B",
    },
    {
        "id": 7,
        "question": "Đơn vị nào thường được dùng để đo tần số xung nhịp (tốc độ) của bộ xử lý trung tâm (CPU)?",
        "options": ["A. GB", "B. GHz", "C. Bps", "D. DPI"],
        "answer": "B",
    },
    {
        "id": 8,
        "question": "Cổng kết nối nào trên máy tính có khả năng truyền tải đồng thời cả hình ảnh và âm thanh chất lượng cao qua một cáp duy nhất?",
        "options": ["A. VGA", "B. HDMI", "C. Cổng mạng LAN", "D. PS/2"],
        "answer": "B",
    },
    {
        "id": 9,
        "question": "Thiết bị nào sau đây được phân loại là thiết bị vừa vào vừa ra (I/O device) của máy tính?",
        "options": [
            "A. Bàn phím không dây",
            "B. Màn hình cảm ứng",
            "C. Máy in",
            "D. Máy quét ảnh",
        ],
        "answer": "B",
    },
    {
        "id": 10,
        "question": "Cổng kết nối nào dưới đây là cổng giao tiếp đa năng phổ biến nhất trên máy tính hiện nay để cắm USB, chuột, bàn phím và ổ cứng di động?",
        "options": [
            "A. Cổng VGA",
            "B. Cổng USB",
            "C. Cổng COM",
            "D. Cổng LPT",
        ],
        "answer": "B",
    },
    {
        "id": 11,
        "question": "Phát biểu nào sau đây thể hiện rõ nhất đặc điểm khác biệt của hệ điều hành dành cho thiết bị di động so với hệ điều hành máy tính cá nhân?",
        "options": [
            "A. Giao diện phức tạp đòi hỏi phải tìm hiểu nhiều thì mới sử dụng được các chức năng của hệ điều hành.",
            "B. Không hỗ trợ kết nối mạng không dây và chỉ chạy độc lập.",
            "C. Giao diện đặc biệt thân thiện, tối ưu cho màn hình cảm ứng và dễ dàng kết nối mạng di động.",
            "D. Chỉ dùng để lập trình và không hỗ trợ các tiện ích cá nhân.",
        ],
        "answer": "C",
    },
    {
        "id": 12,
        "question": "Khi nói về mối quan hệ giữa phần cứng, hệ điều hành và phần mềm ứng dụng trong hệ thống máy tính, phát biểu nào sau đây là đúng?",
        "options": [
            "A. Phần mềm ứng dụng hoạt động độc lập mà không cần hệ điều hành quản lý phần cứng.",
            "B. Hệ điều hành đóng vai trò là nền tảng quản lý, điều phối tài nguyên phần cứng để các phần mềm ứng dụng hoạt động hiệu quả.",
            "C. Phần cứng tự động điều khiển phần mềm ứng dụng mà không thông qua hệ điều hành.",
            "D. Hệ điều hành chỉ là một phần mềm ứng dụng cài thêm khi cần thiết.",
        ],
        "answer": "B",
    },
    {
        "id": 13,
        "question": "Tại sao nói phần mềm thương mại và phần mềm nguồn mở không loại trừ lẫn nhau mà có vai trò bổ sung cho nhau trong sự phát triển của CNTT?",
        "options": [
            "A. Vì cả hai loại đều bắt buộc phải thu phí bản quyền giống hệt nhau.",
            "B. Vì mỗi loại phục vụ các nhu cầu và đối tượng khác nhau.",
            "C. Vì phần mềm nguồn mở sẽ sớm thay thế phần mềm thương mại.",
            "D. Vì chúng dùng chung một hệ thống mã nguồn đóng duy nhất.",
        ],
        "answer": "B",
    },
    {
        "id": 14,
        "question": "Đặc điểm quan trọng nào sau đây phân biệt phần mềm chạy trên Internet so với phần mềm cài đặt truyền thống trên máy tính cục bộ?",
        "options": [
            "A. Bắt buộc phải mua đĩa CD cài đặt mới sử dụng được.",
            "B. Sử dụng qua mạng mà không cần cài đặt cục bộ trên máy.",
            "C. Chỉ chạy được khi ngắt kết nối hoàn toàn với mạng Internet.",
            "D. Không bao giờ lưu trữ dữ liệu trên môi trường mạng.",
        ],
        "answer": "B",
    },
    {
        "id": 15,
        "question": "Phát biểu nào sau đây chính xác nhất khi nói về bản chất và vai trò của các mạch logic (AND, OR, NOT) bên trong máy tính?",
        "options": [
            "A. Là các linh kiện cơ khí giúp truyền động cho các quạt tản nhiệt trong máy tính.",
            "B. Mạch điện tử xử lý giá trị nhị phân để thực hiện tính toán.",
            "C. Là các phần mềm ứng dụng chuyên dùng để soạn thảo văn bản.",
            "D. Là các cổng kết nối ngoại vi truyền tín hiệu âm thanh.",
        ],
        "answer": "B",
    },
    {
        "id": 16,
        "question": "Khi tìm hiểu tài liệu kỹ thuật để kết nối một thiết bị ngoại vi mới vào máy tính, ý nghĩa của các tham số kỹ thuật như độ phân giải hoặc tốc độ truyền dữ liệu là gì?",
        "options": [
            "A. Đánh giá tính tương thích và cách kết nối.",
            "B. Xác định mức giá bán và thời gian bảo hành.",
            "C. Cho biết tên nhà sản xuất và năm xuất xưởng.",
            "D. Quy định khối lượng và kích thước vật lý.",
        ],
        "answer": "A",
    },
    {
        "id": 17,
        "question": "Khi bạn kết nối một máy in mới hoặc một chuột quang vào máy tính nhưng thiết bị không hoạt động, việc đầu tiên bạn cần làm theo đúng quy trình khắc phục sự cố phần cứng cơ bản là gì?",
        "options": [
            "A. Tháo bo mạch chủ của máy tính để thay thế chip ROM.",
            "B. Kiểm tra lại kết nối vật lý, thử cổng kết nối khác.",
            "C. Mua ngay một hệ điều hành bản quyền mới thay thế.",
            "D. Cài đặt lại toàn bộ hệ thống mạng LAN của phòng máy.",
        ],
        "answer": "B",
    },
    {
        "id": 18,
        "question": "Khi sử dụng tiện ích Optimize (hợp mảnh/tối ưu hóa đĩa cứng) trên hệ điều hành Windows, hệ thống sẽ giúp ích gì cho máy tính của bạn?",
        "options": [
            "A. Xóa vĩnh viễn toàn bộ các tệp ảnh hưởng đến tốc độ của hệ điều hành.",
            "B. Sắp xếp lại các phần của tệp bị phân mảnh trên ổ đĩa để tăng tốc độ truy cập dữ liệu và nâng cao hiệu năng hoạt động.",
            "C. Tăng tốc độ kết nối mạng Wi-Fi lên gấp đôi.",
            "D. Xóa bớt dữ liệu, tăng tốc độ CPU và RAM.",
        ],
        "answer": "B",
    },
    {
        "id": 19,
        "question": "Một người dùng muốn chọn mua một chiếc máy tính xách tay phục vụ cho việc học tập văn phòng và xử lý các tác vụ đồ họa, biên tập video nặng. Dựa trên kiến thức về phần cứng máy tính, thông số nào sau đây là quan trọng nhất cần ưu tiên xem xét?",
        "options": [
            "A. Tốc độ xung nhịp CPU nhiều nhân và Dung lượng PIN.",
            "B. Tốc độ xung nhịp CPU nhiều nhân, dung lượng RAM lớn và card đồ họa rời chuyên dụng.",
            "C. Dung lượng PIN sử dụng được nhiều giờ và dung lượng RAM lớn.",
            "D. Công suất loa và thương hiệu màn hình hiển thị.",
        ],
        "answer": "B",
    },
    {
        "id": 20,
        "question": "Khi bạn đang làm việc với một tệp văn bản nhưng gặp sự cố tệp bị khóa hoặc không thể xóa/đổi tên được do đang mở trong một ứng dụng khác, biện pháp xử lý sự cố phần mềm thông thường phù hợp nhất là gì?",
        "options": [
            "A. Mang máy tính ra tiệm sửa chữa phần cứng ngay lập tức.",
            "B. Đóng ứng dụng đang mở tệp đó.",
            "C. Cài đặt lại toàn bộ hệ điều hành Windows từ đầu.",
            "D. Format lại toàn bộ ổ cứng máy tính.",
        ],
        "answer": "B",
    },
]

# Tạo menu lựa chọn giữa chế độ Học sinh làm bài và Giáo viên xem bảng điểm
st.sidebar.title("📌 Điều hướng")
role = st.sidebar.radio(
    "Chọn chế độ:", ("👨‍🎓 Học sinh làm bài", "👩‍🏫 Giáo viên xem bảng điểm")
)

if role == "👨‍🎓 Học sinh làm bài":
  st.title("💻 KIỂM TRA TRỰC TUYẾN MÔN TIN HỌC")
  st.markdown("---")

  # Nhập thông tin học sinh
  fullname = st.text_input(
      "Nhập họ và tên đầy đủ của em:", placeholder="Ví dụ: Nguyễn Văn A"
  )

  if fullname:
    st.info(
        f"Xin chào em **{fullname}**. Bài kiểm tra gồm 20 câu hỏi trắc nghiệm."
    )

    with st.form("quiz_form"):
      user_answers = {}
      for idx, q in enumerate(QUIZ_DATA):
        st.markdown(f"**Câu {idx + 1}:** {q['question']}")
        # Lấy chữ cái đầu tiên (A, B, C, D) làm lựa chọn
        choice = st.radio(
            "Chọn đáp án:",
            q["options"],
            key=f"q_{q['id']}",
            index=None,
            label_visibility="collapsed",
        )
        if choice:
          user_answers[str(q["id"])] = choice[0]  # Lấy ký tự đầu A/B/C/D
        st.write("")

      submitted = st.form_submit_button("🚀 Nộp bài thi")

      if submitted:
        if not fullname.strip():
          st.error("Vui lòng nhập họ và tên trước khi nộp bài!")
        else:
          # Chấm điểm
          score = 0
          total = len(QUIZ_DATA)
          for q in QUIZ_DATA:
            qid_str = str(q["id"])
            if (
                qid_str in user_answers
                and user_answers[qid_str] == q["answer"]
            ):
              score += 1

          final_score = round((score / total) * 10, 2)

          # Lưu kết quả vào danh sách chung
          submission = {
              "fullname": fullname,
              "score": final_score,
              "raw_score": f"{score}/{total}",
              "time": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
          }
          st.session_state.results_db.append(submission)

          st.success("🎉 Nộp bài thành công!")
          st.balloons()
          st.metric(
              label="Kết quả của bạn",
              value=f"{final_score} điểm",
              delta=f"Đúng {score}/{total} câu",
          )
  else:
    st.warning("⚠️ Vui lòng nhập họ và tên ở ô trên để hiển thị đề kiểm tra.")

elif role == "👩‍🏫 Giáo viên xem bảng điểm":
  st.title("📊 QUẢN LÝ BẢNG ĐIỂM HỌC SINH")
  st.markdown("---")

  if st.session_state.results_db:
    st.write(
        f"Tổng số bài đã nộp: **{len(st.session_state.results_db)}** học sinh"
    )

    # Hiển thị bảng kết quả
    st.table(st.session_state.results_db)

    if st.button("🗑️ Xóa toàn bộ dữ liệu bảng điểm"):
      st.session_state.results_db = []
      st.rerun()
  else:
    st.info("Hiện tại chưa có học sinh nào nộp bài.")