from datetime import datetime
import random
import sqlite3
import pandas as pd
import streamlit as st

# --- CẤU HÌNH DATABASE SQLITE ---
DB_NAME = "ket_qua_thi.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            score REAL NOT NULL,
            raw_score TEXT NOT NULL,
            violations INTEGER NOT NULL,
            time TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()


init_db()


def save_result(fullname, score, raw_score, violations):
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  time_str = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
  cursor.execute(
      "INSERT INTO results (fullname, score, raw_score, violations, time) VALUES"
      " (?, ?, ?, ?, ?)",
      (fullname, score, raw_score, violations, time_str),
  )
  conn.commit()
  conn.close()


def get_all_results():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT fullname, score, raw_score, violations, time FROM results ORDER BY"
      " id DESC"
  )
  rows = cursor.fetchall()
  conn.close()
  return rows


def clear_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM results")
  conn.commit()
  conn.close()


# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Thi Trực Tuyến Môn Tin Học", page_icon="💻", layout="wide"
)

# Duy trì trạng thái đăng nhập của giáo viên không bị mất khi reload
if "teacher_logged_in" not in st.session_state:
  st.session_state.teacher_logged_in = False

# Danh sách gốc 20 câu hỏi trắc nghiệm
ORIGINAL_QUIZ_DATA = [
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
            "C. Cài đặt lại toàn bộ hệ thống mạng LAN của phòng máy.",
            "D. Mua ngay hệ điều hành bản quyền mới.",
        ],
        "answer": "B",
    },
    {
        "id": 18,
        "question": "Khi sử dụng tiện ích Optimize (hợp mảnh/tối ưu hóa đĩa cứng) trên hệ điều hành Windows, hệ thống sẽ giúp ích gì cho máy tính của bạn?",
        "options": [
            "A. Xóa vĩnh viễn toàn bộ các tệp ảnh hưởng đến tốc độ.",
            "B. Sắp xếp lại các phần của tệp bị phân mảnh trên ổ đĩa để tăng tốc độ truy cập dữ liệu và nâng cao hiệu năng hoạt động.",
            "C. Tăng tốc độ kết nối mạng Wi-Fi lên gấp đôi.",
            "D. Xóa bớt dữ liệu, tăng tốc độ CPU.",
        ],
        "answer": "B",
    },
    {
        "id": 19,
        "question": "Một người dùng muốn chọn mua một chiếc máy tính xách tay phục vụ cho việc học tập văn phòng và xử lý các tác vụ đồ họa, biên tập video nặng. Thông số nào là quan trọng nhất cần ưu tiên?",
        "options": [
            "A. Tốc độ xung nhịp CPU nhiều nhân và Dung lượng PIN.",
            "B. Tốc độ xung nhịp CPU nhiều nhân, dung lượng RAM lớn và card đồ họa rời chuyên dụng.",
            "C. Dung lượng PIN và RAM lớn.",
            "D. Công suất loa và thương hiệu màn hình.",
        ],
        "answer": "B",
    },
    {
        "id": 20,
        "question": "Khi bạn đang làm việc với một tệp văn bản nhưng gặp sự cố tệp bị khóa hoặc không thể xóa/đổi tên được do đang mở trong ứng dụng khác, biện pháp xử lý phù hợp nhất là gì?",
        "options": [
            "A. Mang máy tính ra tiệm sửa chữa phần cứng ngay.",
            "B. Đóng ứng dụng đang mở tệp đó.",
            "C. Cài đặt lại toàn bộ hệ điều hành.",
            "D. Format lại toàn bộ ổ cứng.",
        ],
        "answer": "B",
    },
]

# Menu chọn chế độ
st.sidebar.title("📌 Điều Hướng")
role = st.sidebar.radio(
    "Chọn chế độ:", ("👨‍🎓 Học sinh làm bài", "👩‍🏫 Giáo viên quản lý")
)

if role == "👨‍🎓 Học sinh làm bài":
  st.title("💻 HỆ THỐNG KIỂM TRA TRỰC TUYẾN MÔN TIN HỌC")
  st.markdown("---")

  fullname = st.text_input(
      "Nhập họ và tên đầy đủ của em:", placeholder="Ví dụ: Nguyễn Văn A"
  )

  if fullname:
    st.info(
        f"Xin chào em **{fullname}**. Bài kiểm tra gồm 20 câu hỏi trắc nghiệm."
        " Thời gian làm bài: 15 phút."
    )

    # Đảo thứ tự câu hỏi và xáo trộn đáp án riêng cho mỗi học sinh khi load trang
    if "shuffled_quiz" not in st.session_state or st.session_state.get(
        "current_user"
    ) != fullname:
      st.session_state.current_user = fullname
      # Copy và xáo trộn danh sách câu hỏi
      shuffled_questions = list(ORIGINAL_QUIZ_DATA)
      random.shuffle(shuffled_questions)

      # Xáo trộn các phương án lựa chọn trong từng câu hỏi và lưu lại đáp án đúng tương ứng
      processed_quiz = []
      for q in shuffled_questions:
        # Tách lấy chữ cái đáp án đúng cũ (ví dụ "C") và nội dung tương ứng
        correct_text = next(
            opt for opt in q["options"] if opt.startswith(q["answer"])
        )

        options = list(q["options"])
        random.shuffle(options)

        # Tìm lại ký tự nhãn mới sau khi xáo trộn (A, B, C, D)
        new_correct_letter = ""
        new_options = []
        labels = ["A", "B", "C", "D"]
        for idx, opt in enumerate(options):
          # Lấy nội dung sau dấu chấm (ví dụ " 2009")
          opt_content = opt.split(".", 1)[1]
          new_opt_str = f"{labels[idx]}.{opt_content}"
          new_options.append(new_opt_str)
          if opt == correct_text:
            new_correct_letter = labels[idx]

        processed_quiz.append({
            "id": q["id"],
            "question": q["question"],
            "options": new_options,
            "answer": new_correct_letter,
        })
      st.session_state.shuffled_quiz = processed_quiz
      st.session_state.violation_count = 0

    quiz_to_render = st.session_state.shuffled_quiz

    # Script JavaScript giám sát vi phạm & đếm ngược thời gian
    timer_violation_html = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #f8f9fa; padding: 10px 15px; border-radius: 8px; border: 1px solid #dee2e6; margin-bottom: 20px;">
            <div>
                <span style="font-weight: bold; color: #dc3545;">⚠️ Số lần vi phạm (Chuyển tab/Thu nhỏ): </span>
                <span id="violation-display" style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">0</span> lần
            </div>
            <div>
                <span style="font-weight: bold; color: #0d6efd;">⏳ Thời gian còn lại: </span>
                <span id="countdown-timer" style="font-size: 1.2rem; font-weight: bold; color: #0d6efd;">15:00</span>
            </div>
        </div>

        <input type="hidden" id="hidden_violations" value="0">

        <script>
        let totalSeconds = 15 * 60;
        const timerElement = document.getElementById("countdown-timer");
        
        const countdownInterval = setInterval(function() {{
            if (totalSeconds <= 0) {{
                clearInterval(countdownInterval);
                alert("Đã hết thời gian làm bài! Hệ thống sẽ tự động nộp bài.");
                const submitBtns = parent.document.querySelectorAll('button');
                submitBtns.forEach(btn => {{
                    if (btn.innerText.includes("Nộp Bài Thi")) {{
                        btn.click();
                    }}
                }});
                return;
            }}
            totalSeconds--;
            let minutes = Math.floor(totalSeconds / 60);
            let seconds = totalSeconds % 60;
            timerElement.innerText = (minutes < 10 ? "0" : "") + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
        }}, 1000);

        let vCount = 0;
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                vCount++;
                document.getElementById("violation-display").innerText = vCount;
                // Đồng bộ giá trị vào input ẩn để Streamlit nhận diện được
                const hiddenInput = document.getElementById("hidden_violations");
                if (hiddenInput) {{
                    hiddenInput.value = vCount;
                    hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
                alert("⚠️ CẢNH BÁO: Phát hiện bạn vừa rời khỏi màn hình thi (chuyển tab hoặc thu nhỏ cửa sổ)! Hành vi này đã được ghi nhận.");
            }}
        }});
        </script>
        """
    st.components.v1.html(timer_violation_html, height=70)

    with st.form("quiz_form"):
      user_answers = {}
      for idx, q in enumerate(quiz_to_render):
        st.markdown(f"**Câu {idx + 1}:** {q['question']}")
        choice = st.radio(
            "Chọn đáp án:",
            q["options"],
            key=f"q_{q['id']}",
            index=None,
            label_visibility="collapsed",
        )
        if choice:
          user_answers[str(q["id"])] = choice[
              0
          ]  # Lấy ký tự chữ cái đầu A, B, C, D
        st.write("")

      # Thêm ô ẩn nhận số lần vi phạm từ JS
      violations_input = st.text_input(
          "violations_hidden", value="0", label_visibility="collapsed"
      )

      submitted = st.form_submit_button("🚀 Nộp Bài Thi")

      if submitted:
        if not fullname.strip():
          st.error("Vui lòng nhập họ và tên trước khi nộp bài!")
        else:
          score = 0
          total = len(quiz_to_render)
          for q in quiz_to_render:
            qid_str = str(q["id"])
            if (
                qid_str in user_answers
                and user_answers[qid_str] == q["answer"]
            ):
              score += 1

          final_score = round((score / total) * 10, 2)

          # Lấy số lần vi phạm thực tế từ form
          try:
            recorded_violations = int(violations_input)
          except:
            recorded_violations = 0

          # Lưu vào cơ sở dữ liệu SQLite vĩnh viễn
          save_result(
              fullname, final_score, f"{score}/{total}", recorded_violations
          )

          st.success(
              "🎉 Nộp bài thi thành công! Điểm và lỗi vi phạm đã được cập nhật"
              " vào hệ thống."
          )
          st.balloons()
          st.metric(
              label="Kết quả của bạn",
              value=f"{final_score} điểm",
              delta=f"Đúng {score}/{total} câu",
          )
  else:
    st.warning("⚠️ Vui lòng nhập họ và tên ở ô phía trên để bắt đầu làm bài.")

elif role == "👩‍🏫 Giáo viên quản lý":
  st.title("🔐 ĐĂNG NHẬP HỆ THỐNG GIÁO VIÊN")
  st.markdown("---")

  if not st.session_state.teacher_logged_in:
    with st.form("login_form"):
      username = st.text_input("Tên đăng nhập:")
      password = st.text_input("Mật khẩu:", type="password")
      login_btn = st.form_submit_button("Đăng Nhập")

      if login_btn:
        if username == "admin" and password == "Giaovien@2026":
          st.session_state.teacher_logged_in = True
          st.success("Đăng nhập thành công!")
          st.rerun()
        else:
          st.error("Sai tên đăng nhập hoặc mật khẩu!")
  else:
    col1, col2 = st.columns([4, 1])
    with col1:
      st.title("📊 BẢNG ĐIỂM & GIÁM SÁT LỖI VI PHẠM HỌC SINH")
    with col2:
      if st.button("Đăng Xuất"):
        st.session_state.teacher_logged_in = False
        st.rerun()

    st.markdown("---")

    # Tự động làm mới bảng điểm mỗi 5 giây để giáo viên xem trực tiếp học sinh nộp bài mà không cần bấm reload
    from streamlit_autorefresh import st_autorefresh

    st_autorefresh(interval=5000, limit=1000000, key="datarefresh")

    rows = get_all_results()

    if rows:
      st.write(f"Tổng số học sinh đã nộp bài: **{len(rows)}**")

      df = pd.DataFrame(
          rows,
          columns=[
              "Họ và Tên",
              "Điểm Số (Hệ 10)",
              "Số Câu Đúng",
              "Số Lần Vi Phạm",
              "Thời Gian Nộp",
          ],
      )
      st.dataframe(df, use_container_width=True)

      if st.button("🗑️ Xóa toàn bộ dữ liệu bảng điểm"):
        clear_db()
        st.rerun()
    else:
      st.info(
          "Hiện tại chưa có học sinh nào nộp bài. Bảng sẽ tự động cập nhật khi"
          " có học sinh nộp."
      )
