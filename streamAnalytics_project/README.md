<img src="../logos/logoAUEB.png" width="280" height="80" align="right"></img>
<img src="../logos/dmst.png" width="200" height="80" align="left"></img><br><br>
<br><br><br>
[![BDSMasters](https://img.shields.io/badge/codedby-bdsmasters-brightgreen.svg?style=flat-square)](https://github.com/dbsmasters)
![stream analytics](https://img.shields.io/badge/stream-analytics-blue.svg?style=flat-square)

### <a id="contents" href="#contents">Contents</a>

1. [Azure Stream Anlytcis Project: On-demand real-time analytics](#azure-stream-project-intro)
1. [Azure Stream Analytics: Configuration](#configuring-azure)
1. [Azure Stream Analytics: Output to PowerBI](#power-bi)
1. [Azure Stream Analytics: Queries](#queries-execution)
1. [Team](#team)
1. [See also](#see-also)

### <a id="azure-stream-project-intro" href="#azure-stream-project-intro">Azure Stream Anlytcis Project: On-demand real-time analytics</a>

This assignment is a part of a project implemented in the context of the course "Big Data Management Systems" taught by Prof. Chatziantoniou in the Department of Management Science and Technology (AUEB). The aim of the project is to familiarize the students with big data management systems such as Hadoop, Redis, MongoDB and Neo4j.

In the context of this assignment on Stream Analytics, Azure Stream Analytics will be used in order to process a data stream of ATM transactions and answer stream queries. The schema of the stream is the following: (ATMCode, CardNumber, Type, Amount).

A detailed description of the assignment can be found [here](Proj4_StreamAnalytics_Description.pdf).

### <a id="configuring-azure" href="#configuring-azure">Azure Stream Analytics: Configuration</a>

In order to execute stream processes and queries on Azure Stream Analytics platform the following steps are required:

1. Create an **Azure account**.
2. Setup an **Event Hub**.
3. **Feed** the Event Hub with data.
4. Setup a **Storage account**.
5. Upload the **Reference Data** files (if any).
6. Create a **Blob Storage Output**.
7. Setup a **Stream Analytics Job**.
8. Use the Event Hub and/or Reference Data Files as **Input**.
9. **Run** the queries.

More information can be found [here](https://docs.microsoft.com/en-us/azure/stream-analytics/).

### <a id="power-bi" href="#power-bi">Azure Stream Analytics: Output to PowerBI</a>

In order to connect Azure Stream Anlytics with **PowerBI**, the following steps are required:

1. Select the Outputs box in the middle of the job dashboard. Then select + Add to create your output.
2. Select Authorize.
3. A window opens where you can provide your Azure credentials (for a work or school account). It also provides your Azure job with access to your Power BI area.
4. The authorization disappears after you've provided the necessary information. The New output area has fields for the Dataset Name and Table Name.
5. Select Create. 

More information can be found [here](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-power-bi-dashboard).

### <a id="queries-execution" href="#queries-execution">Azure Stream Analytics: Queries</a>

The following queries are designed and expressed in a **SQL-like language**, in order to be executed on the Azure Stream analytics platform:

1. Show the total 'Amount' of 'Type = 0' transactions at 'ATM Code = 21' of the last 10 minutes. Repeat as new events keep flowing in (use a sliding window).
2. Show the total 'Amount' of 'Type = 1' transactions at 'ATM Code = 21' of the last hour. Repeat once every hour (use a tumbling window).
3. Show the total 'Amount' of 'Type = 1' transactions at 'ATM Code = 21' of the last hour. Repeat once every 30 minutes (use a hopping window).
4. Show the total 'Amount' of 'Type = 1' transactions per 'ATM Code' of the last one hour (use a sliding window).
5. Show the total 'Amount' of 'Type = 1' transactions per 'Area Code' of the last hour. Repeat once every hour (use a tumbling window).
6. Show the total 'Amount' per ATM’s 'City' and Customer’s 'Gender' of the last hour. Repeat once every hour (use a tumbling window).
7. Alert (SELECT '1') if a Customer has performed two transactions of 'Type = 1' in a window of an hour (use a sliding window).
8. Alert (SELECT “1”) if the “Area Code” of the ATM of the transaction is not the same as the “Area Code” of the “Card Number” (Customer’s Area Code) - (use a sliding window).

### <a id="team" href="#team">Team</a>
|[![Lamprini Koutsokera](https://s.gravatar.com/avatar/fbf0a9ea90d21fda02132701e8082bf2?s=144)](https://github.com/lamprini-koutsokera)|[![Stratos Gounidellis](https://s.gravatar.com/avatar/761a071e4bb22145269c5b33aab8249d?s=144)](https://github.com/stratos-gounidellis)|
|---|---|
|[![Lamprini Koutsokera](https://img.shields.io/badge/Lamprini-Koutsokera-brightgreen.svg?style=flat-square)](https://github.com/lamprini-koutsokera)|[![Stratos Gounidellis](https://img.shields.io/badge/Stratos-Gounidellis-blue.svg?style=flat-square)](https://github.com/stratos-gounidellis)|

### <a id="see-also" href="#see-also">See also</a>

External resources

* [Azure Stream Analytics Documentation - Tutorials, API Reference - Docs.microsoft.com.](https://docs.microsoft.com/en-us/azure/stream-analytics/)
