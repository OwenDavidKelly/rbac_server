CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'ex_role_1'),
(2, 'ex_role_2');

CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL UNIQUE,
  `password` varchar(60) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `users` (`uid`, `username`, `password`) VALUES
(1, 'user_a', '$2b$12$cJYELd7QKfTe70AnIVcEVe0LaU/jMv3g5hbQADtyUwCKMyJ8XQaGi'),
(2, 'user_b', '$2b$12$Hy2FR3kZk5pwX6rIZgtjiOqHjF4cnNHqKHUXJiLTVO9lwGB3gRj2C'),
(3, 'user_c', '$2b$12$4Llp0XBuOYAR7.9sE4ZSA.caDMlxmc03Vf42iBbZQDWtAPa12IDYS'),
(4, 'user_d', '$2b$12$o/AbEp/5K9x6NhKSaSADHe95184UPxi5lHuv0yFANv0UnlfwRLUhW'),
(5, 'user_e', '$2b$12$/4menkt2kvJ/ebPpc5/OpectiGnzH9oH/4DAscWtbFTC9lrQeAgAe');

CREATE TABLE `user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `r_access` tinyint(1) NOT NULL DEFAULT 0,
  `w_access` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user_role` (`user_id`, `role_id`, `r_access`, `w_access`) VALUES
(1, 1, 1, 1),
(1, 2, 1, 1),
(2, 1, 1, 0),
(2, 2, 1, 0),
(3, 1, 0, 1),
(3, 2, 0, 1),
(4, 1, 1, 1);

ALTER TABLE `user_role`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `role_id` (`role_id`);

ALTER TABLE `user_role`
  ADD CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE; 
