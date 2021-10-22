USE [HR_sample_database];

/*Viết một câu truy vấn để hiển thị full_name (first_name + last_name) 
 và mức lương của nhân viên không nằm trong phạm vi từ $10000 đến $15000*/
SELECT
  [first_name] + ' ' + [last_name] AS full_name,
  salary
FROM
  [dbo].[employees]
WHERE
  salary NOT BETWEEN 10000
  AND 15000;

/*Viết truy vấn để hiển thị nhân viên có [first_name] có ký tự thứ ba là 'e'*/
SELECT
  *
FROM
  [dbo].[employees]
WHERE
  [first_name] like '_e%';

/*Viết một truy vấn để hiển thị full_name và ngày tuyển dụng của các nhân viên đã thuê năm 1997*/
SELECT
  [first_name] + ' ' + [last_name] AS full_name,
  hire_date
FROM
  [dbo].[employees]
WHERE
  hire_date > convert(date, '1996-12-31')
  and hire_date < convert(date, '1998-01-01');

/*Viết một truy vấn để hiển thị nhân viên làm việc ở phòng IT */
SELECT
  *
FROM
  [dbo].[employees] e
WHERE
  department_id = (
    SELECT
      department_id
    FROM
      [dbo].[departments]
    WHERE
      department_name = 'IT'
  );

/*Viết truy vấn để tìm nhân viên có quản lý làm việc tại US*/
SELECT
  *
FROM
  [dbo].[employees] e
  JOIN [dbo].[departments] d ON e.department_id = d.department_id
  JOIN [dbo].[locations] l ON d.location_id = l.location_id
WHERE
  e.employee_id IN (
    SELECT
      distinct manager_id
    FROM
      [dbo].[employees]
  )
  AND l.country_id = 'US';

/*Viết truy vấn để hiển thị first_name, last_name , công việc và mức lương của nhân viên có công việc Programmer or Shipping Clerk và lương không bằng $4500, $10000 hoặc $15000*/
SELECT
  [first_name],
  [last_name],
  [phone_number],
  job_title,
  [salary]
FROM
  [dbo].[employees] e
  JOIN [dbo].[jobs] j ON e.job_id = j.job_id
WHERE
  j.job_title IN ('Programmer', 'Shipping Clerk')
  AND salary NOT IN (4500, 10000, 15000);

/*Viết truy vấn để hiển thị first_name, last_name, phone_number. phone_number có chuỗi con '123' sẽ được thay thế bằng '999', nếu NULL hiển thị '-'*/
SELECT
  [first_name],
  [last_name],
  COALESCE(REPLACE(phone_number, '123', '999'), '-') AS phone_number,
  [salary]
FROM
  [dbo].[employees];

/*Viết truy vấn để hiển thị tên, email mới cho nhân viên (last_name@email.com) nếu trùng tên sẽ thêm số vào email: last_name1@email.com, last_name2@email.com theo thứ tự gia nhập.
 Gợi ý: dùng ROW_NUMBER () */
SELECT
  first_name,
  last_name,
  last_name + CASE
    WHEN ROW_NUMBER() OVER(
      PARTITION BY last_name
      ORDER BY
        hire_date ASC
    ) = 1 THEN ''
    ELSE CONVERT(
      varchar,
      ROW_NUMBER() OVER(
        PARTITION BY last_name
        ORDER BY
          hire_date ASC
      ) -1
    )
  END + '@email.com' AS new_email
FROM
  [dbo].[employees]