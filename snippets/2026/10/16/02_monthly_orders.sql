-- 用 CTE 汇总每月订单金额
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS order_count,
        SUM(amount) AS total_amount
    FROM orders
    WHERE created_at >= DATE '2024-12-01'
    GROUP BY 1
)
SELECT
    month,
    order_count,
    total_amount,
    ROUND(total_amount / NULLIF(order_count, 0), 2) AS avg_amount
FROM monthly
ORDER BY month DESC
LIMIT 8;
