/*
    @author Stratos Gounidellis <stratos.gounidellis@gmail.com>
    @author Lamprini Koutsokera <lkoutsokera@gmail.com>
*/

/*
    Q1: Show the total 'Amount' of 'Type = 0' transactions at 'ATM Code = 21'
    of the last 10 minutes. Repeat as new events keep flowing 
    in (use a sliding window).
*/
SELECT
    SUM(CAST([BDSMastersInput].[Amount] AS BIGINT)) AS TotalAmount,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
WHERE CAST([BDSMastersInput].[Type] AS BIGINT) = 0 AND
      CAST([BDSMastersInput].[ATMCode] AS BIGINT) = 21
GROUP BY SlidingWindow(minute, 10)

/*
    Q2: Show the total 'Amount' of 'Type = 1' transactions at 'ATM Code = 21'
    of the last hour. Repeat once every hour (use a tumbling window).
*/
SELECT
    SUM(CAST([BDSMastersInput].[Amount] AS BIGINT)) AS TotalAmount,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
WHERE CAST([BDSMastersInput].[Type] AS BIGINT) = 1 AND
      CAST([BDSMastersInput].[ATMCode] AS BIGINT) = 21
GROUP BY TumblingWindow(hour, 1)

/*
    Q3: Show the total 'Amount' of 'Type = 1' transactions at 'ATM Code = 21'
    of the last hour. Repeat once every 30 minutes (use a hopping window).
*/
SELECT
    SUM(CAST([BDSMastersInput].[Amount] AS BIGINT)) AS TotalAmount,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
WHERE CAST([BDSMastersInput].[Type] AS BIGINT) = 1 AND 
      CAST([BDSMastersInput].[ATMCode] AS BIGINT) = 21
GROUP BY HoppingWindow(minute, 60, 30)

/*
    Q4: Show the total 'Amount' of 'Type = 1' transactions per 'ATM Code'
    of the last one hour (use a sliding window).
*/
SELECT
    CAST([BDSMastersInput].[ATMCode] AS BIGINT) AS AtmCode,
    SUM(CAST([BDSMastersInput].[Amount] AS BIGINT)) AS TotalAmount,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
WHERE CAST([BDSMastersInput].[Type] AS BIGINT) = 1
GROUP BY CAST([BDSMastersInput].[ATMCode] AS BIGINT), 
         SlidingWindow(hour, 1)

/*
    Q5: Show the total 'Amount' of 'Type = 1' transactions per 'Area Code'
    of the last hour. Repeat once every hour (use a tumbling window).
*/
SELECT
    CAST([atmRef].[area_code] AS BIGINT) AS AreaCode,
    SUM(CAST([BDSMastersInput].[Amount] AS BIGINT)) AS TotalAmount,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
INNER JOIN [atmRef]
    ON CAST([atmRef].[atm_code] AS BIGINT) = CAST([BDSMastersInput].[atmCode] AS BIGINT)
WHERE CAST([BDSMastersInput].[Type] AS BIGINT) = 1
GROUP BY CAST([atmRef].[area_code] AS BIGINT), 
         TumblingWindow(hour, 1)

/*
    Q6: Show the total 'Amount' per ATM's 'City' and Customer's 'Gender' 
    of the last hour. Repeat once every hour (use a tumbling window).
*/
SELECT
    [areaRef].[area_city] AS City,
    [customerRef].[gender] AS Gender,
    SUM(CAST([BDSMastersInput].[Amount] AS BIGINT)) AS TotalAmount,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
INNER JOIN [customerRef]
    ON CAST([customerRef].[card_number] AS BIGINT) = CAST([BDSMastersInput].[CardNumber] AS BIGINT)
INNER JOIN [atmRef]
    ON CAST([atmRef].[atm_code] AS BIGINT) = CAST([BDSMastersInput].[ATMCode] AS BIGINT)
INNER JOIN [areaRef]
    ON CAST([areaRef].[area_code] AS BIGINT) = CAST([atmRef].[area_code] AS BIGINT)
GROUP BY [areaRef].[area_city],
         [customerRef].[gender],
         TumblingWindow(hour, 1)

/*
    Q7: Alert (SELECT '1') if a Customer has performed two transactions
    of 'Type = 1' in a window of an hour (use a sliding window).
*/
SELECT
    [customerRef].[first_name] AS Name,
    [customerRef].[last_name] AS Surname,
    CAST([BDSMastersInput].[CardNumber] AS BIGINT) AS CardNo,
    COUNT (*) AS Transactions,
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
INNER JOIN [customerRef]
    ON CAST([customerRef].[card_number] AS BIGINT) = CAST([BDSMastersInput].[CardNumber] AS BIGINT)
WHERE CAST([BDSMastersInput].[Type] AS BIGINT) = 1
GROUP BY [customerRef].[first_name],
         [customerRef].[last_name],
         CAST([BDSMastersInput].[CardNumber] AS BIGINT),
         SlidingWindow(hour, 1)
HAVING Transactions = 2

/*
    Q8: Alert (SELECT '1') if the 'Area Code' of the ATM of the transaction 
    is not the same as the 'Area Code' of the 'Card Number' 
    (Customer's Area Code) - (use a sliding window).
*/
SELECT
    CAST([atmRef].[area_code] AS BIGINT) AS AtmAreaCode,
    CAST([customerRef].[area_code] AS BIGINT) AS CustomerAreaCode,
    COUNT (*),
    System.Timestamp AS Time
INTO
    [BDSMastersOutput]
FROM
    [BDSMastersInput]
INNER JOIN [customerRef]
    ON CAST([customerRef].[card_number] AS BIGINT) = CAST([BDSMastersInput].[CardNumber] AS BIGINT)
INNER JOIN [atmRef]
    ON CAST([atmRef].[atm_code] AS BIGINT) = CAST([BDSMastersInput].[ATMCode] AS BIGINT)
WHERE CAST([atmRef].[area_code] AS BIGINT) != CAST([customerRef].[area_code] AS BIGINT)
GROUP BY CAST([atmRef].[area_code] AS BIGINT),
         CAST([customerRef].[area_code] AS BIGINT), 
         SlidingWindow(hour, 1)
