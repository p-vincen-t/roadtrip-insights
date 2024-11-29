<h1 align="center" style="border-bottom: none">
    RoadTrip Insights - Vehicle Operational Data Management Application
</h1>

<div align="center">
  <a href="https://github.com/your_username/RoadTrip-Insights/releases"><img src="https://img.shields.io/github/tag-pre/your_username/RoadTrip-Insights.svg?color=blueviolet" alt="Last Version" /></a>
  <a href="https://github.com/your_username/RoadTrip-Insights/blob/develop/LICENSE"><img src="https://img.shields.io/github/license/your_username/RoadTrip-Insights?color=blueviolet" alt="License" /></a>
  <a href="https://github.com/your_username/RoadTrip-Insights/stargazers"><img src="https://img.shields.io/github/stars/your_username/RoadTrip-Insights?color=blueviolet&logo=github" alt="Github star" /></a> <br>
  <a href="https://your_website.com"><img src="https://img.shields.io/badge/Website-your_website.com-192A4E?color=blueviolet" alt="RoadTrip Insights Website"></a>
  <a href="https://your_slack.com"><img src="https://img.shields.io/badge/Slack-Join%20Community-blueviolet?logo=slack" alt="Slack"></a>
</div>

<br />

<p align="center">
    <a href="https://x.com/your_twitter"><img height="25" src="https://your_website.com/twitter.svg" alt="X(formerly Twitter)" /></a> &nbsp;
    <a href="https://www.linkedin.com/company/your_linkedin/"><img height="25" src="https://your_website.com/linkedin.svg" alt="linkedin" /></a> &nbsp;
    <a href="https://www.youtube.com/@your_youtube"><img height="25" src="https://your_website.com/youtube.svg" alt="youtube" /></a> &nbsp;
</p>

<p align="center">
    <a href="https://your_website.com/get-started-video" target="_blank">
        <img src="https://your_website.com/startvideo.png" alt="Get started in 4 minutes with RoadTrip Insights" width="640px" />
    </a>
</p>
<p align="center" style="color:grey;"><i>Click on the image to learn how to get started with RoadTrip Insights in 4 minutes.</i></p>

## 🌟 What is RoadTrip Insights?

RoadTrip Insights is a Streamlit application designed to manage and analyze vehicle operational data, including daily income/expenses and trip details. The purpose of the application is to provide a comprehensive dashboard for tracking and visualizing financial and trip data, helping users make informed decisions based on real-time data.

**Key Features:**
- **Daily Income & Expense Management:** Input and track daily income and expenses categorized by type (Revenue, Fuel, Repair, Spare Parts). Data is stored in a PostgreSQL database.
- **Trip Data Handling:** Upload trip data from CSV or PDF files. Data is stored in an InfluxDB time-series database.
- **Dashboard & Visualization:** Interactive charts and tables visualize financial data and trip reports (daily income/expenses, profit/loss, total distance, average trip duration, trip timeline).
- **Data Clearing:** Clear all trip data from InfluxDB.
- **Financial Chart Creation:** Create financial charts using provided data.
- **Trip Timeline Visualization:** Create timeline visualizations for trip data.
- **Trip Summary Table:** Create summary tables for trip data.
- **Daily Trip Mileage Chart:** Create charts showing daily trip count vs. mileage.
- **Expense vs. Revenue Chart:** Create charts showing expense vs. revenue over different timestamps.
- **Trip Efficiency Chart:** Create charts showing trip efficiency metrics.
- **Expense Forecasting Chart:** Create charts showing expense forecasting.

<p align="center">
  <img src="images/financials.png" alt="Daily Expenses">
</p>

---

## 🚀 Quick Start

### Try the Live Demo

Try RoadTrip Insights with our [**Live Demo**](https://demo.your_website.com/ui/login?auto). No installation required!

### Get Started Locally in 5 Minutes

#### Launch RoadTrip Insights in Docker

Make sure that Docker is running. Then, start RoadTrip Insights in a single command:

```bash
docker run --pull=always --rm -it -p 8080:8080 --user=root \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp your_username/RoadTrip-Insights:latest server local
```

Access the RoadTrip Insights UI at [http://localhost:8080](http://localhost:8080) and start building your first flow!

## 🌐 Join the Community

Stay connected and get support:

- **Slack:** Join our [Slack community](https://your_website.com/slack) to ask questions and share ideas.
- **LinkedIn:** Follow us on [LinkedIn](https://www.linkedin.com/company/your_linkedin/) — next to Slack and GitHub, this is our main channel to share updates and product announcements.
- **YouTube:** Subscribe to our [YouTube channel](https://www.youtube.com/@your_youtube) for educational video content. We publish new videos every week!
- **X:** Follow us on [X](https://x.com/your_twitter) if you're still active there.

---

## 🤝 Contributing

We welcome contributions of all kinds!

- **Report Issues:** Found a bug or have a feature request? Open an [issue on GitHub](https://github.com/your_username/RoadTrip-Insights/issues).
- **Contribute Code:** Check out our [Contributor Guide](https://your_website.com/docs/getting-started/contributing) for initial guidelines, and explore our [good first issues](https://go.your_website.com/contribute) for beginner-friendly tasks to tackle first.
- **Contribute to our Docs:** Contribute edits or updates to keep our [documentation](https://github.com/your_username/docs) top-notch.

---

## 📄 License

RoadTrip Insights is licensed under the Apache 2.0 License © [RoadTrip Insights Technologies](https://your_website.com).

---

## ⭐️ Stay Updated

Give our repository a star to stay informed about the latest features and updates!

[![Star the Repo](https://your_website.com/star.gif)](https://github.com/your_username/RoadTrip-Insights)

---

## LangChain Integration
The project utilizes LangChain for PDF extraction. The `pdf_parser.py` script has been updated to use a LangChain agent to extract the required trip data from PDF files as a list of records.

### Recommended Models
For optimal performance, it is recommended to use the following OpenAI models:
- `gpt-3.5-turbo`: A powerful model suitable for general text extraction tasks.
- `gpt-4`: An advanced model with enhanced capabilities for complex text extraction and understanding.

### Configuration
Ensure that the following environment variables are set in the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_openai_model
OPENAI_API_URL=your_openai_api_url
