# **Who is the Greatest F1 Driver of All Time?**

This project explores the fascinating question of who the greatest Formula 1 driver of all time is, using a data-driven approach. By analyzing performances relative to teammates, teams, and competitors across various eras, we aim to bring objectivity to this perennial debate.

The analysis is powered by a **custom, comprehensive dataset**, meticulously scraped and cleaned from official Formula 1 sources and race archives. No pre-made datasets were used, ensuring the data is complete, accurate, and tailored for this project.

---

## **Project Overview**

Formula 1 is a sport of immense complexity, where success depends not only on driver skill but also on team dynamics, car performance, and the competitive landscape. This project leverages historical F1 data to compare drivers using metrics that normalize for these variables, such as:

- Performance relative to teammates in identical machinery.
- Performance compared to competitors in similar competitive contexts.
- Adjusted metrics for dominance during an era (e.g., driver skill vs. car advantage).

The custom dataset includes detailed information from every race since Formula 1 began in 1950, including qualifying, race results, lap-by-lap performance, and contextual data such as weather and circuit characteristics.

---

## **Features**

- **Teammate Comparisons**: Assessing how drivers performed relative to their teammates.
- **Competitive Context Analysis**: Evaluating performance relative to other drivers on the grid.
- **Team Performance Adjustments**: Accounting for car performance differences across seasons.
- **Era Normalization**: Normalizing metrics to compare drivers from different eras.
- **Custom Visualizations**: Providing compelling visual insights into driver dominance and consistency.

---

## **Data Sources**

This project is built entirely on a **custom dataset** created by scraping data from official Formula 1 sources, historical race archives, and other publicly available records. The dataset includes:

- Detailed race results for every season since 1950.
- Qualifying and lap-by-lap data.
- Teammate and team performance metrics.
- Contextual data like weather, circuit characteristics, and car specifications.

All data was scraped, cleaned, and processed into a unified format specifically for this analysis.

---

## **Methodology**

1. **Data Collection and Preprocessing**  
   - Scraping data from official Formula 1 race archives and public resources.
   - Cleaning and transforming raw HTML tables, PDFs, and other formats into structured datasets.

2. **Feature Engineering**  
   - Calculating performance metrics such as win percentage, qualifying gaps, and points per race.
   - Creating teammate comparison metrics and car performance indices.

3. **Modeling and Analysis**  
   - Statistical modeling to evaluate driver skill independently of car performance.
   - Comparing drivers within the same team and across different teams.
   - Clustering drivers by era and normalizing performance data.

4. **Visualization**  
   - Building visualizations to showcase trends and performance highlights.
   - Generating driver ranking charts and heatmaps.

---
