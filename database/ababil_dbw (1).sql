-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 22, 2024 at 07:07 PM
-- Server version: 8.3.0
-- PHP Version: 8.1.2-1ubuntu2.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ababil_dbw`
--

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE `log` (
  `id` int NOT NULL,
  `tipo` int NOT NULL,
  `nombre` int NOT NULL,
  `apellido` int NOT NULL,
  `usuario` int NOT NULL,
  `password` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_m_client`
--

CREATE TABLE `tb_m_client` (
  `client_id` int NOT NULL,
  `client_name` varchar(100) DEFAULT NULL,
  `client_address` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_m_client`
--

INSERT INTO `tb_m_client` (`client_id`, `client_name`, `client_address`) VALUES
(1, 'NEC', 'Jakarta'),
(2, 'TAM', 'Jakarta'),
(3, 'TUA', 'Bandung');

-- --------------------------------------------------------

--
-- Table structure for table `tb_m_project`
--

CREATE TABLE `tb_m_project` (
  `project_id` int NOT NULL,
  `project_name` varchar(100) DEFAULT NULL,
  `client_id` int DEFAULT NULL,
  `project_start` date DEFAULT NULL,
  `project_end` date DEFAULT NULL,
  `project_status` char(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tb_m_project`
--

INSERT INTO `tb_m_project` (`project_id`, `project_name`, `client_id`, `project_start`, `project_end`, `project_status`) VALUES
(5, 'WMS', 1, '2022-07-28', '2022-08-28', 'OPEN'),
(6, 'FILMS', 1, '2022-06-01', '2022-08-31', 'DOING'),
(8, 'POS', 3, '2022-05-01', '2022-08-31', 'DOING'),
(14, 'asu', 1, '2024-06-22', '2024-06-22', 'DONE');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remember_token` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_m_client`
--
ALTER TABLE `tb_m_client`
  ADD PRIMARY KEY (`client_id`);

--
-- Indexes for table `tb_m_project`
--
ALTER TABLE `tb_m_project`
  ADD PRIMARY KEY (`project_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_m_client`
--
ALTER TABLE `tb_m_client`
  MODIFY `client_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tb_m_project`
--
ALTER TABLE `tb_m_project`
  MODIFY `project_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_m_project`
--
ALTER TABLE `tb_m_project`
  ADD CONSTRAINT `tb_m_project_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `tb_m_client` (`client_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
