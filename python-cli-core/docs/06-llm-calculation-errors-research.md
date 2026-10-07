# **Key Recent Papers & Findings**

| **Paper** | **Core Claim / Findings** | **Why LLMs Err in Math / Calculation** |
| --- | --- | --- |
| Mathematical Computation and Reasoning Errors by Large Language Models (2025) | Benchmarking arithmetic, algebra, and number theory tasks; identify step-level error types. | Procedural “slips” (arithmetic errors, simplification mistakes) are the dominant error class; logical errors and missing steps also common. |
| Right Is Not Enough: The Pitfalls of Outcome Supervision in Training LLMs for Math Reasoning (2025) | Correct answers can arise from flawed reasoning (“reward hacking”); process correctness lags answer correctness. | Models may memorize “shortcuts” to correct answer without understanding math steps; supervision only on final answer fails to enforce sound reasoning. |
| Large Language Models and Mathematical Reasoning Failures (2025) | Using new high school word problems; analyze both answers and reasoning steps. | Errors include spatial reasoning, over-reliance on numeric patterns, poor handling of real-world semantics, and arithmetic blunders even when reasoning path is plausible. |
| Can LLMs Reason Abstractly Over Math Word Problems Without CoT? (2025) | Decompose math performance into abstract formulation vs arithmetic computation; show computation is often the bottleneck. | The model often formulates equations correctly (abstract step) but fails in executing the arithmetic accurately. Chain-of-thought helps mostly with the computation, not the abstraction. |
| Can LLMs understand Math? Exploring the Pitfalls in Mathematical Reasoning (2025) | Proposes a multi-stage evaluation to reveal hidden reasoning/miscalculation issues. | Many errors are masked when only final answer is judged; models make misinterpretations, invalid logic, or incoherent steps even if final result looks correct. |
| Over-Reasoning and Redundant Calculation of Large Language Models (2024) | LLMs tend to add unnecessary calculations even when the problem is trivial. | Redundant steps increase the exposure to arithmetic errors; models sometimes hallucinate or introduce variables. Also, reward models may prefer longer (more verbose) explanations, encouraging over-calculation. |
| LLMs can Find Mathematical Reasoning Mistakes (2024) | On self-correction: LLMs can partly detect and fix their errors, but struggle in many cases. | Detecting mistakes is itself hard; sometimes the model’s error is subtle or misleads the self-checking procedure. |

# **Synthesis: Why LLMs Fail in “Simple” Calculations**

From the literature, we can summarize a set of interacting reasons why LLMs often fail to compute correctly:

1. Arithmetic / Procedural Slips
    - Even if the reasoning structure is fine, performing multi-digit arithmetic (carry, borrowing, sign errors) is error-prone for a token-based model.
    - Simplification errors (algebraic mistakes) occur when combining or rearranging expressions.
    - Models lack the low-level deterministic arithmetic circuitry that symbolic systems or calculators have.
2. 
3. Reward / Training Pressure on Output Rather than Process
    - Many LLMs are trained (via reinforcement learning with human feedback) to maximize “good-looking” answers; they often get rewarded for correct final answer (or plausible answer) even if internal reasoning is flawed (“reward hacking”). (“Right Is Not Enough”)
    - Reward models may favor verbose outputs or longer explanations, pushing the model to over-reason or over-calculate. (“Over-Reasoning and Redundant Calculation”)
4. 
5. Separation of Abstraction vs Computation
    - Research shows that abstraction (figuring out what equations to write) and computation (solving those equations) are distinct, and many failures happen in the computation step. (“Can LLMs Reason Abstractly …”)
    - Even when the model “knows” the right steps, the arithmetic computation is the weak link.
6. 
7. Inadequate Error Detection / Self-Correction
    - LLMs often fail to detect their own errors, especially subtle arithmetic slips. (“LLMs can Find Mathematical Reasoning Mistakes”)
    - Self-correcting approaches help but are not perfect — the model may amplify earlier errors or misjudge which step is wrong.
8. 
9. Overcomplex / Unnecessary Reasoning (“Over-Reasoning”)
    - For some problems, no calculation is needed, but LLMs still insert chains of reasoning, increasing the chance of mistakes. (“Over-Reasoning …”)
    - Redundant reasoning also makes the answer less clear and more error-prone.
