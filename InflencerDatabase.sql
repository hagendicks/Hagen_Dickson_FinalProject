DROP DATABASE IF EXISTS NewFinalsdb;
CREATE DATABASE NewFinalsdb;
USE NewFinalsdb;

CREATE TABLE INDUSTRY (
    IndustryID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Industryname VARCHAR(100) NOT NULL
);

INSERT INTO INDUSTRY (Industryname) VALUES 
('Entertainment'), ('Music'), ('Fashion'), ('Lifestyle'), ('Beauty'), ('Comedy');

CREATE TABLE BRAND (
    BrandID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Brandname VARCHAR(100) NOT NULL,
    PayPackage DECIMAL(15, 2),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    LogoPic VARCHAR(255)
);

INSERT INTO BRAND (Brandname, PayPackage, Email, Password)
VALUES
('MTN Ghana', 25000.00, 'marketing@mtn.com.gh', '123'),
('Vodafone Ghana', 20000.00, 'sales@vodafone.com.gh', '123'),
('Coca-Cola', 28000.00, 'ghana@coca-cola.com', '123'),
('Ghana Oil Company (GOIL)', 15000.00, 'info@goil.com.gh', '123'),
('Samsung Ghana', 30000.00, 'contact@samsung.com.gh', '123'),
('FanMilk Ghana', 12000.00, 'sales@fanmilk.com', '123'),
('Kasapreko', 18000.00, 'info@kasapreko.com', '123'),
('Woodin', 22000.00, 'fashion@woodin.com', '123'),
('GTP Fashion', 21000.00, 'sales@gtpfashion.com', '123'),
('Fidelity Bank', 26000.00, 'banking@fidelity.com.gh', '123'),
('Jumia Ghana', 14000.00, 'support@jumia.com.gh', '123'),
('Bolt Ghana', 13000.00, 'rides@bolt.com', '123'),
('KFC Ghana', 17000.00, 'food@kfc.com.gh', '123'),
('Melcom', 19000.00, 'shop@melcom.com', '123'),
('Twellium Industries', 16500.00, 'info@twellium.com', '123');

CREATE TABLE APPLICATION (
    ApplicationID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ApplicationStatus VARCHAR(50),
    Date_Applied DATE,
    BID_Amount DECIMAL(15, 2)
);

INSERT INTO APPLICATION (ApplicationStatus, Date_Applied, BID_Amount) VALUES
('Approved', '2025-04-01', 1500.00), ('Approved', '2025-04-02', 1200.00),
('Pending', '2025-04-03', 1100.00), ('Approved', '2025-04-04', 1800.00),
('Rejected', '2025-04-05', 1300.00), ('Pending', '2025-04-06', 2000.00),
('Approved', '2025-04-07', 2500.00), ('Rejected', '2025-04-08', 900.00),
('Pending', '2025-04-09', 1600.00), ('Approved', '2025-04-10', 3000.00),
('Pending', '2025-04-11', 1450.00), ('Rejected', '2025-04-12', 5000.00),
('Approved', '2025-04-13', 2200.00), ('Pending', '2025-04-14', 1250.00),
('Approved', '2025-04-15', 1900.00);

