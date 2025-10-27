import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

// Dummy data for charts
const salesData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  datasets: [
    {
      label: 'Sales Revenue',
      data: [12000, 19000, 15000, 25000, 22000, 30000, 28000, 35000, 32000, 40000, 38000, 45000],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      tension: 0.4,
    },
    {
      label: 'Profit',
      data: [8000, 12000, 10000, 18000, 15000, 22000, 20000, 25000, 23000, 30000, 28000, 35000],
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.4,
    }
  ]
};

const userActivityData = {
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  datasets: [
    {
      label: 'Active Users',
      data: [1200, 1900, 3000, 5000, 2000, 300, 800],
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 205, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(255, 159, 64, 0.8)',
        'rgba(199, 199, 199, 0.8)',
      ],
    }
  ]
};

const categoryData = {
  labels: ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty'],
  datasets: [
    {
      data: [35, 25, 15, 12, 8, 5],
      backgroundColor: [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
        '#4BC0C0',
        '#9966FF',
        '#FF9F40',
      ],
    }
  ]
};

const conversionData = {
  labels: ['Q1', 'Q2', 'Q3', 'Q4'],
  datasets: [
    {
      label: 'Conversion Rate (%)',
      data: [2.5, 3.2, 2.8, 4.1],
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
    }
  ]
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Chart Title',
    },
  },
};

function App() {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>BerInsight Dashboard</h1>
        <p>Analytics & Performance Overview</p>
      </header>

      <div className="dashboard-grid">
        {/* Key Metrics Cards */}
        <div className="metrics-row">
          <div className="metric-card">
            <h3>Total Revenue</h3>
            <div className="metric-value">$342,000</div>
            <div className="metric-change positive">+12.5%</div>
          </div>
          <div className="metric-card">
            <h3>Active Users</h3>
            <div className="metric-value">15,420</div>
            <div className="metric-change positive">+8.2%</div>
          </div>
          <div className="metric-card">
            <h3>Orders</h3>
            <div className="metric-value">2,847</div>
            <div className="metric-change negative">-3.1%</div>
          </div>
          <div className="metric-card">
            <h3>Conversion Rate</h3>
            <div className="metric-value">3.2%</div>
            <div className="metric-change positive">+0.4%</div>
          </div>
        </div>

        {/* Charts Row 1 */}
        <div className="charts-row">
          <div className="chart-container">
            <h3>Sales & Revenue Trend</h3>
            <Line data={salesData} options={{
              ...chartOptions,
              plugins: {
                ...chartOptions.plugins,
                title: { display: true, text: 'Monthly Sales & Revenue' }
              }
            }} />
          </div>
          <div className="chart-container">
            <h3>Weekly User Activity</h3>
            <Bar data={userActivityData} options={{
              ...chartOptions,
              plugins: {
                ...chartOptions.plugins,
                title: { display: true, text: 'Daily Active Users' }
              }
            }} />
          </div>
        </div>

        {/* Charts Row 2 */}
        <div className="charts-row">
          <div className="chart-container">
            <h3>Sales by Category</h3>
            <Doughnut data={categoryData} options={{
              ...chartOptions,
              plugins: {
                ...chartOptions.plugins,
                title: { display: true, text: 'Revenue Distribution' }
              }
            }} />
          </div>
          <div className="chart-container">
            <h3>Quarterly Conversion Rate</h3>
            <Bar data={conversionData} options={{
              ...chartOptions,
              plugins: {
                ...chartOptions.plugins,
                title: { display: true, text: 'Conversion Rate by Quarter' }
              }
            }} />
          </div>
        </div>

        {/* Additional Metrics */}
        <div className="additional-metrics">
          <div className="metric-card">
            <h3>Average Order Value</h3>
            <div className="metric-value">$120.50</div>
          </div>
          <div className="metric-card">
            <h3>Customer Satisfaction</h3>
            <div className="metric-value">4.7/5.0</div>
          </div>
          <div className="metric-card">
            <h3>Return Rate</h3>
            <div className="metric-value">5.2%</div>
          </div>
          <div className="metric-card">
            <h3>Inventory Turnover</h3>
            <div className="metric-value">6.8x</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App
