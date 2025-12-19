# Hagen_Dickson_FinalProject

BrandConnect: Project Documentation and Developer ReadMe
Project Overview
I developed BrandConnect to serve as a specialized, data-powered marketplace that addresses the fragmentation in the influencer marketing industry in West Africa. My primary goal was to solve the three distinct disconnects I identified in my research: the communication disconnect, the location disconnect, and the collaboration disconnect. I built this web application to serve as a centralisedcentralized hub where Brands and Influencers can connect based on relevant data, rather than just physical proximity or word of mouth.
Below is a detailed breakdown of the files I created, the logic behind my coding choices, and instructions on how to interact with each component of the system.
1. The Core Application Logic
app.py
This is the heart of the application. I chose Python with the Flask framework because I needed a lightweight yet powerful backend to handle routing, database interactions, and session management. When I designed this file, I wanted to ensure that the logic for Brands and Influencers remained distinct yet accessible within the same ecosystem.
One of the most significant decisions I made recently was to refactor the Brand routing logic. Initially, I had separate routes and pages for the profile, campaign management, and the dashboard. I realized that this created a disjointed user experience, where users had to navigate away from their central hub to perform basic tasks. To fix this, I consolidated the logic into a single brand_dashboard route. This function now fetches everything at once: statistical data, the profile information, active campaigns, and the timeline posts. By doing this, I effectively turned the dashboard into a single-page application (SPA) feel without the complexity of a frontend framework like React.
I also implemented the "Smart Matching Algorithm" directly inside the dashboard routes. I wrote SQL queries that examine the user's Industry tag and compare it against the database to retrieve relevant counterparts. For influencers, I query campaigns that match their specific industry. For brands, I query influencers who have the highest follower counts in the niche for which the Brand is hiring. This ensures that the moment a user logs in, they are immediately presented with value.
db_connect.py
I separated the database connection logic into this file to maintain clean code and follow the "Don't Repeat Yourself" (DRY) principle. Instead of writing the MySQL connection string in every single route inside app.py, I defined it once here. This makes the application easier to maintain. If I need to change the database password or host address later, I only have to edit this one file, and the change will propagate throughout the entire system.
2. Database Structure
InflencerDatabase.sql
I designed this SQL schema to be relational and robust. I created distinct tables for INFLUENCER, BRAND, CAMPAIGN, POSTS, and MESSAGES. I intentionally added foreign keys to link these tables together. For example, the INFLUENCER_CAMPAIGN table serves as a junction table, linking a specific influencer to a particular campaign. This allows me to track the status of an application (Pending, Approved, Rejected) without altering the original campaign data. I also included an Industry table to standardize the categories users can select, which is critical for the matching algorithm I mentioned earlier to work significantly better than free-text matching.
3. The User Interface (Templates)
brand_dashboard.html
This is the most complex frontend file in the project. My thought process here was to create a "Command Centre" for the brand user. I merged the profile editing form, the campaign management table, and the applicant review section into this single file. I used HTML tabs to visually separate these content areas while keeping them on the same page in terms of code.
I have integrated the applicant review table directly here, allowing a brand manager to view who has applied and immediately click "Approve" or "Reject." I added logic that dynamically reveals a "View Contract" button only after an applicant is approved. This solves the collaboration disconnect by automating the legal paperwork step immediately after a decision is made.
influencer_dashboard.html
For the influencer side, I focused on simplicity and opportunity discovery. I designed this dashboard to highlight the "Recommended for You" section at the very top. I wanted the Influencer to log in and immediately see the jobs for which they are qualified. I also included a status tracker so they can see if their previous applications are still pending or if they have been accepted.
login.html, signup.html, brand_signup.html, influencer_signup.html
I split the signup process because Brands and Influencers require vastly different data points. An influencer needs to provide their handle, gender, and number of followers, whereas a brand needs to provide its budget and company name. However, I kept a single login.html file that smartly detects which user table to check based on the role selected. This streamlines the entry point while maintaining structured data storage.
messages.html
To solve the communication disconnect, I built an internal messaging system. I did not want users to have to leave the site to negotiate. This file renders a dual-view interface, with a list of recent conversations on the left and the active chat on the right. I designed the backend query to check for messages where the current user is either the sender OR the receiver, ensuring the entire conversation history is captured chronologically.
4. Static Assets
style.css
I wanted the application to feel modern, professional, yet distinct. I chose a dark theme with a specific colour palette: a deep charcoal background paired with a vibrant green for success actions and a warm orange for calls to action. I recently updated the typography to use the Merriweather font family for headings and body text. This serif font gave the platform a more editorial and trustworthy feel compared to standard sans-serif fonts. I also wrote extensive CSS animations (fade-ins, slides) to make the user interface feel responsive and alive.
script.js
I kept the JavaScript vanilla (no frameworks) to ensure fast load times. The primary job of this file is to handle the tab switching in the dashboard and to perform asynchronous operations (AJAX). For example, when you click "Approve" on an applicant, the JavaScript sends a request to the backend API without reloading the page. It then updates the text status and colour on the screen instantly. This provides immediate feedback to the user, making the application feel snappy and high-quality.
How to Run the Application
Database Setup: First, you must import the InflencerDatabase.sql file into your local MySQL server (using Workbench or PHPMyAdmin) to create the necessary tables.
Configuration: Open db_connect.py and ensure the database credentials (user, password, host) match your local setup.
Start the Server: Run the app.py file using Python. You will see the Flask server start on port 5000.
Access: Open your web browser and go to the local host address provided in the terminal. You should see the index.html landing page.
Usage: Navigate to the Signup page and create a test Brand account and a test Influencer account. Log in as the Brand to post a campaign, then log in as the Influencer to apply for it. Return to the Brand dashboard to approve the application and view the generated contract.

USE OF AI
AI  was used in the creation of dummy data for the website.
AI was also used to give suggestion on how to improve the css and javascript functions of the website.
