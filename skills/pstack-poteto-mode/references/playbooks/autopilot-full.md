# autopilot-full

First confirm that this task authorizes creating, pushing, and merging every target PR. Give each PR one owner and a separate workspace. The owner implements, verifies, handles review, and checks CI. A coordinator independently verifies the current SHA before any merge. Without merge authorization, deliver review-ready results. Bound concurrency and time, propagate stop requests, and use real scheduling for durable operation. Writing “run in background” is not scheduling.