CREATE TABLE INDUSTRY_BRAND (
  INDB_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Industryname VARCHAR(100),
  Brandname VARCHAR(100),
  PayPackage DECIMAL(15,2),
  IndustryID INT,
  BrandID INT,
  FOREIGN KEY (IndustryID) REFERENCES INDUSTRY (IndustryID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (BrandID) REFERENCES BRAND (BrandID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO INDUSTRY_BRAND (Industryname, Brandname, PayPackage, IndustryID, BrandID) VALUES
('Entertainment', 'MTN Ghana', 25000.00, 1, 1),
('Lifestyle', 'Vodafone Ghana', 20000.00, 4, 2),
('Beauty', 'Coca-Cola', 28000.00, 5, 3),
('Lifestyle', 'Samsung Ghana', 30000.00, 4, 5),
('Lifestyle', 'FanMilk Ghana', 12000.00, 4, 6),
('Entertainment', 'Kasapreko', 18000.00, 1, 7),
('Fashion', 'Woodin', 22000.00, 3, 8),
('Fashion', 'GTP Fashion', 21000.00, 3, 9),
('Lifestyle', 'Fidelity Bank', 26000.00, 4, 10),
('Lifestyle', 'Jumia Ghana', 14000.00, 4, 11),
('Lifestyle', 'Bolt Ghana', 13000.00, 4, 12),
('Lifestyle', 'KFC Ghana', 17000.00, 4, 13),
('Lifestyle', 'Melcom', 19000.00, 4, 14),
('Lifestyle', 'Twellium Industries', 16500.00, 4, 15);

CREATE TABLE INFLUENCER (
  InfluencerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  InfluencerName VARCHAR(100),
  Age INT,
  Gender VARCHAR(10),
  Industry VARCHAR(100),
  Handle VARCHAR(100),
  Field VARCHAR(100),
  ApplicationID INT,
  Email VARCHAR(255) UNIQUE,
  Password VARCHAR(255),
  ProfilePic VARCHAR(255),
  FOREIGN KEY (ApplicationID) REFERENCES APPLICATION (ApplicationID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO INFLUENCER (InfluencerName, Age, Gender, Industry, Handle, Field, ApplicationID, Email, Password)
VALUES
('Jackie Appiah', 40, 'Female', 'Entertainment', '@jackieappiah', 'Acting', 1, 'jackie@gmail.com', '123'),
('Yvonne Nelson', 38, 'Female', 'Entertainment', '@yvonnenelsongh', 'Film Production', 2, 'yvonne@gmail.com', '123'),
('Michael Blackson', 42, 'Male', 'Comedy', '@michaelblackson', 'Comedy', 3, 'michael@gmail.com', '123'),
('Zynnell Zuh', 35, 'Female', 'Fashion', '@zynnellzuh', 'Fashion & Film', 4, 'zynnell@gmail.com', '123'),
('Joe Mettle', 37, 'Male', 'Music', '@joemettle', 'Gospel Music', 5, 'joe@gmail.com', '123'),
('Kwadwo Sheldon', 29, 'Male', 'Entertainment', '@kwadwosheldon', 'YouTuber/Critic', 6, 'kwadwo@gmail.com', '123'),
('Nana Ama McBrown', 46, 'Female', 'Lifestyle', '@iamamamcbrown', 'TV Host/Acting', 7, 'nana@gmail.com', '123'),
('Sister Derby', 39, 'Female', 'Fashion', '@sisterdeborah', 'Modeling/Music', 8, 'derby@gmail.com', '123'),
('Kobby Kyei', 33, 'Male', 'Lifestyle', '@kobbykyei', 'Blogging', 9, 'kobby@gmail.com', '123'),
('Enam', 25, 'Female', 'Music', '@enam_music', 'Afro-Pop', 10, 'enam@gmail.com', '123'),
('MadeInGhana', 28, 'Male', 'Comedy', '@madeinghana', 'Skit Maker', 11, 'made@gmail.com', '123'),
('Wode Maya', 33, 'Male', 'Lifestyle', '@wodemaya', 'Vlogging', 12, 'wode@gmail.com', '123'),
('Berla Mundi', 35, 'Female', 'Lifestyle', '@berlamundi', 'TV Host', 13, 'berla@gmail.com', '123'),
('Sarkodie', 38, 'Male', 'Music', '@sarkodie', 'HipHop', 14, 'sark@gmail.com', '123'),
('Stonebwoy', 36, 'Male', 'Music', '@stonebwoy', 'Afro-Dancehall', 15, 'stone@gmail.com', '123');

CREATE TABLE INFLUENCER_BRAND (
  INFB_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  BrandID INT,
  InfluencerID INT,
  FOREIGN KEY (BrandID) REFERENCES BRAND (BrandID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (InfluencerID) REFERENCES INFLUENCER (InfluencerID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO INFLUENCER_BRAND (BrandID, InfluencerID) VALUES
(1, 1), (2, 1), (1, 2), (3, 2), (2, 3), (8, 4), (13, 6), (14, 7), (9, 8), (11, 9), (10, 12), (5, 13), (6, 14);

CREATE TABLE CAMPAIGN (
  CampaignID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  CampaignName VARCHAR(255),
  CampaignStatus VARCHAR(50),
  StartDate DATE,
  EndDate DATE,
  BrandID INT,
  IndustryID INT,
  FOREIGN KEY (BrandID) REFERENCES BRAND (BrandID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO CAMPAIGN (CampaignName, CampaignStatus, StartDate, EndDate, BrandID, IndustryID) VALUES
('Summer Vibes Promo', 'Active', '2025-06-01', '2025-06-30', 1, 1),
('Q1 Data Push', 'Completed', '2025-03-01', '2025-04-01', 2, 4),
('Fashion Week Special', 'Active', '2025-07-01', '2025-07-31', 8, 3),
('Holiday Savings', 'Pending', '2025-12-01', '2025-12-31', 14, 4),
('Independence Day Ad', 'Completed', '2025-03-01', '2025-03-06', 7, 1),
('Galaxy S25 Launch', 'Active', '2025-05-01', '2025-06-15', 5, 4),
('Coke Zero Refresh', 'Pending', '2025-08-01', '2025-09-01', 3, 5),
('FanYogo Blast', 'Active', '2025-06-10', '2025-07-20', 6, 4),
('KFC Streetwise', 'Completed', '2025-01-01', '2025-02-28', 13, 4),
('Bolt Ride Safe', 'Active', '2025-04-01', '2025-05-30', 12, 4);

CREATE TABLE INFLUENCER_CAMPAIGN (
  CAM_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Age INT,
  Gender VARCHAR(10),
  Followers INT,
  Industry VARCHAR(100),
  Handle VARCHAR(100),
  CampaignStatus VARCHAR(50),
  StartDate DATE,
  EndDate DATE,
  InfluencerID INT,
  CampaignID INT,
  FOREIGN KEY (InfluencerID) REFERENCES INFLUENCER (InfluencerID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (CampaignID) REFERENCES CAMPAIGN (CampaignID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO INFLUENCER_CAMPAIGN (Age, Gender, Followers, Industry, Handle, CampaignStatus, StartDate, EndDate, InfluencerID, CampaignID) VALUES
(40, 'Female', 5000000, 'Entertainment', '@jackieappiah', 'Active', '2025-06-01', '2025-06-30', 1, 1),
(38, 'Female', 4000000, 'Entertainment', '@yvonnenelsongh', 'Completed', '2025-03-01', '2025-04-01', 2, 2),
(35, 'Female', 300000, 'Fashion', '@zynnellzuh', 'Active', '2025-07-01', '2025-07-31', 4, 3),
(46, 'Female', 3500000, 'Lifestyle', '@iamamamcbrown', 'Pending', '2025-12-01', '2025-12-31', 7, 4),
(29, 'Male', 550000, 'Entertainment', '@kwadwosheldon', 'Completed', '2025-01-01', '2025-02-28', 6, 9),
(35, 'Female', 800000, 'Lifestyle', '@berlamundi', 'Active', '2025-05-01', '2025-06-15', 13, 6),
(33, 'Male', 1000000, 'Lifestyle', '@wodemaya', 'Active', '2025-04-01', '2025-05-30', 12, 10);

CREATE TABLE BRAND_APPLICATION (
  BA_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Brandname VARCHAR(100),
  PayPackage DECIMAL(15,2),
  INDB_ID INT,
  BrandID INT,
  ApplicationID INT,
  FOREIGN KEY (ApplicationID) REFERENCES APPLICATION (ApplicationID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (BrandID) REFERENCES BRAND (BrandID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (INDB_ID) REFERENCES INDUSTRY_BRAND (INDB_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO BRAND_APPLICATION (Brandname, PayPackage, BrandID, ApplicationID) VALUES
('MTN Ghana', 1500.00, 1, 1), ('Vodafone Ghana', 1200.00, 2, 2), ('Coca-Cola', 1300.00, 3, 3),
('Woodin', 1400.00, 8, 4), ('Samsung Ghana', 1350.00, 5, 5), ('KFC Ghana', 2000.00, 13, 6),
('Melcom', 2500.00, 14, 7), ('GTP Fashion', 900.00, 9, 8), ('Fidelity Bank', 1600.00, 10, 9),
('Jumia Ghana', 3000.00, 11, 10), ('Bolt Ghana', 1450.00, 12, 11), ('FanMilk Ghana', 5000.00, 6, 12),
('Kasapreko', 2200.00, 7, 13), ('Twellium', 1250.00, 15, 14), ('MTN Ghana', 1900.00, 1, 15);