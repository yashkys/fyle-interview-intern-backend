-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grading_counts AS (
    SELECT teacher_id, COUNT(*) AS graded_assignments
    FROM assignments WHERE state = 'GRADED' GROUP BY teacher_id
),
max_teacher AS (
    SELECT teacher_id
    FROM teacher_grading_counts ORDER BY graded_assignments DESC LIMIT 1
)
SELECT COUNT(*) AS grade_A_count 
FROM assignments WHERE teacher_id = (SELECT teacher_id FROM max_teacher) AND grade = 'A';