10. 
11. Generalization / Out-of-Distribution Strain
    - LLMs may “memorize patterns” and interpolate, but when asked tasks outside their training distribution (
12. 

---

Dưới đây là bản tóm tắt các nghiên cứu mới nhất trên arXiv (2024–2025) về lý do vì sao các mô hình ngôn ngữ lớn (LLM) thường “tính sai” hoặc mắc lỗi trong lập luận toán học, được viết bằng tiếng Việt dễ hiểu 👇

# **🔍 Tổng hợp các bài báo mới trên arXiv**

| **Bài báo** | **Phát hiện chính** | **Nguyên nhân LLM tính sai** |
| --- | --- | --- |
| Mathematical Computation and Reasoning Errors by LLMs (2025) | Thống kê lỗi số học, đại số, lý luận toán trên nhiều bài kiểm tra. | Phần lớn lỗi là “trượt tay” trong phép tính (cộng/trừ sai, rút gọn sai). Cấu trúc lập luận đúng nhưng phép tính cụ thể lại sai. |
| Right Is Not Enough: The Pitfalls of Outcome Supervision (2025) | Việc huấn luyện chỉ dựa trên đáp án cuối cùng khiến mô hình “ăn gian” được điểm. | Mô hình học mẹo ra kết quả đúng mà không hiểu lý do. Bị “hacker reward”: được thưởng vì đúng kết quả chứ không vì lập luận đúng. |
| Large Language Models and Mathematical Reasoning Failures (2025) | Dùng bài toán thực tế cấp 3 để đánh giá. | Sai vì hiểu sai ngữ cảnh, suy luận theo khuôn mẫu số học, lẫn lộn giữa logic và phép tính. |
| Can LLMs Reason Abstractly Over Math Word Problems Without CoT? (2025) | Phân tách khả năng “hiểu bài” và “tính toán”. | Mô hình thường viết đúng công thức, nhưng làm sai bước tính (ví dụ 3×7+5=25). Chain-of-thought chỉ giúp phần tính toán, không giúp hiểu bài. |
| Can LLMs Understand Math? Exploring the Pitfalls (2025) | Đề xuất đánh giá theo từng giai đoạn để phát hiện lỗi ẩn. | Nhiều bài trông như đúng, nhưng khi phân tích từng bước thì sai logic hoặc thiếu bước trung gian. |
| Over-Reasoning and Redundant Calculation in LLMs (2024) | Phát hiện hiện tượng “làm quá mức cần thiết”. | Mô hình thêm bước tính dư thừa, tăng khả năng sai. Cũng có thể do huấn luyện RLHF thưởng cho câu trả lời dài, khiến mô hình “tính vòng vo”. |
| LLMs Can Find Mathematical Reasoning Mistakes (2024) | Nghiên cứu khả năng tự phát hiện lỗi. | LLM đôi khi nhận ra lỗi của chính mình, nhưng thường đánh giá sai lỗi tinh vi hoặc sửa sai bằng cách sai khác. |

# **⚙️ Vì sao LLM thường “tính sai”**

1. Lỗi số học (arithmetic slips)
    - Mô hình không có “mạch tính toán chính xác” như máy tính, chỉ dựa vào mô hình ngôn ngữ.
    - Dễ sai ở phép nhân/chia nhiều chữ số hoặc rút gọn biểu thức phức tạp.
2. 
3. Huấn luyện chỉ chú trọng đáp án cuối cùng
    - Mô hình được thưởng khi ra kết quả “đẹp”, nên học cách “đoán đúng” thay vì suy luận đúng.
    - Giống học sinh chép kết quả mà không hiểu cách làm.
4. 
5. Phân tách giữa “hiểu bài” và “tính toán”
    - LLM có thể diễn giải đúng đề, đặt được phương trình, nhưng tính sai kết quả.
    - Đây là lỗi phổ biến nhất hiện nay.
6. 
7. Không tự phát hiện lỗi
    - Khi tự kiểm tra, mô hình thường “tin vào chính mình”.
    - Các phương pháp “self-consistency” hoặc “reflection” giúp được phần nào, nhưng chưa đủ.
8. 
9. Lập luận vòng vo, dư thừa
    - Với bài đơn giản, thay vì trả lời ngắn, mô hình lại “lý luận vòng” → càng nhiều bước càng dễ sai.
    - Do cơ chế RLHF thưởng cho câu trả lời dài, chi tiết.
10. 
11. Không tổng quát tốt (out-of-distribution)
    - Khi gặp số lớn, công thức lạ hoặc ngữ cảnh không quen, mô hình dễ “vỡ logic”.
    - Ngôn ngữ tự nhiên cho phép sai sót nhỏ, còn toán học thì không.
12. 
13. Cách đánh giá chưa đúng
    - Nhiều bài chỉ chấm kết quả cuối cùng mà không chấm “quá trình lập luận”, nên không thấy lỗi thật.
14. 

# **🧭 Hướng cải thiện trong tương lai**

- Huấn luyện dựa trên “quy trình đúng” thay vì “kết quả đúng” (Process-based RLHF).
- Kết hợp mô hình ngôn ngữ với máy tính hoặc công cụ symbolic (Python, SymPy) để xử lý phép tính chính xác.
- Đánh giá từng bước (step-level evaluation) thay vì chỉ nhìn kết quả.
- Phát triển các mô hình “self-refinement” có khả năng kiểm lỗi toán học trước khi xuất ra kết quả cuối.

Nếu bạn muốn, tôi có thể lấy danh sách 10 bài báo arXiv gần nhất (trong 2 tháng qua) về mathematical reasoning errors in LLMs và tóm tắt chi tiết nội dung từng bài.

