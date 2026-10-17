-- 找出同一部门内薪资高于直属上级的员工
SELECT
    e.employee_id,
    e.name AS employee_name,
    m.name AS manager_name,
    e.salary,
    m.salary AS manager_salary
FROM employees AS e
JOIN employees AS m ON m.employee_id = e.manager_id
WHERE e.department_id = 3
  AND e.salary > m.salary
ORDER BY e.salary DESC;
