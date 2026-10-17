-- 按部门统计薪资前三名
WITH ranked AS (
    SELECT
        employee_id,
        department_id,
        salary,
        RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
    FROM employees
    WHERE department_id IN (2, 3, 7, 8)
)
SELECT employee_id, department_id, salary, salary_rank
FROM ranked
WHERE salary_rank <= 3
ORDER BY department_id, salary_rank;
