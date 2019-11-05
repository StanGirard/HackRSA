CREATE TABLE `cert` (
  `id` int(11) NOT NULL,
  `company` varchar(120) NOT NULL,
  `domain` varchar(120) NOT NULL,
  `issuer` varchar(120) NOT NULL,
  `pubkey` varchar(1500) NOT NULL,
  `valid_from` varchar(100) NOT NULL,
  `valid_to` varchar(100) NOT NULL,
  `fingerprint` varchar(100) NOT NULL,
  `fingerprint256` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci