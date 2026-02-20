-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 20, 2026 at 05:51 PM
-- Server version: 8.0.45-0ubuntu0.24.04.1
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ruri_discord_bot`
--

-- --------------------------------------------------------

--
-- Table structure for table `guilds`
--

CREATE TABLE `guilds` (
  `discord_guild_id` bigint NOT NULL,
  `name` text NOT NULL,
  `updates_channel_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `manga`
--

CREATE TABLE `manga` (
  `manga_updates_id` bigint NOT NULL,
  `name` text NOT NULL,
  `latest_chapter` float NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tracked_manga`
--

CREATE TABLE `tracked_manga` (
  `discord_guild_id` bigint NOT NULL,
  `manga_updates_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for table `guilds`
--
ALTER TABLE `guilds`
  ADD PRIMARY KEY (`discord_guild_id`),
  ADD UNIQUE KEY `updates_channel_id` (`updates_channel_id`);

--
-- Indexes for table `manga`
--
ALTER TABLE `manga`
  ADD PRIMARY KEY (`manga_updates_id`);

--
-- Indexes for table `tracked_manga`
--
ALTER TABLE `tracked_manga`
  ADD PRIMARY KEY (`discord_guild_id`,`manga_updates_id`),
  ADD KEY `manga_updates_id` (`manga_updates_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tracked_manga`
--
ALTER TABLE `tracked_manga`
  ADD CONSTRAINT `tracked_manga_ibfk_1` FOREIGN KEY (`manga_updates_id`) REFERENCES `manga` (`manga_updates_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tracked_manga_ibfk_2` FOREIGN KEY (`discord_guild_id`) REFERENCES `guilds` (`discord_guild_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
